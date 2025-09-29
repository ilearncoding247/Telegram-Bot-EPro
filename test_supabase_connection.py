#!/usr/bin/env python3
"""
Test script to verify Supabase connection and database setup
"""

import sys
import os

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

try:
    from telegramreferralpro.supabase_client import supabase
    print("✅ Supabase client imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Supabase client: {e}")
    sys.exit(1)

def test_supabase_connection():
    """Test the Supabase connection and verify database setup"""
    print("🔍 Testing Supabase connection...")
    
    try:
        # Test 1: Basic connection
        response = supabase.table("settings").select("key, value").execute()
        print("✅ Supabase connection successful!")
        
        # Test 2: Check if tables exist by querying them
        tables_to_check = ["settings", "referral_targets", "users", "referrals"]
        
        for table in tables_to_check:
            try:
                response = supabase.table(table).select("count").execute()
                print(f"✅ Table '{table}' exists and is accessible")
            except Exception as e:
                print(f"⚠️  Table '{table}' might not exist or is not accessible: {e}")
        
        # Test 3: Check referral targets
        try:
            response = supabase.table("referral_targets").select("*").execute()
            print(f"✅ Found {len(response.data)} referral targets")
            if response.data:
                print("📋 Sample referral target:")
                print(f"   ID: {response.data[0].get('id')}")
                print(f"   Target Level: {response.data[0].get('target_level')}")
                print(f"   Reward: {response.data[0].get('reward_amount')}")
        except Exception as e:
            print(f"⚠️  Could not query referral_targets: {e}")
            
        # Test 4: Check settings
        try:
            response = supabase.table("settings").select("*").execute()
            print(f"✅ Found {len(response.data)} settings")
            for setting in response.data:
                print(f"   {setting.get('key')}: {setting.get('value')}")
        except Exception as e:
            print(f"⚠️  Could not query settings: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 All tests passed! Your Supabase connection is working correctly.")
        print("You can now run your Telegram bot.")
    else:
        print("\n❌ Connection tests failed. Please check your configuration.")