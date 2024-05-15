# -*- coding: utf-8 -*-
# @Time : 2024/1/15 11:00
# @Author : ZH
# @File : setup.py
# @Software: PyCharm
from setuptools import setup, find_packages

setup(
    name='jinqingutils',
    version='0.0.1',
    author="HengZhang",
    author_email="zhang19990906@gmail.com",
    description="堇青平台调用方法",
    packages=find_packages(),
    url="https://gitee.com/zh19990906/jinqingutils",
    install_requires=[
        'requests'
    ],
    python_requires='>=3.7',
)
