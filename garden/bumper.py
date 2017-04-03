#!/bin/python3
"""
bumper
======

Version bumping interface.

Allows bumping by specified version and SemVer semantics.
"""
from abc import ABCMeta, abstractmethod
from garden.log import logger
import argparse
import enum
import re


_logger = logger


#: Regex for matching version numbers
RE_VERSION = '(?P<version>(?:\d+\.?){3})'
_version_help = ('Either a Semantic Version alias (patch, minor, major), or a'
                 ' specified version, like x.y.z')


class SemVer(enum.Enum):
    patch = 'patch'
    minor = 'minor'
    major = 'major'


def snr(line_gen, pattern, version):
    """Search & replace a pattern from a stream of strings.

    The first capture group will be replaced with the given version.
    """
    p = re.compile(pattern, re.MULTILINE)

    line = next(line_gen, False)
    while line:
        yield eager_replace(p, version, line)
        line = next(line_gen, False)


def eager_replace(pattern, repl, line):
    m = re.match(pattern, line)
    if m:
        line = re.sub(m.groups[1], repl, line)
    return line


class Bumper(metaclass=ABCMeta):

    @abstractmethod
    def bump(self, target, version=SemVer.patch, **kwargs):
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


def bump_version(version, new_version=SemVer.patch):
    """Changes the version by the given semantic versioning new_version, or specific
    version."""
    if re.match(RE_VERSION, version):
        return new_version

    x = split_version()
    if new_version == SemVer.patch:
        x[2] += 1
    elif new_version == SemVer.minor:
        x[2] = 0
        x[1] += 1
    elif new_version == SemVer.major:
        x[1], x[2] = 0, 0
        x[0] += 1
    else:
        _logger.warning('No semver match')
        return version
    return '.'.join(list(map(str, x)))


def to_version(arg):
    """Converts 'arg' to a SemVer value of 'x.y.z' string."""
    try:
        return SemVer(arg)
    except ValueError:
        if re.match(RE_VERSION, arg):
            return arg
        else:
            raise argparse.ArgumentError(_version_help)


def split_version(version):
    return list(map(int, version.split('.')))


def setup_parser(argparser, repos):
    """Attach arguments to the given argparser."""
    def do_bump(args):
        _logger.debug('Calling bump on %s', args.repo)
        try:
            # Load the entrypoint code
            repos['bump'][args.repo].load()
            # Call registered 'bump' method on target repo
            repos[args.repo](args.target, args.version, *args.args)
        except KeyError:
            _logger.warning("No repo called '%s' found", args.repo)

    argparser.add_argument('repo')
    argparser.add_argument('target', type=str)
    argparser.add_argument('version', type=to_version, help=_version_help)
    argparser.add_argument('args', nargs=argparse.REMAINDER,
                           help='Addtional arguments to pass through')
    argparser.set_defaults(func=do_bump)
    _logger.debug('Setup bump() parsing')
