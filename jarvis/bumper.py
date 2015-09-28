#!/bin/python3
"""
bumper
======

Version bumping interface.

Allows bumping by specified version and SemVer semantics.
"""
from abc import ABCMeta
import enum


class SemVer(enum.Enum):
    patch = 'patch'
    minor = 'minor'
    major = 'major'


class Bumper(metaclass=ABCMeta):

    @abstractmethodd
    def bump(self, target, semver=None, **kwargs):
        """Increments the target version with the code base.

        It is up to the implementation to define valid targets.

        :arg str target: Name of target within code.
        :kwarg `SemVer` semver: Semantic version level to version bump by.
        """
        pass


    @classmethod
    def __subclasshook__(cls, C):
        # If comparing *against* Bumper
        if cls is Bumper:
            if any("bump" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented



def semver_bump(version, level=Semver.patch.name):
    x = list(map(int, version.split('.')))
    if level == Semver.patch.name:
        x[2] += 1
    elif level == Semver.minor.name:
        x[2] = 0
        x[1] += 1
    elif level == Semver.major.name:
        x[1], x[2] = 0, 0
        x[0] += 1
    else:
        _logger.warning('No semver match')
        return version
    return '.'.join(list(map(str, x)))


