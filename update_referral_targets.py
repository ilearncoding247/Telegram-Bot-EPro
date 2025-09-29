#!/usr/bin/env python3
"""
Script to update referral targets in Supabase
"""

import sys
import os
from typing import List, Dict

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def get_all_referral_targets() -> List[Dict]:
    """Get all referral targets from Supabase"""
    try:
        response = supabase.table("referral_targets").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error getting referral targets: {e}")
        return []

def add_referral_target(target_level: int, reward_description: str, reward_amount: float, is_active: bool = True) -> bool:
    """Add a new referral target"""
    try:
        new_target = {
            "target_level": target_level,
            "reward_description": reward_description,
            "reward_amount": reward_amount,
            "is_active": is_active
        }
        
        response = supabase.table("referral_targets").insert(new_target).execute()
        print(f"Successfully added referral target: {target_level}")
        return True
    except Exception as e:
        print(f"Error adding referral target {target_level}: {e}")
        return False

def update_referral_target(target_id: int, target_level: int = None, reward_description: str = None, 
                          reward_amount: float = None, is_active: bool = None) -> bool:
    """Update an existing referral target"""
    try:
        update_data = {}
        if target_level is not None:
            update_data["target_level"] = target_level
        if reward_description is not None:
            update_data["reward_description"] = reward_description
        if reward_amount is not None:
            update_data["reward_amount"] = reward_amount
        if is_active is not None:
            update_data["is_active"] = is_active
            
        if not update_data:
            print("No update data provided")
            return False
            
        response = supabase.table("referral_targets").update(update_data).eq("id", target_id).execute()
        print(f"Successfully updated referral target ID {target_id}")
        return True
    except Exception as e:
        print(f"Error updating referral target {target_id}: {e}")
        return False

def set_active_referral_target(target_id: int) -> bool:
    """Set the active referral target"""
    try:
        # Update settings to point to the new active target
        settings_update = {
            "key": "active_referral_target_id",
            "value": str(target_id)
        }
        
        response = supabase.table("settings").upsert(settings_update).execute()
        print(f"Successfully set active referral target ID to {target_id}")
        return True
    except Exception as e:
        print(f"Error setting active referral target: {e}")
        return False

def main():
    """Main function to demonstrate usage"""
    print("Referral Targets Management Script")
    print("=================================")
    
    # Show current referral targets
    print("\nCurrent Referral Targets:")
    targets = get_all_referral_targets()
    if targets:
        for target in targets:
            status = "ACTIVE" if target["is_active"] else "INACTIVE"
            print(f"ID: {target['id']}, Level: {target['target_level']}, "
                  f"Reward: ${target['reward_amount']}, Status: {status}")
    else:
        print("No referral targets found")
    
    # Example of adding a new target
    # Uncomment the following lines to add a new target:
    # print("\nAdding new referral target...")
    # add_referral_target(100, "Diamond referral reward", 500.00, True)
    
    # Example of updating a target
    # Uncomment the following lines to update a target:
    # print("\nUpdating referral target...")
    # update_referral_target(1, reward_amount=15.00)
    
    # Example of setting active target
    # Uncomment the following lines to set active target:
    # print("\nSetting active referral target...")
    # set_active_referral_target(2)

if __name__ == "__main__":
    main()