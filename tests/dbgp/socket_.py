# coding: utf-8
'''
    tests.dbgp.socket
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
import socket

from attest import Tests, raises

from vimbug.dbgp import Socket, SocketListener
from vimbug.dbgp import (SocketConnectionFailedError,
                         SocketNotEstablishedError)


OPTIONS = {
    'main_port':8990,
    # A port that nothing should be listening on. This will be
    # used for failed connection testing.
    'empty_port':8991,
}

socktest = Tests()

@socktest.context
def create_sockets():
    '''Create the socket context.'''
    client = Socket()
    listener = SocketListener()

    listener.listen(port=OPTIONS['main_port'])
    client.connect(port=OPTIONS['main_port'])
    listener.accept()
    
    try:
        yield (client, listener)
    finally:
        client.close()
        listener.close()

@socktest.test
def failing_connection():
    '''There is no remote server to connect to.'''
    sock = Socket()

    with raises(socket.error) as error:
        sock.connect(port=OPTIONS['empty_port'])

    assert sock.connected() == False

@socktest.test
def successful_connection(client, listener):
    '''Successfully connect to the listener.'''
    assert client.connected() == True
    assert listener.connected() == True

@socktest.test
def echo_data(client, listener):
    '''Send data from the client, and receive it from the listener sock.'''

    # Just a group of data to send.
    datas = [
        'Hello World',
    ]

    for data in datas:
        client.send(data)
        assert listener.socket.receive() == data

@socktest.test
def close_connection(client, listener):
    '''Close the connection, and make sure it's closed.'''

    client.close()
    listener.close()
    assert client.connected() == False
    assert listener.connected() == False

