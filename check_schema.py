#!/usr/bin/env python3
"""
Script to check the actual database schema
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def check_schema():
    """Check the actual database schema"""
    print("🔍 Checking Database Schema...")
    
    try:
        # Try to get information about the users table
        print("\n1. Checking users table structure...")
        response = supabase.table("users").select("*").limit(1).execute()
        print(f"   ✅ Successfully queried users table")
        print(f"   Sample data: {response.data[0] if response.data else 'No data'}")
        
        # Try to get column information
        print("\n2. Checking available columns...")
        # This is a workaround to see what columns are available
        try:
            response = supabase.table("users").select("id,user_id,username,referral_code").limit(1).execute()
            print(f"   ✅ Successfully queried specific columns")
            print(f"   Column data: {response.data[0] if response.data else 'No data'}")
        except Exception as e:
            print(f"   ❌ Error querying specific columns: {e}")
            
        # Try a simple insert to see what works
        print("\n3. Testing simple insert...")
        test_data = {
            "referral_code": "test_referral_code_123"
        }
        response = supabase.table("users").insert(test_data).execute()
        print(f"   ✅ Successfully inserted test data: {response.data}")
        
        # Clean up test data
        if response.data:
            user_id = response.data[0]['id']
            supabase.table("users").delete().eq("id", user_id).execute()
            print(f"   🧹 Cleaned up test data")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    check_schema()