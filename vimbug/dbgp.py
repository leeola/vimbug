# -*- coding: utf-8 -*-
'''
    vimbug.dbgp
    ~~~~~~~~~~~

    A collection of classes to handle protocol communications with a
    DBGp server.

    :copyright: (c) 2011 by Lee Olayvar.
    :license: MIT, see LICENSE for more details.
'''

import base64
import socket

from lxml import etree


class DBGP:
    '''A friendly frontend which allows for cleaner access to a DBGp Server.

    Communication itself is handled by :class:`DBGPConnection`.
    '''
    pass

class DBGPConnection:
    '''A class which manages communication to the DBGp server by translating
    DBGp commands given to it and with the aid of :class:`SocketConnection`
    recieve or send commands/data with the DBGp Server.
    '''
    pass

class SocketConnection:
    '''A simple class focused simply on sending and recieving sockets, with
    some basic xml management done aswell.
    '''
    pass

