'''
'''
import logging
from random import randint

import vim


logger = logging.getLogger('vimbug')


class Window(object):
    '''An instance of a Vim window.'''


    def __init__(self, wid=None, name=None):
        '''
        :param wid:
            If None, the current window id is used or one is generated for the
            current window if needed. If not None, a search is preformed
            looking for the supplied wid, and if found an instance is created
            for that window. If one is not found, the supplied wid is created
            for the current window.
        :param name:
            The name for the current window.

        :raises WIDConflict:
            No matching wid was found for the supplied wid, and the current
            window already has a wid. Due to this the instance cannot be
            created and is failing.
        '''

        # Get the current winnr
        current_winnr = int(vim.eval('winnr()'))

        # If the given wid is None, generate one.
        if wid is None:
            # Generate the wid
            wid = self._find_unique_id()

            # Assign it to the current window.
            self._assign_win_id(wid)
        else:
            # Find the winnr for the wid given, if any.
            matching_wid_winnr = self._get_winnr_from_id(wid)
            
            if matching_wid_winnr is None:
                # If there are no matching winnr wids, assign it to the current
                # window.
                # Note that if there is a matching id, we don't need to
                # create/assign anything.
                self._assign_win_id(wid)

        #: The window id for the current window instance.
        self.wid = wid       

    def _assign_win_id(self, wid=None, winnr=None):
        '''Assign a window id for a window.

        :param wid:
            The window id to use. If None, a unique id is generated.
        :param winnr:
            If None, the current window.
        '''
        
        if wid is None:
            # Create a window id if needed.
            wid = self._find_unique_id()

        if winnr is None:
            # Get the window number if it is None.
            winnr = int(vim.eval('winnr()'))
            current_winnr = winnr
        else:
            current_winnr = int(vim.eval('winnr()'))

        winnr_wid = vim.eval('getwinvar(%s, "id")' % winnr)
        if winnr_wid is not None and not overwrite:
            # If the target winnr is not None, then we need to fail so we don't
            # overwrite the id. Unless it's specified, of course.
            raise WIDConflict('The winnr:%s already has an id when a write '
                              'was attempted.' % winnr)

        if winnr == current_winnr:
            # The two winnrs are the same. No need to select one, assign, and
            # switch back.
            vim.command('let w:id="%s"' % wid)
        else:
            # The two winnrs are different.

            # Select the window and then write the var.
            vim.command('exec "normal! \\<C-W>".%s.\'w\'' % winnr)
            vim.command('let w:id="%s"' % wid)
            # Restore the previous window.
            vim.command('exec "normal! \\<C-W>".%s.\'w\'' % current_winnr)

    def _command(self, command, winnr=None, preserve_focus=False):
        '''Execute a command from the specified window.

        :param winnr:
            The winnr of the window to execute the command under.
        :param preserve_focus:
            If True, the window focus will be restored after this command is
            executed.
        '''
        if winnr is None:
            vim.command(command)
            return

        original_winnr = int(vim.eval('winnr()'))
        matching_winnr = original_winnr == winnr
        
        if not matching_winnr:
            # If we need to change focus.. change focus.
            self._set_focus(winnr)

        # Now execute the command.
        vim.command(command)

        if preserve_focus and not matching_winnr:
            # If we need to restore the focus.. do it.
            self._set_focus(winnr)

    def _eval(self, eval_, winnr=None, preserve_focus=False):
        '''Return the eval of a given string.

        :param winnr:
            The window number of the target window.
        :param preserve_focus:
            If True, the window focus will be restored after this command is
            executed.

        :returns:
            The vim eval of the supplied string.
        '''
        if winnr is None:
            return vim.eval(eval_)

        original_winnr = int(vim.eval('winnr()'))
        matching_winnr = original_winnr == winnr
        
        if not matching_winnr:
            # If we need to change focus.. change focus.
            self._set_focus(winnr)

        # Now execute the eval.
        eval_output = vim.eval(eval_)

        if preserve_focus and not matching_winnr:
            # If we need to restore the focus.. do it.
            self._set_focus(winnr)

        return eval_output

    def _find_unique_id(self):
        '''Check every single window var to find a winvar that does not
        exist. This is done by taking the "largest" winvar, and incremented
        by one.
        '''
        total_windows = int(vim.eval('winnr("$")'))

        largest_winid = 0
        # Remember, winnr's start at 1, not 0.
        for _winnr in range(1, total_windows+1):
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

    def _get_winnr(self):
        '''Get the win number of the current window.
        
        :returns:
            The winnr of the current window. None is returned
            if no window has this win id.
        '''
        return self._get_winnr_from_id(self.wid)

    def _get_winnr_from_id(self, wid):
        '''Get the winnr from the given wid.

        :param wid:
            A window id.

        :returns:
            The first winnr that has the wid specified. None is returned
            if none are found to match.
        '''

        total_windows = int(vim.eval('winnr("$")'))
        # Remember, winnr's start at 1 not 0
        for winnr in range(1, total_windows+1):
            winvar_result = vim.eval('getwinvar(%s, "id")' % winnr)
            if winvar_result == str(wid):
                return winnr
        # No matches found. Return None
        return None

    def _set_focus(self, winnr):
        '''Set focus on a window.

        :param winnr:
            The window to set focus to.
        '''
        # Make sure not to use any additional arguments to self._command
        # from self._set_focus... the world may asplode.
        self._command('exec "normal! \\<C-W>".%s.\'w\'' % winnr)

    def has_focus(self):
        '''Does this window have focus?

        :returns:
            True if it does, False otherwise.
        '''
        focused_winnr = int(vim.eval('winnr()'))
        return focused_winnr == self._get_winnr()
    
    def split(self, plane, new_window_side, wid=None, name=None):
        '''Split a window on the plane specified, either horizontal or
        vertical. The new window will go on the side specified,
        either above/below/left/right.

        :param plane:
            The plane to split this window on. Either `horizontal`
            or `vertical`
        :param new_window_side:
            The side the new window will be placed. Depending on the
            splitting plane, either above/below/left/right.
        :param wid:
            The wid of the window.
        :param name:
            The name of the window.

        :returns:
            This will return a new :class:`Window` instance.
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
            name_ = ''
        else:
            name_ = name

        # Create the vim window
        vim.command('%s %s new %s' % (
            vim_plane_options[plane], vim_side_options[new_window_side],
            name_))

        # Now grab the current window, which should be the new window, and
        # create it. .. And return it.
        return Window(wid=wid, name=name)

    
