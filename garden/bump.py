#!/bin/python3
"""
bumper
======

Version bumping interface.

Allows bumping by specified version and SemVer semantics.
"""
from abc import ABCMeta
import enum


#: Regex for matching version numbers
RE_VERSION = '(?P<version>(?:\d+\.?){3})'


class SemVer(enum.Enum):
    patch = 'patch'
    minor = 'minor'
    major = 'major'


class Bumper(metaclass=ABCMeta):

    @abstractmethod
    def bump(self, target, version=SemVer.Patch, **kwargs):
        """Increments the target version with the code base.

        It is up to the implementation to define valid targets.

        :arg str target: Name of target within code.
        :kwarg `SemVer` semver: Semantic version level to version bump by.
        """
        return

    @property
    @abstractmethod
    def targets(self):
        """Returns a list of targets available for bumping."""
        return

    @classmethod
    def __subclasshook__(cls, C):
        # If comparing *against* Bumper
        if cls is Bumper:
            if any("bump" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented



def bump_version(version, new_version=Semver.patch):
    """Changes the version by the given semantic versioning new_version, or specific
    version."""
    if re.match(RE_VERSION, version):
        return new_version

    x = split_version()
    elif new_version == Semver.patch:
        x[2] += 1
    elif new_version == Semver.minor:
        x[2] = 0
        x[1] += 1
    elif new_version == Semver.major:
        x[1], x[2] = 0, 0
        x[0] += 1
    else:
        _logger.warning('No semver match')
        return version
    return '.'.join(list(map(str, x)))


def split_version(version):
    return list(map(int, version.split('.')))
