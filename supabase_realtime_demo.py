#!/usr/bin/env python3
"""
Supabase real-time demo script
Demonstrates real-time database operations and monitoring
"""

import sys
import os
import time
import threading
from datetime import datetime
import json

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase
from telegramreferralpro.database import Database

def test_connection():
    """Test Supabase connection"""
    try:
        response = supabase.table("settings").select("key, value").limit(1).execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def get_database_info():
    """Get comprehensive database information"""
    info = {
        'timestamp': datetime.now().isoformat(),
        'tables': {}
    }
    
    tables = ['users', 'referrals', 'referral_targets', 'settings']
    
    for table in tables:
        try:
            response = supabase.table(table).select("count", count="exact").execute()
            info['tables'][table] = {
                'count': response.count,
                'status': 'accessible'
            }
        except Exception as e:
            info['tables'][table] = {
                'count': 0,
                'status': f'error: {str(e)}'
            }
    
    return info

def insert_test_user():
    """Insert a test user record"""
    try:
        # Generate a unique user ID for testing
        import random
        test_user_id = random.randint(1000000, 9999999)
        
        user_data = {
            "user_id": test_user_id,
            "username": f"test_user_{test_user_id}",
            "referral_code": f"ref_{test_user_id}",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = supabase.table("users").insert(user_data).execute()
        print(f"✅ Inserted test user with ID: {test_user_id}")
        return response.data[0]['id'] if response.data else None
    except Exception as e:
        print(f"❌ Error inserting test user: {e}")
        return None

def update_test_user(user_db_id):
    """Update a test user record"""
    try:
        if not user_db_id:
            return False
            
        update_data = {
            "username": f"updated_test_user_{int(time.time())}",
            "updated_at": "now()"
        }
        
        response = supabase.table("users").update(update_data).eq("id", user_db_id).execute()
        print("✅ Updated test user")
        return True
    except Exception as e:
        print(f"❌ Error updating test user: {e}")
        return False

def delete_test_user(user_db_id):
    """Delete a test user record"""
    try:
        if not user_db_id:
            return False
            
        response = supabase.table("users").delete().eq("id", user_db_id).execute()
        print("✅ Deleted test user")
        return True
    except Exception as e:
        print(f"❌ Error deleting test user: {e}")
        return False

def demonstrate_crud_operations():
    """Demonstrate CRUD operations"""
    print("\n🧪 Demonstrating CRUD operations...")
    print("-" * 40)
    
    # Insert
    user_db_id = insert_test_user()
    time.sleep(1)  # Wait a moment
    
    # Update
    if user_db_id:
        update_test_user(user_db_id)
        time.sleep(1)  # Wait a moment
    
    # Show current state
    info = get_database_info()
    print(f"Users count: {info['tables']['users']['count']}")
    
    # Delete
    if user_db_id:
        delete_test_user(user_db_id)
        time.sleep(1)  # Wait a moment
    
    # Show final state
    info = get_database_info()
    print(f"Users count after cleanup: {info['tables']['users']['count']}")

def monitor_database_continuously(duration=60):
    """Monitor database changes continuously for a specified duration"""
    print(f"\n👁️  Monitoring database for {duration} seconds...")
    print("-" * 50)
    
    start_time = time.time()
    
    while (time.time() - start_time) < duration:
        try:
            info = get_database_info()
            
            # Clear screen (works on Windows and Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"📊 Database Monitor - {info['timestamp']}")
            print("=" * 50)
            
            for table, data in info['tables'].items():
                status_icon = "✅" if data['status'] == 'accessible' else "❌"
                print(f"{status_icon} {table:20} | Count: {data['count']:4} | Status: {data['status']}")
            
            print("\n💡 Press Ctrl+C to stop early")
            print("=" * 50)
            
            time.sleep(3)  # Update every 3 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in monitoring: {e}")
            time.sleep(3)

def show_referral_targets():
    """Display current referral targets"""
    try:
        response = supabase.table("referral_targets").select("*").order("target_level").execute()
        
        print("\n🎯 Current Referral Targets:")
        print("-" * 40)
        
        if response.data:
            for target in response.data:
                status = "🟢 Active" if target.get('is_active') else "🔴 Inactive"
                print(f"ID: {target.get('id'):2} | Level: {target.get('target_level'):2} | "
                      f"Reward: ${target.get('reward_amount', 0):6.2f} | {status}")
        else:
            print("No referral targets found")
            
    except Exception as e:
        print(f"❌ Error fetching referral targets: {e}")

def show_settings():
    """Display current settings"""
    try:
        response = supabase.table("settings").select("*").execute()
        
        print("\n⚙️  Current Settings:")
        print("-" * 30)
        
        if response.data:
            for setting in response.data:
                print(f"{setting.get('key'):25} | {setting.get('value')}")
        else:
            print("No settings found")
            
    except Exception as e:
        print(f"❌ Error fetching settings: {e}")

def main():
    """Main function"""
    print("🚀 Supabase Real-time Demo Script")
    print("=" * 40)
    
    # Test connection
    if not test_connection():
        return
    
    # Show current database state
    info = get_database_info()
    print(f"\n📊 Initial Database State:")
    for table, data in info['tables'].items():
        print(f"   {table}: {data['count']} records")
    
    # Show referral targets
    show_referral_targets()
    
    # Show settings
    show_settings()
    
    # Demonstrate CRUD operations
    demonstrate_crud_operations()
    
    # Monitor for a short period
    monitor_database_continuously(30)
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()