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

# The dbgp connection we will mostly be working with.
dbgpcon = None

@dbgpcon_test.test
def connect_to_pydbgp():
    '''Accept a pydbgp connection.'''
    global dbgpcon

    # Create the connection object.
    dbgpcon = DBGPConnection(
        port=OPTIONS['pydbgp_port'],
        starter=PyDBGPStarter(
            port=OPTIONS['pydbgp_port'],
            url=OPTIONS['debug_file'],
        ),
    )

    # Connect!
    dbgpcon.connect()

    assert dbgpcon.connected() == True

