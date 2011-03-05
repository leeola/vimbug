'''
'''

import logging


logger = logging.getLogger('vimbug')


class Interface(object):
    pass

class VimGui(Interface):
    '''A gui interface for vim.'''

    def __init__(self, session_information):
        self.session_information = session_information

    def load(self):
        '''Load the gui.'''
        pass
 
