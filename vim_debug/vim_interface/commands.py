
from argparse import ArgumentParser


def main(args):
    ''' The main vim-debug command. Called by the user typing "Dbg [options]"
    '''
    pass

def parse_started_args(args):
    ''' Parse the args that Dbg will accept after it has been started.'''
    pass

def parse_stopped_args(args):
    ''' Parse the args that Dbg will accept when it is stopped.'''
    
    # Create a parser.
    parser = ArgumentParser(description='Start a vim-debug session.')

    # Add arguments.
    parser.add_argument('-s', '--server', dest='server',
            default='localhost',
            help='The server vim-debug will connect to.')
    parser.add_argument('-t', '--port', dest='port', default=9000,
            type=int,
            help='The port used in conjunction with --server.')
    parser.add_argument('-l', '--location', dest='location',
            help=('The location of the file/URL to debug. Note that "." is '
                'accepted in place of the current buffer file.'))
    parser.add_argument('-r', '--repeat', dest='repeat', action='store_true',
            help=('Repeat the last debug command. If other options are '
            'provided such as -s, -t, -l, etc, they will be override ' 
            'whatever is stored as the last command.'))
    parser.add_argument('-m', '--main_debug', dest='main_debug',
            action='store_true',
            help=('Debug whatever file/location is in the project config. '
                'Any additional commands supplied will overwrite whatever ' 
                'is read in the config for that single execution, as in -r.'))


