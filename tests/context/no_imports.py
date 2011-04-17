# -*- coding: utf-8 -*-
'''
    tests.context.no_imports
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A single debug file with no imports and no requirements. This helps to
    keep the code path simple.

    :copyright: (c) 2011 by Lee Olayvar
    :license: MIT, see LICENSE for more details.
'''

MODULE_VAR = 0 
MODULE_VAR_LIST = [1, 2, 3,]

# The following is a group of single functions.
# That is, they don't run anything outside of their own scope.
def single_return_none():
    '''This function simply returns None. Impressive eh?'''
    return None

def single_zero_division_failure():
    '''Attempt to break the universe.'''
    0/1

def single_raise_not_implemented():
    '''Raise not implemented. This docstring feels a bit redundant.'''
    raise NotImplemented('Everything is going according to plan.')


