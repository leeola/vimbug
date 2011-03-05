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
    global vimbug_session

    if vimbug_session is None:
        processed_args = command_line.process_args(args, session_started=False)

        # Create a session info instance to pass to the vimbug instance.
        session_information = SessionInformation(
            processed_args['server'],
            processed_args['port'],
            processed_args['location'],
        )

        # Create our vimbug instance.
        vimbug_session = VimBug(session_information)
        vimbug_session.load_interface()
    else:
        processed_args = command_line.process_args(args, session_started=True)
        
        command = processed_args['command']
        
        # This will allow us to have a command that maps to another command.
        translations = {
        }
        if translations.has_key(command):
            command = translations[command]

        getattr(vimbug_session, command)()

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



