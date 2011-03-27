'''
'''
import logging
from random import randint

import commands


logger = logging.getLogger('vimbug')


class Buffer(object):
    '''An instance of a vim buffer.'''


    def __init__(self, name=None):
        '''
        :param name:
            A string expression to find/create a buffer from. Some usage
            examples are as follows..::

                __init__('#')       # The alternate buffer
                __init__(3)         # The buffer number 3. Note that this is
                                    # an integer. '3' does not equate to 3.
                __init__('%')       # The current buffer. 
                __init__('file2')   # A buffer where "file2" matches.
                __init__(None)      # The current buffer. Same as '%'
                __init__('new_name')# A new, none existant name. This will
                                    # *create* a buffer.
        '''

        if name is None:
            # No buffer name was specified. Set the buffer name to the
            # current windows buffer.
            name = commands.get_buffer_name(commands.eval('winbufnr(0)'))
        elif not commands.buffer_exists(name):
            # The buffer does not exist. Create it.
            commands.create_buffer(name)

        # Since the only constant with buffers is the number, get that and
        # store it.
        #: The buff number as shown by `:ls`
        self._buffer_number = commands.get_buffer_number(name)

    def get_number(self):
        '''Return the number of this buffer.

        Hint: It's just returning self._buffer_number
        '''
        return self._buffer_number
  
    def set_type(self, type):
        '''Set the type for this buffer.
        
        :param type:
            One of the accepted vim buffer types.
        '''
        commands.set_buffer_type(type=type, expression=self._buffer_number)

class Window(object):
    '''An instance of a Vim window.'''


    def __init__(self, id=None, winnr=None):
        '''
        :param id:
            If None, the current window id is used or one is generated for the
            current window if needed. If not None, a search is preformed
            looking for the supplied id, and if found an instance is created
            for that window. If one is not found, the supplied wid is created
            for the current window. This changes when a winnr is defined.
        :param winnr:
            If not None, the defined winnr is selected and the id is written
            to that winnr. If id is None and the winnr defined already has an
            id, the instance is created with that id. Any conflicts will raise
            the proper exceptions.
        '''
        if winnr is None:
            # The winnr is none. We either create an id, or search for one.

            if id is None:
                # No id is specified. Try and get an id from the current winnr
                self._id = commands.get_id_from_winnr(winnr=None)
                return
            else:
                # The id is defined, so we want to see if it exists already
                # and if not, create it for the current window (and possibly fail)

                id_winnr = commands.get_winnr_from_id(id)
                if id_winnr is None:
                    # There is no winnr which has that id. So assign the id to
                    # the current winnr. This will fail if the current winnr
                    # already has an id.
                    commands.assign_id_to_winnr(id=id, winnr=None)
                    # Store it and return.
                    self._id = id
                    return
                else:
                    # The id is assigned to a winnr. So simply store the id
                    # and return
                    self._id = id
                    return
        else:
            # A specific winnr is being used.

            if id is None:
                # No id is given though. So we find the id of that window
                id = commands.get_id_from_winnr(winnr)
                # Now store it and we're done.
                self._id = id
                return
            else:
                # The winnr is defined, and so is the id. So we need to try
                # and write the id to te specified winnr.
                commands.assign_id_to_winnr(id=id, winnr=winnr)
                # Now if that didn't fail, store the id and return.
                self._id = id
                return
        # The code path should never reach here.

    def command(self, command):
        '''Execute a command in the context of this window.
        
        :param command:
            The vim command to execute.
        '''
        commands.window_comand(command, self._id, toggle=True)

    def eval(self, eval):
        '''Run the given eval in the context of this window.

        :param eval:
            A string to eval in vim.
        '''
        commands.window_eval(eval, self._id, toggle=True)

    def get_winnr(self):
        '''Get the win number of the current window.
        
        :returns:
            The winnr of the current window. None is returned
            if no window has this win id.
        '''
        return commands.get_winnr_from_id(self._id)

    def has_focus(self):
        '''Does this window have focus?

        :returns:
            True if it does, False otherwise.
        '''
        focused_winnr = commands.eval('winnr()')
        return focused_winnr == self.get_winnr()

    def set_buffer(self, buffer):
        '''Set the active buffer for this window.

        :param buffer:
            A :class:`Buffer` instance.
        '''
        commands.set_window_buffer(self._id, buffer.get_number())
    
    def split(self, plane, new_window_side, id=None):
        '''Split a window on the plane specified, either horizontal or
        vertical. The new window will go on the side specified,
        either above/below/left/right.

        :param plane:
            The plane to split this window on. Either `horizontal`
            or `vertical`
        :param new_window_side:
            The side the new window will be placed. Depending on the
            splitting plane, either above/below/left/right.
        :param id:
            The id of the window.

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

        # Create the vim window
        commands.window_command('%s %s new' % (
            vim_plane_options[plane], vim_side_options[new_window_side]),
            id=self._id,
            toggle=True)

        # Get the winnr of the new window. If this is a leftabove split
        # then the winnr should be one less than this windows winnr. Otherwise
        # it should be one more.
        if vim_side_options[new_window_side] == 'leftabove':
            new_winnr = commands.get_winnr_from_id(self._id) - 1
        else:
            new_winnr = commands.get_winnr_from_id(self._id) + 1

        # Now create the window instance and return it.
        return Window(id=id, winnr=new_winnr)

