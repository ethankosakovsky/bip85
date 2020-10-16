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

from bip85.extras import BIP85Extras
import pytest

# install scatter logic circle pencil average fall shoe quantum disease suspect usage
XPRV = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'


def test_cripple():
    bip85 = BIP85Extras()
    result = bip85.bip32_to_cripple_seed("m/574946'/0'", XPRV)
    assert result == 'ssyKPX1uyL4mTpba6hHDRTX2Cj6gT'


def test_monero():
    bip85 = BIP85Extras()
    result = bip85.bip32_to_monero_seed("m/83696968'/12839'/25'/0'", XPRV, 32)
    assert result == 'paradise wield himself fungal jive wept faked pitched pebbles lymph suitcase foxes lifestyle jagged navy around rally when apart exotic virtual joyous austere nightly wept'

if __name__ == "__main__":
    pytest.main()

