
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
    main_group = parser.add_mutually_exclusive_group()
    config_group = parser.add_mutually_exclusive_group()

    # Add arguments.
    main_group.add_argument('-s', '--server', dest='server',
            default='localhost',
            help='The server vim-debug will connect to.')
    main_group.add_argument('-t', '--port', dest='port', default=9000,
            type=int,
            help='The port used in conjunction with --server.')
    main_group.add_argument('-l', '--location', dest='location',
            help=('The location of the file/URL to debug. Note that "." is '
                'accepted in place of the current buffer file.'))
    main_group.add_argument('-r', '--repeat', dest='repeat', action='store_true',
            help=('Repeat the last debug command. If other options are '
            'provided such as -s, -t, -l, etc, they will be override ' 
            'whatever is stored as the last command.'))
    main_group.add_argument('-m', '--main_debug', dest='main_debug',
            action='store_true',
            help=('Debug whatever file/location is in the project config. '
                'Any additional commands supplied will overwrite whatever ' 
                'is read in the config for that single execution, as in -r.'))

    config_group.add_argument('--create_config', dest='create_config',
            action='store_true',
            help=('Create a config if it doesn\'t exist. Use --replace_config '
            'if a config already exists.'))
    config_group.add_argument('--replace_config', dest='replace_config',
            action='store_true',
            help='Replace an existing config file.')


