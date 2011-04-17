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
import logging

from lxml import etree


logger = logging.getLogger('vimbug.dbgp')


class DBGP:
    '''A friendly frontend which allows for cleaner access to a DBGp Server.

    Communication itself is handled by :class:`DBGPConnection`.
    '''
    pass

class DBGPConnection:
    '''A class which manages communication to the DBGp server by translating
    DBGp commands given to it and with the aid of :class:`SocketConnection`,
    recieve or send commands/data with the DBGp Server.
    '''
    pass

class DBGPServerNotFoundError(Exception):
    '''The DBGp Server did not connect to a listening client.'''
    pass

class SocketConnection(object):
    '''A simple socket class designed to handle the socket mojo with the DBGp
    in mind.
    '''

    def __init__(self, address='localhost', port=9000, listen_timeout=5):
        '''
        :param address:
            The address of the DBGp Server. Defaults to "localhost"
        :param port:
            The port that the DBGp server is set to. Defaults to 9000 (the
            protocol default too)
        :param listen_timeout:
            How long the IDE *(this class)* will listen for the DBGp server
            to connect.
        '''
        #: The socket object for IO data with the DBGp server. None if 
        #: no connection has been made.
        self._sock = None
        #: The server address
        self.ADDRESS = address
        #: The port the server is listening on.
        self.PORT = port
        #: How long to listen for DBGp to connect to this client.
        self.LISTEN_TIMEOUT = listen_timeout

    def __enter__(self):
        '''Setup code for this connection object.'''
        # I don't think anything needs to be done here. Calling
        # self._sock.__enter__() may be a possibility though.
        pass

    def __exit__(self):
        '''Call close on this connection.'''
        self.close()

    def connect(self):
        '''Start listening for the DBGp server.

        :raises DBGPServerNotFound:
            Raised if a socket.timeout is thrown from the socket.
        '''
        logger.debug(
            'SocketConnection connecting to "%(address)s:%(port)i."' % {
                'address':self.ADDRESS,
                'port':self.PORT,
            })

        # Set the timeout.
        socket.setdefaulttimeout(5)
        
        # Create our socket stream to listen on.
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The sock will block for 5 seconds.
        serv.settimeout(5)
        # Set the socket options.. yea i forget what these are about.
        serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the address.
        serv.bind(('', self.PORT))
        serv.listen(5)

        try:
            # Now start listening for a connection!
            (self._sock, remote_address) = serv.accept()
        except socket.timeout:
            logger.debug('Socket connection failed!')
            raise DBGPServerNotFoundError(
                'No connection was established coming from '
                '"%(address)s:%(port)i".' % {
                    'address':self.ADDRESS,
                    'port':self.PORT,
                })
        else:
            logger.debug('Socket connection established! The other end of '
                         'the connection is at "%s:%i".' % remote_address)
        finally:
            serv.close()

    def connected(self):
        '''Check if this object is connected to the DBGp Server.

        :returns:
            True if a socket connection has been established, False otherwise.
        '''
        # Eventually i'll need to set this to actually check the connection.
        # so if the DBGp server drops, this will reflect a broken connection.
        return self._sock is not None

