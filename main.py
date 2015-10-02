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
EP_TOOLS = '{}.tools'.format(ENTRYPOINT)
EP_FUNCS = (
    'bump',
)


def main():
    # TODO Aggregate ArgumentParsers from loaded entrypoint modules.
    logger.info('Running Garden')
    tools = load_tools()
    repos = load_repos()


def load_tools():
    """Load Garden interfaces/libraries."""
    tools = {}
    logger.debug('Loading interfaces')
    for ep in iter_entry_points(EP_TOOLS):
        logger.debug('\t%s', ep)
        tools[ep.name] = ep.load()
    return tools


def load_repos():
    """Load plugins registered under the Garden entrypoint."""
    registry = defaultdict(list)
    for func in EP_FUNCS:
        ep_group = '.'.join((ENTRYPOINT, func))
        logger.debug('Loading entrypoints for %s', ep_group)
        for ep in iter_entry_points(ep_group):
            logger.debug('Loaded entrypoint: %s', ep)
            registry[func] = ep
    return registry


def parse_cli(tools):
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers()
    for name, code in tools:
        # Create sub-command for tool
        tool_parser = subp.add_parser(name)
        # Have that tool's module set CLI arguments
        tools[name].add_parser(tool_parser)


if __name__ == '__main__':
    main()
