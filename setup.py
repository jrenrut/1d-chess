#!/usr/bin/env python

from distutils.core import setup

setup(
    name="onedchess",
    version="0.0",
    description="Flexible One Dimensional Chess Implementation",
    author="Jeremy Turner",
    url="https://github.com/jrenrut/1d-chess",
    packages=["distutils", "pre-commit", "black", "flake8", "isort"],
)
