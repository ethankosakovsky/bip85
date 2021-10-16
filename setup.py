#!/usr/bin/env python
import setuptools

with open("README.md", "rt") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bip85",
    version="0.2.0",
    license="MIT",
    author="Ethan Kosakovsky",
    author_email="ethankosakovsky@protonmail.com",
    description="Implementation of Bitcoin BIP 85",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethankosakovsky/bip85",
    packages=setuptools.find_packages(),
    keywords=['BIP85', 'entropy', 'bitcoin'],
    install_requires=[
        "mnemonic~=0.19",
        "pycoin~=0.90",
        "base58~=2.1",
        "monero~=0.8",
        "pycryptodome~=3.10",
    ],
    extras_require={"dev": ["pytest~=6.2", "pip-tools~=6.4"]},
    tests_require=["pytest~=6.2"],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    entry_points={
        "console_scripts": ["bip85-cli=bip85.cli:main"],
    },
)
