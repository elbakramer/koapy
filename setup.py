#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.1.2',
    'PySide2>=5.15.1',
    'grpcio>=1.32.0',
    'grpcio-tools>=1.32.0',
    'protobuf>=3.13.0',
    'pyhocon>=0.3.55',
    'discord.py>=1.5.0',
    'schedule>=0.6.0',
    'tabulate>=0.8.7',
    'tqdm>=4.50.2',
    'wrapt>=1.12.1',
    'numpy>=1.19.2',
    'pandas>=1.1.3',
    'xlrd>=1.2.0',
    'SQLAlchemy>=1.3.20',
    'Send2Trash>=1.5.0',
    'pendulum>=2.1.2',
    'pytz>=2020.1',
    'tzlocal>=2.1',
    'rx>=3.1.1',
    'trading-calendars>=2.0.0',
    'korean_lunar_calendar>=0.2.1',
    'pywin32>=228;sys_platform=="win32"',
    'pywinauto>=0.6.8;sys_platform=="win32"',
]

requirements_extras = {
    'backtrader': [
        'backtrader>=1.9.76.123',
        'matplotlib<=3.2.2',
    ],
    'PyQt5': [
        'PyQt5>=5.15.1',
    ],
}

setup(
    author="Yunseong Hwang",
    author_email='kika1492@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Natural Language :: Korean',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Office/Business :: Financial',
    ],
    description="Kiwoom Open Api Python",
    entry_points={
        'console_scripts': [
            'koapy=koapy.cli:cli',
        ],
    },
    install_requires=requirements,
    extras_require=requirements_extras,
    license="MIT OR Apache-2.0 OR GPL-3.0-or-later",
    long_description=readme + '\n\n' + history,
    package_data={
        'koapy': [
            'grpc/KiwoomOpenApiService.proto',
            'openapi/data/fid.xlsx',
            'openapi/data/realtype_by_desc.json',
            'openapi/data/trinfo_by_code.json',
            'openapi/data/dispatch_signatures_by_name.pkl',
            'openapi/data/event_signatures_by_name.pkl',
            'utils/krx/data/holiday.json',
            'config.conf',
        ]
    },
    include_package_data=True,
    keywords='koapy',
    name='koapy',
    packages=find_packages(include=['koapy', 'koapy.*']),
    test_suite='tests',
    url='https://github.com/elbakramer/koapy',
    version='0.1.14',
    zip_safe=False,
)
