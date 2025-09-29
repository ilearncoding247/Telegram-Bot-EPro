#!/usr/bin/env python3
"""
Script to initialize referral targets data in Supabase
This script uses the existing Supabase client methods rather than raw SQL
"""

import sys
import os

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def initialize_referral_targets():
    """Initialize referral targets data in Supabase using client methods"""
    
    try:
        # Check if referral_targets table exists by trying to query it
        try:
            response = supabase.table("referral_targets").select("id").limit(1).execute()
            print("referral_targets table already exists")
        except Exception as e:
            print("referral_targets table does not exist yet. Please run the SQL migration first.")
            return False
        
        # Check if there are any existing referral targets
        response = supabase.table("referral_targets").select("id").execute()
        if not response.data:
            # Insert default referral targets
            default_targets = [
                {
                    "target_level": 5,
                    "reward_description": "Basic referral reward",
                    "reward_amount": 10.00,
                    "is_active": True
                },
                {
                    "target_level": 10,
                    "reward_description": "Silver referral reward",
                    "reward_amount": 25.00,
                    "is_active": True
                },
                {
                    "target_level": 25,
                    "reward_description": "Gold referral reward",
                    "reward_amount": 75.00,
                    "is_active": True
                },
                {
                    "target_level": 50,
                    "reward_description": "Platinum referral reward",
                    "reward_amount": 200.00,
                    "is_active": True
                }
            ]
            
            response = supabase.table("referral_targets").insert(default_targets).execute()
            print(f"Inserted {len(response.data)} default referral targets")
        else:
            print(f"Found {len(response.data)} existing referral targets")
        
        # Check if active_referral_target_id setting exists
        response = supabase.table("settings").select("value").eq("key", "active_referral_target_id").execute()
        if not response.data:
            # Insert the setting
            setting = {
                "key": "active_referral_target_id",
                "value": "1"
            }
            response = supabase.table("settings").insert(setting).execute()
            print("Inserted active_referral_target_id setting")
        else:
            print("active_referral_target_id setting already exists")
        
        # Update existing users to have referral_target_id = 1 if not set
        response = supabase.table("users").select("id").is_("referral_target_id", "null").execute()
        if response.data:
            user_ids = [user["id"] for user in response.data]
            print(f"Found {len(user_ids)} users without referral_target_id")
            
            # Update in batches to avoid timeouts
            batch_size = 100
            for i in range(0, len(user_ids), batch_size):
                batch = user_ids[i:i+batch_size]
                response = supabase.table("users").update({"referral_target_id": 1}).in_("id", batch).execute()
                print(f"Updated {len(response.data)} users with referral_target_id = 1")
        else:
            print("All users already have referral_target_id set")
        
        print("Referral targets data initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing referral targets data: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        # Try a simple query to test connection
        response = supabase.table("settings").select("key").limit(1).execute()
        print("Successfully connected to Supabase database")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Initializing referral targets data in Supabase...")
    
    if not test_connection():
        print("Cannot connect to database. Exiting.")
        sys.exit(1)
    
    success = initialize_referral_targets()
    if success:
        print("Initialization completed successfully!")
        sys.exit(0)
    else:
        print("Initialization failed!")
        sys.exit(1)