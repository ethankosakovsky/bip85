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
    name="bip85",
    version="0.1",
    author="Ethan Kosakovsky",
    author_email="ethankosakovsky@protonmail.com",
    description="Implementation of Bitcoin BIP 85",
    long_description=read("README.md"),
    url="https://github.com/ethankosakovsky/bip85",
    download_url="https://github.com/ethankosakovsky/bip85/archive/0.1.tar.gz",
    install_requires=["mnemonic", "pycoin", "base58", "pytest"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
    ],
)
