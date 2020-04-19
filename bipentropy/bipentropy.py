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
from mnemonic import Mnemonic as bip39
from pycoin.symbols.btc import network as BTC
from pycoin.encoding.bytes32 import from_bytes_32, to_bytes_32


class BIPEntropy(object):
    def __decorate_path(self, path):
        return path.replace("m/", "").replace("'", "p")

    def __get_k_from_node(self, node):
        return to_bytes_32(node.secret_exponent())

    def __derive_k(self, path, xprv):
        path = self.__decorate_path(path)
        node = xprv.subkey_for_path(path)
        return self.__get_k_from_node(node)

    def __hmac_sha512(self, message_k):
        return hmac.new(message_k, msg=b'bip-entropy-from-k', digestmod=hashlib.sha512).digest()

    def bip39_mnemonic_to_entropy(self, path, mnemonic, passphrase=''):
        bip39_seed = bip39.to_seed(mnemonic, passphrase=passphrase)
        xprv = BTC.keys.bip32_seed(bip39_seed)
        return self.__hmac_sha512(self.__derive_k(path, xprv))

    def bip32_xprv_to_entropy(self, path, xprv_string):
        xprv = BTC.parse(xprv_string)
        if xprv is None:
            raise ValueError('ERROR: Invalid xprv')
        return self.__hmac_sha512(self.__derive_k(path, xprv))

    def bip32_xprv_to_hex(self, path, width, xprv_string):
        # export entropy as hex
        path = self.__decorate_path(path)
        ent = self.bip32_xprv_to_entropy(path, xprv_string)
        return ent[0:width].hex()

    def bip32_xprv_to_xprv(self, path, xprv_string):
        path = self.__decorate_path(path)
        node = BTC.parse.bip32_prv(xprv_string).subkey_for_path(path)

        # if API to pycoin hadn't been shitcoined:
        # return BIP32Node(node.chain_code(), secret_exponent=node.secret_exponent()).hwif()

        node._depth = 0
        node._parent_fingerprint = bytes(4)
        node._child_index = 0

        return node.hwif(as_private=True)

    def entropy_from_wif(self, wif):
        node = BTC.keys.from_text(wif)
        return self.__hmac_sha512(self.__get_k_from_node(node))

    def entropy_to_wif(self, entropy):
        return BTC.keys.private(secret_exponent=from_bytes_32(entropy[:32])).wif()

    def entropy_to_bip39(self, entropy, words, language='english'):
        width = (words - 1) * 11 // 8 + 1
        assert 16 <= width <= 32
        m = bip39(language)
        return m.to_mnemonic(entropy[:width])
