#!/usr/bin/env python3
###############################################################################
# NAME:             BugFileTree.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      Concrete implementation of the IFileTree class.
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/22/2019
###

from IFileTree import IFileTree
from RepositoryFactory import RepositoryFactory
from RepositoryExceptions import NotAValidRepositoryException
from FileTreeExceptions import NotAValidFileTreeRootException
from BugFileTreeNode import BugFileTreeNode

class BugFileTree(IFileTree):
    """
    This class implements the IFileTree abstract class. This class must have
    a BugFileTreeNode containing a valid Repository object at its root.
    """
    def __init__(self, path):
        super()
        try:
            self.repository = RepositoryFactory.getRepository(path)
            self.rootNode = BugFileTreeNode(path)
        except NotAValidRepositoryException:
            raise NotAValidFileTreeRootException()

    def searchTopDown(function, *args):
        """
        Search the file tree, top down, and invoke function on each node in the
        tree. The function must take an IFileTreeNode object as it's first
        argument. Subsequent arguments may be passed using the variable args.
        It's important that function does not change the paths of files in the
        directory, as that results in undefined behavior.
        """
        pass

    @staticmethod
    def readIgnoreFile(ignoreFilename):
        """INTERNAL. Read ignoreFilename file for the list of regexes."""
        try:
            with open(ignoreFilename, 'r') as ignoreFile:
                return list(filter(('').__ne__,
                                   [ln.rstrip('\n')
                                    for ln in ignoreFile.readlines()]))
        except FileNotFoundError:
            pass

    def getIgnoreList():
        """Get the list of files to ignore in the file tree."""
        # Automatically ignore .git/ and bugs
        rejectFilenames = [self.path + '.git/', '~']
        rejectRegexes = []
        # Read .bignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.path + '/.bignore')
                             or [])
        # Read .gitignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.path + '/.gitignore')
                             or [])

        # Expand shell-style globs in rejectRegexes
        for regex in rejectRegexes:
            if '*' in regex:
                rejectFilenames.extend(glob(self.path + '/**/' + regex,
                                            recursive=True))
            else:
                rejectFilenames.append(regex)


###############################################################################
