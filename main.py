#!/usr/bin/env python3
"""
main
====

Entrypoint into Jarvis.

Aggregates loaded modules and provides an aggregated CLI.
"""
from pkginfo import Installed
from pkg_resources import iter_entry_points

from jarvis.log import logger


def main():
    # TODO Aggregate ArgumentParsers from loaded entrypoint modules.
    logger.info('Running Jarvis')
    pass


def load_entrypoints(self):
    """Load plugins registered under the Jarvis entrypoint."""
    for ep in iter_entry_points:
        logger.debug('Loaded entrypoint: %s', ep)


if __name__ == '__main__':
    main()
