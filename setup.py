#!/usr/bin/env python
'''
'''

import setuptools
from distutils.core import setup
import os


setup(
    name='vimbug',
    description=('A plugin for vim that creates an integrated debugging '
        'environment.'),
    long_description=open('README.rst').read(),
    maintainer='Lee Olayvar',
    maintainer_email='leeolayvar@gmail.com',
    version='0.0.0',
    url='http://github.com/leeolayvar/vimbug',
    packages=[
        'vimbug',
        'vim_debug',
        ],
    scripts=['bin/install-vim-debug.py'],
)

# vim: et sw=4 sts=4
