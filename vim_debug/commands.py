import os
import sys
import vim
import socket
import traceback
from new_debugger import Debugger

import shlex

def get_vim(name, default, fn=str):
    if vim.eval('exists("%s")' % name) == '1':
        return vim.eval(name)
    return default

_old_commands = _commands = {}
def debugger_cmd(plain):
    global _commands, debugger
    if not _commands:
        return start(*shlex.split(plain))
    if ' ' in plain:
        name, plain = plain.split(' ', 1)
        args = shlex.split(plain)
    else:
        name = plain
        plain = ''
        args = []
    if name not in _commands:
        print '[usage:] dbg command [options]'
        tpl = ' - %-7s :: %s'
        leader = get_vim('mapleader', '\\')
        for command in _commands:
            print tpl % (command, _commands[command]['options'].get('help', ''))
            if 'lead' in _commands[command]['options']:
                print '           shortcut: %s%s' % (leader, _commands[command]['options']['lead'])
        return
    cmd = _commands[name]
    try:
        if not callable(cmd['function']):
            if debugger.bend.connected():
                    debugger.bend.command(cmd['function'])
        elif cmd['options'].get('plain', False):
            cmd['function'](plain)
        else:
            cmd['function'](*args)
    except (EOFError, socket.error):
        if debugger is not None:
            debugger.disable()
    if name == 'quit':
        _commands = None
        debugger = None

def cmd(name, help='', plain=False):
    def decor(fn):
        _commands[name] = {'function':fn, 'options': {'help':help, 'plain':plain}}
        return fn
    return decor

debugger = None

def start(*args):
    global debugger
    if debugger and debugger.started:
        return
    
    # Get the type we're going to be working with.
    if len(args) >= 1:
        supported_types = {
                'py':'python',
                'php':'php',
                }
        try:
            debug_type = supported_types[args[0]]
        except KeyError:
            debug_type = None
    else:
        debug_type = None

    # Get the main option
    if len(args) >= 2:
        option = args[1]
    else:
        option = None

    # Get the option arguments
    if len(args) >= 3:
        option_arguments = args[2:]
    else:
        option_arguments = []

    type_switch = {
            None:start_repeat,
            'python':start_python,
            'php':start_php,
            }
    type_switch[debug_type](option, option_arguments)

def start_repeat(option, option_arugments):
    print 'Not implemented.'

def start_python(option, option_arguments):
    global debugger
    if debugger and debugger.started:
        return
       
    def is_python_file(file_name):
        if not os.path.exists(file_name):
            return False 
        
        # If the file is not a python file
        if file_name.endswith('.py'):
            return True
        else:
            # Check the first line to see if it contains a python executable
            first_line = open(file_name, 'r').readline()
            if first_line.startswith('#!') and first_line.endswith('python'):
                return True

            # This is not a python file, return false
            return False
    
    def file_does_not_exist_warning():
        print 'Error: The file provided does not exist or is not a python file.'
    
    # Set the option to file, and the arguments to the current file.
    if option == '.':
        option = 'file'
        option_arguments = [vim.current.buffer.name]
 
    # If the option is project, we want to find and run the main debug
    # file for this project, if there is one.
    if option == 'project':
        print 'Not implemented..'
        return

    if option == 'file': 
        if len(option_arguments) == 0:
            print '''Invalid usage.
            Correct usage: Dbg py file /some/dir/file.py'''
            return
        
        # Get the absolute path for this file
        file_name = os.path.expanduser(option_arguments[0])
        buffer_directory = os.path.dirname(vim.current.buffer.name)
        rel_file = os.path.relpath(file_name, buffer_directory)
        
        if not is_python_file(rel_file):
            file_does_not_exist_warning()
            return

        debugger = Debugger()

        # Black magic from the original script. This needs to be documented..
        # Well.. first it needs to be figured out dammit.
        debugger.init_vim()
        global _commands
        _commands = debugger.commands()

        # Start the debug server.
        debugger.start_py(rel_file)
        
def start_php(option, option_arugments):
    print 'Not implemented.'

def start_deprecated(url = None):
    global debugger
    if debugger and debugger.started:
        return
    if url is not None:
        if url in ('.', '-') or url.startswith('py:') :
            pass
        elif url.isdigit():
            urls = load_urls()
            num = int(url)
            if num < 0 or num >= len(urls):
                print 'invalid session number'
                url = None
            else:
                url = urls.pop(num)
                urls.insert(0, url)
        else:
            save_url(url)
        if url is not None:
            debugger = Debugger()
            fname = vim.current.buffer.name
            debugger.init_vim()
            global _commands
            _commands = debugger.commands()
            if url == '.':
                if not (os.path.exists(fname) and fname.endswith('.py')):
                    print 'Current file is not python (or doesn\'t exist on your hard drive)'
                    return
                debugger.start_py(fname)
            elif url == '-':
                debugger.start()
            elif url.startswith('py:'):
                fname = url[3:]
                if not (os.path.exists(fname) and fname.endswith('.py')):
                    print 'Current file is not python (or doesn\'t exist on your hard drive)'
                    return
                debugger.start_py(fname)
            else:
                debugger.start_url(url)
            return
    urls = load_urls()
    if not urls:
        print 'No saved sessions'
    for i, url in enumerate(urls):
        print '    %d) %s' % (i, url)
    print '''\
usage: dbg - (no auto start)
       dbg . (autostart current file -- python)
       dbg py:path/to/file.py (autostart the specified file)
       dbg url (autostart a URL -- PHP)
       dbg num (autostart a past url -- PHP)'''

session_path = os.path.expanduser('~/.vim/vim_phpdebug.sess')

def load_urls():
    if os.path.exists(session_path):
        return open(session_path).read().split('\n')
    return []

def save_url(url):
    urls = load_urls()
    urls.insert(0, url)
    urls = urls[:5]
    open(session_path, 'w').write('\n'.join(urls))

