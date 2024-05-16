# -*- coding:utf-8 -*-
"""
@Author: 风吹落叶
@Contact: waitKey1@outlook.com
@Version: 1.0
@Date: 2024/5/15 16:15
@Describe: 
"""
from setuptools import setup, find_packages

setup(
    name='silgeai',
    version='1.2',
    packages=find_packages(),
    description='洞墟科技有限公司AI产品SDK',
  #  long_description=open('README.md').read(),
    # python3，readme文件中文报错
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/my_package',
    author='WhiteCome',
    author_email='waitKey1@outlook.com',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ]
)
