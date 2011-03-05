'''
'''
import logging

import command_line
from debugger import Debugger
from interface import VimGui as Interface


logger = logging.getLogger('vimbug')
# An instance of VimBug if a session exists.
vimbug_session = None


def main(args):
    '''The main vim-bug command. Called by the user typing "Vb [options]"
    '''
    if vimbug_session is None:
        session_settings = command_line.process_args(args, session_started=False)
    else:
        # Technically we have no idea what vimbug_session is right now
        # But i'm leaving this loose for possibly flexibility.
        session_settings = command_line.process_args(args, session_started=True)

    # Create a session info instance to pass to the vimbug instance.
    session_information = SessionInformation(
        session_settings['server'],
        session_settings['port'],
        session_settings['location'],
    )

    # Create our vimbug instance, and load the interface.
    VimBug(session_information).load_interface()

class VimBug(object):
    '''The main class for VimBug.'''

    def __init__(self, session_information):
        self.interface = Interface(session_information)
        self.debugger = Debugger(session_information)
        self.session_information = session_information

    def exit(self):
        '''Fully quit the debugger and close the interface.'''
        raise NotImplemented()

    def load_interface(self):
        '''Load the interface'''
        
        self.interface.load()



