#!/usr/bin/env python3
"""
main
====

Entrypoint into Garden.

Aggregates loaded modules and provides an aggregated CLI.
"""
import argparse
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
    logger.info('Running Garden')
    tools = load_tools()
    repos = load_repos()
    print(repos)
    parser = parse_cli(tools, repos)
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_usage()


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
    registry = {}
    for func in EP_FUNCS:
        ep_group = '.'.join((ENTRYPOINT, func))
        logger.debug('Loading entrypoints for %s', ep_group)
        for ep in iter_entry_points(ep_group):
            logger.debug('Loaded entrypoint: %s', ep)
            registry[func] = {ep.name: ep}
    return registry


def parse_cli(tools, repos):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for tool_name, fn in tools.items():
        # Create sub-command for tool
        tool_parser = subparsers.add_parser(tool_name)
        ### Delegate:
        # Have that tool's module set CLI arguments & default action
        fn.setup_parser(tool_parser, repos)
    return parser


if __name__ == '__main__':
    main()
