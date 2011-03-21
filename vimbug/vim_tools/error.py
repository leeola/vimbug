'''Errors for vim tools.'''

from exception import Exception


class VimToolsError(Exception):
    '''The base VimTools error.'''
    pass

class NoWindowDError(VimToolsError):
    '''A vim window does not have the value w:id'''
    pass

