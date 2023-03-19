'''
这是一个用于安装PyNARS的setup.py文件，其中包含了PyNARS的版本信息、依赖关系、作者信息等。通过运行此文件，可以将PyNARS安装到本地环境中。

包依赖关系：
    setuptools
    pynars

全局变量名称及其作用：
    this_directory: 当前文件所在目录的绝对路径
    long_description: 用于在PyPI上展示的项目介绍

各函数的依赖关系和主要功能：
    read_file(filename):
        依赖：os_path
        功能：读取指定文件的内容并返回

    read_requirements(filename):
        依赖：read_file
        功能：读取指定文件中的依赖关系并返回

    setup():
        依赖：find_packages, read_requirements
        功能：设置PyNARS的安装信息，包括名称、版本、作者、依赖关系等
'''

from os import path as os_path
from setuptools import setup, find_packages
import pynars
this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='pynars',
    python_requires='>=3.7.0', # python version
    version= pynars.version, # package version
    description="An implementation of Non-Axiomatic Reasoning System",  # introduction, displayed on PyPI
    long_description=read_file('README.md'), # Readme
    long_description_content_type="text/markdown",  # markdown
    author="Bowen XU",
    author_email='xubowen@pku.edu.cn',
    url='https://github.com/bowen-xu/PyNARS',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'), 
    include_package_data=True,
    package_data={
        '': ['*.json', '*.lark', '*.txt'], 
        'pynars.utils.SparseLUT': ['*.pyd', '*.pyi'], 
        },
    license="MIT",
    keywords=['NARS', 'Non-Axiomatic Reasoning System', 'NAL', 'Non-Axiomatic Logic', 'Narsese'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)