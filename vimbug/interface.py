'''
'''

import logging
from vim_tools.gui import Buffer, Window


logger = logging.getLogger('vimbug')


class Interface(object):
    pass

class VimGui(Interface):
    '''A gui interface for vim.'''

    def __init__(self, session_information):
        self.session_information = session_information

    def _create_buffers(self):
        '''Create the buffers for the vim gui.'''

        self.buffers = {
            # Load the current buffer.
            'source':Buffer(),
            # Create the other used to display debug info.
            'stdstream':Buffer(name='STDOUT_STDERR', type='nofile'),
            'scope':Buffer(name='SCOPE', type='nofile'),
            'stack':Buffer(name='STACK', type='nofile'),
            'prompt':Buffer(name='PROMPT', type='nofile'),
            'prompt_out':Buffer(name='PROMPT_OUT', type='nofile'),
        }

    def _create_windows(self):
        '''Create the windows for the vim gui.'''

        self.windows = {}
        # Create an instance of our current window..
        self.windows['source'] = Window(wid='source',
                                        buffer=self.buffers['source'])
        # And all our splits from that.
        self.windows['stdstream'] = self.windows['source'].split(
            plane='vertical', new_window_side='right',
            wid='stdout_stderr', buffer=self.buffers['stdstream'],)
        self.windows['scope'] = self.windows['stdstream'].split(
            plane='horizontal', new_window_side='above',
            wid='scope', buffer=self.buffers['scope'],)
        self.windows['stack'] = self.windows['scope'].split(
            plane='horizontal', new_window_side='above',
            wid='stack', buffer=self.buffers['stack'],)
        self.windows['prompt'] = self.windows['stack'].split(
            plane='horizontal', new_window_side='above',
            wid='prompt', buffer=self.buffers['scope'],)
        self.windows['prompt_out'] = self.windows['prompt'].split(
            plane='vertical', new_window_side='right',
            wid='prompt_output', buffer=self.buffers['prompt_output'])

    def close(self, load_original_state=True):
        ''''''
        pass

    def load(self, save_original_state=True):
        '''Create the gui, load the buffers, etc.'''
        
        if save_original_state:
            pass

        logger.debug('Loading VimGui..')

        self._create_buffers()
        self._create_windows()
 
