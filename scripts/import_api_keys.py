#!/usr/bin/env python3
"""
Script to import API keys from .env.local to the encrypted storage
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.api_keys_manager import get_api_keys_manager
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

def import_keys():
    """Import API keys from environment to encrypted storage"""
    manager = get_api_keys_manager()
    
    # Get keys from environment (even if commented, we'll parse them)
    with open('.env.local', 'r') as f:
        lines = f.readlines()
    
    keys_to_import = {}
    for line in lines:
        # Remove comment if present
        if '# JINA_API_KEY=' in line:
            keys_to_import['jina_api_key'] = line.split('=')[1].strip()
        elif '# ANTHROPIC_API_KEY=' in line:
            keys_to_import['anthropic_api_key'] = line.split('=')[1].strip()
        elif '# OPENAI_API_KEY=' in line:
            keys_to_import['openai_api_key'] = line.split('=')[1].strip()
        elif '# BRIGHT_DATA_API_KEY=' in line:
            keys_to_import['bright_data_api_key'] = line.split('=')[1].strip()
    
    # Update keys in manager
    if keys_to_import:
        manager.update_keys(**keys_to_import)
        print(f"✅ Imported {len(keys_to_import)} API keys to encrypted storage")
        
        # Test each key
        for key_name in keys_to_import:
            result = manager.test_api_key(key_name)
            status = "✅" if result['success'] else "❌"
            print(f"{status} {key_name}: {result['message']}")
    else:
        print("❌ No API keys found to import")

if __name__ == "__main__":
    import_keys()