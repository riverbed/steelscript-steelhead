# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import print_function, division

import sys
import itertools

from setuptools.command.test import test as TestCommand
from gitpy_versioning import get_version

from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main("%s tests" % " ".join(self.test_args))
        sys.exit(errno)

readme = open('README.rst').read()

test = ['pytest', 'testfixtures', 'mock']

doc = ['sphinx']

setup(
    name='steelscript.steelhead',
    namespace_packages=['steelscript'],
    version=get_version(),
    description='Python modules for interacting with Riverbed SteelHead with SteelScript',
    long_description=readme,
    author='Riverbed Technology',
    author_email='eng-github@riverbed.com',
    packages=find_packages(exclude=('gitpy_versioning',)),
    include_package_data=True,
    install_requires=['steelscript.cmdline'],
    extras_require={'test': test,
                    'doc': doc,
                    'dev': [p for p in itertools.chain(test, doc)],
                    'all': []
                    },
    tests_require = test,
    keywords='steelscript.steelhead',
    cmdclass = {'test': PyTest},
)
