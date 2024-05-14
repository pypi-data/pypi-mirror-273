import time
import requests
import json
import re

import biliup.common.util
from biliup.config import config
from . import match1, logger
from biliup.plugins.Danmaku import DanmakuClient
from ..common import tools
from ..engine.decorators import Plugin
from ..engine.download import DownloadBase


@Plugin.download(regexp=r'(?:https?://)?(?:(?:www|m|live)\.)?bilibili\.com')
class Bililive(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        self.live_time = 0
        self.bilibili_danmaku = config.get('bilibili_danmaku', False)
        self.fake_headers['referer'] = url
        if config.get('user', {}).get('bili_cookie'):
            self.fake_headers['cookie'] = config.get('user', {}).get('bili_cookie')
        else:
            cookie_file_name = config.get('user', {}).get('bili_cookie_file')
            if cookie_file_name:
                try:
                    with open(cookie_file_name, encoding='utf-8') as stream:
                        cookies = json.load(stream)["cookie_info"]["cookies"]
                        cookies_str = ''
                        for i in cookies:
                            cookies_str += f"{i['name']}={i['value']};"
                        self.fake_headers['cookie'] = cookies_str
                        # logger.info(f"未配置bili_cookie使用{cookie_file_name}")
                except Exception:
                    logger.exception("load_cookies error")

    async def acheck_stream(self, is_check=False):
        OFFICIAL_API = "https://api.live.bilibili.com"
        room_id = match1(self.url, r'/(\d+)')
        qualityNumber = int(config.get('bili_qn', 10000))
        plugin_msg = f"Bililive - {room_id}"

        # with requests.Session() as s:
        biliup.common.util.client.headers.update(self.fake_headers)
        # 获取直播状态与房间标题
        info_by_room_url = f"{OFFICIAL_API}/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}"
        try:
            room_info = (await biliup.common.util.client.get(info_by_room_url, timeout=5)).json()
        except Exception:
            logger.exception(f"{plugin_msg}")
            return False
        if room_info['code'] != 0:
            logger.error(f"{plugin_msg}: {room_info}")
            return False
        if room_info['data']['room_info']['live_status'] != 1:
            logger.debug(f"{plugin_msg}: 未开播")
            return False
        self.live_cover_url = room_info['data']['room_info']['cover']
        live_start_time = room_info['data']['room_info']['live_start_time']
        if self.room_title is None:
            self.room_title = room_info['data']['room_info']['title']
        if live_start_time > self.live_time:
            self.live_time = live_start_time
            is_new_live = True
        else:
            is_new_live = False
        if is_check:
            _res = (await biliup.common.util.client.get('https://api.bilibili.com/x/web-interface/nav', timeout=5)).json()
            user_data = _res.get('data', {})
            is_login = user_data.get('isLogin', False)
            if is_login:
                logger.info(f"用户名：{user_data['uname']}, mid：{user_data['mid']}, isLogin：{is_login}")
            else:
                logger.warning("登录态校验失败: " + str(_res))
            return True

        protocol = config.get('bili_protocol', 'stream')
        perf_cdn = config.get('bili_perfCDN')
        cdn_fallback = config.get('bili_cdn_fallback', True)
        force_source = config.get('bili_force_source', False)
        ov05_ip = config.get('bili_force_ov05_ip')
        main_api = config.get('bili_liveapi', OFFICIAL_API).rstrip('/')
        fallback_api = config.get('bili_fallback_api', OFFICIAL_API).rstrip('/')
        cn01_sids = config.get('bili_replace_cn01_sid', '').split(',')
        normalize_cn204 = config.get('bili_normalize_cn204', False)

        params = {
            'room_id': room_id,
            'protocol': '0,1',  # 0: http_stream, 1: http_hls
            'format': '0,1,2',  # 0: flv, 1: ts, 2: fmp4
            'codec': '0',  # 0: avc, 1: hevc, 2: av1
            'qn': qualityNumber,
            'platform': 'html5',  # web, html5, android, ios
            # 'ptype': '8',
            'dolby': '5',
            # 'panorama': '1' # 全景(不支持 html5)
        }
        streamname_regexp = r"(live_\d+_\w+_\w+_?\w+?)"  # 匹配 streamName

        # if self.raw_stream_url is not None \
        #         and qualityNumber >= 10000 \
        #         and not is_new_live:
        #     # 同一个 streamName 即可复用，除非被超管切断
        #     # 前面拿不到 streamName，目前使用开播时间判断
        #     health, url = await self.acheck_url_healthy(self.raw_stream_url)
        #     if health:
        #         logger.debug(f"{plugin_msg}: 复用 {url}")
        #         return True
        #     else:
        #         logger.debug(f"{plugin_msg}: health-{health}; url-{self.raw_stream_url}")
        #         self.raw_stream_url = None

        try:
            play_info = await get_play_info(main_api, params)
            if play_info is None or check_areablock(play_info['data']['playurl_info']['playurl']):
                logger.debug(f"{plugin_msg}: {main_api} 返回 {play_info}")
                play_info = await get_play_info(fallback_api, params)
                if play_info is None or check_areablock(play_info['data']['playurl_info']['playurl']):
                    logger.debug(f"{plugin_msg}: {fallback_api} 返回 {play_info}")
                    return False
        except Exception:
            logger.exception(f"{plugin_msg}")
            return False
        if play_info['code'] != 0:
            logger.error(f"{plugin_msg}: {play_info}")
            return False

        playurl_info = play_info['data']['playurl_info']['playurl']
        streams = playurl_info['stream']
        stream = streams[1] if protocol.startswith('hls') and len(streams) > 1 else streams[0]
        stream_format = stream['format'][0]
        if protocol == "hls_fmp4":
            if len(stream['format']) > 1:
                stream_format = stream['format'][1]
            elif int(time.time()) - live_start_time <= 60:  # 60s 宽容等待 fmp4
                return False
            elif stream_format['format_name'] == 'ts':
                stream_format = streams[0]['format'][0]

        stream_info = stream_format['codec'][0]

        stream_url = {
            'base_url': stream_info['base_url'],
        }
        if perf_cdn is not None:
            perf_cdn_list = perf_cdn.split(',')
            for url_info in stream_info['url_info']:
                if 'host' in stream_url:
                    break
                for cdn in perf_cdn_list:
                    if cdn in url_info['extra']:
                        stream_url['host'] = url_info['host']
                        stream_url['extra'] = url_info['extra']
                        logger.debug(f"Found {stream_url['host']}")
                        break
        if len(stream_url) < 3:
            stream_url['host'] = stream_info['url_info'][-1]['host']
            stream_url['extra'] = stream_info['url_info'][-1]['extra']

        # 移除 streamName 内画质标签
        # streamName = match1(stream_url['base_url'], streamname_regexp)
        # if streamName is not None and force_source and qualityNumber >= 10000:
        #     new_base_url = stream_url['base_url'].replace(f"_{streamName.split('_')[-1]}", '')
        #     if (await self.acheck_url_healthy(f"{stream_url['host']}{new_base_url}{stream_url['extra']}"))[0]:
        #         stream_url['base_url'] = new_base_url
        #         logger.debug(stream_url['base_url'])

        self.raw_stream_url = f"{stream_url['host']}{stream_url['base_url']}{stream_url['extra']}"

        if normalize_cn204:
            self.raw_stream_url = re.sub(r"(?<=cn-gotcha204)-[1-4]", "", self.raw_stream_url, 1)

        if ov05_ip and "ov-gotcha05" in stream_url['host']:
            self.raw_stream_url = await oversea_expand(self.raw_stream_url, ov05_ip)

        # url_health, _url = await self.acheck_url_healthy(self.raw_stream_url)
        # if not url_health:
        #     if cdn_fallback:
        #         i = len(stream_info['url_info'])
        #         while i:
        #             i -= 1
        #             try:
        #                 self.raw_stream_url = "{}{}{}".format(stream_info['url_info'][i]['host'],
        #                                                       stream_url['base_url'],
        #                                                       stream_info['url_info'][i]['extra'])
        #                 url_health, _url = await self.acheck_url_healthy(self.raw_stream_url)
        #                 if url_health:
        #                     self.raw_stream_url = _url
        #                     break
        #             except TimeoutError as e:
        #                 logger.debug(f"Timeout Error: {e} at {stream_info['url_info'][i]['host']}")
        #                 continue
        #             except Exception:
        #                 logger.exception("Uncaught exception:")
        #                 continue
        #             finally:
        #                 logger.debug(f"{i} - {self.raw_stream_url}")
        #         else:
        #             logger.debug(play_info)
        #             self.raw_stream_url = None
        #             return False
        # else:
        #     self.raw_stream_url = _url
        print(self.raw_stream_url)
        return True

    def danmaku_init(self):
        if self.bilibili_danmaku:
            self.danmaku = DanmakuClient(self.url, self.gen_download_filename())


async def get_play_info(api, params):
    api = (lambda a: a if a.startswith(('http://', 'https://')) else 'http://' + a)(api)
    full_url = f"{api}/xlive/web-room/v2/index/getRoomPlayInfo"
    try:
        return (await biliup.common.util.client.get(full_url, params=params, timeout=5)).json()
    except Exception as e:
        logger.warning(f'{api} 获取直播流信息失败 {e}')
    return None


# Copy from room-player.js
def check_areablock(data):
    '''
    :return: True if area block
    '''
    if data is None:
        logger.error('Sorry, bilibili is currently not available in your country according to copyright restrictions.')
        logger.error('非常抱歉，根据版权方要求，您所在的地区无法观看本直播')
        return True
    return False


async def oversea_expand(url, ov05_ip):
    # 强制替换ov05 302redirect之后的真实地址为指定的域名或ip达到自选ov05节点的目的
    r = await biliup.common.util.client.get(url, stream=True)
    logger.debug(f'将ov-gotcha05的节点ip替换为了{ov05_ip}')
    return re.sub(r".*(?=/d1--ov-gotcha05)", f"http://{ov05_ip}", r.url, 1)
