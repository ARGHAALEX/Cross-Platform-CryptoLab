from pathlib import Path
import getpass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

ITERATIONS = 600_000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
MIN_FILE_SIZE = SALT_SIZE + NONCE_SIZE + 16  # AES-GCM authentication tag

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))

def main():
    encrypted_file = Path("secret.enc")
    if not encrypted_file.is_file():
        raise SystemExit("secret.enc not found. Place it in this folder.")

    data = encrypted_file.read_bytes()
    if len(data) < MIN_FILE_SIZE:
        raise SystemExit("Encrypted file is too small or invalid.")

    salt = data[:SALT_SIZE]
    nonce = data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = data[SALT_SIZE + NONCE_SIZE:]

    password = getpass.getpass("Enter encryption password: ")
    key = derive_key(password, salt)

    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise SystemExit("Decryption failed: wrong password or file was modified.")

    Path("decrypted.txt").write_bytes(plaintext)
    print("Decryption successful. Output: decrypted.txt")

if __name__ == "__main__":
    main()
