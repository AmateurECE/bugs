#!/usr/bin/env python3
"""A simple bug tracking tool."""
###############################################################################
# NAME:		    bugs.py
#
# AUTHOR:	    Ethan D. Twardy <edtwardy@mtu.edu>
#
# CREATED:	    02/28/2019
#
# LAST EDITED:	    03/01/2019
###

from pathlib import Path
import os
import sys
import re

from t import t
from colorama import colorama
from colorama.colorama import Fore, Style

###############################################################################
# FUNCTIONS
###

class Bugs:
    """Contains the logic of the `b' tool."""

    # Static class members
    # Matches C/C++ and Bash style comments
    todoRegex = r'(%|#|/(\*|/))\s*TODO:\s*(.*)'
    r_todo = re.compile(todoRegex)

    def __init__(self, pwd):
        # Locate the root of the git repository, or if we aren't in one.
        self.gitDir = self.findRepositoryRoot(pwd)

    def synchronizeBugDict(self, delete=False):
        """Initializes t.py's TaskDict object with the current state."""
        if delete:
            # Remove the bugs file if it exists
            try:
                os.unlink(self.gitDir + '/bugs')
            except FileNotFoundError:
                pass

        # Initialize the TaskDict object
        self.bugDict = t.TaskDict(taskdir=self.gitDir, name='bugs')

    @staticmethod
    def findRepositoryRoot(pwd):
        """
        Determine if `pwd' is inside of a git repository and, if so, return the
        path of the root directory of the repository.
        """
        gitHere = Path(os.fspath(pwd) + '/.git')
        rootDir = os.path.abspath(os.sep) # Platform independent
        while os.path.abspath(pwd) != rootDir:
            if gitHere.is_dir():
                return pwd
            pwd = Path(os.fspath(pwd) + '/..')
            gitHere = Path(os.fspath(pwd) + '/.git')
        return None

    @staticmethod
    def readIgnoreFile(ignoreFilename):
        """INTERNAL. Read ignoreFilename file for the list of regexes."""
        try:
            with open(ignoreFilename, 'r') as ignoreFile:
                return [ln.rstrip('\n') for ln in ignoreFile.readlines()]
        except FileNotFoundError:
            pass

    def buildFileList(self):
        """INTERNAL. Builds the list of files to search for TODO comments."""
        # Automatically ignore .git/ and bugs
        rejectRegexes = ['.git/', 'bugs', '~']
        # Read .bignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.gitDir + '/.bignore')
                             or [])
        # Read .gitignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.gitDir + '/.gitignore')
                             or [])

        # Remove the empty string
        rejectRegexes = list(filter(('').__ne__, rejectRegexes))

        # Walk the repository
        #pylint: disable=unused-variable
        validPaths = list()
        for dirpath, dirnames, filenames in os.walk(self.gitDir):
            # First, check if the dirpath contains something we're supposed to
            # ignore.
            for regex in rejectRegexes:
                if regex in dirpath:
                    continue

            # Then, consider each file in the current directory.
            for fn in filenames:
                fn = dirpath + '/' + fn
                reject = False
                # If the filename matches any of the lines in .bignore,
                # reject it.
                # TODO: Implement glob matching for ignore file entries
                for regex in rejectRegexes:
                    if regex in fn:
                        reject = True
                if not reject:
                    validPaths.append(fn)
        return validPaths

    def update(self):
        """Update the bugs file in the gitDir directory."""
        # Initialize the BugDict
        self.synchronizeBugDict(delete=True)
        # Build the file list
        fileList = self.buildFileList()

        # Begin looking for bugs
        for fn in fileList:
            try:
                bugs = self.getBugs(fn) or []
                for bug in bugs:
                    # Add the bug to the dictionary
                    self.bugDict.add_task(fn + ': ' + bug)
            except UnicodeDecodeError:
                print((Fore.YELLOW + 'Warning' + Style.RESET_ALL +
                       ': Could not decode file "{}". If this is a '
                       'binary file, consider adding it to your '
                       '.bignore or .gitignore').format(fn), file=sys.stderr)
                continue

        # Finally, write the changes to disk
        self.bugDict.write(delete_if_empty=True)

    @staticmethod
    def getBugs(fileName):
        """Get a list of bugs in the file `fileName'"""
        bugs = list()
        with open(fileName, 'r') as inputFile:
            for line in inputFile.readlines():
                # Attempt to match the regex.
                bug = Bugs.r_todo.search(line)
                if bug is not None:
                    # If we are matching C style comments, remove the ' */'
                    if bug.group(2) == '*' and bug.group(3)[-3:] == ' */':
                        bugs.append(bug.group(3)[:-3])
                    else:
                        bugs.append(bug.group(3))
        return bugs

    def printBugs(self):
        """Print the bugs in the bugs file"""
        # Initialize the bugDict object
        self.synchronizeBugDict()
        # Print the list of bugs
        self.bugDict.print_list()

###############################################################################
# MAIN
###

def main():
    """Run bugs"""
    colorama.init() # Initialize colorama

    ### Find the Git repository
    bugs = Bugs('.')

    # TODO: This is a test bug
    try:
        ### Perform b update
        if sys.argv[1] == 'update':
            bugs.update()
        else:
            print('fatal: command not understood')
            return 1
    except IndexError:
        bugs.printBugs()
    return 0

if __name__ == '__main__':
    main()

##############################################################################
