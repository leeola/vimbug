
from attest import Tests, Attest

from vim_debug.interface import commands


interface_commands = Tests()

@interface_commands.test
def stopped_debugger():
    pass

