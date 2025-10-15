#!/usr/bin/env python3
"""
Credential Migration Script
Migrates encrypted data from old credentials to new credentials
"""

import os
import sys
import json
import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass

DATA_DIR = 'secure_data'


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def get_user_file(username: str) -> str:
    """Get user-specific data file path"""
    safe_username = hashlib.sha256(username.encode()).hexdigest()[:16]
    return os.path.join(DATA_DIR, f'{safe_username}.enc')


def list_encrypted_files():
    """List all encrypted data files"""
    if not os.path.exists(DATA_DIR):
        return []
    
    files = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.enc'):
            filepath = os.path.join(DATA_DIR, filename)
            size = os.path.getsize(filepath)
            files.append((filename, filepath, size))
    return files


def decrypt_data(username: str, filepath: str):
    """Decrypt data with given credentials"""
    try:
        # Read encrypted data
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
        
        # Extract salt and content
        salt = encrypted_data[:16]
        encrypted_content = encrypted_data[16:]
        
        # Derive key and decrypt
        key = derive_key(username, salt)
        fernet = Fernet(key)
        
        decrypted = fernet.decrypt(encrypted_content)
        data = json.loads(decrypted.decode())
        
        return data
    except Exception as e:
        return None


def encrypt_data(username: str, data):
    """Encrypt data with new credentials"""
    user_file = get_user_file(username)
    
    # Generate salt and derive key
    salt = secrets.token_bytes(16)
    key = derive_key(username, salt)
    fernet = Fernet(key)
    
    # Encrypt data
    json_data = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_data)
    
    # Save salt + encrypted data
    with open(user_file, 'wb') as f:
        f.write(salt + encrypted)
    
    return user_file


def main():
    print("=" * 70)
    print("🔐 CREDENTIAL MIGRATION TOOL")
    print("=" * 70)
    print()
    
    # List existing encrypted files
    files = list_encrypted_files()
    
    if not files:
        print("❌ No encrypted data files found in secure_data/")
        print("   Nothing to migrate!")
        sys.exit(1)
    
    print(f"Found {len(files)} encrypted file(s):")
    for i, (filename, filepath, size) in enumerate(files, 1):
        print(f"  {i}. {filename} ({size} bytes)")
    print()
    
    # Get old credentials
    print("OLD CREDENTIALS (that encrypted the existing data):")
    old_password = input("  Old Password: ").strip()
    old_otp = input("  Old OTP: ").strip()
    old_username = f"{old_password}:{old_otp}"
    
    print()
    
    # Get new credentials
    print("NEW CREDENTIALS (from your .env file):")
    new_password = input("  New Password: ").strip()
    new_otp = input("  New OTP: ").strip()
    new_username = f"{new_password}:{new_otp}"
    
    print()
    print("-" * 70)
    print()
    
    # Find the old file
    old_file = get_user_file(old_username)
    
    if not os.path.exists(old_file):
        print(f"❌ Could not find file for old credentials: {old_file}")
        print()
        print("Available files:")
        for filename, filepath, size in files:
            print(f"  - {filepath}")
        print()
        print("💡 Tip: The file is hashed from 'password:otp'")
        sys.exit(1)
    
    print(f"✅ Found old data file: {old_file}")
    print()
    
    # Decrypt with old credentials
    print("🔓 Decrypting data with old credentials...")
    data = decrypt_data(old_username, old_file)
    
    if data is None:
        print("❌ Failed to decrypt! Check your old password/OTP are correct.")
        sys.exit(1)
    
    print(f"✅ Successfully decrypted {len(data)} website(s)!")
    print()
    
    # Show what will be migrated
    if data:
        print("Data to migrate:")
        for i, website in enumerate(data, 1):
            name = website.get('name') or website.get('domain', 'Unknown')
            print(f"  {i}. {name}")
        print()
    
    # Confirm
    confirm = input("Proceed with migration? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Migration cancelled.")
        sys.exit(0)
    
    print()
    print("🔒 Encrypting data with new credentials...")
    
    # Encrypt with new credentials
    new_file = encrypt_data(new_username, data)
    
    print(f"✅ Successfully encrypted to: {new_file}")
    print()
    
    # Backup old file
    backup_file = old_file + '.backup'
    import shutil
    shutil.copy2(old_file, backup_file)
    print(f"💾 Backed up old file to: {backup_file}")
    print()
    
    print("=" * 70)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Restart server: pkill -f server.py && python3 server.py")
    print("  2. Login with NEW credentials")
    print("  3. Your websites should appear!")
    print()
    print(f"Old file backed up to: {backup_file}")
    print("(You can delete this backup once you confirm everything works)")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


