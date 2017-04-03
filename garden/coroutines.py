"""
couroutines
===========
Implements the file reading, modifying, and writing procedures as coroutines.

Example
>>>  open('hello world.txt') as f:
...      stream(snr(sink(io.String()), 'hello', 'goodbye cruel'), f)
"""
import re

from garden.bumper import eager_replace


def stream(target, filepath):
    with open(filepath) as f:
        for line in f:
            target.send(f)
        target.close()


def snr(target, pattern, repl):
    p = re.compile(pattern, re.MULTILINE)
    while True:
        line = (yield)
        target.send(eager_replace(p, repl, line))


def sink(fileio, newline=True):
    eol = '\n' if newline else ''
    while True:
        line = (yield)
        fileio.write(line + eol)
