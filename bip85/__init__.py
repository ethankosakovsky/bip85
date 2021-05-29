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
import base58


class BIP85(object):
    def _decorate_path(self, path):
        return path.replace("m/", "").replace("'", "p")

    def _get_k_from_node(self, node):
        return to_bytes_32(node.secret_exponent())

    def _derive_k(self, path, xprv):
        path = self._decorate_path(path)
        node = xprv.subkey_for_path(path)
        return self._get_k_from_node(node)

    def _hmac_sha512(self, message_k):
        return hmac.new(key=b'bip-entropy-from-k', msg=message_k, digestmod=hashlib.sha512).digest()

    def bip39_mnemonic_to_entropy(self, path, mnemonic, passphrase=''):
        bip39_seed = bip39.to_seed(mnemonic, passphrase=passphrase)
        xprv = BTC.keys.bip32_seed(bip39_seed)
        return self._hmac_sha512(self._derive_k(path, xprv))

    def bip32_xprv_to_entropy(self, path, xprv_string):
        xprv = BTC.parse(xprv_string)
        if xprv is None:
            raise ValueError('ERROR: Invalid xprv')
        return self._hmac_sha512(self._derive_k(path, xprv))

    def bip32_xprv_to_hex(self, path, width, xprv_string):
        # export entropy as hex
        path = self._decorate_path(path)
        ent = self.bip32_xprv_to_entropy(path, xprv_string)
        return ent[0:width].hex()

    def bip32_xprv_to_xprv(self, path, xprv_string):
        path = self._decorate_path(path)
        ent = self.bip32_xprv_to_entropy(path, xprv_string)

        # From Peter Gray
        # Taking 64 bytes of the HMAC digest, the first 32 bytes are the chain code, and second 32 bytes are the private
        # key for BIP32 XPRV value. Child number, depth, and parent fingerprint are forced to zero.
        prefix = b'\x04\x88\xad\xe4'
        depth = b'\x00'
        parent_fingerprint = b'\x00\x00\x00\x00'
        child_num = b'\x00\x00\x00\x00'
        chain_code = ent[:32]
        private_key = b'\x00' + ent[32:]
        extended_key = prefix + depth + parent_fingerprint + child_num + chain_code + private_key
        checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
        derived_xprv_string = base58.b58encode(extended_key + checksum).decode()
        node = BTC.parse(derived_xprv_string)

        return node.hwif(as_private=True)

    def entropy_from_wif(self, wif):
        node = BTC.keys.from_text(wif)
        return self._hmac_sha512(self._get_k_from_node(node))

    def entropy_to_wif(self, entropy):
        return BTC.keys.private(secret_exponent=from_bytes_32(entropy[:32])).wif()

    def entropy_to_bip39(self, entropy, words, language='english'):
        width = (words - 1) * 11 // 8 + 1
        assert 16 <= width <= 32
        m = bip39(language)
        return m.to_mnemonic(entropy[:width])
