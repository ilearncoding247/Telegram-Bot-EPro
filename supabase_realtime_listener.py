#!/usr/bin/env python3
"""
Advanced Supabase real-time listener
This script demonstrates how to use Supabase real-time subscriptions to listen for database changes
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

# Supabase real-time requires additional setup
try:
    from supabase import create_client, Client
    import websockets
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False
    print("⚠️  Real-time dependencies not available. Install with: pip install websockets")

if REALTIME_AVAILABLE:
    from telegramreferralpro.supabase_client import supabase

class SupabaseRealtimeListener:
    def __init__(self):
        self.running = False
        self.listeners = []
        
    async def listen_for_users(self):
        """Listen for changes to the users table"""
        try:
            print("👂 Setting up listener for users table...")
            
            # Define callback for user changes
            def handle_user_changes(payload):
                print(f"\n👤 User change detected at {datetime.now().strftime('%H:%M:%S')}:")
                print(f"   Event: {payload['eventType']}")
                print(f"   Record ID: {payload['new'].get('id', 'N/A')}")
                print(f"   User ID: {payload['new'].get('user_id', 'N/A')}")
                print(f"   Username: {payload['new'].get('username', 'N/A')}")
                print("-" * 40)
            
            # Set up the subscription
            users_listener = supabase.table('users').on('*', handle_user_changes).subscribe()
            self.listeners.append(users_listener)
            
            print("✅ Users table listener active")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up users listener: {e}")
            return False
    
    async def listen_for_referrals(self):
        """Listen for changes to the referrals table"""
        try:
            print("👂 Setting up listener for referrals table...")
            
            # Define callback for referral changes
            def handle_referral_changes(payload):
                print(f"\n👥 Referral change detected at {datetime.now().strftime('%H:%M:%S')}:")
                print(f"   Event: {payload['eventType']}")
                print(f"   Record ID: {payload['new'].get('id', 'N/A')}")
                print(f"   Referrer ID: {payload['new'].get('referrer_id', 'N/A')}")
                print(f"   Referred ID: {payload['new'].get('referred_id', 'N/A')}")
                print("-" * 40)
            
            # Set up the subscription
            referrals_listener = supabase.table('referrals').on('*', handle_referral_changes).subscribe()
            self.listeners.append(referrals_listener)
            
            print("✅ Referrals table listener active")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up referrals listener: {e}")
            return False
    
    async def listen_for_referral_targets(self):
        """Listen for changes to the referral_targets table"""
        try:
            print("👂 Setting up listener for referral_targets table...")
            
            # Define callback for referral target changes
            def handle_target_changes(payload):
                print(f"\n🎯 Referral target change detected at {datetime.now().strftime('%H:%M:%S')}:")
                print(f"   Event: {payload['eventType']}")
                print(f"   Record ID: {payload['new'].get('id', 'N/A')}")
                print(f"   Target Level: {payload['new'].get('target_level', 'N/A')}")
                print(f"   Is Active: {payload['new'].get('is_active', 'N/A')}")
                print("-" * 40)
            
            # Set up the subscription
            targets_listener = supabase.table('referral_targets').on('*', handle_target_changes).subscribe()
            self.listeners.append(targets_listener)
            
            print("✅ Referral targets table listener active")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up referral targets listener: {e}")
            return False
    
    async def test_connection(self):
        """Test the Supabase connection"""
        try:
            # Test basic connection by querying settings table
            response = supabase.table("settings").select("key, value").limit(1).execute()
            print("✅ Supabase connection test successful!")
            return True
        except Exception as e:
            print(f"❌ Supabase connection test failed: {e}")
            return False
    
    async def start_listening(self):
        """Start all listeners"""
        print("🚀 Starting Supabase real-time listeners...")
        print("=" * 50)
        
        # Test connection first
        if not await self.test_connection():
            return False
        
        # Set up listeners
        listeners_setup = []
        listeners_setup.append(await self.listen_for_users())
        listeners_setup.append(await self.listen_for_referrals())
        listeners_setup.append(await self.listen_for_referral_targets())
        
        if not any(listeners_setup):
            print("❌ No listeners could be set up")
            return False
        
        success_count = sum(listeners_setup)
        print(f"✅ {success_count}/3 listeners active")
        print("\n👂 Listening for real-time changes...")
        print("💡 Press Ctrl+C to stop")
        print("=" * 50)
        
        self.running = True
        try:
            # Keep the script running
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping listeners...")
            await self.stop_listening()
            return True
        except Exception as e:
            print(f"❌ Error in listening loop: {e}")
            await self.stop_listening()
            return False
    
    async def stop_listening(self):
        """Stop all listeners"""
        print("🧹 Cleaning up listeners...")
        for listener in self.listeners:
            try:
                supabase.remove_subscription(listener)
            except Exception as e:
                print(f"⚠️  Error removing listener: {e}")
        
        self.listeners = []
        self.running = False
        print("✅ All listeners stopped")

async def main():
    """Main async function"""
    if not REALTIME_AVAILABLE:
        print("❌ Real-time functionality not available")
        print("💡 Install required dependencies: pip install websockets")
        return
    
    print("🚀 Supabase Real-time Listener")
    print("=" * 30)
    
    # Create listener instance
    listener = SupabaseRealtimeListener()
    
    try:
        # Start listening
        await listener.start_listening()
        print("\n✅ Real-time listening completed")
    except KeyboardInterrupt:
        print("\n🛑 Real-time listening interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def sync_main():
    """Synchronous main function for compatibility"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    sync_main()