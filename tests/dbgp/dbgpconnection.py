# coding: utf-8
'''
    tests.dbgp.dbgpconnection
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''

from attest import Tests, raises

from vimbug.dbgp import DBGPConnection, PyDBGPStarter


OPTIONS = {
    # A simple file to run the debug server against.
    'debug_file':abspath(join(
        dirname(__file__), '..', 'context', 'no_imports.py')),
    # The port the debug server will be connecting on.
    'pydbgp_port':8990,
}

dbgpcon_test = Tests()

@dbgpcon_test.context
def setup_context():
    pass

@dbgpcon_test.test
def accept_pydbgp():
    '''Accept a pydbgp connection.'''
    dbgpcon = DBGPConnection(
        port=OPTIONS['pydbgp_port'],
        starter=PyDBGPStarter(
            port=OPTIONS['pydbgp_port'],
            url=OPTIONS['debug_file'],
        ),
    )

    
