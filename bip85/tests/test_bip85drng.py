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
import pytest

XPRV = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
MNEMONIC = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'


def test_drng():
    bip85 = BIP85()
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", MNEMONIC)
    drng = BIP85DRNG.new(test)
    expected = 'b78b1ee6b345eae6836c2d53d33c64cdaf9a696487be81b03e822dc84b3f1cd883d7559e53d175f243e4c349e822a957bbff'
    assert drng.read(50).hex() == expected
    expected = '9224bc5dde9492ef54e8a439f6bc8c7355b87a925a37ee405a7502991111cd2dddaf1883f4e962abf4fb4b31cd28d5cf6b14f6ddcc9c19fd56d7f960a4b27f1d423a55dda4865aa6ddd6b4c26f18d400bb0a593e6c785d6d7e28c9c64608624318eddc01'
    assert drng.read(100).hex() == expected
    expected = '23750caa2a271f35faa6a3ca292b4be357404eca6842c69a3717dc3e41f7b38c67be492395b32221470aa08a2c489018c635a175f731245330e1f47091dbfb26f2923d10bd2e09280bffd1d94eb2a88f964aeb1774da04aad3bb1fdde0f77cd5ca79617ae317375417a51339523057bebef434c4400303890332e458425242f56a4293dad4f632b82713467b18ed6e1dab633220523d'
    assert drng.read(150).hex() == expected

    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    drng = BIP85DRNG.new(test)
    expected = 'b78b1ee6b345eae6836c2d53d33c64cdaf9a696487be81b03e822dc84b3f1cd883d7559e53d175f243e4c349e822a957bbff9224bc5dde9492ef54e8a439f6bc8c7355b87a925a37ee405a7502991111'
    assert drng.read(80).hex() == expected
    expected = 'cd2dddaf1883f4e962abf4fb4b31cd28d5cf6b14f6ddcc9c19'
    assert drng.read(25).hex() == expected

    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    drng = BIP85DRNG.new(test)
    expected = 'b78b1ee6b345eae6836c2d53d33c64cdaf9a6964'
    assert drng.read(20).hex() == expected
    expected = '87be81b03e822dc84b3f1cd883d7559e53d175f243e4c349e8'
    assert drng.read(25).hex() == expected


def test_determinism():
    bip85 = BIP85()
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", MNEMONIC)
    drng1 = BIP85DRNG.new(test)
    drng2 = BIP85DRNG.new(test)
    drng3 = BIP85DRNG.new(test)

    result1 = drng1.read(10).hex() + drng1.read(20).hex() + drng1.read(30).hex() + drng1.read(40).hex()
    result2 = drng2.read(40).hex() + drng2.read(30).hex() + drng2.read(20).hex() + drng2.read(10).hex()
    result3 = drng3.read(100).hex()

    assert result1 == result2
    assert result2 == result3


def test_lengths():
    bip85 = BIP85()
    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    drng = BIP85DRNG.new(test)

    assert len(drng.read(1)) == 1
    assert len(drng.read(10)) == 10
    assert len(drng.read(100)) == 100
    assert len(drng.read(1000)) == 1000
    assert len(drng.read(10000)) == 10000
    assert len(drng.read(100000)) == 100000
    assert len(drng.read(10000001)) == 10000001


def test_drng_exceptions():
    bip85 = BIP85()
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/1'", MNEMONIC)
    for i in range(64):
        with pytest.raises(ValueError, match="BIP85DRNG input entropy must be exactly 512 bits."):
            BIP85DRNG.new(test[:i])

    for i in [True, False, None, [], {}, (),
              '1234567890123456789012345678901234567890123456789012345678901234',
              int(123456789),
              ]:
        with pytest.raises(TypeError, match="BIP85DRNG input entropy must be bytes."):
            BIP85DRNG.new(i)


if __name__ == "__main__":
    pytest.main()

