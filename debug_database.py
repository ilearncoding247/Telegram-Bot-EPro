#!/usr/bin/env python3
"""
Debug script to test database operations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.database import Database
from telegramreferralpro.referral_system import ReferralSystem

def test_database():
    """Test database operations"""
    print("🔧 Testing Database Operations...")
    
    # Initialize database
    print("\n1. Initializing database...")
    database = Database()
    print("   ✅ Database initialized")
    
    # Test adding a user
    print("\n2. Testing user addition...")
    test_user_id = 123456789
    referral_code = f"user_{test_user_id}_ref_test"
    
    success = database.add_user(
        user_id=test_user_id,
        username="test_user",
        first_name="Test",
        last_name="User",
        referral_code=referral_code
    )
    
    if success:
        print("   ✅ User addition reported as successful")
    else:
        print("   ❌ User addition failed")
    
    # Test retrieving the user
    print("\n3. Testing user retrieval...")
    user = database.get_user(test_user_id)
    if user:
        print(f"   ✅ User retrieved successfully: {user}")
    else:
        print("   ❌ Failed to retrieve user")
    
    # Test referral system
    print("\n4. Testing referral system...")
    referral_system = ReferralSystem(database)
    progress = referral_system.get_referral_progress(test_user_id)
    print(f"   ✅ Referral progress: {progress}")

if __name__ == "__main__":
    test_database()