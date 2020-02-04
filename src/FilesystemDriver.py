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

def listdir(path='.'):
    """List the contents of a directory."""
    return os.listdir(path)

def abspath(path):
    """Return a normalized absolutized version of the pathname path."""
    return os.path.abspath(path)

def basename(path):
    """Return the basename of the pathname path."""
    return os.path.basename(path)

def isdir(path):
    """Return True if path is an existing directory."""
    return os.path.isdir(path)

def join(path):
    """Join one or more path components intelligently."""
    return os.sep.join(path)

def split(path):
    """Split path into a list of path components using the native separator."""
    return os.sep.split(path)

###############################################################################
