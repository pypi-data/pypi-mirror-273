#!/usr/bin/env python
import os
import sys
from codecs import open
import setuptools

from setuptools import setup
from setuptools.command.test import test as TestCommand

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Requests requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.

If you can't upgrade your Python version, you'll need to
pin to an older version of Requests (<2.32.0).
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count

            self.pytest_args = ["-n", str(cpu_count()), "--boxed"]
        except (ImportError, NotImplementedError):
            self.pytest_args = ["-n", "1", "--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

requires = [
    "charset_normalizer>=2,<4",
    "idna>=2.5,<4",
    "urllib3>=1.21.1,<3",
    "certifi>=2017.4.17",
]
test_requirements = [
    "pytest-httpbin==2.0.0",
    "pytest-cov",
    "pytest-mock",
    "pytest-xdist",
    "PySocks>=1.5.6, !=1.5.7",
    "pytest>=3",
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open("src/__version__.py", "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    url="https://github.com/git-mehedi/dxh_test_package",
    license=about["__license__"],
    keywords=about["__keywords__"],
    packages=setuptools.find_packages(".", exclude=["*.tests"]),
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    project_urls={"Source": "https://github.com/git-mehedi/dxh_test_package"},
)