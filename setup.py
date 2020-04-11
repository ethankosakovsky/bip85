#!/usr/bin/env python
import os
from setuptools import setup, find_packages

CWD = os.path.dirname(os.path.realpath(__file__))


def read(*path):
    filename = os.path.join(CWD, *path)
    with open(filename, "r") as f:
        return f.read()


setup(
    packages=find_packages(),
    name="bipentropy",
    version="0.1",
    author="Ethan Kosakovsky",
    author_email="ethankosakovsky@protonmail.com",
    description="Implementation of Bitcoin BIP Entropy",
    long_description=read("README.md"),
    url="https://github.com/ethankosakovsky/bipentropy",
    install_requires=["mnemonic", "base58", "pycoin"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
