#!/usr/bin/env python3
"""
Test script for configuration profile system
"""

from config_profiles import create_default_profiles, get_profile_manager

def test_profile_system():
    """Test the configuration profile CRUD operations"""
    print("🧪 Testing Configuration Profile System")
    print("=" * 50)
    
    # Initialize and create defaults
    create_default_profiles()
    manager = get_profile_manager()
    
    # Test getting all profiles
    profiles = manager.get_all_profiles()
    print(f"✅ Found {len(profiles)} profiles:")
    for profile in profiles:
        print(f"   - {profile.name}: {profile.website_url}")
    
    # Test creating a new profile
    from config_profiles import ConfigProfile, WordPressConfig
    
    new_profile = ConfigProfile(
        name="Test ServiceDogUS",
        description="Test configuration for ServiceDogUS production",
        website_url="https://servicedogus.org", 
        wordpress=WordPressConfig(
            url="https://wp.servicedogus.org",
            username="test-user",
            password="test-password",
            auth_method="application",
            verify_ssl=True
        )
    )
    
    created_profile = manager.create_profile(new_profile)
    print(f"✅ Created profile: {created_profile.name} (ID: {created_profile.id[:8]}...)")
    
    # Test duplicating profile
    duplicated = manager.duplicate_profile(created_profile.id, "ServiceDogUS Copy")
    if duplicated:
        print(f"✅ Duplicated profile: {duplicated.name}")
    
    # Test setting active profile
    success = manager.set_active_profile(created_profile.id)
    if success:
        active = manager.get_active_profile()
        print(f"✅ Active profile: {active.name}")
    
    # Test searching profiles
    search_results = manager.search_profiles("servicedogus")
    print(f"✅ Search results for 'servicedogus': {len(search_results)} profiles")
    
    # Test export/import
    exported = manager.export_profile(created_profile.id)
    if exported:
        print(f"✅ Exported profile data ({len(str(exported))} characters)")
    
    print("\n🎉 Profile system tests completed successfully!")
    
    return len(profiles) + 2  # Original + 2 new ones

if __name__ == "__main__":
    test_profile_system()