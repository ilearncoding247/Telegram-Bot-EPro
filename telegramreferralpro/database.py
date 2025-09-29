from .supabase_client import supabase
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = supabase
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                 last_name: str = None, referral_code: str = None, referred_by: int = None) -> bool:
        """Add a new user to the database"""
        try:
            self.client.table("users").insert({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "referral_code": referral_code,
                "referred_by": referred_by
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user by ID"""
        try:
            response = self.client.table("users").select("*").eq("user_id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def get_user_by_referral_code(self, referral_code: str) -> Optional[dict]:
        """Get user by referral code"""
        try:
            response = self.client.table("users").select("*").eq("referral_code", referral_code).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user by referral code {referral_code}: {e}")
            return None
    
    def update_channel_membership(self, user_id: int, is_member: bool) -> bool:
        """Update user's channel membership status"""
        try:
            self.client.table("users").update({"is_channel_member": is_member}).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating channel membership for user {user_id}: {e}")
            return False
    
    def add_referral(self, referrer_id: int, referred_user_id: int) -> bool:
        """Add a referral relationship"""
        try:
            # Add is_active field with default value True
            self.client.table("referrals").insert({
                "referrer_id": referrer_id,
                "referred_id": referred_user_id,
                "is_active": True  # Add this field
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error adding referral: {e}")
            return False
    
    def get_referral_stats(self, user_id: int) -> Tuple[int, int]:
        """Get referral statistics for a user (active referrals, total referrals)"""
        try:
            # First try to get stats with is_active column
            try:
                response = self.client.table("referrals").select("id").eq("referrer_id", user_id).execute()
                total_count = len(response.data)

                response = self.client.table("referrals").select("id").eq("referrer_id", user_id).eq("is_active", True).execute()
                active_count = len(response.data)
            except Exception as e:
                # Fallback if is_active column doesn't exist yet
                logger.warning(f"is_active column not found, using fallback method: {e}")
                response = self.client.table("referrals").select("id").eq("referrer_id", user_id).execute()
                total_count = len(response.data)
                active_count = total_count  # Assume all are active if column doesn't exist
            
            return active_count, total_count
        except Exception as e:
            logger.error(f"Error getting referral stats for user {user_id}: {e}")
            return 0, 0
    
    def deactivate_referral(self, referrer_id: int, referred_user_id: int) -> bool:
        """Deactivate a referral when user leaves channel"""
        try:
            # Try to update with is_active field
            try:
                self.client.table("referrals").update({"is_active": False}).eq("referrer_id", referrer_id).eq("referred_id", referred_user_id).execute()
            except Exception as e:
                # Fallback if is_active column doesn't exist yet
                logger.warning(f"Could not update is_active column: {e}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating referral: {e}")
            return False
    
    def mark_reward_claimed(self, user_id: int) -> bool:
        """Mark reward as claimed for a user"""
        try:
            self.client.table("users").update({"reward_claimed": True}).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking reward claimed for user {user_id}: {e}")
            return False
    
    def get_all_users_count(self) -> int:
        """Get total number of users"""
        try:
            response = self.client.table("users").select("id", count="exact").execute()
            return response.count
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0

    def get_channel_members_count(self) -> int:
        """Get number of active channel members"""
        try:
            response = self.client.table("users").select("id", count="exact").eq("is_channel_member", True).execute()
            return response.count
        except Exception as e:
            logger.error(f"Error getting channel members count: {e}")
            return 0
    
    def get_active_referral_target(self) -> Optional[int]:
        """Get the current active referral target from referral_targets table"""
        try:
            # First try to get the active referral target ID from settings
            settings_response = self.client.table("settings").select("value").eq("key", "active_referral_target_id").execute()
            if settings_response.data:
                target_id = int(settings_response.data[0]["value"])
                
                # Get the target level from referral_targets table
                target_response = self.client.table("referral_targets").select("target_level").eq("id", target_id).eq("is_active", True).execute()
                if target_response.data:
                    return target_response.data[0]["target_level"]
            
            # Fallback to old method
            response = self.client.table("settings").select("value").eq("key", "referral_target").execute()
            if response.data:
                return int(response.data[0]["value"])
            
            return None
        except Exception as e:
            logger.error(f"Error getting active referral target: {e}")
            return None
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value by key"""
        try:
            response = self.client.table("settings").select("value").eq("key", key).execute()
            return response.data[0]["value"] if response.data else None
        except Exception as e:
            logger.error(f"Error getting setting {key}: {e}")
            return None
    
    def get_referral_target_by_id(self, target_id: int) -> Optional[dict]:
        """Get referral target by ID"""
        try:
            response = self.client.table("referral_targets").select("*").eq("id", target_id).eq("is_active", True).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting referral target {target_id}: {e}")
            return None
    
    def get_all_referral_targets(self) -> list:
        """Get all active referral targets"""
        try:
            response = self.client.table("referral_targets").select("*").eq("is_active", True).order("target_level").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting referral targets: {e}")
            return []
    
    def update_user_referral_target(self, user_id: int, target_id: int) -> bool:
        """Update user's referral target"""
        try:
            self.client.table("users").update({"referral_target_id": target_id}).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating user {user_id} referral target: {e}")
            return False
    
    def mark_target_reached(self, user_id: int) -> bool:
        """Mark that user has reached their referral target"""
        try:
            from datetime import datetime
            self.client.table("users").update({"target_reached_at": datetime.utcnow().isoformat()}).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking target reached for user {user_id}: {e}")
            return False