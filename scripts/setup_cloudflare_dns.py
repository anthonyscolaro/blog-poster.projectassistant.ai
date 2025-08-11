#!/usr/bin/env python3
"""
Setup Cloudflare DNS entries for blog-poster deployment
Configures blogpost.projectassistant.ai to point to Digital Ocean
"""
import os
import sys
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Cloudflare configuration
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')

if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
    print("❌ Error: Cloudflare credentials not found in .env.local")
    print("Please ensure CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID are set")
    sys.exit(1)

# API configuration
CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

def list_dns_records() -> list:
    """List all existing DNS records"""
    response = requests.get(CLOUDFLARE_API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"❌ Error listing DNS records: {response.status_code}")
        print(response.json())
        return []

def find_record(name: str, record_type: str = "A") -> Optional[Dict[str, Any]]:
    """Find existing DNS record by name and type"""
    records = list_dns_records()
    for record in records:
        if record['name'] == name and record['type'] == record_type:
            return record
    return None

def create_or_update_record(name: str, content: str, record_type: str = "A", proxied: bool = True) -> bool:
    """Create or update a DNS record"""
    existing = find_record(name, record_type)
    
    data = {
        "type": record_type,
        "name": name,
        "content": content,
        "ttl": 1,  # Auto TTL
        "proxied": proxied
    }
    
    if existing:
        # Update existing record
        print(f"🔄 Updating existing {record_type} record for {name}")
        url = f"{CLOUDFLARE_API_URL}/{existing['id']}"
        response = requests.put(url, json=data, headers=HEADERS)
    else:
        # Create new record
        print(f"➕ Creating new {record_type} record for {name}")
        response = requests.post(CLOUDFLARE_API_URL, json=data, headers=HEADERS)
    
    if response.status_code in [200, 201]:
        print(f"✅ Successfully configured {name} → {content}")
        return True
    else:
        print(f"❌ Error configuring {name}: {response.status_code}")
        print(response.json())
        return False

def setup_blog_poster_dns(digital_ocean_ip: Optional[str] = None):
    """Setup DNS entries for blog-poster application"""
    print("\n🚀 Setting up DNS for blog-poster on projectassistant.ai\n")
    
    if not digital_ocean_ip:
        # If no IP provided, set up CNAME to Digital Ocean app
        # This will be updated once we have the actual DO app URL
        print("ℹ️  No Digital Ocean IP provided, setting up placeholder entries")
        print("ℹ️  Update these after deploying to Digital Ocean App Platform\n")
        
        # For now, create CNAME records pointing to a placeholder
        # These will be updated to point to the actual DO app URL
        records = [
            ("blogpost", "app.digitalocean.com", "CNAME"),  # Will be updated to actual DO app URL
            ("api.blogpost", "app.digitalocean.com", "CNAME"),  # Optional API subdomain
        ]
        
        print("📝 Note: After deploying to Digital Ocean, update these records to:")
        print("   blogpost.projectassistant.ai → your-app.ondigitalocean.app")
        print("   api.blogpost.projectassistant.ai → your-app.ondigitalocean.app\n")
    else:
        # Create A records pointing to Digital Ocean IP
        records = [
            ("blogpost", digital_ocean_ip, "A"),
            ("api.blogpost", digital_ocean_ip, "A"),
        ]
    
    success = True
    for name, content, record_type in records:
        full_name = f"{name}.projectassistant.ai"
        if not create_or_update_record(full_name, content, record_type):
            success = False
    
    return success

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Cloudflare DNS for blog-poster")
    parser.add_argument(
        "--ip",
        help="Digital Ocean App Platform IP address (optional)",
        default=None
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all current DNS records"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\n📋 Current DNS Records for projectassistant.ai:\n")
        records = list_dns_records()
        for record in records:
            if 'blogpost' in record['name']:
                print(f"  {record['type']:5} {record['name']:40} → {record['content']}")
        print()
        return
    
    # Setup DNS entries
    if setup_blog_poster_dns(args.ip):
        print("\n✅ DNS setup complete!")
        print("\n📌 DNS Entries configured:")
        print("  - https://blogpost.projectassistant.ai (Web UI)")
        print("  - https://api.blogpost.projectassistant.ai (API)")
        print("\n⏱️  DNS propagation may take 1-5 minutes")
        
        if not args.ip:
            print("\n⚠️  Remember to update DNS records after deploying to Digital Ocean:")
            print("  python scripts/setup_cloudflare_dns.py --ip <your-do-app-ip>")
            print("  OR update CNAME to point to: your-app.ondigitalocean.app")
    else:
        print("\n❌ DNS setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()