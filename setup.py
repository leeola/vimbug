#!/usr/bin/env python
'''
VimBug
======

VimBug is a plugin for vim that creates an integrated debugging environment
focused on the debugging of Python applications. It is also intended to
work with any DBGp compliant server, it just hasn't been reliably 
-- *if at all* --  tested for any servers other than Python.

Note that this plugin was forked from 
`vim-debug <http://github.com/jabapyth/vim-debug>`_ due to the author
*(`Jared Forsyth <http://jaredforsyth.com>`_)* being on an extended trip and
unable to respond to any pull requests. It is the intention of this project
to one day merge with vim-debug again.

Thanks for the wonderful work Jared!
'''

import setuptools
from distutils.core import setup
import os


setup(
    name='vimbug',
    description=('A plugin for vim that creates an integrated debugging '
        'environment.'),
    long_description=__doc__,
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
