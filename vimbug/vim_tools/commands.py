# -*- coding: utf-8 -*-
'''
    vim_tools.commands
    ~~~~~~~~~~~~~~~~~~

    A collection of vim commands in python form and often with added utility.

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
import logging
from random import randint

from error import BufferNotFoundError, WIDConflictError, WIDNotFoundError


# Get the logger
logging.basicConfig()
logger = logging.getLogger('vim_tools')

# This should allow us to run tests that import this vim code without
# blowing up if we're not inside of vim.
try:
    from vim import eval as vim_eval
    from vim import command as vim_command
except ImportError:
    logger.warning('Vim import failed.')


def _format_expression(expression):
    '''A little function to format an expression for vim. Eg: strings are
    formatted as '"string"', integers as 'int', and None as '%'.

    :param expression:
        A string expression to find a buffer name from. See
        `Buffer.__init__()` documentation for reference.
    
    :returns:
        A formatted string expression.
    '''
    if expression is None:
        return '"%"'
    elif isinstance(expression, int):
        return str(expression)
    else:
        return '"%s"' % expression

def _set_focus(winnr):
    '''The private version of :func:`set_focus()`. The only difference is
    that this function takes a winnr, rather than a window id. This is
    specifically for the private functions that never get a window id.

    :param winnr:
        The window number.

        **Note**: This winnr *is *not** checked for existance. In other words,
        this may blow up if not checked before hand.
    '''
    command('exec "normal! \\<C-W>".%s.\'w\'' % winnr)

def _toggle_buffer(formatted_expression, func, args=None, kwargs=None):
    '''A helper function to set the active buffer to the buffer specified,
    and then return the active buffer to the original.. i worded that poorly.

    :param formatted_expression:
        A string expression which will match the buffer to toggle. See
        :func:`buffer_command()` documentation for reference.

        **Note**: This string *is *not** formatted. In other words, it needs
        to be previously formatted or the world may asplode.
    :param func:
        The function to wrap. Generally just `buffer_command`, or `buffer_eval`.
    :param args:
        A tuple of arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.
    :param kwargs:
        A dictionary of keyword arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.

    :raises BufferNotFoundError:
        Raised if there are no buffers that match the expression given.

    :returns:
        The product of running `func(*args, **kwargs)`.
    '''
    # Create defaults for args and kwargs if None.
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}

    # Get the current and target buffers..
    original_bufnr = buffer_eval('bufnr("%")')
    target_bufnr = buffer_eval('bufnr(%s)' % formatted_expression)
    same_bufnr = original_bufnr == target_bufnr
    if target_bufnr == '-1':
        raise BufferNotFoundError(
            'No buffer matching the following expression: '
            '%s' % formatted_expression)

    if same_bufnr:
        return func(*ags, **kwargs)

    # Change the active buffer..
    command('b %s' % target_bufnr)
    # Get the result
    func_result = func(*args, **kwargs)
    # And now change it back.
    command('b %s' % original_bufnr)

    return func_result

def _toggle_window(winnr, func, args=None, kwargs=None):
    '''A helper function to set the active window to the window specified,
    and then after the function is executed return the active window to the
    original active window.. i worded that worse than before.

    :param winnr:
        The window number.

        **Note**: This id *is *not** checked for existance. In other words,
        this may blow up if not checked before hand.
    :param func:
        The function to wrap. Generally just `window_command` or `window_eval`
    :param args:
        A tuple of arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.
    :param kwargs:
        A dictionary of keyword arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.
    
    :returns:
        The product of running `func(*args, **kwargs)`
    '''
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}
    original_winnr = eval('winnr()')
    
    if original_winnr == winnr:
        return func(*args, **kwargs)

    _set_focus(winnr)
    func_result = func(*args, **kwargs)
    _set_focus(original_winnr)

    return func_result

def assign_id_to_winnr(id=None, winnr=None):
    '''Assign a window id for a window.

    :param wid:
        The window id to use. If None, a unique id is generated.
    :param winnr:
        If None, the current window.

    :raises WIDConflictError:
        No matching wid was found for the supplied wid, and the current
        window already has a wid. Due to this the instance cannot be
        created and is failing.
    '''
    if id is None:
        # Create a window id if needed.
        id = find_unique_window_id()

    # Now we need to get the winnr so we can make sure we're not overwriting
    # an already existing w:id
    if winnr is None:
        # Get the window number if it is None.
        winnr = int(eval('winnr()'))
        current_winnr = winnr
    else:
        current_winnr = int(eval('winnr()'))

    winnr_id = eval('getwinvar(%s, "id")' % winnr)
    if winnr_id is not None:
        # If the target winnr is not None, then we need to fail so we don't
        # overwrite the id.
        raise WIDConflictError('The winnr:%s already has an id when a write '
                               'was attempted. Current id:%s, attempted '
                               'id:%s' % (winnr, winnr_id, id))

    # We have to toggle ourselves, since no w:id exists to pass into
    # window_command()
    _toggle_window(winnr, command, args=('let w:id="%s"' % id,))

def buffer_command(command_, expression=None):
    '''Run the given command in the specified buffer, if any.
 
    **Note:** This currently uses "b bufnr" as the command to toggle buffers.
    This may not be the optimal way to switch buffers, as it will affect the
    users by changing their ability to use "b #".

    :param command_:
        The command to execute.
    :param expression:
        A string expression used to find a buffer from. Some usage examples
        are as follows..::

            buffer_command('#')     # The alternate buffer
            buffer_command(3)       # The buffer number 3. Note that this is
                                    # an integer. '3' does not equate to 3.
            buffer_command('%')     # The current buffer. 
            buffer_command('file2') # A buffer where "file2" matches.

        **Note**: This string *is* formatted.

    :raises NoBufferFoundError:
        Raised if there are no buffers that match the expression given.
    '''
    if expression is not None:
        expression = _format_expression(expression)

        # Run the command
        _toggle_buffer(expression, command, args=(command_,))
    else:
        command(command_)

def buffer_eval(eval_, expression=None):
    '''Run the given eval in the specified buffer, if any.
    See :func:`buffer_command()` for further documentation.

    :returns:
        The eval response from the context of the expression.
    '''
    if expression is not None:
        expression = _format_expression(expression)

        # Get the result
        return  _toggle_buffer(expression, eval, args=(eval_,))
    else:
        return eval(eval_)

def buffer_exists(expression):
    '''Check whether a buffer exists or not.

    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.
    
    :returns:
        True if a match for the expression is found, False otherwise.
    '''
    # Format the exp.
    expression = _format_expression(expression)

    return eval('bufexists(%s)' % expression) == '1'

def command(command_):
    '''A simple local function for vim.command.

    :param command_:
        The string to execute.
    '''
    vim_command(command_)

def create_buffer(name):
    '''Create a new buffer.

    :param name:
        The name of the buffer.
    '''
    # This may not be the best way to create a buffer. Cross
    # your fingers folks.. hey, i think it works, leave me alone.
    command('badd %s' % name)

def delete_buffer_content(bufnr):
    '''Delete the contents of the specified buffer.

    :param bufnr:
        The buffer number to delete.
    '''
    # Grabbed from irc support.. not sure if the underscore is even useful..
    buffer_command(command_='%delete _', expression=bufnr)

def eval(eval_):
    '''A simple local function for vim.eval.

    :param eval_:
        The string to eval.

    :returns:
        The product of `vim.eval(eval_)`.
    '''
    return vim_eval(eval_)

def find_unique_window_id(self):
    '''Check every single window var to find a winvar that does not
    exist. This is done by taking the "largest" winvar, and incremented
    by one.
    '''
    total_windows = int(eval('winnr("$")'))

    largest_winid = 0
    # Remember, winnr's start at 1, not 0.
    for _winnr in range(1, total_windows+1):
        winvar_result = eval('getwinvar(%s, "id")' % _winnr)
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

def get_current_winnr():
    '''Simply get the current winnr.

    :returns:
        The currently active window number. Converted to an int.
    '''
    return int(eval('winnr()'))

def get_buffer_name(expression):
    '''Get a buffer name.

    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.

    :returns:
        The buffer name.
    '''
    # Format the exp.
    expression = _format_expression(expression)

    # Get the bufname result.
    return eval('bufname(%s)' % expression)

def get_buffer_number(expression=None):
    '''Get a buffer number.

    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.

    :returns:
        The buffer number.
    '''
    # Format the exp.
    expression = _format_expression(expression)

    # Get the bufnum.
    eval_result = eval('bufnr(%s)' % expression)
    if eval_result == '-1':
        raise BufferNotFoundError(
            'No buffer matching the following expression: %s' % expression)
    return int(eval_result)

def get_vim_height():
    '''Get the height of the vim frame itself.

    :returns:
        The height of the vim frame itself, in lines.
    '''
    return int(eval('&lines'))

def get_vim_width():
    '''Get the width of the vim frame itself.

    :returns:
        The width of the vim frame itself, in lines.
    '''
    return int(eval('&columns'))

def get_winnr_from_id(id):
    '''Get the winnr from the given window id.

    :param id:
        A window id.

    :returns:
        The first winnr that has the wid specified. None is returned
        if none are found to match.
    '''

    total_windows = int(eval('winnr("$")'))
    # Remember, winnr's start at 1 not 0
    for winnr in range(1, total_windows+1):
        winvar_result = eval('getwinvar(%s, "id")' % winnr)
        if winvar_result == str(id):
            return winnr
    # No matches found. Return None
    return None

def set_buffer_type(type, expression=None):
    '''Set the buftype variable for the given expression. If any.

    :param type:
        One of the accepted vim buffer types. If None, an empty buftype is used.
    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.
 
    :raises BufferNotFoundError:
        Raised if there are no buffers that match the expression given.
    '''
    if type is None:
        type = ''
    buffer_command('set buftype=%s' % type, expression)

def set_window_buffer(id, buffer_name):
    '''Set the buffer a window is using.

    :param id:
        A window id to assign the buffer to.
    :param buffer_name:
        The buffer name or number to assign to this window.
    '''
    window_command('b %s' % buffer_name, id=id, toggle=True)

def set_window_height(id, height):
    '''Set the window height.

    :param id:
        The id of the window to set the height of.
    :param height:
        The height of the window, in lines.
    '''
    winnr = get_winnr_from_id(id)
    _toggle_window(winnr, command, args=('resize %s' % height,))

def set_window_width(id, width):
    '''Set the window width.

    :param id:
        The id of the window to set the width of.
    :param width:
        The width of the window, in lines.
    '''
    winnr = get_winnr_from_id(id)
    _toggle_window(winnr, command, args=('vertical resize %s' % width,))

def window_command(command_, id=None, toggle=True):
    '''Execute a command within the specified window, if any.

    :param command_:
        The vim command to execute.
    :param id:
        The window id to switch to.
    :param toggle:
        If True, switch to the window id given and after the command is
        executed, switch back to the original window id. If False, don't do
        that.
    
    :raises WIDNotFoundError:
        The wid supplied cannot be found within the current tab.
    '''
    if id is None:
        # If the id is None, we can't toggle anything anyway,
        # so run the command.
        command(command_)

    winnr = get_winnr_from_id(id)
    if winnr is None: 
        # If the window id does not exist, raise a failure.
        raise WIDNotFoundError('The window id given does not exist.')
    
    if toggle:
        _toggle_window(winnr, command, args=(command_,))
    else:
        _set_focus(winnr)
        command(command_)

def window_eval(eval_, id=None, toggle=True):
    '''Run the given eval in the specified window, if any.
    See :func:`window_command()` for further documentation.

    :returns:
        The eval response from the context of the window specified.
    '''
    if id is None:
        # If the id is None, we can't toggle anything anyway,
        # so run the command.
        command(command_)

    winnr = get_winnr_from_id(id)
    if winnr is None: 
        # If the window id does not exist, raise a failure.
        raise WIDNotFoundError('The window id given does not exist.')
    
    if toggle:
        _toggle_window(winnr, eval, args=(eval_,))
    else:
        _set_focus(winnr)
        eval(eval_)

def window_id_exists(id):
    '''Check whether a window id exists or not. Currently this is done by
    looping through all of the windows and seeing if an id exists. In
    the future a tab var holding all of the ids is planned.. i think?

    :param id:
        The id to check.

    :returns:
        True if a window is found to have a w:id variable with the value of
        id, and False otherwise.
    '''
    total_windows = int(eval('winnr("$")'))
    
    # Remember, winnr's start at 1, not 0.
    for _winnr in range(1, total_windows+1):
        winvar_result = eval('getwinvar(%s, "id")' % _winnr)
        if winvar_result is not None and winvar_result == str(id):
            return True
    return False

def write_buffer(text, line='$', expression=None):
    '''Write text to a buffer.

    :param text:
        The text to write.
    '''
    if isinstance(text, basestring):
        # Wrap the string in quotes so that it is submitted to the command
        # as a vim string.
        line = '"%s"' % line
    buffer_command(command_='call append(line(%s), %s)' % (line, text.split('\n')),
                   expression=expression)

