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
    install_requires=["mnemonic", "pycoin", "base58", "monero", "pycryptodome"],
    tests_require=["pytest"],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    entry_points = {
        "console_scripts": ["bip85-cli=bip85.cli:main"],
    },
)
