#!/usr/bin/env python3
###############################################################################
# NAME:             IFileTreeNode.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

#pylint: disable=unnecessary-pass,non-parent-init-called

from abc import ABC, abstractmethod

class IFileTreeNode(ABC):
    """
    An abstract class to represent an entry on the filesystem. This class does
    not care about the type of the entry (file, directory, symlink, etc). A
    FileTree contains these nodes in a tree structure, mirroring the structure
    of the filesystem.
    """
    def __init__(self):
        super.__init__()

    @abstractmethod
    def getPath(self):
        """Return the filesystem path referring to this node."""
        pass

    @abstractmethod
    def getName(self):
        """Return the base name of the filesystem entry this node refers to."""
        pass

    @abstractmethod
    def getContainingFileTree(self):
        """Return the FileTree object containing this node, if it exists."""
        pass

    @abstractmethod
    def getChildren(self):
        """Return a list of the children of this node."""
        pass

    @abstractmethod
    def getParent(self):
        """Return the FileTreeNode parent of this node."""
        pass

###############################################################################
