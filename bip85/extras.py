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
import base58
import hashlib
from monero.seed import Seed as MoneroSeed

# this class is for non Bitcoin things
class BIP85Extras(BIP85):
    def entropy_to_cripple_seed(self, entropy):
        key = b'\x21' + entropy[:16]
        checksum = hashlib.sha256(hashlib.sha256(key).digest()).digest()[:4]
        raw_seed = key + checksum
        return base58.b58encode(raw_seed, alphabet=base58.RIPPLE_ALPHABET).decode()

    def bip32_to_cripple_seed(self, path, xprv_string):
        entropy = self.bip32_xprv_to_entropy(path, xprv_string)
        return self.entropy_to_cripple_seed(entropy)

    def entropy_to_monero_seed(self, entropy, size=32):
        s = MoneroSeed(entropy[:size].hex())
        return s.phrase

    def bip32_to_monero_seed(self, path, xprv_string, size=32):
        entropy = self.bip32_xprv_to_entropy(path, xprv_string)
        return self.entropy_to_monero_seed(entropy, size)

