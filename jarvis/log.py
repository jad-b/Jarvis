#!/bin/python3
"""
log
===

Central Jarvis logger.
"""
import logging
import sys

# TODO make configurable via CLI
LOG_LEVEL = logging.DEBUG

logger = logging.getLogger('bump')

logger.setLevel(LOG_LEVEL)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(LOG_LEVEL)
logger.addHandler(sh)
