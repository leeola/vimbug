'''
'''
import logging
from random import randint

import vim


logger = logging.getLogger('vimbug')


def get_current_window():
    return Window(vim.current.window)

class WindowLayout(object):
    '''A layout manager for Vim..'''

    def __init__(self, from_window_id=None, *args, **kwargs):
        super(WindowLayout, self).__init__(*args, **kwargs)

        if from_window_id is None:
            # Try and get the winid of the current window. Create one if needed.
            window_id = self._get_win_id()
            if window_id is None:
                self._assign_win_id()
                window_id = self._get_win_id()

        # With the winid, create a window instance.
        self.add_window(Window(id=window_id))

    def _assign_win_id(self, window_number=None, window_id=None)
        '''Assign a window id for a window.

        :param window_number:
            If None, the current window.
        :param window_id:
            The window id to use. If None, a unique id is generated.
        '''
        
        # Create a window id if needed.
        if window_id is None:
            window_id = self._find_unique_id()

        # Get the window number if it is None.
        if window_number is None:
            window_number = int(vim.eval('winnr()'))

        # Get the current window number so we can restore it.
        current_winnr = int(vim.eval('winnr()'))

        # Select the window and then write the var.
        vim.command('exec "normal! \\<C-W>".%s.\'w\'' % window_number)
        vim.command('let w:id="%s"' % window_id)
        
        # Restore the previous window.
        vim.command('exec "normal! \\<C-W>".%s.\'w\'' % current_winnr)

    def _find_unique_id(self):
        '''Check every single window var to find a winvar that does not
        exist. For reference, the "largest" winvar is chosen, and incremented
        by one.
        '''
        total_windows = int(vim.eval('winnr("$")'))

        largest_winid = 0
        for _winnr in total_windows:
            winvar_result = vim.eval('getwinvar(%s, "id")' % _winnr)
            if winvar_result is not None:
                try:
                    winvar_result = int(winvar_result)
                except ValueError:
                    # If there is a value error, this winvar is not
                    # an integer. So in that case, just continue since we're
                    # only interested in generating integer ids.
                    continue

                if winvar_result > largest_winid:
                    largest_winid = winvar_result
        
        # Now we should have the largest_winid assigned, if any.
        # So increase it by one, and everyone's happy!
        return largest_winid + 1

    def _get_win_id(self, window_number=None):
        '''Get the id of the current window. An exception is raised of the
        window does not have an id.

        :param window_number:
            The number of the window you want to check. If None, the current
            window is used.

        :returns:
            The window id for the given window number. If no id exists None
            is returned.
        '''
        if window_number is None:
            window_number = int(vim.eval('winnr()'))
        return vim.eval('getwinvar(%s, "id")' % window_number)

    def _win_id_exists(self, window_id):
        '''Check if a window id exists. Note that this is an expensive
        operation as it searches through *all* of the windows on
        the current tab to find the given window_id.
        '''
        total_windows = int(vim.eval('winnr("$")'))
        for winnr in total_windows:
            winvar_result = vim.eval('getwinvar(%s, "id")' % winnr)
            if winvar_result == window_id:
                return True
        return False

    def create_window(window_id, name=None):
        '''Create a new window, and return the window object.'''

        # Just putting a hold on this function for now.
        raise NotImplemented()

        # Check if that id already exists. If it does, fail it.
        if self._win_id_exists(window_id):
            raise NotImplemented()

        # For now, just create a window by splitting the current window to the
        # top.
        vim.command('topleft new %s' % name)
        # Get the latest, hopefully newest, window.
        vim_window = vim.windows[len(vim.windows)-1]
        return Window(vim_window)

class SplitLayout(WindowLayout):
    '''A layout manager based around splitting windows.'''

    def __init__(self, *args, **kwargs):
        super(SplitLayout, self).__init__(*args, **kwargs)

        # Since we are basing this layout off of splits, we want to get
        # all the windows and create an internal list for every window
        # index. We will only lazily create these windows though.

        # Grab the total windows, and create a list.
        self._window_list = [None] * len(vim.windows)

        # Create a window object for the current window.
        current_winnr = vim.eval('winnr()')
        self._window_list[current_winnr-1] = Window(self) 

class Window(object):
    '''An instance of a Vim window.'''


    def __init__(self, layout):

        # The layout manager for this window.
        self._layout = layout

    def _command(self, silent=False):
        '''Execute a command from the current window.'''
        pass

    def _get_winnr(self):
        '''Get the win number of the current window.'''
        pass
    
    def split(self, plane, new_window_side, name=None):
        '''Split a window on the plane specified, either horizontal or
        vertical. The new window will go on the side specified,
        either above/below/left/right.

        This will return a new Window object.
        '''

        # A simple translation map converting the acceptable arguments into
        # valid vim arguments. eg..:
        # Input: plane=horizontal, new_window_side=below
        # Output: "rightbelow new name"
        # Input: plane=vertical, new_window_side=left
        # Output: "vertical leftabove new name"
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
    
