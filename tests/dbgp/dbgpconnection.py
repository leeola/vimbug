# coding: utf-8
'''
    tests.dbgp.dbgpconnection
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
from os.path import abspath, dirname, join

from attest import Tests, raises

from vimbug.dbgp import DBGPConnection, PyDBGPStarter


OPTIONS = {
    # A simple file to run the debug server against.
    'debug_file':abspath(join(
        dirname(__file__), '..', 'context', 'no_imports.py')),
    # The port the debug server will be connecting on.
    'pydbgp_port':8990,
}

# Our test object
dbgpcon_test = Tests()


# ====
# Note
# ====
# We are using globals to store our states since Attest, via the current
# version 0.5, has no way to share contexts between tests. Currently each
# test is given a copy of the original context. Not so great for our socket
# connection.

# The dbgp connection we will mostly be working with.
dbgpcon = None

@dbgpcon_test.test
def connect_pydbgp():
    '''Accept a pydbgp connection.'''
    global dbgpcon

    # Create the connection object.
    dbgpcon = DBGPConnection(
        OPTIONS['debug_file'],
        port=OPTIONS['pydbgp_port'],
        starter=PyDBGPStarter(
            port=OPTIONS['pydbgp_port'],
        ),
    )

    # Connect!
    dbgpcon.connect()

    assert dbgpcon.connected() == True

@dbgpcon_test.test
def basic_send_receive():
    '''Send a status command, make sure we get a response.'''
    global dbgpcon

    dbgpcon.send('status')

    assert dbgpcon.receive() is not None 

@dbgpcon_test.test
def disconnect_pydbgp():
    '''Disconnect the connection.'''
    global dbgpcon

    dbgpcon.disconnect()

    assert dbgpcon.connected() == False

