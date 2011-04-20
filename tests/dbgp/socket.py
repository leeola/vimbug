# coding: utf-8
'''
    tests.dbgp.socket
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
from attest import Tests, raises

from vimbug.dbgp import Socket, SocketListener


OPTIONS = {
    'main_port':8990,
    # A port that nothing should be listening on. This will be
    # used for failed connection testing.
    'empty_port':8991,
}

socket = Tests()

@socket.test
def failing_connection():
    '''There is no remote server to connect to.'''
    sock = Socket()

    with raises(SocketConnectionFailedError) as error:
        sock.connect(port=OPTIONS['empty_port'])

    assert sock.connected() == False

@socket.context
def create_sockets():
    '''Create the socket context.'''
    client = Socket()
    listener = SocketListener()

    try:
        yield (client, listener)
    finally:
        client.close()
        listener.close()

@socket.test
def successful_connection(client, listener):
    '''Successfully connect to the listener.'''
    listener.listen(port=OPTIONS['main_port'])
    client.connect(port=OPTIONS['main_port'])
    listener.accept()

    # Now check both sockets to make sure they're connected.
    assert client.connected() == True
    assert listener.socket.connected() == True

@socket.test
def echo_data(client, listener):
    '''Send data from the client, and receive it from the listener sock.'''

    # Just a group of data to send.
    datas = [
        'Hello World',
    ]

    for data in datas:
        client.send(data)
        assert listener.socket.receive() == data

@socket.test
def close_connection(client, listener):
    '''Close the connection, and make sure it's closed.'''

    client.close()
    assert client.connected() == False
    assert listener.socket.connected() == False

