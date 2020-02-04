#!/usr/bin/env python3
###############################################################################
# NAME:             RepositoryFactory.py
#
# AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
#
# DESCRIPTION:
#
# CREATED:          07/18/2019
#
# LAST EDITED:      07/18/2019
###

from RepositoryExceptions import NotAValidRepositoryException

from GitRepository import GitRepository
# TODO: Add support for SVN repositories.
# from SvnRepository import SvnRepository

#pylint: disable=too-few-public-methods

class RepositoryFactory():
    """Constructs a concrete Repository object from path and returns it."""
    def __init__(self):
        pass

    @staticmethod
    def getRepository(path):
        """
        A factory method using Chain-Of-Command pattern to construct a
        repository object. It's annoying that this method is so closely coupled
        to each implementation of IRepository, but this developer feels like
        its unavoidable here.
        """
        try:
            return GitRepository(path)
        except NotAValidRepositoryException:
            raise # pass (added with support for SVN)
        # try:
        #     return SvnRepository(path)
        # except NotAValidRepositoryException as e:
        #     raise

###############################################################################
