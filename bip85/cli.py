import argparse
import binascii

from mnemonic import Mnemonic as bip39
from pycoin.symbols.btc import network as BTC

from bip85 import app


def _bip32_master_seed_to_xprv(bip32_master_seed: bytes):
    if len(bip32_master_seed) < 16 or len(bip32_master_seed) > 64:
        raise ValueError('BIP32 master seed must be between 128 and 512 bits')
    xprv = BTC.keys.bip32_seed(bip32_master_seed).hwif(as_private=True)
    return xprv


def _get_xprv_from_args(args):
    if args.xprv:
        return args.xprv
    if args.bip32_master_seed:
        return _bip32_master_seed_to_xprv(
            bytearray.fromhex(args.bip32_master_seed))
    bip39_mnemonic = args.bip39_mnemonic
    if args.bip39_entropy:
        bip39_mnemonic = bip39(args.language).to_mnemonic(
            binascii.unhexlify(args.bip39_entropy))
    return _bip32_master_seed_to_xprv(bip39.to_seed(bip39_mnemonic))


def main():
    parser = argparse.ArgumentParser(description='BIP85 CLI tool')
    seed_group = parser.add_mutually_exclusive_group(required=True)
    seed_group.add_argument(
        '--bip32-master-seed',
        help='Input BIP32 master seed (AKA initial entropy), which is usually '
        'computed by hashing the BIP39 mnemonic. Must be in hex format')
    seed_group.add_argument('--bip39-entropy',
                            help='Input BIP39 initial entropy (used to derive '
                            'the mnemonic)')
    seed_group.add_argument('--bip39-mnemonic',
                            help='Input BIP39 mnemonic phrase')
    seed_group.add_argument('--xprv',
                            help='Input BIP32 root master private key')
    parser.add_argument('--index',
                        type=int,
                        required=True,
                        help='Derived key index')
    subparsers = parser.add_subparsers(dest='bip85_app')
    subparsers.required = True
    app_bip39_parser = subparsers.add_parser('bip39',
                                             help='Derive a BIP39 mnemonic')
    app_bip39_parser.add_argument('--language',
                                  choices=app.LANGUAGE_LOOKUP,
                                  default='english',
                                  help='Language for BIP39 mnemonic')
    app_bip39_parser.add_argument('--num-words',
                                  type=int,
                                  choices=(12, 15, 18, 21, 24),
                                  default=12,
                                  help='Number of words in the BIP39 mnemonic')
    subparsers.add_parser('wif', help='Derive a HD-Seed WIF')
    app_hex_parser = subparsers.add_parser('hex',
                                           help='Derive a HEX bytes sequence')
    app_hex_parser.add_argument('--num-bytes',
                                type=int,
                                required=True,
                                help='Number of bytes to generate')
    subparsers.add_parser('xprv', help='Derive an XPRV (master private key)')
    args = parser.parse_args()
    xprv = _get_xprv_from_args(args)
    print(f"Using master private key: {xprv}")
    if args.bip85_app == 'bip39':
        print(app.bip39(xprv, args.language, args.num_words, args.index))
    elif args.bip85_app == 'wif':
        print(app.wif(xprv, args.index))
    elif args.bip85_app == 'hex':
        print(app.hex(xprv, args.index, args.num_bytes))
    elif args.bip85_app == 'xprv':
        print(app.xprv(xprv, args.index))


if __name__ == "__main__":
    main()
