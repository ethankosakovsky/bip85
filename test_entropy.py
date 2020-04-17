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

from bipentropy import bipentropy
import pytest

XPRV = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'

def test_mnemonic():
    e = bipentropy.BIPEntropy()
    mnemonic = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'
    test = e.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic)
    expected = '71356cdf2f6851c0499b47fe16ef121883f8c58e7d6fb4c33a9017df71f3b0fe21f92d043ee4f19676384a3d943554904caca131269dcb84151ecb2f7ca31902'
    assert test.hex() == expected

    # with password
    test = e.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic, 'TREZOR')
    expected = '5c56a2a19ebe8f86c4cbb788dd264bd96387dac2047dac799c51fb6218da0513da44bc0f4603815cc8c8c456dbd3aae79e334fb19dbeffc43fc236d58368ebdb'
    assert test.hex() == expected

def test_xprv_to_entropy():
    e = bipentropy.BIPEntropy()
    test = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    expected = '71356cdf2f6851c0499b47fe16ef121883f8c58e7d6fb4c33a9017df71f3b0fe21f92d043ee4f19676384a3d943554904caca131269dcb84151ecb2f7ca31902'
    assert test.hex() == expected


def test_entropy_to_mnemonic():
    e = bipentropy.BIPEntropy()
    entropy = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)

    words12 = 'illness problem daughter gain lunar then chapter happy wrap resist setup corn'
    assert e.entropy_to_bip39(entropy, 12) == words12

    words15 = 'illness problem daughter gain lunar then chapter happy wrap resist setup country display glare debate'
    assert e.entropy_to_bip39(entropy, 15) == words15

    words24 = 'illness problem daughter gain lunar then chapter happy wrap resist setup country display glare delay pupil regular border piano cook warfare what sentence supreme'
    assert e.entropy_to_bip39(entropy, 24) == words24

def test_wif_from_entropy():
    # PDG: not sure about this?
    e = bipentropy.BIPEntropy()
    entropy = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    assert e.entropy_to_wif(entropy) == 'L11mqGbaozsMYDHS7dfZ2bPGL2viSH6zHr69MKwvpxuw7cCR4M1u'

def test_applications():
    e = bipentropy.BIPEntropy()
    entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/12'/0'", XPRV)
    assert entropy[:16].hex() == 'f0337580e36fd50ef8734cd9dcfb9a78'
    assert e.entropy_to_bip39(entropy, 12) == \
                     'usual option gasp short wool manual tide hat supply treat track valve'

    entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/18'/0'", XPRV)
    assert entropy[:24].hex() == '60529dbbf2707ea89e4cd41f7e26fcebf2b492b9a99c5e95'
    assert e.entropy_to_bip39(entropy, 18) == \
                     'gate neutral humble top among february junior once buyer van sand subject clip enable trade crime future protect'

    entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/24'/0'", XPRV)
    assert entropy[:32].hex() == '5166983339d6fc685abe49162327ac2e915fcc17132dad7a2b1e8f324b2f06bd'
    assert e.entropy_to_bip39(entropy, 24) == \
                     'fabric crumble art inhale hurt crouch helmet since bike bomb twelve frog bicycle toward fox grant pulp spend sibling bunker caution nurse brain prison'

def test_xprv_application():
    e = bipentropy.BIPEntropy()
    result = e.bip32_xprv_to_xprv(0, XPRV)
    assert result == 'xprv9s21ZrQH143K3KJoGoKpsDsWdDNDBKs1wqFymBpCGJtrYXrfKzykGDBadZq5SrNde22F83X9qhFZr4uyV9TptTgLqCBc6XFN9tssphdxVeg'

if __name__ == "__main__":
    pytest.main()


