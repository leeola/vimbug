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
  
    def set_type(self, type):
        '''Set the type for this buffer.
        
        :param type:
            One of the accepted vim buffer types.
        '''
        raise NotImplemented()

class Window(object):
    '''An instance of a Vim window.'''


    def __init__(self, id=None):
        '''
        :param id:
            If None, the current window id is used or one is generated for the
            current window if needed. If not None, a search is preformed
            looking for the supplied id, and if found an instance is created
            for that window. If one is not found, the supplied wid is created
            for the current window.
        '''

        # Get the current winnr
        current_winnr = int(vim.eval('winnr()'))

        # If the given wid is None, generate one.
        if id is None:
            # Generate the wid
            id = commands.find_unique_window_id()

            # Assign it to the current window.
            commands.assign_window_id(id)
        else:
            # Find the winnr for the id given, if any.
            id_winnr = commands.get_winnr_from_id(id)
            
            if id_winnr is None:
                # If there are no matching winnr ids, assign it to the current
                # window.
                # Note that if there is a matching id, we don't need to
                # create/assign anything.
                commands.assign_window_id(id)

        #: The window id for the current window instance.
        self._id = id

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
        raise NotImplementedError()
    
    def split(self, plane, new_window_side, id=None, buffer=None):
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
        :param buffer:
            An instance of the :class:`Buffer` class. If None, no buffer
            is used.

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
        vim.command('%s %s new' % (
            vim_plane_options[plane], vim_side_options[new_window_side]))

        # Now grab the current window, which should be the new window, and
        # create it.
        window = Window(id=id)

        #if buffer is not None:
        #    window.set_buffer(buffer)

        return window

