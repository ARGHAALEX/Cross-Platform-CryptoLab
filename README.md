# Cross-Platform Secure File Encryption & Integrity Verification

A beginner-friendly cybersecurity lab demonstrating authenticated file encryption on Windows and decryption on Kali Linux using Python.

## Features

- AES-256-GCM authenticated encryption
- PBKDF2-HMAC-SHA256 password-based key derivation
- Random 16-byte salt and 12-byte nonce for each encryption
- Cross-platform decryption (Windows / Linux)
- SHA-256 hash comparison to verify that the recovered file matches the original

## Project files

- `encrypt.py` — encrypts `secret.txt` and creates `secret.enc`
- `decrypt.py` — decrypts `secret.enc` and creates `decrypted.txt`
- `requirements.txt` — Python dependency
- `.gitignore` — excludes secrets and generated files from Git

## Requirements

- Python 3
- `cryptography` Python package

Install dependency:

```bash
python -m pip install -r requirements.txt
```

On Kali Linux, alternatively:

```bash
sudo apt update
sudo apt install python3-cryptography -y
```

## Run on Windows

1. Put a test file named `secret.txt` in this project folder. Use non-sensitive sample text.
2. Open Command Prompt in the project folder.
3. Run:

```bash
python encrypt.py
```

4. Enter a password of at least 12 characters. Do not share or commit this password.
5. The program creates `secret.enc`.

## Transfer and decrypt on Kali Linux

Copy `secret.enc` to the Kali project folder using a VirtualBox shared folder or another secure transfer method.

Run:

```bash
python3 decrypt.py
```

Enter the exact same password used for encryption. The program creates `decrypted.txt`.

## Verify integrity

On Windows, calculate the SHA-256 hash of the original file:

```cmd
certutil -hashfile secret.txt SHA256
```

On Kali Linux, calculate the SHA-256 hash of the decrypted file:

```bash
sha256sum decrypted.txt
```

The two 64-character hash values should match exactly. A match indicates the original and decrypted files are byte-for-byte identical.

## Encrypted file format

`secret.enc` is stored as:

```text
16-byte salt | 12-byte nonce | AES-GCM ciphertext + 16-byte authentication tag
```

The salt and nonce are not secret; they are stored with the ciphertext. The password must remain private.

## Security notes

- Use a unique, strong password and keep it in a password manager.
- Never upload real confidential files or passwords to a public repository.
- Do not reuse a nonce with the same AES-GCM key. This project generates a fresh random salt and nonce for each encryption.
- SHA-256 comparison checks file equality; AES-GCM also authenticates the ciphertext during decryption.
- This is an educational project, not a reviewed production encryption product.

## Learning outcomes

- Understand symmetric authenticated encryption
- Understand password-based key derivation
- Transfer encrypted data between operating systems
- Perform decryption and integrity verification
