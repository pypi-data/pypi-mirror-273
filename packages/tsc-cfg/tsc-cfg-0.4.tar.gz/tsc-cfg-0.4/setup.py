# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

if os.path.exists('readme.md'):
    long_description = open('readme.md', 'r', encoding='utf8').read()
else:
    long_description = '教程: https://github.com/aitsc/tsc-cfg'

setup(
    name='tsc-cfg',
    version='0.4',
    description="自定义的配置文件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='aitsc',
    license='GPLv3',
    url='https://github.com/aitsc/tsc-cfg',
    keywords='tools',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.7',
    install_requires=[
        'tsc-base',
        'watchdog',
        'redis',
        'jsonpath-ng',
    ],
    extras_require={
        'recommended': [
            'tsc-base==0.42',
            'watchdog==3.0.0',
            'redis==5.0.1',
            'jsonpath-ng==1.6.0',
        ]
    }
)
