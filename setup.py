#!/usr/bin/env python

"""The setup script."""

from __future__ import annotations

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "click>=8.1.2",
    "cryptography>=36.0.2",
    "deprecated>=1.2.13",
    "discord.py>=1.7.3",
    "exchange-calendars>=3.6.1",
    "grpcio>=1.44.0",
    "grpcio-tools>=1.44.0",
    "lxml>=4.8.0",
    "numpy>=1.22.3",
    "openpyxl>=3.0.9",
    "pandas>=1.4.2",
    "protobuf>=3.20.0",
    "psutil>=5.9.0",
    "pygtrie>=2.4.2",
    "pyhocon>=0.3.59",
    "PySide2>=5.15.2.1",
    "pytz>=2022.1",
    "QtPy>=2.0.1",
    "requests>=2.27.1",
    "Rx>=3.2.0",
    "schedule>=1.1.0",
    "Send2Trash>=1.8.0",
    "SQLAlchemy>=1.4.35",
    "tabulate>=0.8.9",
    "tqdm>=4.64.0",
    "tzlocal>=4.2",
    "wrapt>=1.14.0",
    "pywin32>=303;sys_platform=='win32'",
    "pywinauto>=0.6.8;sys_platform=='win32'",
    "windows-curses>=2.3.0;sys_platform=='win32'",
    "typing-extensions>=4.1.1;python_version<'3.10'",
]

requirements_dev = [
    "actions-toolkit>=0.1.13",
    "black>=22.3.0",
    "bump2version>=1.0.1",
    "codecov>=2.1.12",
    "coverage>=6.3.2",
    "dunamai>=1.11.1",
    "flake8>=4.0.1",
    "isort>=5.10.1",
    "mypy>=0.942",
    "pip-tools>=6.6.0",
    "pre-commit>=2.18.1",
    "pylint>=2.13.5",
    "pytest>=7.1.1",
    "pytest-cov>=3.0.0",
    "pytest-xdist>=2.5.0",
    "pyupgrade>=2.32.0",
    "astunparse>=1.6.3;python_version<'3.9'",
]

requirements_doc = [
    "Sphinx>=4.5.0",
    "sphinx-autoapi>=1.8.4",
    "nbconvert>=6.5.0",
    "nbsphinx>=0.8.8",
    "ipython>=8.2.0",
]

requirements_dev += requirements_doc

setup(
    author="Yunseong Hwang",
    author_email="kika1492@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Natural Language :: Korean",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Office/Business :: Financial",
    ],
    description="Kiwoom Open Api Plus Python",
    entry_points={"console_scripts": ["koapy=koapy.cli:main"]},
    setup_requires=["setuptools-git"],
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "doc": requirements_doc,
    },
    license="MIT OR Apache-2.0 OR GPL-3.0-or-later",
    long_description=readme + "\n\n" + history,
    name="koapy",
    packages=find_packages(include=["koapy", "koapy.*"]),
    include_package_data=True,
    test_suite="tests",
    url="https://github.com/elbakramer/koapy",
    version="0.8.1",
    zip_safe=False,
)
