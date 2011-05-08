# coding: utf-8
'''
    tests.dbgp.dbgp
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
from os.path import abspath, dirname, join

from attest import Tests, raises

from vimbug.dbgp import DBGP, PyDBGPStarter


OPTIONS = {
    # The directory for all of our debugging test files.
    'context_dir':abspath(join(dirname(__file__), '..', 'context')),
    # The port the debug server will be connecting on.
    'pydbgp_port':8990,
}

# Our test object
dbgp_test = Tests()


# ====
# Note
# ====
# We are using globals to store our states since Attest, via the current
# version 0.5, has no way to share contexts between tests. Currently each
# test is given a copy of the original context. Not so great for our socket
# connection.

# The dbgp object we will mostly be working with.
dbgp = DBGP(
    port=OPTIONS['pydbgp_port'],
    relative_uri=OPTIONS['context_dir'],
    starter=PyDBGPStarter(
        port=OPTIONS['pydbgp_port'],
    ),
)

@dbgp_test.test
def hello_world_copy():
    '''Run our hello world file.'''
    global dbgp

    dbgp.set_debug('hello_world.py', relative=True)
    dbgp.connect_debug()
    dbgp.stdout(output='copy')
    dbgp.run()
    
    data = dbgp.read(
        continuous=True, return_copy=True, call_subscribers=False)

    assert data[1]['type'] == 'stdout'
    assert data[1]['encoding'] == 'base64'
    assert data[1]['value'] == 'SGVsbG8gV29ybGQ='

    # Don't forget to end our debug session.
    dbgp.disconnect_debug(stop=True)

@dbgp_test.test
def hello_world_subscribers():
    '''Run our hello world file.'''
    global dbgp

    dbgp.set_debug('hello_world.py', relative=True)
    dbgp.connect_debug()
    dbgp.stdout(output='copy')
    dbgp.run()

    subscribed_data = []
    def subscribed_to_stream(type, encoding, data):
        subscribed_data.append((type, encoding, data))

    dbgp.subscribe_stream(subscribed_to_stream)
    
    return_data = dbgp.read(
        continuous=True, return_copy=False, call_subscribers=True)

    assert return_data is None

    assert data[0]['type'] == 'stdout'
    assert data[0]['encoding'] == 'base64'
    assert data[0]['value'] == 'SGVsbG8gV29ybGQ='

    # Don't forget to end our debug session.
    dbgp.disconnect_debug(stop=True)

