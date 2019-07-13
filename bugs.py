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

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
import os
import sys
import re
from glob import glob

from t import t
from colorama import colorama
from colorama.colorama import Fore, Style

###############################################################################
# Class BugTracker
###

# TODO: Make filenames optional
# TODO: Optionally print line numbers for comments
# TODO: Optionally print only filename instead of full path.

class BugTracker:
    """Controls the logic concerning the usage of the Bugs class."""

    def __init__(self, args, bugs):
        self.args = vars(self.parseArgs(args))
        self.bugs = bugs

    @staticmethod
    def parseArgs(args):
        """Parse 'args' as a list of command line arguments."""
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest='function',
                                           help='help for subcommand')
        updateParser = subparsers.add_parser('update',
                                             help=('Update the list of bugs '
                                                   'for this repository'),
                                             formatter_class=
                                             RawTextHelpFormatter)
        updateParser.add_argument("--path", "-p", type=str,
                                  help=('Select the format of the file path '
                                        'in the output file:\n'
                                        '  * long:  Show full path\n'
                                        '  * short: Show only file name\n'
                                        '  * none:  Do not show the filename'))
        updateParser.add_argument("-l", "--line-numbers", action="store_true",
                                  default=False, help=('Show line numbers in '
                                                       'the output. Only '
                                                       'valid if --path is not'
                                                       ' none'))
        subparsers.add_parser('print', help=('Print the list of bugs for this'
                                             ' repository'))
        return parser.parse_args(args)

    def run(self):
        """Perform the function of the program."""
        if self.args['function'] == 'update':
            self.bugs.update()
        elif self.args['function'] == 'print':
            self.bugs.printBugs()
        else:
            print('fatal: command not understood')
            return 1
        return 0

###############################################################################
# Class Bugs
###

class Bugs:
    """Contains the logic of the `b' tool."""

    # Static class members
    # Matches C/C++ and Bash style comments
    todoRegex = r'(;;|%|#|/(\*|/))\s*TODO:\s*(.*)'
    r_todo = re.compile(todoRegex)

    def __init__(self, pwd):
        # Locate the root of the git repository, or if we aren't in one.
        self.gitDir = self.findRepositoryRoot(pwd)
        self.bugDict = None

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
                return str(pwd)
            pwd = Path(os.fspath(pwd) + '/..')
            gitHere = Path(os.fspath(pwd) + '/.git')
        return None

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

    def buildFileList(self):
        """INTERNAL. Builds the list of files to search for TODO comments."""
        # Automatically ignore .git/ and bugs
        rejectFilenames = ['.git/', '~']
        rejectRegexes = []
        # Read .bignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.gitDir + '/.bignore')
                             or [])
        # Read .gitignore file, if it exists
        rejectRegexes.extend(self.readIgnoreFile(self.gitDir + '/.gitignore')
                             or [])

        # Expand shell-style globs in rejectRegexes
        for regex in rejectRegexes:
            if '*' in regex:
                rejectFilenames.extend(glob('./**/' + regex, recursive=True))
            else:
                rejectFilenames.append(regex)

        # Walk the repository
        validPaths = list()
        for filename in glob('./**/*', recursive=True):
            invalid = False
            for regex in rejectFilenames:
                if regex in filename or regex == filename \
                   or Path(filename).is_dir():
                    invalid = True
            if not invalid:
                validPaths.append(filename)
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
        self.bugDict.print_list(quiet=True)

###############################################################################
# MAIN
###

def main():
    """Run bugs"""
    colorama.init() # Initialize colorama

    # TODO: bugs.py uses parent repo's .bignore when repo is submodule
    # TODO: Determine the config
    #       based on the format of the strings in the previous file (if exists)
    #       then overwrite with any flags.

    ### Find the Git repository
    bugTracker = BugTracker(sys.argv[1:], Bugs('.'))
    return bugTracker.run()

if __name__ == '__main__':
    main()

##############################################################################
