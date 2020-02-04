#!/usr/bin/env python3
###############################################################################
# NAME:             FileTreeExceptions.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

#pylint: disable=unnecessary-pass

class NoContainingFileTreeException(Exception):
    """
    This exception is thrown when a FileTreeNode has no valid containing
    FileTree object.
    """
    pass

class NotValidFileTreeRootException(Exception):
    """
    This exception is thrown when a FileTree cannot be constructed from the
    path supplied.
    """
    pass

###############################################################################
