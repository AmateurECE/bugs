#!/usr/bin/env python3
###############################################################################
# NAME:             GitRepository.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:      
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

import os

from IRepository import IRepository
from RepositoryExceptions import NotAValidRepositoryException

class GitRepository(IRepository):
    """
    Concrete implementation of the IRepository abstract class representing
    Git repositories.
    """
    def __init__(self, path):
        super()
        for name in os.listdir(path):
            if name == '.git':
                self.path = os.path.abspath(path)
                return
        raise NotAValidRepositoryException()

###############################################################################
