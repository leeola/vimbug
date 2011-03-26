'''Errors for vim tools.'''

from exceptions import Exception


class VimToolsError(Exception):
    '''The base VimTools error.'''
    pass

class BufferNotFoundError(VimToolsError):
    pass

class WIDConflictError(VimToolsError):
    pass

class WIDNotFoundError(VimToolsError):
    pass

