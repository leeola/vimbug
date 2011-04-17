# -*- coding: utf-8 -*-
'''
    tests.dbgp.socket_connection
    ~~~~~~~~~~~~~~~~~~~~~
    
    Tests to assure the SocketConnection class is working properly.

    :copyright: (c) 2011 by Lee Olayvar.
    :license: MIT, see LICENSE for more details.
'''
import subprocess
from os.path import abspath, dirname, join

from attest import Tests, Assert
from attest.contexts import raises

from vimbug.dbgp import SocketConnection
from vimbug.dbgp import DBGPServerNotFoundError


# A set of options to run this test against.
OPTIONS = {
    # A simple file to run the debug server against.
    'debug_file':abspath(join(
        dirname(__file__), '..', '..', 'context', 'no_imports.py')),
    # The port the debug server will be listening on.
    'pydbgp_port':9000,
    # A port that nothing should be listening on. This will be
    # used for failed connection testing.
    'empty_port':8991,
}

socket_connection = Tests()


@socket_connection.test
def connecting_to_nothing():
    '''Ensure the socket fails when connecting to an empty port.'''
    con = SocketConnection(port=OPTIONS['empty_port'])
    with raises(DBGPServerNotFoundError) as error:
        con.connect()

@socket_connection.context
def create_socket():
    '''Create context needed for the socket tests.'''
    try:
        yield SocketConnection(port=OPTIONS['pydbgp_port'])
    finally:
        pass

@socket_connection.test
def connect_to_pydbg(con):
    '''Initiate the pydbgp process and start listening for it.'''
    # Launch the pydbgp process
    print OPTIONS['debug_file']
    pydbgp_proc = subprocess.Popen(
        ('pydbgp.py', '-d', 'localhost:%i' % OPTIONS['pydbgp_port'],
        OPTIONS['debug_file']),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,)
    # Set SocketConnection to listening.
    con.connect()
    # Ensure that the connection is established.
    Assert(con.connected) == True

