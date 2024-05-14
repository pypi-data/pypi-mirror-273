# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/10
contact: 【公众号】思维兵工厂
description: 讯飞星火Web端。

但出现因Token失效而导致的访问失败，会自动尝试重新登录。
--------------------------------------------
"""

from typing import Optional, Union
from pathlib import Path
import logging
import base64
import random
import time
import json
import sys
import io
import re

from PIL import Image
import numpy as np
import requests
import ddddocr
import execjs

from .base import LLMBase
from .types import AiAnswer
from .errors import LoginFailError, NeedLoginError, UnexpectResponseError

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static_data'
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True)


class GTrace(object):
    def __init__(self):
        self.__pos_x = []
        self.__pos_y = []
        self.__pos_z = []

    def __set_pt_time(self):
        """
        设置各节点的时间
        分析不同时间间隔中X坐标数量的占比
        统计结果: 1. 80%~90%的X坐标在15~20毫秒之间
                2. 10%~15%在20~200及以上，其中 [-a, 0, x, ...] 这里x只有一个，取值在110~200之间
                    坐标集最后3~5个坐标取值再50~400之间，最后一个坐标数值最大

        滑动总时间的取值规则: 图片宽度260，去掉滑块的宽度剩下200;
                        如果距离小于100，则耗时1300~1900之间
                        如果距离大于100，则耗时1700~2100之间
        """
        __end_pt_time = []
        __move_pt_time = []
        self.__pos_z = []

        total_move_time = self.__need_time * random.uniform(0.8, 0.9)
        start_point_time = random.uniform(110, 200)
        __start_pt_time = [0, 0, int(start_point_time)]

        sum_move_time = 0

        _tmp_total_move_time = total_move_time
        while True:
            delta_time = random.uniform(15, 20)
            if _tmp_total_move_time < delta_time:
                break

            sum_move_time += delta_time
            _tmp_total_move_time -= delta_time
            __move_pt_time.append(int(start_point_time + sum_move_time))

        last_pt_time = __move_pt_time[-1]
        __move_pt_time.append(last_pt_time + _tmp_total_move_time)

        sum_end_time = start_point_time + total_move_time
        other_point_time = self.__need_time - sum_end_time
        end_first_ptime = other_point_time / 2

        while True:
            delta_time = random.uniform(110, 200)
            if end_first_ptime - delta_time <= 0:
                break

            end_first_ptime -= delta_time
            sum_end_time += delta_time
            __end_pt_time.append(int(sum_end_time))

        __end_pt_time.append(int(sum_end_time + (other_point_time / 2 + end_first_ptime)))
        self.__pos_z.extend(__start_pt_time)
        self.__pos_z.extend(__move_pt_time)
        self.__pos_z.extend(__end_pt_time)

    def __set_distance(self, _dist):
        """
        设置要生成的轨迹长度
        """
        self.__distance = _dist

        if _dist < 100:
            self.__need_time = int(random.uniform(500, 1500))
        else:
            self.__need_time = int(random.uniform(1000, 2000))

    def __get_pos_z(self):
        return self.__pos_z

    def __get_pos_y(self):
        _pos_y = [random.uniform(-40, -18), 0]
        point_count = len(self.__pos_z)
        x = np.linspace(-10, 15, point_count - len(_pos_y))
        arct_y = np.arctan(x)

        for _, val in enumerate(arct_y):
            _pos_y.append(val)

        return _pos_y

    def __get_pos_x(self, _distance):
        """
        绘制标准的数学函数图像: 以 tanh 开始 以 arctan 结尾
        根据此模型用等比时间差生成X坐标
        """
        # first_val = random.uniform(-40, -18)
        # _distance += first_val
        _pos_x = [random.uniform(-40, -18), 0]
        self.__set_distance(_distance)
        self.__set_pt_time()

        point_count = len(self.__pos_z)
        x = np.linspace(-1, 19, point_count - len(_pos_x))
        ss = np.arctan(x)
        th = np.tanh(x)

        for idx in range(0, len(th)):
            if th[idx] < ss[idx]:
                th[idx] = ss[idx]

        th += 1
        th *= (_distance / 2.5)

        i = 0
        start_idx = int(point_count / 10)
        end_idx = int(point_count / 50)
        delta_pt = abs(np.random.normal(scale=1.1, size=point_count - start_idx - end_idx))
        for idx in range(start_idx, point_count):
            if idx * 1.3 > len(delta_pt):
                break

            th[idx] += delta_pt[i]
            i += 1

        _pos_x.extend(th)
        return _pos_x[-1], _pos_x

    def get_mouse_pos_path(self, distance):
        """
        获取滑动滑块鼠标的滑动轨迹坐标集合
        """
        result = []
        _distance, x = self.__get_pos_x(distance)
        y = self.__get_pos_y()
        z = self.__get_pos_z()

        for idx in range(len(x)):
            result.append([int(x[idx]), int(y[idx]), int(z[idx])])

        return int(_distance), result


class WebLogin(object):
    """该类用于讯飞网页版登录，获取登录token"""

    def __init__(
            self,
            account_name: str,
            password: str,
            logger: logging.Logger = None,
            generate_w_js_file_path: str = None,
    ):
        """

        :param account_name: 账号
        :param password: 密码
        """

        self.generate_w_js_file_path = generate_w_js_file_path
        self.account_name = account_name
        self.password = password
        self.logger = logger or logging.getLogger(__name__)

        self.gt = ''
        self.challenge = ''
        self.c = ''
        self.s = ''
        self.w = ''
        self.validate = ''
        self.score = ''
        self.sso_session_id = ''
        self.account_id = ''
        self.session = requests.Session()
        self.session.verify = False

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',

            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

    @staticmethod
    def get_timestamp():
        """
        获取当前时间戳
        :return:
        """

        return int(time.time() * 1000)

    @staticmethod
    def get_json_data(text):
        """
        提取出geetest_ddd(*)里的json数据，返回dict
        :param text:
        :return:
        """

        # re取出geetest_1694239359661()中的json
        json_str = re.search(r'geetest_\d+\((.*?)\)', text).group(1)

        # 转为json
        json_data = json.loads(json_str)
        return json_data

    @staticmethod
    def parse_bg_captcha(img, im_show=False, save_path=None):
        """
        滑块乱序背景图还原
        :param img: 图片路径str/图片路径Path对象/图片二进制
            eg: 'assets/bg.webp'
                Path('assets/bg.webp')
        :param im_show: 是否显示还原结果, <type 'bool'>; default: False
        :param save_path: 保存路径, <type 'str'>/<type 'Path'>; default: None
        :return: 还原后背景图 RGB图片格式
        """

        if isinstance(img, (str, Path)):
            _img = Image.open(img)
        elif isinstance(img, bytes):
            _img = Image.open(io.BytesIO(img))
        else:
            raise ValueError(f'输入图片类型错误, 必须是<type str>/<type Path>/<type bytes>: {type(img)}')
        # 图片还原顺序, 定值
        _Ge = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43,
               42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        w_sep, h_sep = 10, 80

        # 还原后的背景图
        new_img = Image.new('RGB', (260, 160))

        for idx in range(len(_Ge)):
            x = _Ge[idx] % 26 * 12 + 1
            y = h_sep if _Ge[idx] > 25 else 0
            # 从背景图中裁剪出对应位置的小块
            img_cut = _img.crop((x, y, x + w_sep, y + h_sep))
            # 将小块拼接到新图中
            new_x = idx % 26 * 10
            new_y = h_sep if idx > 25 else 0
            new_img.paste(img_cut, (new_x, new_y))

        # new_img转为bytes
        if im_show:
            new_img.show()
        if save_path is not None:
            save_path = Path(save_path).resolve().__str__()
            new_img.save(save_path)

        stream = io.BytesIO()
        new_img.save(stream, format='JPEG')
        image_bytes = stream.getvalue()

        # 关闭字节流
        stream.close()

        return image_bytes

    @staticmethod
    def get_slice_res(target_bytes, background_bytes):
        slide = ddddocr.DdddOcr(det=False, ocr=False)

        res = slide.slide_comparison(target_bytes, background_bytes)

        return res

    def if_captcha(self):

        headers = self.headers.copy()
        headers['Host'] = 'sso.xfyun.cn'
        headers['Origin'] = 'https://passport.xfyun.cn'
        headers['Referer'] = 'https://passport.xfyun.cn/'

        host = 'https://sso.xfyun.cn/SSOService/login/if-captcha'

        params = {
            'accountName': self.account_name,
            '_': self.get_timestamp(),
        }

        response = self.session.get(host, headers=headers, params=params, verify=False)

        if response.status_code != 200:
            self.logger.error('【if-captcha】请求失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('【if_captcha】请求失败')
        self.logger.info('【if-captcha】请求成功')

    def get_gt_and_challenge(self):
        """
        获取gt和challenge
        :return:
        """

        host = 'https://sso.xfyun.cn/SSOService/login/gee-captcha'

        current_timestamp = self.get_timestamp()

        params = {'&_': current_timestamp}

        headers = self.headers.copy()

        headers['Host'] = 'sso.xfyun.cn'
        headers['Origin'] = 'https://passport.xfyun.cn'
        headers['Referer'] = 'https://passport.xfyun.cn/'

        response = self.session.get(host, headers=headers, params=params)

        data = response.json()

        gt = data.get('data', {}).get('gt')
        challenge = data.get('data', {}).get('challenge')

        if not gt or not challenge:
            self.logger.error('获取gt和challenge失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('获取gt和challenge失败')

        self.challenge = challenge
        self.gt = gt

        self.logger.info('【get_gt_and_challenge】请求成功，已获取到gt和challenge')
        self.logger.info(f'\n【get_gt_and_challenge】gt: {gt};\n challenge: {challenge}')
        return gt, challenge

    def get_type(self):

        host = 'https://api.geetest.com/gettype.php'

        headers = self.headers.copy()
        headers['Host'] = 'api.geetest.com'
        headers['Referer'] = 'https://passport.xfyun.cn/'

        params = {
            'gt': self.gt,
            'callback': f'geetest_{self.get_timestamp()}',
        }

        response = self.session.get(
            host,
            params=params,
            headers=headers
        )

        if response.status_code != 200:
            self.logger.error('获取type失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('获取type失败')

        self.logger.info('【get_type】请求成功，已获取到type')

    def other_static_js_1(self):

        host = 'https://static.geetest.com/static/js/fullpage.9.1.9-glhvqm.js'

        headers = self.headers.copy()
        headers['Referer'] = 'https://passport.xfyun.cn/'

        second_response = self.session.get(
            host,
            headers=headers
        )

        if second_response.status_code != 200:
            self.logger.error('获取type失败')
            self.logger.info(f"响应数据为：【{second_response.text}】")
            raise Exception('获取type失败')
        self.logger.info('额外请求：【other_static_js_1】请求成功，已获取到fullpage.js文件')

    def get_c_and_s(self):
        # host = 'https://api.geetest.com/get.php'

        callback = f'geetest_{self.get_timestamp()}'

        # params = {
        #     'pt': 0,
        #     'gt': self.gt,
        #     'challenge': self.challenge,
        #     'lang': 'zh',
        #     'client_type': 'web',
        #     'callback': callback,
        # }

        host = f'https://api.geetest.com/get.php?gt={self.gt}&challenge={self.challenge}&lang=zh&pt=0&client_type=web&callback={callback}&w='

        headers = self.headers.copy()
        headers['Referer'] = 'https://passport.xfyun.cn/'
        headers['Host'] = 'api.geetest.com'

        # 这里很奇怪，使用session反而不行，
        # response = self.session.get(host, headers=headers)

        response = requests.get(host, verify=False)

        data = self.get_json_data(response.text)

        status = data.get('status')

        if status != 'success':
            raise Exception('获取c和s失败')

        c = data.get('data', {}).get('c')
        s = data.get('data', {}).get('s')

        if not c or not s:
            self.logger.error('获取c和s失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('获取c和s失败')

        self.logger.info('【get_c_and_s】请求成功，已获取到c和s')
        self.logger.info(f'【get_c_and_s】\nc: {c};\n s: {s}')

        self.c = c
        self.s = s

        return c, s

    def check_ajax(self):

        headers = self.headers.copy()
        headers['Host'] = 'api.geetest.com'
        headers['Referer'] = 'https://passport.xfyun.cn/'

        callback = f'geetest_{self.get_timestamp()}'

        host = f'https://api.geetest.com/ajax.php?gt={self.gt}&challenge={self.challenge}&lang=zh&pt=0&client_type=web&callback={callback}&w='

        response = self.session.get(host)

        if response.status_code != 200:
            self.logger.error('ajax请求失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('ajax请求失败')

        data = self.get_json_data(response.text)
        self.logger.info('【check_ajax】请求成功')

    def other_statis_js_2(self):

        headers = self.headers.copy()
        headers['Referer'] = 'https://passport.xfyun.cn/'
        headers['Origin'] = 'https://passport.xfyun.cn'

        response = self.session.get('https://static.geetest.com/static/js/slide.7.9.2.js', headers=headers)
        if response.status_code != 200:
            self.logger.error('获取js失败')
            self.logger.info(f"响应数据为：【{response.text}】")
            raise Exception('获取js失败')
        self.logger.info('额外请求：【other_statis_js_2】请求成功，已获取到slide.js文件')

    def get_img(self, api_server, url):

        """
        网络请求获取图片二进制数据
        :return:
        """

        headers = {
            'authority': 'static.geetest.com',
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.geetest.com',
            'pragma': 'no-cache',
            'referer': 'https://www.geetest.com/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        # host = f"https://{api_server}{url}".replace('jpg', '.webp')

        # response = self.session.get(host, headers=headers)
        response = self.session.get(f"https://{api_server}{url}", headers=headers)

        self.logger.info(f'【get_img】请求成功，已获取到图片。【f"https://{api_server}{url}"】')
        return response.content

    def get_img_and_params(self):

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',

            'Host': 'api.geetest.com',
            'Pragma': 'no-cache',
            'Referer': 'https://passport.xfyun.cn/',

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
        }

        params = {
            'is_next': 'true',
            'type': 'slide3',
            'gt': self.gt,
            'challenge': self.challenge,
            'lang': 'zh',
            'https': 'false',
            'protocol': 'https://',
            'offline': 'false',
            'product': 'embed',
            'api_server': 'api.geetest.com',
            'isPC': 'true',
            'autoReset': 'true',
            'width': '100%',
            'callback': f'geetest_{self.get_timestamp()}',
        }

        host = f'https://api.geetest.com/get.php?is_next=true&type=slide3&gt={self.gt}&challenge={self.challenge}&lang=zh&https=false&protocol=https%3A%2F%2F&offline=false&product=embed&api_server=api.geetest.com&isPC=true&autoReset=true&width=100%25&callback=geetest_{self.get_timestamp()}'

        # 这里很奇怪，加上headers反而不成功
        # response = self.session.get(
        #     host,
        #     headers=headers
        # )

        response = requests.get(host, verify=False)

        self.logger.info(f'get_img_and_params方法请求状态码：{response.status_code}')

        try:

            json_data = json.loads(response.text)
            status = json_data.get('status')
            error = json_data.get('error')
            user_error = json_data.get('user_error')
            # print('status:', status)
            # print('error:', error)
            # print('user_error:', user_error)
            self.logger.info('【get_img_and_params】请求失败')
            self.logger.info(f"响应数据为：【{response.text}】")
        except:

            resp_data = self.get_json_data(response.text)
            self.logger.info('【get_img_and_params】请求成功')

            # 更新参数
            self.gt = resp_data['gt']
            self.challenge = resp_data['challenge']
            self.c = resp_data['c']
            self.s = resp_data['s']

            full_bg = self.get_img(resp_data['static_servers'][0], resp_data['fullbg'])
            bg = self.get_img(resp_data['static_servers'][0], resp_data['bg'])

            background_bytes = self.parse_bg_captcha(full_bg, im_show=False, save_path=str(STATIC_DIR / 'full_bg.jpg'))
            target_bytes = self.parse_bg_captcha(bg, im_show=False, save_path=str(STATIC_DIR / 'bg.jpg'))

            return target_bytes, background_bytes

        if user_error:
            raise Exception(user_error)

    def generate_w(self, target_bytes, background_bytes):

        res = self.get_slice_res(target_bytes, background_bytes)
        self.logger.info(f'【generate_w】识别结果：{res}')

        # 读取slide.js执行get_w()方法
        with open(self.generate_w_js_file_path, 'r', encoding='utf-8') as f:
            js = f.read()

        ctx = execjs.compile(js)

        gtrace = GTrace()

        # -10，图片不是从头部开始的
        distance, track = gtrace.get_mouse_pos_path(res['target'][0] - 10)
        self.logger.info(f'【generate_w】距离:{distance}')
        self.logger.info(f'【generate_w】轨迹:{track}')
        # print(f"距离:{distance}")
        # print(f"距离track:{track}")

        params = {
            # , gt, challenge, pass_distance, c, s, trance
            'gt': self.gt,
            'challenge': self.challenge,
            'distance': distance,
            "passtime": track[len(track) - 1][2],
            'c': self.c,
            's': self.s,
            'track': track
        }

        self.w = ctx.call('generate_w', params)

        return self.w

    def slice_main(self):
        """
        滑块验证
        :return:
        """

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://www.geetest.com/',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'gt': self.gt,
            'challenge': self.challenge,
            'lang': 'zh',
            '$_BCN': '0',
            'client_type': 'web',
            'w': self.w,
            'callback': f'geetest_{self.get_timestamp()}',
        }

        response = self.session.get(
            f'https://api.geetest.com/ajax.php',
            headers=headers,
            params=params,
        )
        json_data = self.get_json_data(response.text)
        self.logger.info(f'【slice_main】请求状态码：{response.status_code}')
        self.logger.info(f'【slice_main】请求响应数据：{json_data}')

        self.validate = json_data.get('validate')
        self.score = json_data.get('score')

        return json_data

    def get_geetest_seccode(self):

        encoded_a = base64.b64encode(self.validate.encode('utf-8'))
        return encoded_a.decode('utf-8')  # 输出编码后的字符串

    def login(self):

        if not self.validate:
            self.logger.error('没有validate值，无法登录')
            return

        host = 'https://sso.xfyun.cn/SSOService/login/check-account'
        geetest_seccode = self.get_geetest_seccode()

        data = {
            'geetest_challenge': self.challenge,
            'geetest_validate': self.validate,
            'geetest_seccode': geetest_seccode,
            'accountName': self.account_name,
            'accountPwd': self.password,
            'isAct': False,
            'specCode': '',
        }

        headers = self.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Host'] = 'sso.xfyun.cn'
        headers['Referer'] = 'https://passport.xfyun.cn/'
        headers['Origin'] = 'https://passport.xfyun.cn'

        response = self.session.post(
            host,
            headers=headers,
            data=data,
        )

        self.logger.info(f'【login】请求响应数据：{response.text}')
        try:

            if '用户名或密码错误' in response.text:
                self.logger.error(f'【login】用户名或密码错误')
                return False

            json_data = json.loads(response.text)
            self.logger.info(f'【login】请求响应数据：{json_data}')

            self.sso_session_id = json_data.get('data', {}).get('ssoSessionId')
            self.account_id = json_data.get('data', {}).get('account_id')

            self.logger.info(f'【login】ssoSessionId:{self.sso_session_id}')
            self.logger.info(f'【login】account_id:{self.account_id}')

            return True
        except:
            self.logger.error(f'【login】请求响应数据：{response.text}')
            return False

    def get_cookie(self):

        if not self.sso_session_id:
            self.logger.error(f'【get_cookie】没有ssoSessionId，无法获取cookie')
            return

        if not self.account_id:
            self.logger.error(f'【get_cookie】没有account_id，无法获取cookie')
            return

        host = f'https://sso.xfyun.cn/SSOService/login/setcookies?ssoSessionId={self.sso_session_id}&account_id={self.account_id}&url=aHR0cHM6Ly93d3cueGZ5dW4uY24v'

        headers = self.headers.copy()
        headers['Referer'] = 'https://passport.xfyun.cn/'
        headers['Host'] = 'sso.xfyun.cn'
        headers['Sec-Fetch-Dest'] = 'document'
        headers['Upgrade-Insecure-Requests'] = '1'

        response = self.session.get(
            host,
            headers=headers,
        )

        self.logger.info(f'【get_cookie】请求响应数据：{response.text}')

        for k, v in self.session.cookies.items():
            print(f'{k}: {v}')

    def run(self):

        if not self.generate_w_js_file_path:
            print('缺少js解密文件')
            return

        self.if_captcha()
        print(f"第一次请求，if_captcha")

        print('-'.center(50, '-'))

        self.get_gt_and_challenge()
        print(f"第二次请求，获取gt和challenge")
        print(f"gt: {self.gt}")
        print(f"challenge: {self.challenge}")
        print('-'.center(50, '-'))

        self.get_type()
        print(f"第三次请求，获取type")
        print('-'.center(50, '-'))

        self.other_static_js_1()
        print(f"第四次请求，获取fullpage.js文件")
        print('-'.center(50, '-'))

        time.sleep(1)

        self.get_c_and_s()
        print(f"第五次请求，获取c和s")
        print(f"c: {self.c}")
        print(f"s: {self.s}")
        print('-'.center(50, '-'))

        self.check_ajax()
        print(f"第六次请求，ajax请求")
        print('-'.center(50, '-'))

        self.other_statis_js_2()
        print(f"第七次请求，获取slide.js文件")
        print('-'.center(50, '-'))

        time.sleep(2)

        target_bytes, background_bytes = self.get_img_and_params()
        print(f"第八次请求，获取图片")
        print('-'.center(50, '-'))

        w = self.generate_w(target_bytes, background_bytes)
        print(f"w: {w}")
        print('-'.center(50, '-'))

        time.sleep(1)
        self.slice_main()
        print(f"第九次请求，滑块验证，获得validate和score")
        print(f"validate: {self.validate}")
        print(f"score: {self.score}")
        print('-'.center(50, '-'))

        print(f"第十次请求，准备登录")
        self.login()
        print('-'.center(50, '-'))

        if self.sso_session_id:
            print(f"第十一次请求，获取cookie")
            self.get_cookie()

    def get_session_id(self, generate_w_js_file_path: str = None):

        self.generate_w_js_file_path = generate_w_js_file_path

        if not self.generate_w_js_file_path:
            raise Exception('缺少js解密文件')

        for i in range(3):

            self.if_captcha()

            self.get_gt_and_challenge()

            self.get_type()

            self.other_static_js_1()

            time.sleep(1)

            self.get_c_and_s()

            self.check_ajax()

            self.other_statis_js_2()

            time.sleep(1)

            target_bytes, background_bytes = self.get_img_and_params()

            w = self.generate_w(target_bytes, background_bytes)

            time.sleep(1)

            self.slice_main()

            result = self.login()

            if result:
                return self.sso_session_id


class XunFeiWeb(LLMBase):
    model_name = 'XunFeiWeb'
    base_url = 'https://xinghuo.xfyun.cn'

    def __init__(
            self,
            cookie: str = None,
            account: str = None,
            password: str = None,
            error_dir: str = None,
            sso_session_id: str = None,
            logger_obj: logging.Logger = None,
            generate_w_js_file_path: str = None,
            *args,
            **kwargs
    ):
        """
        :param generate_w_js_file_path: js解密文件
        :param account: 账号
        :param password: 密码
        :param cookie: cookie
        :param sso_session_id: ssoSessionId
        :param logger_obj: 日志对象
        :param error_dir: 错误保存目录
        """

        self.logger = logger_obj
        self.account = account
        self.password = password
        self.cookie = cookie
        self._sso_session_id = sso_session_id
        self._account_id: str = ''
        self.__gt_token = ''
        self.error_dir = error_dir
        self.generate_w_js_file_path = generate_w_js_file_path

        super().__init__()
        self.request_session.cookies.update(self.cookies_dict)

        if self._sso_session_id:
            self.request_session.cookies.update('ssoSessionId', self._sso_session_id)

        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",

            "Cache-Control": "no-cache",
            'Pragma': "no-cache",
            'Priority': "u=1, i",

            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            'User-Agent': self.user_agent,

            'Host': 'xinghuo.xfyun.cn',
            'Origin': 'https://xinghuo.xfyun.cn',
            'Referer': 'https://xinghuo.xfyun.cn/desk'
        }
        self.chat_id: str = ''
        self.single_answer: str = ''
        self.single_answer_obj: Optional[AiAnswer] = None
        self.single_answer_padding: str = ''

    @property
    def account_id(self) -> str:
        """ 获取cookie中的账号id """

        if self._account_id:
            return self._account_id

        result = self.login()
        if result:
            return self._account_id
        raise LoginFailError(f'{self.model_name} login failed')

    @property
    def sso_session_id(self) -> str:
        """ 获取ssoSessionId """

        if self._sso_session_id:
            return self._sso_session_id

        result = self.login()
        if result:
            return self._sso_session_id

    @property
    def gt_token(self):

        if self.__gt_token:
            return self.__gt_token
        self.__gt_token = 'R0VFAAYwMDE0NzVhYjkyODEyMDFkZWZiOGM0ZDEwZDU3YTlmMWM3NDAyOWM0OTQ0M2U3YWQ5M2U5YmNkY2EwMDA5MTA1MTY1OGI4MTY3MTc1YmI2ZWMyMDM0NDZhODdhYjAwZGZjYjRkZmE0ZjcyOWU4MWZkNWM0ZmYxMWMyMjRjZWI2Yjg4YzZlYzZmODE2MTA1ZGNmNWZiNGJiYzE2NWI5NTFhMGRlNTc3YTQ1ZWM3MWU4ZWMxMGJmMmIzMTIyZTg4NTUyMGI5ODkxZjZlYzZjZmUwMmE4ZGM3MzkyMmVkZmEwN2NkMDVkNDgxMjYwY2JlMjllMzFlNjAyM2YwNjIwNWI0ZjA4ZmVkMTYzMzIyN2EzMWVkYWI5MTI5ZmRjOTQzZWNmMDlhZGYwNjMzNDk1MDk2ZjgzZWY5Y2RkMDc3ZTk0N2U1YmY1ODI3MjhmOWY4ZmQ3ZDVkN2JlYjRlN2NhYWEwNWRjMWU1Y2YwNDc1YzZhNGRmNzM2M2QxZTQxNjAwZjA2ZjI3ZDQyNjZmNmNhZTE5NjE3YzU5MGFlZjViNjE4NDNhNzIyMmFhNDVmYThmODc2MTAyOWFjZGJiZDZiNTVlMzQzNTQxZTFmMWE2ZTc3Y2I2OTk3NDkyZDk5OTZjYjY1YTY0ODkzN2UxNmU5YmRhYTY5OGE2NjIzMzJhYzhiZDllZjlkMGEyMTFkMDM1YmRkZjE4MjA4ZjBkMTg4NDA4OGUyMmM2NjY2OTFiMmU4NzU3ZTg0YTIzZDk3MGJjNTY2ZTFlMDllNzU4ZmFkNjUzNzdhNDJjODgyMDE3OTAzNWU5OWRmMjcwNzJkM2Q2MzEwZGU5NTFjY2ZiOTlmZWU3NDMyZDg3OGQ0N2IxYjkyMWRjNWY4MGE0NWRjMmUzYjFmOGVmYWYzYTNhNTE2Zjk4MjRjZjM1YmQ4ZjllYTA3YTRiMjQ5Y2FkMzBiMTgyY2FkY2Y1NjlkODk0MDQ3NDBjYTA2MjJiM2I4ZmJhZDY3ZjE4ODBhZjdhYzhjZGZlZTZjMDQ5ZmI2ZWNhMWFjYmNhMDc1NTM0MjYzMjY2MjlkMTA4MDhjYzhjMTU3ZDRjMDRkNDkyZWRjYTEwMjc2NGJmNzdjNDA5MWQ1ZGE5ZDdmYTI5ZmM5NmVmNjdhOWJlZGU4ZTFiM2VjODM1NjdkMjFhMjIyMmEzYmVkOTZlNjVlZDczNzU4MzkyODFjODNkZmJhMjIzZmE5N2E4OWFjZjc3ZGI3MzQ1OWRmNWJlNjQyYzU2MmI4ZGZjZDg2YmMxNWI5YThlMzAyN2YyMDk4NDZjN2JjNjg3NDQzMGNmZWNkODJkMDE1MmRmMDQ1ZDE3ZjUyZjM1NjM1ZDVlZmE4Y2UxZjc5NWM4NzcyMWUyOWE2ZTEyMTZmNWIyNTEzMDM1MmQ0MDcxOGQ3M2I0Nzg5YWQ1NWIwMWJiM2VhYmQ0NmJhYjVmODFlMjE5YTJjNGE1MDQ2NGJiODg4ZGZiNjA0ODc4NTIxYWM1NmRlMWYyMzYwNTFiZTE3ZTg4ZWExNDJjOGQxNzdjMzIwZWZlMGM5ZmZjYjZkNGI1NzBmYjRjMjk2Y2I5N2U1ZGQ4NzEwMTg5ZmFhMTk2NzI5OTQ5MmFkZWYzOTM4MTNmOTc0MTVjZDZhM2VjYTkxOTM1NmJjMjkxMWExNDMwOWUxNjhkOWIxOWZjZDExZjNjZGIyMDU4OWM3MTAxNzhiMWRlYWI1ZDk5ZDY1YmE1ZmZkYWM2MjljZWI3YmEwMTBjMDQzNjgzOTQ3YmY5MTdhNjQ4Mjk1N2ZlMTk5N2QxYWNjNWNhN2M0MGI4NjMzYzI2YzFkYWJmN2Y0OTBlOWU1NDY3ZjNkNjY4MTQ0N2I0ZTVkNDczOTcyMDA0ZjlhM2JmMWJiMzQxZDFhODk5M2ZhZTIyZjE0NTI4YzNhN2ViM2U0YjYzZWYyNWFkYWUyMzY2NjhiZjcxMzhlYzc5ODA0ZDg3MmRmNzViMDI0MDdhNzI3NjliN2QyODg2YWZjNmNiNzUzOTFiY2RhNTYwMGY0YmRlYTdkZWZmYzc4NDkwYTBiYTFkYjBiZTdkYjc0ZDI1Yjg0ZDNkMDRiZWViOTMzMDM5ZDFiY2NjM2EwYTA4YzNiNWQ1ODJlMzcxNjgxZWYzNmM3NWRkNDA4NDJmZTgxN2I5YjZiYzRmYzRhYjViODRlNTllYzc2NzVlYTE3YzlmNmYyYTQxYTJmNWM1YTllYWE1YjQ2NjcwMDM1NzU0NGM1OGUyMGIwNzRlOTQ5NDA4MWZiMzRiOGRjZjkwMjdmMDI0ZTI2M2I4MTVlMjI2ODEyNGMyNGJjODQ4OGExZTMzZDAwOGIwZDljMDdkZWIwMjI5OGYyNDFmNDU5NzZmOTg3YzdiZmM2MTQxOGFmNzNjNDBjMGFkZGQ4NmMzM2FjOTFhYjRiZmU1ODc5ZWVkOWM1ZDJhNDRlZGY1YTc4NTk4ZmRhMzU0YmUwMDIzYTA1ZjYyNDk4ZWNmNTZiOWZiMDU5YzhmZDU5ZTYxOWUwYzU1YjQ4YmE4YjdkZTA5MjYzZDMyMWE0OWY0YTE4ZDY2ZjdmZDA4ZDg4YzY4MmM1NGQ2NjhjMzdkMTdlOTg0ZDgxNmJmYjJkZTkyYTQwNTEyMWM4NjIwZjE5NmViYTJjYTdjZjcwODA0ZjRmZTQ5NDg5NjMyYTBmMjJmYmIzMzU1NzBjNjM4N2E2Y2QyNzVkYWRiMGM5NjMwZmVmZTIxZWY0NmE2MWMxNzRhOGUxNjVhMWUxNTYwMTY5NWQzNGVlMDBmMmVkZjFlMDA4MGMxNGZiMzExOWQxYzg5MWFmY2IxMTZhYmFjZTEyNDUzNjY3NjMwOTlkOWNlODM0YjNkZWY4NTM5MzQ4MjU2NzM3ODY0M2E4MDQwYjc1N2Q2YTM1OGMwZTk5YmZiOGNiZDE3MzNiMTlhMTAwZjI0ZjcyZTBkNzM2MDMzZTUzNWZlNWRkY2QwNmMwYzQ0ZDRlZmJlMDhlMjZhMDMwZDFlOGUyYmQ1OTY0ZjQ1ZTMxYTkwMjA3NmQ0YzhkODMzMTBjNzAxYTY3NmRkMWU0YTY5NjhjZDU3YzY5ZmRiYzA2NjM1ZWZiYzMzZmNhNWJkYzc5YThjOWQ4YzI3YzdlNDg4YjdjMTUyNjQ0ODMxZDU3M2U3ZTJhZDUzZGNiYmRhYzM1ZmQ3MTcwYTVlNWIzOTg2ZTA0Y2RjOTg4OTg0MzBmOWYxNjRiODljMTJjYjdiYWM3ZDNmOGMxNTUyOWRlZjNjMGJmMTUyYWIxMzM1MmVhYTg1ODAwNDcyYzIwYjYyMTdmYzY1YTlmZTJkYmZiYzQ5NjJhZjEwMzEyODA0ZmUyN2YxYjYwYmEzYmZhOTAzMzVjY2FmNmQzMTM5ZGRhODE2ZjM3NzBlYWNiM2Y4MTZiYmQ3OTc0YWYzNjc0MGYxYjU2YjQ3NzY4ZWM0ZmM2NTkyN2IzOTcxODA3NzhlN2ZhZDJmNTEzZTE1MjIyOWE2NGQ3ZjM0OTY1M2I1MjEzNTdjZTJjOGI0MDYzYWQ4ZWYxZWUwYTMwYTNlOGFiMTg2ODYxYzhkMGFkYWNhMWZjMzgxMTIwOWIzNWQ4ZGI2MGExMGY0M2MzNDVmYTFjOWM3YzM5MGVjMmVhNDljZjQ2N2QxNWIwNzFlYjU5NDNkM2U0MzVhMGQyZDUzODE4YWY3OTJiNDcwNTExMzk2ZWY1YzUzYjZiMzI2NWNhODlhZDVlYmUyNTYyMTQzMzk1YTY4OWM5MWNjODBhNmJhYzJiNDhkOGQ2MWY5Y2RjZmFiNDI3MWQwYjQ5ZTQ2ZDBiZDg5NzVjMmE2Mjk1ZGRhMDY2MTkyZThlNTc1NTA2YmI4MGUxNDAxMjcxODkwNjU5NGYzOTIwYmViZTczYmYzNzgxM2YxNzMxMjMxYzUwMGZlMDliNGYwYzc4NjZlYjhhMGE4NTg2MDhmZjUzZGRhOGFmZDhlMjQ0YjNlYmU3NGZhMjZiYjYzYWEwNGZiOGUwYmI2ZThhOGFhNTg5YWVkYzI3MDVhNWIzMDVmMTM2YWFiYTk2ZDM2YjM3ZmQ0ZWVhN2E2YmYxYjEyN2FkM2NmZWNlNWJjMWMwODI5YzNjNzA4YzYzNjYwYTNjYzA0MDY3OTM0YzZmNmYwZWU0Y2EyZGU1NzczNTA2MGE1M2MwOTU3YmM3MGU1Yjg1ZGUzYjk1YzQ0MmJjNzNmMzgzMmM5MjU2YzJmNDZlYzIwOTFkNjY0ODBlNjU0ZDlkZmY1NTk0NmY0N2ViMjY0ZWE4NjdjYjY5ZGExZmMyM2ZjYWEwNWMzYmY0NzE1ZTU3NzU3NDkyZDcxZmZjYjdmMjJmODE4OTEzOGNlMzhlMGQzMzhhODczZTI5ZTNmOWYzZDRlZjlhNzk0MDlhMGRhZWQ4ZmEyMDZiZDQ0NmEyZDY5YmU5ZjNhZWJjMDdiMjM4YjEzNWVjMTAwYzhhNzdjZTZjN2U4MzI0MzI3ZTI5NmIyZDQyNDg2ZGEzNzQxNTkzMGQ5ZjJjNzMzNmM1MjVjYjM5OGE3ZDMxODkzNWFjNzMxMjFiMzJiY2RmOTMyOWQ1NjdjOTY3Zjc2ZWYxODVjNGQ0ZmZkZTBhODRkZmNkZjU3MDEyMGIwOGI0ZWU0MmEwNDkxNjYxNzRlZjVjMjAyYzIxODNmNDhhNTJkZTFmMWVjZjRjZGJiMmI1ZmQ1ZGU5ZTJiMWMwYzgzYjk4NTBlNmZmNmFjN2VmODhlYTMzMzRmNTU5YmQ4Yzk0ZWI0YmFhMmVkMWY0NzdiMDFjNGI2NDJjZWJlMTQ3YjE0NzhmMzJkMDQ0NDIyNDVmNGZjZDgxMDdkY2RhMjliMzc0MTAzYjRhODdjNTkwNWZhNTlkNDVkODAyMDYxMThiOTA3ZGM2MDRmNGJhY2Y5ZjljM2E2ZjI5YjJhZDA1OWIwNjBhMTkyNTNmZmU0MTNjNzNiNWNiZmMwYWM2ZWZlZTM0ZWU5Y2E4MWM4ZDYwOWZmOTg0ZmYwMjE0YzE2MGNmN2Y0OTgyZDFkNGFlN2I0MTY1MGUxYTE1NDJjNWMyYWUxYTc5M2Y0MTdjMTdhNTk5OGE2MmFhNjBiNDgxMDg5YWRmOGY5MDMzMTlhNTFhYTQ0NDNkMjY0MzAyYWFhMjRiYjRhNjA4ZmE3NDQ4NTU1OThkZmY5MDMzMTYyNTI3ZDZhNmFkODA1N2VjN2Y3ZTU1NzE0ODZmYWRjM2RkNWRiNGVhYzQ0ZjM3NjJhZGI4MmNiZWY4NmVmMDMxNGJmOGYyNDdmNjU2MWFmNjVhOTllNDkzNjdlYWZmN2U3YWM1YjliZmIxMGQwMGU3M2RkODRkYzRjNTc2MDYwMGM2MmUyMzg1M2Y1MGJhOGMwZDU4NGE0NDllOTQ1MGNhNGY2MWIxZmQyZmEzYmVjOTczNTVmMGQzZGRhZmY2ODBjY2Y5ZTg3MmFkZGJiNGZkZTViZGZhOTZiNzQwZTkyNzEzMzJhMzBhMmUwYzg4NzZkYmY0ZjQzNDM5MDI0YTUyNGJmNmU5ZDY4OWQ1ZTJmMDgzNDgzNDkxODU3OGFkNGJkZDZmMjMxOTkyYzY3MDQ2YmE2Y2I4ZTgwNGFkN2Y3YWYzYTYyOTUzNWQ3ZTk0NTZkOTM0YzE4YjE1NGMwMTJlMmFkNjY3OTkxZjMwZDhjMGIxODRmMTViYTlhMGMwM2M5ZTQxMGNhYzcwZTFkYTg2ZGYzY2ZkYzczODkwMTZjMTFmZDllMTgyYjM4ZjE3NjgzOWVjNGUxZTgzMTYxMDJjZWIyNjg3NzZjNmY1YTU3NTU0YTI1NmFiNDM5NDFkY2RjMTA2ZjU0NWI5ODI1Nzc3ZmRhZThmNmE3M2YyNmNlNGVhN2JiYjg3NDlmMjM4ZThjODc4Y2U3Y2JiOWI2OTVjODNjMmVlZjVkN2M3ZjM2YzNhMGFkMjlkMmM0NzYyMDkxNDkzNTFlZWRjZjUyY2E2NTI1ZmExYjQ5MTAwYjgyYWEwMjJhOTk4ZTg2YzY4NjljZGZmYWZlYjg4ODcyYjk5OWNlZWE0OTI4MmExMDBjODBhZTA3MTYyYTAyNDA0N2QyOGUyYTE4MDIzYWQ5ZDI5ZDRjZGFiY2RmY2VlYmEzNTk3NWQzMTM2MGY4NzU4MDNmNzUzYjdkNzNmYjc0MGRjYTU1ZDBkYTQyMGJmNTJkOGY5ODk1MzYwZmQ4NWYyZjRlYWFiMzAwZWZkOTA5ZDU0YjY5MTYwYjg2MjQ5YzdiNGUyNWU3NTk4ZjY1ZGM0OWNiYjZlYzVhNzJlMzgyMWY0NzhkYTJkZTI5Yzg3MTE0YjBiMDM5MTkzNjA3NWFlNmJiY2EyMzViMWM4M2IzOGZkM2Y2ZWJjOTY0MmI3N2Y1NTkyOWEwMDYyYWY1ODgyYTg3ZjdiZTNlNDQ2ZDRmYTRlZDkzYTY2N2Y1YTQyOGVhMGU5MjI5ZDY5ODFkYmZjNmEwODQ4ZGNkYWE0Mjk2MGYwMWUzYmRkZTI5YTA5NmJiNGUzNTVjZTUxYjBiZTVjN2RkYWZlZWExMzBlNGUwMTQwMjYzYmY3YzAwNzljNDA0MDViZjAwMmQwYmMxMjNhZDAwYWVhN2VlYmNlMDdmMWU2YWQyNzM3MTM1YzlmYzk5YzAxNTlmYTgyOTZlMzVlOTUwZWI3ZDAxNGQ3OTA1MTg1YjUyZTg1MjQ1MjdhNzkyNzI5ZGVlZDUzMzgzMmYxYmI3NjQ5NWYyNjRiNGIzZTZmMDVhMzUwNGFhNjU2N2I1ODJmN2Q1MzcwNjg3ODhlYThkM2RhNWVhMGY5MGYyOGE4YTMwY2EwNjBmMDE5OTIyZDQzMjdhNTVhZTA0MTAwNTBkMmVlMjcxYmNiYWJkNGQzNjFjZTA4ZmI0MzQyNjc4OGFjMTE4NTA5N2EwNDgzMDRmZGIwZTdiZDRmNDFhNzI5Mzc1OTllNGNhMGVhNGRhNjcxOGJiNGY1M2NmNWRiMGNkMDQ0M2U2ZTA2Mzk1ZmVkYjlhZGM0ZjZiNzdiZTQyNDNlYmRjOGRiMjdhNDc4YTgyYWVlOGZjOTc3MTFmODI0NDhmYTk5YzFiMWY2Y2UxNDFkMzYyNTc4MmUwNWQ0ZmM0ZDJkOGY2NGE2MzM1MmNmNjUxNGFjZTQ5ZTMwNmJlNWEzMmZjZDllNDRlNjZhMTYzYjVmMmExMDI0NGVhZTc0N2U1Y2I2NmQyNmY4ZmMwYTg0ZmU1ZTcxNDc2ZDJiYmFiZjZkZWNkMzEwMGFiNmYwOTEzZGJlZDdlMGI5YTNhMWVmNjVkMjA0YTRmNTRmMzJjYTU1MTY2OGRiYTQ5NjBjYjI4ODUxZWIyYjg4ZmRlODY1MmUyMjBiNjIzNzA3MWJlM2NhMjQ3NmM1NTllZTk5OTU1OGM4ODA0ODVlNzgwYzYwMDIxOWNlNTdjZjJiNTA1YWJjNGUzMDljOTVlODZhZWIyNDhkYmJiZDM5Y2RhNTgwMmJkNTQ2MjZhNDYwZTk3MWQ3YjM2N2QwYjM5ZWJhZDJhOWQxZDVjMjYyN2JiOWQyZTM5ZTFhMmViZDEyNWYzMTMzZDk5OGUwMDQ0MjQ0OTgxYWU2MjNkODY1MTdhMTBhM2E3ZmZhNmRlYWQzMzAxOGI2ZTdlMTA2Yzg4NjJjNzY1MTc1ZmY0ZDljMDUzNmYzYjViMzUxMTg1MDU0ZjYyZjZiYTU2ZTFlNmViYjI3YmY0NWMyOTE4NmY2NTUxOTQ5NzUyNWVhZTVkZGNmYjNlMjIzZmIzNTcyNjk0Y2ExNjRkM2JmNjlkMTVjZDEzMDQwYTgwNWVkZTg2MDQ5MzE0Yzg1NzJjZjBiNDNhZTg5ZjkxZTdiM2NkY2Q4MzkzMTMwODQ5YjJkOTBmMTIyMzkxYjk2YzVhOTZiZmYxY2E2Mzg1M2YzZDNhMzM4MWM2MTFiNTAyMzNiNzQ0YTMzY2QyMzBhMTEwNTU0NGNkZjBmOGNhYTcyNjgxMzc1NTAzZDAyMWFkZTU3MzY3MTUyOGJiNmVjZTcwNzA4ZWMxNWY2ODNiNWE1MmE5MzJhYjU5ZjE0NjkwZTU5NDYxNGYwMmVkZjNlNTYyMDFkZTQyNDU4NmY3NmE1MjY0ODNlNzE4NDQ3YTkxNjc3ZmEzYzE2MTVmNmYxOWFlNzgyZWFlNzFhYjZkOGRhZmIxZWRkNzU1Yjg3ZTZmMTU5ZDNhNTIwYWU1NTFjMjM2NzFiODIzMDg4OGE5NTM0ZWU5MWMxMWVmODY4NjM1ZDYzNDBiZjhlNmUwZWZlZmRkNDhhZDg0OGU5ZTMwNWZjYjJkYzFmYWM1ZWNjNzJmNjdkNWZhY2Q1YThkMGEyNGNkM2FmODQxNzhmYzVkYWExY2M2MTcwM2Q1NmY5ZDBiZTQ3NDQyN2E3MjZjZDY5YzExOWU3OTYyNWJmNDhhZjlmYmI5NTYyMWU0NjBkMmFhYjE5ZTk3NWZiOTcwZGIxYzA2MjBkNDRlNTYzOWNhODM1M2NlYTQwNjhkZDBjNmU4NDA4MGZmMjA4YmYxMmEyMDE2ZTkyMmJjZTgzZWRlMzk5OTE1MjZmMDlkMDM5MTcwMTE0OGI4ODdkOTM4OGNhNzVlNDNhZWU1NjE3ZDRmOTdkMjkxYjQyYTkyMjY0YzJjYjQ4MmE4YTAxYmMxODNlOWU4MmE3NTM4N2UwOTBhNDQxYWY4MTNiZjQ1ZDUwMjkzNzRjMWI0ZTRiODE4ZjRjOGM1Y2ZjYzMxNGYzZDlkODkyNTBmZGUwYTU1MTY5ZGU0YjRmZmM5MGE4NWRkODAzY2VjZGFiMDJiNDJkNmZkMTQzZThhZDgyN2IwOGJkM2U2YzUwZDQ0ZTRkZTZmMTk2OTAxMGEyNDhiYjFhYWVkYTFhMmFjNGUzMjllMjQ0NDUzODk2MzVjZjk2M2M2ZTFhOTgwN2FhMjM3NDYxMzgwMGIwM2IxNjY1MDBhYzJkMTU0MmIzOWVhZDEyYjFkYzdjZDI3MDY4NjgwYWRlOTFlZWQ1MjFiMjZkMzMyYmEyYTE4ZDUwNmNhYjE0MzExZDMwZmU1YTgyZDI0YTdkZWM3ZjFkMjZjOGNkNmRlMWFiOWM3MDdlYzA4ZjViODQ3YThjYzgxMWFhYjI4NjU1YzJiMWI0M2UyNWU1NTJiMjdkZGRmMzY1ZmZlYTQ0NmQxNDU4YWY4OTMxMWMyM2RmYmZkYjgxYjA2NDNlODEyOTU2NTljNGU4ZmM1NTA4MDY0NTU0ZDZlMjZiZmNiNzQ4MWZkZjhhNTJmMmNmZjMzOGQxMGU5MGFhYTZlMjdjZjFmNTcyYzllN2QxODdhODNhOWJmYjUxMDc5OTBmMzI5ODQxYTIxZTAxMDA2NGFmZjU2MjA4OTU4MzA0YzIxMDYwMmIxZWY5N2UwMWQ5NWU1Y2VhMWI5ZTkzN2YyMzEwOTg4MTA5YzcyMGYxYzJiZTZhMTQ3ZmY2Njk2NTgzYmJmN2M2Njg2ZDM1NmVlZjFkYmYxM2M4NThlMTZiOTZiZDcwZmRkMmUxMzA4NzUzNDY1NDBhZjE5MmFiYTQyNTU2ZGE1NDI0YTZiNWM3ZDVhZWVlYzhlYjc0YzRjODhiY2I2OTY3MzIzMWU3NTcwZjlmM2UxMDViMmY3MmE0Yzg2MmM5NDY3YTFlNWU2Y2E2M2JmNTNhODZlNWYwMjQzYWY4MTVjOGYxNWVkY2YyNmJmZDZjYzJjNzgyMGMwYjkxZTEyYzliZDVkZGRjZWEyYTA2MDdlOWFmYWI5NzVlMmM3MGZlYjVlNzNmNGE1ZWY5ODkzMDhiZmJhMzlmMGVhODNjNTMzYmEwZDc3NzI0NDU3ZTMzNTZkMTc5MTc2ZTg0MWNhMzVjZWI2NjBkYWIwODExYTk5YWFmYzU0ZGZiMzNmZDI0OTZiNGVjNzNjODJjY2RmNmRjOTIzYmFkYQ=='
        return self.__gt_token

    @staticmethod
    def decode(text):
        try:
            decoded_data = base64.b64decode(text).decode('utf-8')
            return decoded_data
        except Exception as e:
            return ''

    def check_response_status(self, response: requests.Response, jsonfy: bool, function_name: str = None):

        result = {
            'is_success': True,
            'response': response,
            'continue': True
        }

        if response.status_code == 200:
            if jsonfy:
                result['response'] = self.parse_data(response, function_name=function_name)

        elif response.status_code == 401:
            self.logger.error(f'The response status_code is 401, need to login again.')

            self.logger.info('即将尝试重新登录...')
            login_result = self.login()
            if login_result:
                self.logger.info('重新登录成功，即将重新请求...')
                result['is_success'] = False

            self.logger.error('重新登录失败，即将退出程序...')
            result['continue'] = False

        else:
            self.logger.error(f'【{self.model_name}】 get failed, status_code: 【{response.status_code}】')
            result['continue'] = False

        return result

    def get(
            self,
            url: str,
            headers: dict = None,
            params: Optional[dict] = None,
            function_name: str = None,
            jsonfy: bool = False,
    ) -> Optional[Union[requests.Response, dict]]:

        for i in range(3):
            try:
                if not headers:
                    headers = self.__headers

                response = self.request_session.get(
                    url,
                    headers=headers,
                    params=params,
                    verify=False,
                )

                check_result = self.check_response_status(response, jsonfy=jsonfy, function_name=function_name)

                if check_result['is_success']:
                    return check_result['response']
                elif check_result['continue']:
                    continue
                else:
                    return

            except NeedLoginError:

                self.logger.info('即将尝试重新登录...')
                result = self.login()

                # 如果成功重新登录，则重新请求
                if result:
                    self.logger.info('重新登录成功，即将重新请求...')
                    continue

                # 如果登录失败，则跳出循环，直接返回
                self.logger.error('重新登录失败，即将退出程序...')
                break
            except UnexpectResponseError:
                # TODO 这里暂时留空，后续补充
                pass

            except:
                self.logger.error(f'【{self.model_name}】 get request got an unexpected error.', exc_info=True)

    def post(
            self,
            url: str,
            headers: dict = None,
            params: Optional[dict] = None,
            _json: Optional[dict] = None,
            data: [dict, str] = None,
            stream=False,
            function_name: str = None,
            jsonfy: bool = False,
    ) -> Optional[Union[requests.Response, dict]]:

        # 防止网络错误，设置重试次数
        for i in range(3):

            try:
                if not headers:
                    headers = self.__headers

                response = self.request_session.post(
                    url,
                    headers=headers,
                    params=params,
                    json=_json,
                    data=data,
                    stream=stream,
                    verify=False
                )

                check_result = self.check_response_status(response, jsonfy=jsonfy, function_name=function_name)

                if check_result['is_success']:
                    return check_result['response']
                elif check_result['continue']:
                    continue
                else:
                    return

            except NeedLoginError:

                self.logger.info('即将尝试重新登录...')
                result = self.login()

                # 如果成功重新登录，则重新请求
                if result:
                    self.logger.info('重新登录成功，即将重新请求...')
                    continue

                # 如果登录失败，则跳出循环，直接返回
                self.logger.error('重新登录失败，即将退出程序...')
                break
            except UnexpectResponseError:
                # TODO 这里暂时留空，后续补充
                self.logger.error('出现了预期外的回应数据...')
            except:
                self.logger.error(f'【{self.model_name}】 post request got an unexpected error.', exc_info=True)

    def login(self) -> bool:
        """登录新方法，添加极验滑块的逆向"""

        try:
            handler = WebLogin(
                account_name=self.account,
                password=self.password,
            )
            session_id = handler.get_session_id(self.generate_w_js_file_path)

            if session_id:
                self.request_session.cookies.update({'ssoSessionId': session_id})
                self.request_session.headers.update({'Cookie': f'ssoSessionId={session_id}'})
                self._sso_session_id = session_id
                return True
        except:
            self.logger.error(f'【{self.model_name}】 login failed', exc_info=True)

        return False

    def __login(self) -> bool:
        """登录旧方法，那时讯飞不验证极验滑块"""

        if not self.account or not self.password:
            self.logger.error(f'【{self.model_name}】 account or password is empty')
            return False

        url = 'https://sso.xfyun.cn/SSOService/login/check-account'

        data = {
            'accountName': self.account,
            'accountPwd': self.password,
        }

        try:
            response = self.post(url=url, data=data)
            resp_json = response.json()

            code = resp_json.get('code')

            if code != 0:
                self.logger.error(
                    f'【{self.model_name}】 login failed, code: 【{code}】, message: 【{resp_json.get("desc")}】')
                return False

            self.logger.info(f'【{self.model_name}】 login success')

            self._sso_session_id = data['ssoSessionId']
            self._account_id = data['account_id']
            self.request_session.cookies.update('ssoSessionId', data['ssoSessionId'])
            self.request_session.cookies.update('account_id', data['account_id'])

            return True
        except:
            self.logger.error(f'【{self.model_name}】 login request got an unexpected error.', exc_info=True)
            return False

    def get_chat_list(self) -> dict:
        """获取会话列表"""

        url = self.base_url + '/iflygpt/u/chat-list/v1/chat-list'

        return self.get(url=url, function_name='get_chat_list', jsonfy=True)

    def get_prompt_list(self) -> dict:
        """
        获取提示列表
        :return：提示列表
        """

        url = self.base_url + '/iflygpt/u/prompt/getPromptList'

        return self.get(url=url, function_name='get_prompt_list', jsonfy=True)

    def get_chat_history(self, chat_id: [int, str]) -> dict:
        """
        获取会话记录
        :param chat_id：会话 ID
        :return：会话记录
        """

        url = self.base_url + f'/iflygpt/u/chat_history/all/{chat_id}'

        data = self.get(url=url, function_name='get_chat_history', jsonfy=True)
        return data.get('data', {})

    def create_new_chat(self, chat_name: str = None, bot_id: str = None) -> str:
        """
        创建新的会话，注意，在新的会话窗口未被使用前，重复创建返回的chat_id是一样的
        :return：成功时返回新建的chat_id；失败时返回空字符串
        """

        url = self.base_url + '/iflygpt/u/chat-list/v1/create-chat-list'
        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json;charset=UTF-8'

        if bot_id:
            data = json.dumps({"botId": bot_id})
        else:
            data = "{}"

        data = self.post(url=url, headers=headers, data=data, function_name='create_new_chat', jsonfy=True)

        if not data:
            return ''

        chat_id = data.get('data', {}).get('id')

        if chat_id:

            if chat_name:
                self.rename_chat(chat_id, chat_name)

            self.chat_id = chat_id
            return chat_id

    def rename_chat(self, chat_id: int, chat_name: str) -> dict:
        """
        重命名会话
        :param chat_id：会话 ID
        :param chat_name：新的会话名
        :return：bool
        """

        # 名称长度存在限制，截取前15个字符
        chat_name = chat_name[:15]

        url = self.base_url + '/iflygpt/u/chat-list/v1/rename-chat-list'
        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json;charset=UTF-8'

        _json = {'chatListId': chat_id, 'chatListName': chat_name}

        return self.post(url=url, headers=headers, _json=_json, function_name='rename_chat', jsonfy=True)

    def delete_chat(self, chat_id: int) -> dict:
        """
        删除会话
        :param chat_id：会话 ID
        :return：bool
        """

        url = self.base_url + '/iflygpt/u/chat-list/v1/del-chat-list'
        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json;charset=UTF-8'
        _json = {'chatListId': chat_id}

        return self.post(url=url, headers=headers, _json=_json, function_name='delete_chat', jsonfy=True)

    def get_chat_sid(self, chat_id: str) -> str:
        """
        通过会话id获取最新的机器人消息的sid；
        该值与chat_id一起确保了会话的上下文记忆
        新会话没有消息时，返回空字符串；
        """

        try:
            history_list = self.get_chat_history(chat_id)
            return history_list[-1]["historyList"][-1]["sid"]
        except:
            self.logger.error(f'【{self.model_name}】 get_chat_sid failed, chat_id: 【{chat_id}】')

    def parse_data(self, response: Optional[requests.Response], function_name: str = None) -> dict:

        if not response:
            self.logger.error(f'【{self.model_name}】 search_bot failed.')
            return {}

        resp_json = response.json()
        code = resp_json.get('code')
        if code != 0:
            self.logger.error(
                f'【{self.model_name}】 {function_name} failed, code: 【{code}】, message: 【{resp_json.get("desc")}】')

            # 判断是否需要重新登录：80000错误表示token过期，需要重新登录
            if code == 80000:
                msg = (f'【{self.model_name}】 {function_name} failed! Need re-login!\n\n'
                       f'code: 【{code}】, message: 【{resp_json.get("desc")}】')
                self.logger.error(msg)

                raise NeedLoginError(msg)

            # 非预期响应
            msg = (f'【{self.model_name}】 {function_name} got an unexpected response.\n\n'
                   f'code: 【{code}】, message: 【{resp_json.get("desc")}】\n\n'
                   f'full data: 【{response.text}】\n\n')
            self.logger.error(msg)
            raise UnexpectResponseError(msg)

        return resp_json

    def ask(
            self,
            question: str,
            gt_token: str = None,
            chat_id: str = None,
            callback_func=None,
            fd: str = '',
            bot_id: str = '',
            client_type: int = 1
    ) -> AiAnswer:
        """
        在某个会话中聊天
        :param chat_id：会话 ID
        :param callback_func：回调函数
        :param question：发送的文本
        :param gt_token：反爬校验 token，半小时有效(固定一个值即可，有幂等性)
        :param fd：可选参数，目前没发现有什么用>_<
        :param bot_id：可选参数，助手ID
        :param client_type：固定是 1 即可
        :return：AI 响应报文
        """

        url = self.base_url + '/iflygpt-chat/u/chat_message/chat'

        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = 'text/event-stream'

        if not chat_id:
            chat_id = self.create_new_chat()
        else:
            self.chat_id = chat_id

        if not gt_token:
            gt_token = self.gt_token

        data = {
            'fd': fd,
            'isBot': 1 if bot_id else 0,
            'botId': bot_id,
            'chatId': chat_id,
            'text': question,
            'sid': self.get_chat_sid(chat_id),
            'GtToken': gt_token or self.gt_token,
            'clientType': client_type
        }

        response = self.post(url=url, headers=headers, data=data, stream=True)

        if not response:
            self.logger.error(f'【{self.model_name}】 ask failed, status_code: 【{response.status_code}】')
            return AiAnswer()

        self.single_answer = ''
        for line in response.iter_lines():

            if not line:
                continue

            encoded_data = line[len("data:"):]
            missing_padding = len(encoded_data) % 4

            if missing_padding != 0:
                encoded_data += b'=' * (4 - missing_padding)

            if self.decode(encoded_data) != 'zw':
                answer = self.decode(encoded_data).replace('\n\n', '\n')

                if answer.startswith('```') and answer.endswith('```'):
                    answer = ''
                    # answer = '【任务执行中】'

                self.single_answer_padding = answer

                # 执行回调函数，如果有的话
                if callable(callback_func):
                    try:
                        self.logger.debug(f"执行回调函数：内容【{answer}】")
                        callback_func(answer)
                    except Exception as e:
                        self.logger.error(f"回调函数执行出错: {e}", exc_info=True)

                self.single_answer += answer
                sys.stdout.flush()
            else:
                self.logger.debug(f"AI交互结束")

                # 执行回调函数，如果有的话
                if callable(callback_func):
                    try:
                        callback_func('<<<end>>>')
                    except Exception as e:
                        self.logger.error(f"回调函数执行出错: {e}", exc_info=True)

        self.single_answer_obj = AiAnswer(
            content=self.single_answer,
            is_success=True,
            conversation_id=chat_id,
        )

        return self.single_answer_obj

    def search_bot(self, bot_name: str) -> dict:
        """根据名称搜索助手"""

        url = self.base_url + '/iflygpt/bot/search'

        data = {
            "searchValue": bot_name,
            "pageIndex": 1,
            "pageSize": 45,
            "botType": ""
        }

        return self.post(url=url, _json=data, function_name='search_bot', jsonfy=True)

    def reset_bot(self, bot_id: str, chat_id: str):
        """
        【待完成】
        助手2.0重置话题
        """
        url = 'https://xinghuo.xfyun.cn/iflygpt/u/bot/v2/restart'

        params = {
            'botId': bot_id,
            'chatId': chat_id
        }

        response = self.get(url=url, params=params, function_name='reset_bot')

        return response.text

    def get_gt_token(self):
        """
        【待完成】
        对于gt_token，经分析是极验的风控，定时将旧的gt_token更换
        但讯飞似乎并没有进行验证
        """

        url = 'https://riskct.geetest.com/g2/api/v1/client_report'

        data = {
            'gee_token': self.gt_token,
            'u_sign': {
                'time_stamp': '1715318375157',
                'client_type': 20200,
                'carrier': 'CT',
                'callback': 'geetest_1715318384663',
                'format': 'jsonp',
            }
        }

        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['AppID'] = 'ihuqg3dmuzcr2kmghumvivsk7c3l4joe'
        headers['Host'] = 'riskct.geetest.com'

        response = requests.post(url=url, json=data, verify=False, headers=headers)
        print(response.text)
