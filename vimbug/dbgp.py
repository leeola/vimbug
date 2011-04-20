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

class Socket(object):
    '''A simple socket wrapper designed to make dealing with sockets cleaner,
    **in this context**.
    '''
    

    def __init__(self, socket_=None):
        '''
        :param socket_:
            An instance of a `socket.socket()` like object.
        '''
        #: An instance of a `socket.socket()` like object.
        self._socket = socket_

    def connect(self, host='localhost', port=9000):
        '''Connect to a socket at the given address.

        :param host:
            The host to connect to.
        :param port:
            The port to connect to the host on.

        :raises SocketConnectionFailedError:
            Raised if the socket connection fails for some reason. Go figure..
            Yea.. not so descriptive.. i'm sorry :/
        '''
        raise NotImplementedError()

    def connected(self):
        '''Check whether or not this socket is connected.

        :returns:
            True if connected. False otherwise.
        '''
        # Eventually we need to somehow check if the socket is actually
        # connected or not.
        return self._socket is not None

class SocketListener(object):
    '''A simple socket wrapper designed to make listening and accepting
    connections cleaner **in this context**.
    '''
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

    def _receive(self, length):
        '''Receive a set number of characters from the client sock.

        :param length:
            The length of the data to read.
        '''
        # We will store our data by appending each recv result to this.
        data = ''

        while length > 0:
            # While we still want to read data.

            # Get the sockets recv.
            buffer = self._client_sock.recv(length)

            if buffer == '':
                # If we receive nothing, the connection has closed on the
                # other end.

                self.close()
                raise EOFError('The client has closed the connection.')

            # Append whatever we received to the total data.
            data += buffer
            # Ensure we read as much as we intended to read by subtracting
            # what we *actually* read from the original intention.
            length -= len(buffer)
        return data

    def _receive_length(self):
        '''Read the length of the socket buffer by getting a sequence of
        integers found at the beginning of the buffer.

        :raises NotImplementedError:
            Raised if `self._client_sock` is None.
        :raises EOFError:
            Raised if the client sock receives no more data.
        :raises Exception:
            Raised if an unexpected result was returned from the server.
        '''

        # The characters found thus far.
        chars = ''

        while True:
            if self._client_sock is None:
                # If the client sock is None.. well, we should raise some
                # type of error here.. probably custom.. to signal that the
                # socket has not been put up yet. For now we'll raise not 
                # implemented.
                raise NotImplementedError(
                    'Read length was attempted before the client socket was '
                    'established. A proper error has not been implemented..')
            
            # Now, get a char from the socket.
            c = self._client_sock.recv(1)

            if c == '':
                # If c is empty, the connection has been closed. So we need
                # to shut down, and signal the end of the connection.
                self.close()
                raise EOFError('The server has closed the connection.')
            elif c == '\0':
                # If \0 is returned we have reached the end of the length
                # characters. So return what we have gathered thus far in.
                length = int(chars)
                # Don't forget to break the loop!
                break
            elif c.isdigit():
                # If c is a digit, we want to append it to chars and repeat
                # this wheel of fun.
                chars += c
                # Restart the loop
                continue
            else:
                # If we reach here, C is not empty, not \0, and not a digit.
                # What is it!? Well, lets fail it since something obviously
                # isn't right.
                raise Exception(
                    'An unexpected result of "%s" was received from the '
                    'client socket.')
        
        # Not much else to do at this point. Return our length! If length
        # doesn't exist here, we have a bug, so let's not worry about it.
        return length

    def close(self):
        '''Check both of the sockets and close them if active.'''
        
        if self._client_sock is not None:
            self._client_sock.close()

        if self._listening_server is not None:
            self._listening_server.close()

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
            self._listening_server.close()
            raise DBGPServerNotFoundError(
                'No connection was established coming from '
                '"%(address)s:%(port)i".' % {
                    'address':self.ADDRESS,
                    'port':self.PORT,
                })
        
        logger.debug('Closing socket listener.')
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

    def read(self):
        '''Read from the socket connection.'''
        return self._receive(self._receive_length())

