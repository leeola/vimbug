'''
'''
import logging


logger = logging.getLogger('vimbug')


class SessionInformation(object):
    '''An information object in charge of storing basic information
    about the server, port, location, session type, etc.
    '''

    # The supported session types.
    supported_types = [
        'python',
    ]

    def __init__(self, server, port, location):
        '''
        '''
        
        self.server = server
        self.port = port
        self.location = location

        # Try and figure out the session type.
        self.session_type = self._estimate_session_type()
        
        if session_type not in self.supported_types:
            raise NotImplemented()

    def _estimate_session_type(self):
        '''Look at the location and estimate the session type.'''

        def try_python():
            
            if self.location.endswith('.py'):
                return True

            # I need to add a check for the first line of the file
            # to see if a #! python declaration is in there, to support
            # extension-less python files.

            # Nothing matched, return false.
            return False

        type_checkers = {
            'python':try_python,
        }

        for type_, type_checker in type_checkers.items():
            if type_checker():
                return type_
        
        # No type returned True, so return None
        return None

