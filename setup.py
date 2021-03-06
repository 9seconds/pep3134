#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from setuptools.command.test import test


REQUIREMENTS = []


with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


# copypasted from http://pytest.org/latest/goodpractises.html
class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = None  # pylint: disable=W0201

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []  # pylint: disable=W0201
        self.test_suite = True  # pylint: disable=W0201

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="pep3134",
    description="Backport of PEP 3134 (with PEP 415 and PEP 409) "
                "to Python 2 as close as possible",
    long_description="",
    version="0.1.4",
    author="Sergey Arkhipov",
    license="MIT",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    maintainer_email="serge@aerialsounds.org",
    url="https://github.com/9seconds/pep3134/",
    install_requires=REQUIREMENTS,
    tests_require=["pytest==2.6.1"],
    packages=find_packages(),
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    zip_safe=False
)
