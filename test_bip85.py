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
from bip85 import app
import pytest

XPRV = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'


def test_mnemonic():
    bip85 = BIP85()
    mnemonic = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic)
    expected = 'efecfbccffea313214232d29e71563d941229afb4338c21f9517c41aaa0d16f00b83d2a09ef747e7a64e8e2bd5a14869e693da66ce94ac2da570ab7ee48618f7'
    assert test.hex() == expected


def test_mnemonic_pwd():
    bip85 = BIP85()
    mnemonic = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'
    # with password
    test = bip85.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic, 'TREZOR')
    expected = 'd24cee04c61c4a47751658d078ae9b0cc9550fe43eee643d5c10ac2e3f5edbca757b2bd74d55ff5bcc2b1608d567053660d9c7447ae1eb84b6619282fd391844'
    assert test.hex() == expected


def test_xprv_to_entropy():
    bip85 = BIP85()
    test = bip85.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)
    expected = 'efecfbccffea313214232d29e71563d941229afb4338c21f9517c41aaa0d16f00b83d2a09ef747e7a64e8e2bd5a14869e693da66ce94ac2da570ab7ee48618f7'
    assert test.hex() == expected


def test_entropy_to_mnemonic():
    bip85 = BIP85()
    entropy = bip85.bip32_xprv_to_entropy("m/83696968'/0'/0'", XPRV)

    words12 = 'useful guitar veteran zone perfect october explain grant clarify december flight recycle'
    assert bip85.entropy_to_bip39(entropy, 12) == words12

    words15 = 'useful guitar veteran zone perfect october explain grant clarify december flight raw banana estate uncle'
    assert bip85.entropy_to_bip39(entropy, 15) == words15

    words24 = 'useful guitar veteran zone perfect october explain grant clarify december flight raw banana estate unfair grow search witness echo market primary alley forward boring'
    assert bip85.entropy_to_bip39(entropy, 24) == words24

def test_wif_from_entropy():
    bip85 = BIP85()
    entropy = bip85.bip32_xprv_to_entropy("m/83696968'/2'/0'", XPRV)
    entropy = entropy[:32]
    assert bip85.entropy_to_wif(entropy) == 'Kzyv4uF39d4Jrw2W7UryTHwZr1zQVNk4dAFyqE6BuMrMh1Za7uhp'

def test_mnemonic():
    bip85 = BIP85()
    entropy = bip85.bip32_xprv_to_entropy("m/83696968'/39'/0'/12'/0'", XPRV)
    assert entropy[:16].hex() == '6250b68daf746d12a24d58b4787a714b'
    assert bip85.entropy_to_bip39(entropy, 12) == \
                     'girl mad pet galaxy egg matter matrix prison refuse sense ordinary nose'

    entropy = bip85.bip32_xprv_to_entropy("m/83696968'/39'/0'/18'/0'", XPRV)
    assert entropy[:24].hex() == '938033ed8b12698449d4bbca3c853c66b293ea1b1ce9d9dc'
    assert bip85.entropy_to_bip39(entropy, 18) == \
                     'near account window bike charge season chef number sketch tomorrow excuse sniff circle vital hockey outdoor supply token'

    entropy = bip85.bip32_xprv_to_entropy("m/83696968'/39'/0'/24'/0'", XPRV)
    assert entropy[:32].hex() == 'ae131e2312cdc61331542efe0d1077bac5ea803adf24b313a4f0e48e9c51f37f'
    assert bip85.entropy_to_bip39(entropy, 24) == \
                     'puppy ocean match cereal symbol another shed magic wrap hammer bulb intact gadget divorce twin tonight reason outdoor destroy simple truth cigar social volcano'

def test_xprv():
    bip85 = BIP85()
    result = bip85.bip32_xprv_to_xprv("83696968'/32'/0'", XPRV)
    assert result == 'xprv9s21ZrQH143K2srSbCSg4m4kLvPMzcWydgmKEnMmoZUurYuBuYG46c6P71UGXMzmriLzCCBvKQWBUv3vPB3m1SATMhp3uEjXHJ42jFg7myX'

@pytest.mark.parametrize('path, width, expect', [
        ("83696968'/128169'/32'/0'", 32, 'ea3ceb0b02ee8e587779c63f4b7b3a21e950a213f1ec53cab608d13e8796e6dc'),
        ("83696968'/128169'/64'/0'", 64, '492db4698cf3b73a5a24998aa3e9d7fa96275d85724a91e71aa2d645442f878555d078fd1f1f67e368976f04137b1f7a0d19232136ca50c44614af72b5582a5c'),
        ("83696968'/128169'/64'/1234'", 64, '61d3c182f7388268463ef327c454a10bc01b3992fa9d2ee1b3891a6b487a5248793e61271066be53660d24e8cb76ff0cfdd0e84e478845d797324c195df9ab8e'),
    ])
def test_hex(path, width, expect):
    bip85 = BIP85()
    assert bip85.bip32_xprv_to_hex(path, width, XPRV) == expect

def test_bipentropy_applications():
    assert app.bip39(XPRV, 'english', 18, 0) == \
           'near account window bike charge season chef number sketch tomorrow excuse sniff circle vital hockey outdoor supply token'

    assert app.xprv(XPRV, 0) == \
           'xprv9s21ZrQH143K2srSbCSg4m4kLvPMzcWydgmKEnMmoZUurYuBuYG46c6P71UGXMzmriLzCCBvKQWBUv3vPB3m1SATMhp3uEjXHJ42jFg7myX'

    assert app.wif(XPRV, 0) == 'Kzyv4uF39d4Jrw2W7UryTHwZr1zQVNk4dAFyqE6BuMrMh1Za7uhp'

    assert app.hex(XPRV, 0, 32) == 'ea3ceb0b02ee8e587779c63f4b7b3a21e950a213f1ec53cab608d13e8796e6dc'

if __name__ == "__main__":
    pytest.main()

