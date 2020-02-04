#!/usr/bin/env python3
###############################################################################
# NAME:             FileTree.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/22/2019
###

#pylint: disable=too-few-public-methods,unnecessary-pass,non-parent-init-called

# TODO: Delete these interfaces. They're completely superfluous.

from abc import ABC, abstractmethod

class IFileTree(ABC):
    """
    This abstract class is meant to represent a particular type of file tree.
    For any given implementation of FileTree, that implementation is not
    required to allow creation of FileTree objects from any directory. This is
    useful to, for example, have an implementation that only allows its objects
    to refer to version control repositories in the filesystem.
    """
    def __init__(self, path):
        super.__init__()

    @abstractmethod
    def getRootNode(self):
        """Return the FileTreeNode at the root of this tree."""
        pass

###############################################################################
