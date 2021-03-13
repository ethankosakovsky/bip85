#!/usr/bin/env python
#
# Copyright (c) 2020 Ethan Kosakovsky <ethankosakovsky@protonmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from bip85 import BIP85
from bip85 import BIP85DRNG
from Crypto.PublicKey import RSA
import pytest
import hashlib


XPRV = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
MNEMONIC = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'


def test_rsa():
    bip85 = BIP85()
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", MNEMONIC)
    drng_reader = BIP85DRNG.new(test)
    rsa = RSA.generate(bits=2048, randfunc=drng_reader.read, e=65537)
    key = rsa.export_key(format='PEM', pkcs=1)
    key_hash = hashlib.sha256(key).hexdigest()
    expected = '64ff572798a6534c76eda9fd2d7e906a737a1bad893dec31ae3d0488e3f19ed9'
    assert key_hash == expected

    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/1'", XPRV)
    drng_reader = BIP85DRNG.new(test)
    rsa = RSA.generate(bits=2048, randfunc=drng_reader.read, e=65537)
    key = rsa.export_key(format='PEM', pkcs=1)
    key_hash = hashlib.sha256(key).hexdigest()
    expected = '54196fdcbb0cb55c56b14a7068ea633dc784dde21cbe4e7f30f857ec88f9ac36'
    assert key_hash == expected

    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/2'", XPRV)
    drng_reader = BIP85DRNG.new(test)
    rsa = RSA.generate(bits=4096, randfunc=drng_reader.read, e=65537)
    key = rsa.export_key(format='PEM', pkcs=1)
    key_hash = hashlib.sha256(key).hexdigest()
    expected = 'c03f358f4aad4a0216881ec258ed6923201d174f52069bc9bcd341bb611696d5'
    assert key_hash == expected


if __name__ == "__main__":
    pytest.main()

