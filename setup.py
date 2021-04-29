#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.1.2",
    "discord.py>=1.7.1",
    "exchange_calendars>=3.0.2",
    "grpcio>=1.37.0",
    "grpcio-tools>=1.37.0",
    "korean_lunar_calendar>=0.2.1",
    "numpy>=1.20.2",
    "openpyxl>=3.0.7",
    "pandas>=1.2.4",
    "protobuf>=3.15.8",
    "pyhocon>=0.3.57",
    "PySide2>=5.15.2",
    "pytz>=2021.1",
    "qtpy>=1.9.0",
    "requests>=2.25.1",
    "Rx>=3.2.0",
    "schedule>=1.1.0",
    "Send2Trash>=1.5.0",
    "SQLAlchemy>=1.4.11",
    "tabulate>=0.8.9",
    "tqdm>=4.60.0",
    "tzlocal>=2.1",
    "wrapt>=1.12.1",
    'pywin32>=300;sys_platform=="win32"',
    'pywinauto>=0.6.8;sys_platform=="win32"',
]

requirements_extras = {
    "backtrader": [
        "backtrader>=1.9.76.123",
        "matplotlib>=3.4.1",
    ],
    "PyQt5": [
        "PyQt5>=5.15.4",
    ],
}

setup(
    author="Yunseong Hwang",
    author_email="kika1492@gmail.com",
    python_requires=">=3.7.1",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Natural Language :: Korean",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Office/Business :: Financial",
    ],
    description="Kiwoom Open Api Plus Python",
    entry_points={
        "console_scripts": [
            "koapy=koapy.cli:cli",
        ],
    },
    install_requires=requirements,
    extras_require=requirements_extras,
    license="MIT OR Apache-2.0 OR GPL-3.0-or-later",
    long_description=readme + "\n\n" + history,
    package_data={
        "koapy": [
            "backend/daishin_cybos_plus/proxy/CybosPlusProxyService.proto",
            "backend/kiwoom_open_api_plus/data/fid.xlsx",
            "backend/kiwoom_open_api_plus/data/realtype_by_desc.json",
            "backend/kiwoom_open_api_plus/data/trinfo_by_code.json",
            "backend/kiwoom_open_api_plus/grpc/KiwoomOpenApiPlusService.proto",
            "config.conf",
        ]
    },
    include_package_data=True,
    keywords="koapy",
    name="koapy",
    packages=find_packages(include=["koapy", "koapy.*"]),
    test_suite="tests",
    url="https://github.com/elbakramer/koapy",
    version="0.3.5",
    zip_safe=False,
)
