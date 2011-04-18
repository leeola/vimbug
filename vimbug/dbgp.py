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
import socket, select
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

    def __init__(self, address='localhost', port=9000):
        '''
        :param address:
            The address of the DBGp Server. Defaults to "localhost"
        :param port:
            The port that the DBGp server is set to. Defaults to 9000 (the
            protocol default too)
        '''
        #: The socket object for IO data with the DBGp server. None if 
        #: no connection has been made.
        self._client_sock = None
        #: The socket used to listen for the initial server connection.
        self._listening_server = None
        #: The server address
        self.ADDRESS = address
        #: The port the server is listening on.
        self.PORT = port

    def __enter__(self):
        '''Setup code for this connection object.'''
        # I don't think anything needs to be done here. Calling
        # self._client_sock.__enter__() may be a possibility though.
        pass

    def __exit__(self):
        '''Call close on this connection.'''
        self.close()

    def connected(self):
        '''Check if this object is connected to the DBGp Server.

        :returns:
            True if a socket connection has been established, False otherwise.
        '''
        # Eventually i'll need to set this to actually check the connection.
        # so if the DBGp server drops, this will reflect a broken connection.
        return self._client_sock is not None

    def accept(self):
        '''Accept a connection, if one has been made.

        :raises DBGPServerNotFoundError:
            No connection has been made from the DBGp Server.
        '''

        inputs, outputs, exceptions = select.select(
            [self._listening_server], [], [], 1)

        if self._listening_server in inputs:
            (self._client_sock,
             self._client_address) = self._listening_server.accept()

            logger.debug('Socket connection established! The other end of '
                         'the connection is at "%s:%i".' % self._client_address)
        else:
            logger.debug('Socket connection failed!')
            self._listening_server.shutdown(socket.SHUT_RDWR)
            self._listening_server.close()
            raise DBGPServerNotFoundError(
                'No connection was established coming from '
                '"%(address)s:%(port)i".' % {
                    'address':self.ADDRESS,
                    'port':self.PORT,
                })
        
        logger.debug('Closing socket listener.')
        # Look, we're shutting down before we close! We're being good!
        self._listening_server.shutdown(socket.SHUT_RDWR)
        self._listening_server.close()


    def listen(self):
        '''Start listening for the DBGp server.
        '''
        logger.debug(
            'SocketConnection listening on "%(address)s:%(port)i."' % {
                'address':self.ADDRESS,
                'port':self.PORT,
            })

        # Create our socket stream to listen on.
        self._listening_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the address.
        self._listening_server.bind(('', self.PORT))
        self._listening_server.listen(5)

