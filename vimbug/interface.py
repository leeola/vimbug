'''
'''

import logging
from vim_tools.windows import Window, create_window


logger = logging.getLogger('vimbug')


class Interface(object):
    pass

class VimGui(Interface):
    '''A gui interface for vim.'''

    def __init__(self, session_information):
        self.session_information = session_information

    def close(self, load_original_state=True):
        ''''''
        pass

    def create_windows(self):
        self.windows = {}
        
        # Create the first window..
        self.windows['source'] = create_window(
            name='SOURCE',)
        # And all our splits from that.
        self.windows['stdstream'] = self.windows['source'].split(
            plane='vertical', new_window_side='right',
            name='"STDOUT_STDERR"',)
        self.windows['scope'] = self.windows['stdstream'].split(
            plane='horizontal', new_window_side='above',
            name='SCOPE',)
        self.windows['stack'] = self.windows['scope'].split(
            plane='horizontal', new_window_side='above',
            name='STACK',)
        self.windows['prompt'] = self.windows['stack'].split(
            plane='horizontal', new_window_side='above',
            name='PROMPT',)
        self.windows['prompt_out'] = self.windows['prompt'].split(
            plane='vertical', new_window_side='right',
            name='PROMPT_OUTPUT',)

    def load(self, save_original_state=True):
        '''Create the gui, load the buffers, etc.'''
        
        if save_original_state:
            pass

        logger.debug('Loading VimGui..')

        self.create_windows()
 
