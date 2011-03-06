'''
'''
import logging

import vim


logger = logging.getLogger('vimbug')


def get_current_window():
    return Window(vim.current.window)

def create_window(name=None):
    '''Create a new window, and return the window object.'''

    # For now, just create a window by splitting the current window to the
    # top.
    vim.command('topleft new %s' % name)
    # Get the latest, hopefully newest, window.
    vim_window = vim.windows[len(vim.windows)-1]
    return Window(vim_window)

class Window(object):
    '''An instance of a Vim window.'''


    def __init__(self, vim_window):

        self.vim_window = vim_window
    
    def split(self, plane, new_window_side, name=None):
        '''Split a window on the plane specified, either horizontal or
        vertical. The new window will go on the side specified,
        either above/below/left/right.

        This will return a new Window object.
        '''

        # A simple translation map converting the acceptable arguments into
        # valid vim arguments. eg:
        # plane=horizontal, new_window_side=below
        # Equals..
        # "%s %s" % ('', 'rightbelow')
        vim_plane_options = {
            'horizontal':'',
            'vertical':'vertical',
        }
        vim_side_options = {
            'above':'leftabove',
            'below':'rightbelow',
            'left':'leftabove',
            'right':'rightbelow',
        }

        if name is None:
            name = ''

        # Create the vim window
        vim.command('%s %s new %s' % (
            vim_plane_options[plane], vim_side_options[new_window_side],
            name))

        # Get the highest indexing window.. hopefully this is always the
        # latest window.
        return Window(vim.windows[len(vim.windows)-1])
    
