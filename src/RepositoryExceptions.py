#!/usr/bin/env python3
###############################################################################
# NAME:             RepositoryExceptions.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

class NotAValidRepositoryException(Exception):
    """
    This exception is thrown when construction of an implementation of
    IRepository is attempted using a directory that is not the root of a valid
    Repository.
    """
    pass

###############################################################################
