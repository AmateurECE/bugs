#!/usr/bin/env python3
###############################################################################
# NAME:             IRepository.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

from abc import ABC, abstractmethod

#pylint: disable=unnecessary-pass,too-few-public-methods,non-parent-init-called

class IRepository(ABC):
    """
    This class is used to represent a version control repository. If the path
    passed to the constructor is not the root directory of a valid repository,
    the constructor will throw a NotAValidRepositoryException.
    """
    def __init__(self, path):
        super.__init__()
        pass

###############################################################################
