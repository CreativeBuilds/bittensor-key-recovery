#!/usr/bin/env python3
"""
unlock_bt_coldkey.py – dump the seed / mnemonic from a $NACL-encrypted
Bittensor cold-key file.

usage:  python unlock_bt_coldkey.py ~/.bittensor/wallets/<name>/coldkey
deps :  pip install pynacl substrate-interface
"""

from pathlib import Path, PurePosixPath
import json, getpass, sys
from nacl import secret, pwhash
from substrateinterface import Keypair, KeypairType

# Same constant baked into bittensor.keyfile
NACL_SALT = b'\x13q\x83\xdf\xf1Z\t\xbc\x9c\x90\xb5Q\x879\xe9\xb1'

TAG = b"$NACL"
BOX_KEY_BYTES = secret.SecretBox.KEY_SIZE

def main(path):
    blob = Path(path).read_bytes()
    if not blob.startswith(TAG):
        sys.exit("Not a $NACL key-file")

    pwd  = getpass.getpass("Cold-key password: ").encode()

    key = pwhash.argon2i.kdf(
            BOX_KEY_BYTES, pwd, NACL_SALT,
            opslimit=pwhash.argon2i.OPSLIMIT_SENSITIVE,
            memlimit=pwhash.argon2i.MEMLIMIT_SENSITIVE,
    )

    box      = secret.SecretBox(key)
    try:
        plain = box.decrypt(blob[len(TAG):])
    except Exception:
        sys.exit("✗  wrong password")

    # The plaintext is a JSON dump of the keypair
    info = json.loads(plain.decode())

    seed_hex   = (info.get("secretSeed") or "").lstrip("0x")
    mnemonic   = info.get("secretPhrase")
    ss58       = info.get("ss58Address")

    print("\n✓  decrypted")
    if seed_hex:
        seed_bytes = bytes.fromhex(seed_hex)
        print("Seed (hex) :", seed_hex)
        # re-instantiate for convenience / double-check
        kp = Keypair.create_from_seed(seed_bytes, crypto_type=KeypairType.SR25519)
        print("SS58 addr  :", kp.ss58_address)
        print("Mnemonic   :", kp.mnemonic)
    else:
        print("No seed found – file only holds public data")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {PurePosixPath(sys.argv[0]).name} /path/to/coldkey")
        sys.exit(1)
    main(sys.argv[1])
