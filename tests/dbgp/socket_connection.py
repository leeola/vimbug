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

from vimbug.dbgp import SocketConnection


# A set of options to run this test against.
OPTIONS = {
    # A simple file to run the debug server against.
    'debug_file':abspath(join(
        dirname(__file__), '..', '..', 'context', 'no_imports.py')),
    # The port the debug server will be listening on.
    'pydbgp_port':9000,
    # A port that nothing should be listening on. This will be
    # used for failed connection testing.
    'empty_port':9001,
}

socket_connection = Tests()


@socket_connection.test
def connecting_to_nothing():

@socket_connection.context
def create_socket():
    '''Create context needed for the socket tests.'''
    try:
        yield SocketConnection()
    finally:
        pass


