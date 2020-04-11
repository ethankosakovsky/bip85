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
import unittest

class EntropyTest(unittest.TestCase):
    def test_mnemonic(self):
        e = bipentropy.BIPEntropy()
        mnemonic = 'install scatter logic circle pencil average fall shoe quantum disease suspect usage'
        test = e.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic)
        expected = 'efecfbccffea313214232d29e71563d941229afb4338c21f9517c41aaa0d16f00b83d2a09ef747e7a64e8e2bd5a14869e693da66ce94ac2da570ab7ee48618f7'
        self.assertEqual(test.hex(), expected)

        # with password
        test = e.bip39_mnemonic_to_entropy("m/83696968'/0'/0'", mnemonic, 'TREZOR')
        expected = 'd24cee04c61c4a47751658d078ae9b0cc9550fe43eee643d5c10ac2e3f5edbca757b2bd74d55ff5bcc2b1608d567053660d9c7447ae1eb84b6619282fd391844'
        self.assertEqual(test.hex(), expected)

    def test_xprv(self):
        e = bipentropy.BIPEntropy()
        xprv = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
        test = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", xprv)
        expected = 'efecfbccffea313214232d29e71563d941229afb4338c21f9517c41aaa0d16f00b83d2a09ef747e7a64e8e2bd5a14869e693da66ce94ac2da570ab7ee48618f7'
        self.assertEqual(test.hex(), expected)

    def test_entropy_to_mnemonic(self):
        e = bipentropy.BIPEntropy()
        xprv = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
        entropy = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", xprv)

        words12 = 'useful guitar veteran zone perfect october explain grant clarify december flight recycle'
        words15 = 'useful guitar veteran zone perfect october explain grant clarify december flight raw banana estate uncle'
        words24 = 'useful guitar veteran zone perfect october explain grant clarify december flight raw banana estate unfair grow search witness echo market primary alley forward boring'

        self.assertEqual(e.entropy_to_bip39(entropy, 12), words12)
        self.assertEqual(e.entropy_to_bip39(entropy, 15), words15)
        self.assertEqual(e.entropy_to_bip39(entropy, 24), words24)

    def test_wif_from_entropy(self):
        e = bipentropy.BIPEntropy()
        xprv = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
        entropy = e.bip32_xprv_to_entropy("m/83696968'/0'/0'", xprv)
        self.assertEqual(e.entropy_to_wif(entropy), 'L5G6UFMvJaFt1KPvupEtT8TUN2YrFnQJm1LA2nEczWrR7MuoxB1Z')

    def test_applications(self):
        e = bipentropy.BIPEntropy()
        xprv = 'xprv9s21ZrQH143K2LBWUUQRFXhucrQqBpKdRRxNVq2zBqsx8HVqFk2uYo8kmbaLLHRdqtQpUm98uKfu3vca1LqdGhUtyoFnCNkfmXRyPXLjbKb'
        entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/12'/0'", xprv)
        self.assertEqual(entropy[:16].hex(), '6250b68daf746d12a24d58b4787a714b')
        self.assertEqual(e.entropy_to_bip39(entropy, 12),
                         'girl mad pet galaxy egg matter matrix prison refuse sense ordinary nose')

        entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/18'/0'", xprv)
        self.assertEqual(entropy[:24].hex(), '938033ed8b12698449d4bbca3c853c66b293ea1b1ce9d9dc')
        self.assertEqual(e.entropy_to_bip39(entropy, 18),
                         'near account window bike charge season chef number sketch tomorrow excuse sniff circle vital hockey outdoor supply token')

        entropy = e.bip32_xprv_to_entropy("m/83696968'/39'/0'/24'/0'", xprv)
        self.assertEqual(entropy[:32].hex(), 'ae131e2312cdc61331542efe0d1077bac5ea803adf24b313a4f0e48e9c51f37f')
        self.assertEqual(e.entropy_to_bip39(entropy, 24),
                         'puppy ocean match cereal symbol another shed magic wrap hammer bulb intact gadget divorce twin tonight reason outdoor destroy simple truth cigar social volcano')


def __main__():
    unittest.main()


if __name__ == "__main__":
    __main__()


