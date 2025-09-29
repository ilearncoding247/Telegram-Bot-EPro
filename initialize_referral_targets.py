#!/usr/bin/env python3
"""
Script to initialize referral targets in Supabase
"""

import sys
import os

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def initialize_referral_targets():
    """Initialize referral targets in Supabase"""
    
    # Define default referral targets
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
    
    try:
        # Insert default referral targets
        response = supabase.table("referral_targets").insert(default_targets).execute()
        print(f"Successfully inserted {len(response.data)} referral targets")
        
        # Update settings to point to the first target as active
        settings_update = {
            "key": "active_referral_target_id",
            "value": "1"
        }
        
        # Insert or update the setting
        response = supabase.table("settings").upsert(settings_update).execute()
        print("Successfully set active referral target ID to 1")
        
        print("Referral targets initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing referral targets: {e}")
        return False

if __name__ == "__main__":
    print("Initializing referral targets in Supabase...")
    success = initialize_referral_targets()
    if success:
        print("Initialization completed successfully!")
        sys.exit(0)
    else:
        print("Initialization failed!")
        sys.exit(1)