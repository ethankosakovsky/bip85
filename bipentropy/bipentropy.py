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

import hmac
import hashlib
import base58
from mnemonic import Mnemonic as bip39
from pycoin.symbols.btc import network as BTC


class BIPEntropy(object):
    def bip39_mnemonic_to_entropy(self, path, mnemonic, passphrase=''):
        bip39_seed = bip39.to_seed(mnemonic, passphrase=passphrase)
        xprv = BTC.keys.bip32_seed(bip39_seed)
        return self.__hmac_sha512(self.__derive_k(path, xprv))

    def bip32_xprv_to_entropy(self, path, xprv_string):
        xprv = BTC.parse(xprv_string)
        if xprv is None:
            raise ValueError('ERROR: Invalid xprv')
        return self.__hmac_sha512(self.__derive_k(path, xprv))

    def entropy_from_wif(self, wif):
        return self.__hmac_sha512(self.__get_k_from_wif(wif))

    def entropy_to_wif(self, entropy):
        return BTC.keys.private(secret_exponent=int(entropy[:32].hex(), 16)).wif()

    def entropy_to_bip39(self, entropy, words, language='english'):
        bits = (words - 1) * 11 // 8 + 1
        m = bip39(language)
        return m.to_mnemonic(entropy[:bits])

    def __get_k_from_wif(self, wif):
        return base58.b58decode(wif)[1:-5]

    def __decorate_path(self, path):
        return path.replace("m/", "").replace("'", "p")

    def __derive_k(self, path, xprv):
        child_wif = xprv.subkey_for_path(self.__decorate_path(path)).wif()
        return self.__get_k_from_wif(child_wif)

    def __hmac_sha512(self, message_k):
        return hmac.new(b'bip-entropy-from-k', message_k, digestmod=hashlib.sha512).digest()
