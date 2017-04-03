#!/bin/python3
"""
bump
====

Valid targets:

"""
import os
from garden import bumper, log

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Bumper(bumper.Bumper):
    _logger = log.logger
    __dev_envs = ('dev', 'int', 'staging', 'prod')
    __targets = {
        'testfile': 'testfile.py',
    }

    @classmethod
    def bump(self, target, version, *args):
        """Bump updates the target version in the code."""
        _logger.debug('Bumping %s => %s', target, version)
        if target == 'testfile':
            _bump_testfile(self, version)
        else:
            _logger.error('%s is an invalid target', target)

    @property
    def targets(self):
        """Returns a list of valid versioning bumping targets."""
        return __targets.keys()

    def _bump_testfile(self, version):
        # Retrieve current value
        # Update
        # Write to file
        _logger.debug("Bumping version in %s to %s",
                self.__targets['testfile'][env], version)
