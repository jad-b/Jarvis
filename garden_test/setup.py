import subprocess
import os
from setuptools import setup, find_packages


def readme():
    with open('README.md') as _file:
        return _file.read()


def requirements():
    reqs_file = 'reqs.txt'
    if os.path.isfile(reqs_file):
        with open('reqs.txt') as reqs:
            return [line.strip() for line in reqs
                    if line and not line.startswith('#')]
    return []

def latest_git_tag():
    try:
        tag = subprocess.check_output(
            ['git', 'describe', '--abbrev=0', '--tags']
        ).decode().rstrip()
    except subprocess.CalledProcessError:
        return '0.0.0'
    return tag


setup(
    name='garden_test',
    version=latest_git_tag(),
    long_description=readme(),
    description='Python package for testing garden',
    author='Jeremy Dobbins-Bucklad',
    author_email='j.american.db@gmail.com',
    url='https://github.com/jad-b/garden',
    install_requires=requirements(),
    packages = find_packages(),
    package_dir = {'garden': 'garden_test'},
    py_modules=['testfile'],
    entry_points={
        'garden.bump': ['garden_test = garden_test.bump:Bumper.bump'],
    },
    zip_safe=False,
    include_package_data=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ),
)
