#!/usr/bin/env python3
"""
main
====

Entrypoint into Garden.

Aggregates loaded modules and provides an aggregated CLI.
"""
from collections import defaultdict
from pkginfo import Installed
from pkg_resources import iter_entry_points

from garden.log import logger


ENTRYPOINT = 'garden'
EP_FUNCS = (
    'bump',
)


def main():
    # TODO Aggregate ArgumentParsers from loaded entrypoint modules.
    logger.info('Running Garden')
    load_entrypoints()


def load_entrypoints():
    """Load plugins registered under the Garden entrypoint."""
    registry = defaultdict(list)
    for func in EP_FUNCS:
        logger.debug('Loading entrypoints for %s', func)
        for ep in iter_entry_points('.'.join((ENTRYPOINT, func))):
            logger.debug('Loaded entrypoint: %s', ep)
            registry[func] = ep
    return registry


if __name__ == '__main__':
    main()
