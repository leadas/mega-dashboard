#!/usr/bin/env python3
"""
Test script to verify Railway volume mount configuration
Run this to check if the volume is properly mounted and accessible
"""

import os
import json
from datetime import datetime

def test_volume_config():
    print("=== Railway Volume Mount Test ===")
    
    # Check environment variables
    volume_path = os.getenv('RAILWAY_VOLUME_MOUNT_PATH')
    print(f"RAILWAY_VOLUME_MOUNT_PATH: {volume_path}")
    
    # Use the same logic as server.py
    DATA_DIR = os.getenv('RAILWAY_VOLUME_MOUNT_PATH', 'secure_data')
    print(f"DATA_DIR: {DATA_DIR}")
    
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if directory exists
    print(f"DATA_DIR exists: {os.path.exists(DATA_DIR)}")
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"✅ Successfully created/verified DATA_DIR: {DATA_DIR}")
    except Exception as e:
        print(f"❌ Failed to create DATA_DIR: {e}")
        return False
    
    # Test file creation
    test_file = os.path.join(DATA_DIR, 'test_volume.txt')
    try:
        with open(test_file, 'w') as f:
            f.write(f"Volume test - {datetime.now().isoformat()}\n")
            f.write(f"DATA_DIR: {DATA_DIR}\n")
            f.write(f"Volume path: {volume_path}\n")
        print(f"✅ Successfully created test file: {test_file}")
        
        # Read it back
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"✅ Successfully read test file content:\n{content}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create/read test file: {e}")
        return False

if __name__ == "__main__":
    success = test_volume_config()
    if success:
        print("\n🎉 Volume test PASSED - Railway volume should work!")
    else:
        print("\n💥 Volume test FAILED - Check Railway volume configuration!")
