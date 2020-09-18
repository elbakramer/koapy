#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click==7.1.2',
    'PyQt5==5.15.0',
    'grpcio==1.32.0',
    'grpcio-tools==1.32.0',
    'protobuf==3.13.0',
    'pyhocon==0.3.55',
    'mslex==0.1.1',
    'discord.py==1.4.1',
    'schedule==0.6.0',
    'tabulate==0.8.7',
    'pywin32==228;sys_platform=="win32"',
    'mslex==0.1.1;sys_platform=="win32"',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Yunseong Hwang",
    author_email='kika1492@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
    license="MIT license",
    long_description=readme + '\n\n' + history,
    package_data={
        'koapy': [
            'config.conf',
            'openapi/data/fid.xlsx',
            'openapi/data/realtype_by_desc.json',
            'openapi/data/trinfo_by_code.json',
        ]
    },
    include_package_data=True,
    keywords='koapy',
    name='koapy',
    packages=find_packages(include=['koapy', 'koapy.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/elbakramer/koapy',
    version='0.1.2',
    zip_safe=False,
)
