# -*- coding:utf-8 -*-
# Author:凌逆战 | Never
# Date: 2024/5/17
"""

"""

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "neverlib",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    author = "Never.Ling",
    author_email = "1786088386@qq.com",
    url = "https://www.cnblogs.com/LXP-Never",     #项目相关文件地址，一般是github
    description = "A successful sign for python setup",

    packages = find_packages(),
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)