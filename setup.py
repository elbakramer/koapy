#!/usr/bin/env python

"""The setup script."""

from __future__ import annotations

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "click>=8.0.3",
    "cryptography>=36.0.1",
    "deprecated>=1.2.13",
    "discord.py>=1.7.3",
    "exchange-calendars>=3.5.1",
    "grpcio>=1.43.0",
    "grpcio-tools>=1.43.0",
    "lxml>=4.7.1",
    "numpy>=1.22.1",
    "openpyxl>=3.0.9",
    "pandas>=1.4.0",
    "protobuf>=3.19.4",
    "psutil>=5.9.0",
    "pygtrie>=2.4.2",
    "pyhocon>=0.3.59",
    "PySide2>=5.15.2",
    "pytz>=2021.3",
    "QtPy>=2.0.1",
    "requests>=2.27.1",
    "Rx>=3.2.0",
    "schedule>=1.1.0",
    "Send2Trash>=1.8.0",
    "SQLAlchemy>=1.4.31",
    "tabulate>=0.8.9",
    "tqdm>=4.62.3",
    "tzlocal>=4.1",
    "wrapt>=1.13.3",
    "pywin32>=303;sys_platform=='win32'",
    "pywinauto>=0.6.8;sys_platform=='win32'",
    "windows-curses>=2.3.0;sys_platform=='win32'",
    "typing-extensions>=4.0.1;python_version<'3.10'",
]

requirements_dev = [
    "actions-toolkit>=0.1.12",
    "black>=22.1.0",
    "bump2version>=1.0.1",
    "codecov>=2.1.12",
    "coverage>=6.3.1",
    "dunamai>=1.8.0",
    "flake8>=4.0.1",
    "isort>=5.10.1",
    "mypy>=0.931",
    "pip-tools>=6.4.0",
    "pre-commit>=2.17.0",
    "pylint>=2.12.2",
    "pytest>=6.2.5",
    "pytest-cov>=3.0.0",
    "pytest-xdist>=2.5.0",
    "pyupgrade>=2.31.0",
    "astunparse>=1.6.3;python_version<'3.9'",
]

requirements_doc = [
    "Sphinx>=4.4.0",
    "sphinx-autoapi>=1.8.4",
    "nbconvert>=6.4.1",
    "nbsphinx>=0.8.8",
    "ipython>=8.0.1",
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
    version="0.8.0",
    zip_safe=False,
)
