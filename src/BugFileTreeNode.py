#!/usr/bin/env python3
###############################################################################
# NAME:             BugFileTreeNode.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/20/2019
###

import os

from IFileTreeNode import IFileTreeNode

class BugFileTreeNode(IFileTreeNode):
    """Class representing a node in a BugFileTree."""
    def __init__(self, path):
        super()
        self.path = os.path.abspath(path)

    def getPath(self):
        """Return the filesystem path referring to this node."""
        return self.path

    def getName(self):
        """Return the base name of the filesystem entry this node refers to."""
        return os.path.basename(self.path)

    def getContainingFileTree(self):
        """Return the FileTree object containing this node, if it exists."""
        try:
            return BugFileTree(self.path)
        except NotAValidFileTreeRootException:
            if self.path == self._getRootDirectory():
                raise NoContainingFileTreeException
            return self.getParent().getContainingFileTree()

    def getChildren(self):
        """Return a list of the children of this node."""
        children = list()
        if not os.path.isdir(self.path):
            return children
        for fname in os.listdir(self.path):
            children.append(BugFileTreeNode(self.path + os.path.sep + fname))
        return children

    def getParent(self):
        """Return the FileTreeNode parent of this node."""
        root = self._getRootDirectory()
        if self.path == root:
            return None
        return BugFileTreeNode(
            os.path.sep.join(self.path.split(os.path.sep)[:-1]))

    def _getRootDirectory(self):
        """INTERNAL: Get the path of the root directory"""
        return os.path.abspath(self.path).split(os.path.sep)[0]

###############################################################################
