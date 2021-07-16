#!/usr/bin/env python
"""The setup script"""
import os
import re
import sys

from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Klaas Schoute",
    author_email="hello@student-techlife.com",
    classifiers=[
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Asynchronous Python client for getting forecast solar information",
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.0.0",
        "aiodns>=3.0.0",
        'backports.zoneinfo;python_version<"3.9"',
    ],
    keywords=["forecast", "solar", "power", "energy", "api", "async", "client"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="forecast_solar",
    packages=find_packages(include=["forecast_solar"]),
    url="https://github.com/klaasnicolaas/forecast_solar",
    version=os.environ.get("PACKAGE_VERSION"),
    zip_safe=False,
)
