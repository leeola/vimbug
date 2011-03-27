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
            'stdstream':Buffer(name='STDOUT_STDERR'),
            'scope':Buffer(name='SCOPE'),
            'stack':Buffer(name='STACK'),
            'prompt':Buffer(name='PROMPT'),
            'prompt_out':Buffer(name='PROMPT_OUT'),
        }

        # Set the types.
        for key, buffer in self.buffers.items():
            if key != 'source':
                buffer.set_type('nofile')

    def _create_windows(self):
        '''Create the windows for the vim gui.'''

        self.windows = {}
        # Create an instance of our current window..
        self.windows['source'] = Window(id='source')
        # And all our splits from that.
        self.windows['stdstream'] = self.windows['source'].split(
            plane='vertical', new_window_side='right',
            id='stdout_stderr')
        self.windows['scope'] = self.windows['stdstream'].split(
            plane='horizontal', new_window_side='above',
            id='scope')
        self.windows['stack'] = self.windows['scope'].split(
            plane='horizontal', new_window_side='above',
            id='stack')
        self.windows['prompt'] = self.windows['stack'].split(
            plane='horizontal', new_window_side='above',
            id='prompt')
        self.windows['prompt_out'] = self.windows['prompt'].split(
            plane='vertical', new_window_side='right',
            id='prompt_output')

        # Add the buffers
        for key, window in self.windows.items():
            window.set_buffer(self.buffers[key])

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
 
