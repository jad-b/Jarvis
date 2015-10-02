#!/bin/python3
"""
log
===

Central Garden logger.
"""
import logging
import sys

# TODO make configurable via CLI
LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('garden')

logger.setLevel(LOG_LEVEL)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(LOG_LEVEL)
logger.addHandler(sh)
