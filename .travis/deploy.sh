#!/bin/bash
choco install python --version 3.8.5
pip install --upgrade pip setuptools twine wheel
choco install make
make release
