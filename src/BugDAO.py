#!/usr/bin/env python3
###############################################################################
# NAME:             BugDAO.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      DAO object for persisting Bugs. Bug is an ethereal type,
#                   not actually implemented in logic.
#
# CREATED:          07/14/2019
#
# LAST EDITED:      07/15/2019
###

###############################################################################
# Class BugDAO
###

class BugDAO:
    """Data Access Object for the 'Bug' class."""

    def __init__(self, filename):
        """Initialize a BugDAO"""
        self.filename = filename
        self.config = dict()
        self.bugs = self.readBugFile()

    def addBug(self, bug):
        """Add a bug to the bug list."""
        self.bugs.append(bug)

    def parseConfig(self, string):
        """Parse string to obtain the config for this DAO."""
        for pair in string[2].split(' '):
            key, value = pair.split('=')
            self.config[key] = value

    def makeDefaultConfig(self):
        """Set the current object up to have the default config."""
        self.config['filenames']

    def serializeConfig(self):
        """Create a string using the config of this DAO."""
        string = ''
        for key in self.config:
            string += key + '=' + self.config[key]
        return string

    def readBugFile(self):
        """
        Read the bugs file with the name corresponding to the filename that
        this object was instantiated with.
        """
        with open(self.filename, 'r') as inputFile:
            lines = inputFile.readlines()
            if lines[0][0] != '#':
                raise ValueError('The provided filename does not correspond '
                                 'to a valid bugs file')
            self.parseConfig(lines[0])
            return lines[1:]

    def printBugs(self, outputFile):
        """Print the list of bugs to outputFile."""
        for line in self.bugs:
            print(line, file=outputFile)

    def write(self):
        """Write the list of bugs to this BugDAO's file."""
        with open(self.filename, 'w') as outputFile:
            outputFile.write('# ' + self.serializeConfig())
            self.printBugs(outputFile)

###############################################################################
