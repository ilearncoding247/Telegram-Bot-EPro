#!/usr/bin/env python3
"""
Script to check what columns actually exist in the users table
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def check_columns():
    """Check what columns exist in the users table"""
    print("🔍 Checking Users Table Columns...")
    
    # Try different column combinations to see what exists
    columns_to_try = [
        "id",
        "username", 
        "referral_code",
        "created_at",
        "is_channel_member",
        "reward_claimed",
        "referred_by",
        "referral_target_id",
        "target_reached_at"
    ]
    
    for column in columns_to_try:
        try:
            response = supabase.table("users").select(column).limit(1).execute()
            print(f"   ✅ Column '{column}' exists")
        except Exception as e:
            if "does not exist" in str(e):
                print(f"   ❌ Column '{column}' does not exist")
            else:
                # Column exists but there might be other issues
                print(f"   ⚠️ Column '{column}' might exist (other error: {type(e).__name__})")

if __name__ == "__main__":
    check_columns()