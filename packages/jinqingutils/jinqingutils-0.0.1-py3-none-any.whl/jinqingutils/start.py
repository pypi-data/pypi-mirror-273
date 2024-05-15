# -*- coding: utf-8 -*-
# @Time : 2024/1/15 10:43
# @Author : ZH
# @File : start.py
# @Software: PyCharm
import logging
import time

import requests


class LoggingInfo:
    def __init__(self):
        # 创建logger对象
        self.logger = logging.getLogger()

        # 设置日志输出到控制台
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 设置日志等级为DEBUG
        self.logger.setLevel(logging.DEBUG)


def calculate_time(func):
    """
    装饰器
    :param func:
    :return:
    """
    logger = logging.getLogger()

    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录函数开始执行的时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录函数执行结束的时间
        execution_time = end_time - start_time  # 计算函数执行时间
        logger.info(f"函数 {func.__name__} 的执行时间为: {execution_time} 秒")
        return result

    return wrapper


class JinQing(object):
    def __init__(
            self,
            token,
            task_create_url: str = 'http://192.168.1.124:32280/api/v3/task/task_create',
            task_run_url: str = 'http://192.168.1.124:32280/api/v3/shop/shop_run',
            task_state_url: str = 'http://192.168.1.124:32536/api/v3/external/collection_instance_info',
            collection_instance_url: str = 'http://192.168.1.124:32536/api/v3/task/task_export',
    ):
        """
        堇青操作基础类
        :param token: 认证token
        :param task_create_url: 任务创建url
        :param task_run_url: 任务启动url
        :param task_state_url: 获取任务状态url
        :param collection_instance_url: 获取数据url
        """
        self.logging_info = LoggingInfo().logger
        self.logging_info.info('*' * 10)
        self.logging_info.info('天王盖地虎')
        self.logging_info.info('*' * 10)
        self.token = token
        self.task_create_url = task_create_url
        self.task_run_url = task_run_url
        self.task_state_url = task_state_url
        self.collection_instance_url = collection_instance_url
        self.header = self.get_header()
        self.collection_id = None
        self.collection_instance_id = None

    def get_header(self):
        # 首次执行的时候需要获取token
        # 堇青自身token认证，使用年限10年
        collection_token = {'code': 0, 'message': '成功',
                            'data': f'Bearer {self.token}'}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        headers.update({'Authorization': collection_token.get('data')})
        return headers

    def get_requests(self, url, headers, **kwargs):
        try:
            response = requests.get(url, headers=headers, **kwargs)
            return response
        except Exception as e:
            self.logging_info.error(f'请求 {url} 错误 {e}')
            raise Exception(e)

    def post_requests(self, url, headers, **kwargs):
        try:
            response = requests.post(url, headers=headers, **kwargs)
            return response
        except Exception as e:
            self.logging_info.error(f'请求 {url} 错误 {e}')
            raise Exception(e)

    @calculate_time
    def task_create(self, json_data, **kwargs):
        # 任务创建
        response = self.post_requests(url=self.task_create_url, headers=self.header,
                                      json=json_data, verify=False, **kwargs)
        return response

    @calculate_time
    def task_run(self, collection_id):
        """
        启动模板任务
        :param collection_id: 任务id
        :return:
        """
        # 启动模板任务
        params = {
            'collection_id': f'{collection_id}',
        }

        response = self.get_requests(url=self.task_run_url, params=params, headers=self.header,
                                     verify=False)

        return {'state': True, 'collection_instance_id': response.json().get('data').get(
            'id')} if response.status_code == 200 and response.json().get('code') == 0 else {'state': False,
                                                                                             'collection_install_id': None}

    @calculate_time
    def get_task_state(self, collection_instance_id: id) -> dict:
        """
        获取任务状态
        :param collection_instance_id:
        :return:
        """
        params = {
            'collection_instance_id': collection_instance_id,
        }
        response = requests.get(self.task_state_url, params=params, headers=self.header)

        if response.status_code == 200 and response.json().get('code') == 0:
            return response.json()
        else:
            raise Exception('获取任务状态失败')

    @calculate_time
    def get_collection_instance_data(self, collection_instance_id: int, limit: int = 2000) -> dict:
        """
        获取任务数据
        :param collection_instance_id:
        :param limit:
        :return:
        """
        params = {
            'collection_instance_id': collection_instance_id,
            'limit': limit,
        }

        response = self.post_requests(url=self.collection_instance_url, params=params, headers=self.header)

        return response.json()

