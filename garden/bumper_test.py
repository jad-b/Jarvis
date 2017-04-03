#!/usr/bin/env python3
import io
import tempfile
import unittest
from collections import namedtuple


test_data = '''
this is not an important line.

The version is listed below.
[version]
thing=3.1.12
node["thing"]["version"] = 3.1.12

my:
  thing:
    version: 3.1.12
  thing2:
    version: 0.11.23
  dev:
    version: 0.11.23-14-a2c4e6
'''


class TestCLI(unittest.TestCase):

    def temp_file(self):
        tf = tempfile.NamedTemporaryFile(mode='r+')
        tf.write(test_data)
        self.addCleanup(tf.close)  # Defer file cleanup
        return tf

    def string_file(self):
        return io.StringIO().write(test_data)

    def test_cli(self):
        cli_template = "bump.py {filename} {pattern} {new_version}"
        TestCase = namedtuple("TestCase", ['pattern', 'new_version'])
        test_cases = (
            TestCase("'^thing=(?P<version>(\d+\.?){3})$'", '11.22.33'),
            TestCase("'^thing=(\d+\.?){3}$'", '11.22.33'),
            # multiline match
            TestCase("thing:\s*\n\s*version:(\d+\.?){3}", '2.34.567'),
        )
        for case in test_cases:
            tf = self.temp_file()
            cli_str = cli_template.format(
                filename=tf.name,
                pattern=case.pattern,
                new_version=case.new_version
            )
            print("Testing", cli_str)
