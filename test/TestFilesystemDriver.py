###############################################################################
# NAME:             FilesystemDriver.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      An abstraction layer for functions that manipulate the
#                   native filesystem. This is employed to facilitate testing.
#
# CREATED:          07/27/2019
#
# LAST EDITED:      07/27/2019
###

import os
import os.path

sep=os.path.sep
# Structure of internalDict and currentPath:
# internalDict = {
#   'dir' = True
#   'dirEntry1' = {
#       'dir' = True
#       'dirSubentry1 ' = {...}
#   }
#   'dirEntry2' = {
#       'dir' = False
#   }
# }
internalDict=None
currentPath=None

def locateEntry(path):
    """INTERNAL: Locate an entry in the simulated filesystem."""
    components = split(path)
    pathWalk = None
    if components[0] == '.':
        pathWalk = currentPath
    pathWalk = internalDict
    for key in split(path):
        if key == '.':
            continue

def listdir(path='.'):
    """List the contents of a directory."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')
    pathWalk = internalDict
    for key in split(path):
        try:
            pathWalk = pathWalk[key]
        except KeyError as e:
            raise FileNotFoundError(("[Errno 2] No such file or directory:"
                                     " '{}'").format(path))
    return list(pathWalk.keys()).remove('dir')

def abspath(path):
    """Return a normalized absolutized version of the pathname path."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')
    pathWalk = internalDict
    for key in split(path):
        try:
            pathWalk = pathWalk[key]
        except KeyError as e:
            raise FileNotFoundError(("[Errno 2] No such file or directory:"
                                     " '{}'").format(path))

def basename(path):
    """Return the basename of the pathname path."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')
    return split(path)[-1]

def isdir(path):
    """Return True if path is an existing directory."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')

def join(path):
    """Join one or more path components intelligently."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')
    sep.join(path)

def split(path):
    """Split path into a list of path components using the native separator."""
    if internalDict is None or currentPath is None:
        raise Exception('The filesystem driver is uninitialized.')
    path.split(sep)

###############################################################################
