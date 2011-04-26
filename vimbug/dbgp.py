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
        if socket_ is None:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #: True if a connection has been made. False otherwise.
        self._connected = False
        #: An instance of a `socket.socket()` like object.
        self._socket = socket_

    def _receive(self, length):
        '''Receive a set number of characters from the socket.

        :param length:
            The length of the data to read.

        :raises EOFError:
            Raised if the socket receives no more data.
        '''
        # We will store our data by appending each recv result to this.
        data = ''

        while length > 0:
            # While we still want to read data.

            # Get the sockets recv.
            buffer = self._socket.recv(length)

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

        :raises EOFError:
            Raised if the sock receives no more data.
        :raises Exception:
            Raised if an unexpected result was returned from the server.
        '''

        # The characters found thus far.
        chars = ''

        while True:
            # Now, get a char from the socket.
            c = self._socket.recv(1)

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
                    'client socket.' % c)
        
        # Not much else to do at this point. Return our length! If length
        # doesn't exist here, we have a bug, so let's not worry about it.
        return length

    def close(self):
        '''Close the socket connection.'''
        self._socket.close()
        self._connected = False

    def connect(self, hostname='localhost', port=9000):
        '''Connect to a socket at the given address.

        :param hostname:
            The hostname to connect to.
        :param port:
            The port to connect to the host on.
        '''
        try:
            self._socket.connect((hostname, port))
        except socket.error, error:
            # We're just letting any errors bubble up from this. No reason
            # currently to try and catch them all.
            raise error
        else:
            self._connected = True

    def connected(self):
        '''Check whether or not this socket is connected. Note that this is
        mostly just checking if the connection has ever been connected. The
        connection on the other end may have died, and you won't know until
        a read fails.

        :returns:
            True if connected. False otherwise.
        '''
        return self._connected

    def receive(self):
        '''Read from the socket connection.'''
        return self._receive(self._receive_length())

    def send(self, data):
        '''Send data to the server.

        :param data:
            The data to send.
        '''
        data = '%s\0%s' % (len(data), data)
        self._socket.send(data)

class SocketConnectionFailedError(Exception):
    '''Raised if a socket was unable to connect.'''
    pass

class SocketListener(object):
    '''A simple socket wrapper designed to make listening and accepting
    connections cleaner **in this context**.
    '''

    
    def __init__(self):
        ''''''
        #: The listening socket.
        self._listening_socket = None
        #: The data socket
        self.socket = None

    def __enter__(self):
        '''Setup code for this connection object.'''
        # I don't think anything needs to be done here. Calling
        # self._listening_socket.__enter__() may be a possibility though.
        pass

    def __exit__(self):
        '''Call close on this connection.'''
        self.close()

    def accept(self):
        '''Accept a connection, if one has been made.

        :returns:
            A socket connection that was made. None, if no socket connections
            were established.
        '''

        inputs, outputs, exceptions = select.select(
            [self._listening_socket], [], [], 1)

        if self._listening_socket in inputs:
            (client_socket,
             client_address) = self._listening_socket.accept()
   
            self.socket = Socket(client_socket)
            # Here we need to make sure and tell the wrapper that it is connected.
            self.socket._connected = True

            (self._client_hostname, self._client_port) = client_address

            logger.debug('SocketListener connection established! The other '
                         'end of the connection is '
                         'at "%s:%i".' % client_address)
        else:
            logger.debug('SocketListener had no connections made.')

        # Now we need to close *only* the listener. Since this could have been
        # a successful connection.
        self._listening_socket.close()

    def close(self):
        '''Close the socket connection.'''

        logger.debug('Closing socket listener.')

        if self._listening_socket is not None:
            self._listening_socket.close()

        if self.socket is not None:
            self.socket.close()
    
    def connected(self):
        '''Check whether or not this socket is connected.

        :returns:
            True if connected. False otherwise.
        '''
        if self.socket is not None:
            return self.socket.connected()
        else:
            return False

    def listen(self, hostname='localhost', port=9000):
        '''Start listening for a connection.
        '''
        logger.debug(
            'SocketListener listening on "%(hostname)s:%(port)i."' % {
                'hostname':hostname,
                'port':port,
            })

        # Create our socket stream to listen on.
        self._listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the address.
        self._listening_socket.bind((hostname, port))
        self._listening_socket.listen(1)

class SocketNotEstablishedError(Exception):
    '''Raised if a socket was used before it was connected/established.'''
    pass

