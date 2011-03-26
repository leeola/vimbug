# -*- coding: utf-8 -*-
'''
    vim_tools.commands
    ~~~~~~~~~~~~~~~~~~

    A collection of vim commands in python form and often with added utility.

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''
from random import randint

import vim


def _format_expression(expression):
    '''A little function to format an expression for vim. Eg: strings are
    formatted as '"string"', integers as 'int', and None as '%'.

    :param expression:
        A string expression to find a buffer name from. See
        `Buffer.__init__()` documentation for reference.
    
    :returns:
        A formatted string expression.
    '''
    if None:
        expression = '"%"'
    elif ifinstance(expression, int):
        expression = '3'
    else:
        expression = '"%s"' % expression
    return expression

def _toggle_buffer(expression, func, args=None, kwargs=None):
    '''A helper function to set the active buffer to the buffer specified,
    and then return the active buffer to the original.. i worded that poorly.

    :param expression:
        A string expression which will match the buffer to toggle. See
        :func:`buffer_command()` documentation for reference.

        **Note**: This string *is *not** formatted.
    :param func:
        The function to wrap. Generally just `buffer_command`, or `buffer_eval`.
    :param args:
        A tuple of arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.
    :param kwargs:
        A dictionary of keyword arguments which will be fed to func.
        Eg: `func(*args, **kwargs)`.

    :raises NoBufferFoundError:
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
    current_buffer = buffer_eval('bufnr("%")')
    target_buffer = buffer_eval('bufnr(%s)' % expression)
    different_buffer = current_buffer != target_buffer
    if target_buffer == '-1':
        raise NoBufferFoundError(
            'No buffer matching the following expression: %s' % expression)

    # Change the active buffer..
    if different_buffer:
        vim.command('b %s' % target_buffer)

    # Get the result
    func_result = func(*args, **kwargs)

    # And now change it back.
    if different_buffer:
        vim.command('b %s' % current_bufnum)

    return func_result

def buffer_command(command, expression=None):
    '''Run the given command in the specified buffer, if any.
 
    **Note:** This currently uses "b bufnr" as the command to toggle buffers.
    This may not be the optimal way to switch buffers, as it will affect the
    users by changing their ability to use "b #".

    :param eval:
        The string to eval.
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
        _toggle_buffer(expression, vim.command, args=(command,))
    else:
        vim.command(command)

def buffer_eval(eval, expression=None):
    '''Run the given eval in the specified buffer, if any.
    See :func:`buffer_command()` for further documentation.

    :returns:
        The eval'd code from the context of the expression.
    '''
    if expression is not None:
        expression = _format_expression(expression)

        # Get the result
        return  _toggle_buffer(expression, vim.eval, args=(eval,))
    else:
        return vim.eval(eval)

def create_buffer(self, name):
    '''Create a new buffer.

    :param name:
        The name of the buffer.
    '''
    # This may not be the best way to create a buffer. Cross
    # your fingers folks.. hey, i think it works, leave me alone.
    buffer_command('badd %s' % name)

def exists(expression):
    '''Check whether a buffer exists or not.

    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.
    
    :returns:
        True if a match for the expression is found, False otherwise.
    '''
    # Format the exp.
    expression = _format_expression(expression)

    return buffer_eval('bufexists(%s)' % expression) == '1'

def get_buffer_name(self, expression):
    '''Get a buffer name.

    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.

    :raises NoBufferFoundError:
        Raised if there are no buffers that match the expression given.

    :returns:
        The buffer name.
    '''
    # Format the exp.
    expression = self._format_expression(expression)

    # Get the bufname result.
    buffer_name = self._eval('bufname(%s)' % expression)

    if buffer_name is None:
        # Raise an error if no matches were found.
        raise NoBufferFoundError('No buffer name could be found for the '
                                 'expression %s.' % expression)

    return buffer_name

def set_buffer_type(type, expression=None):
    '''Set the buftype variable for the given expression. If any.

    :param type:
        One of the accepted vim buffer types.
    :param expression:
        A string expression to find a buffer name from. See
        :func:`buffer_command()` documentation for reference.
 
    :raises NoBufferFoundError:
        Raised if there are no buffers that match the expression given.
    '''



