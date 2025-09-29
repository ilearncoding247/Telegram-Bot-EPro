#!/usr/bin/env python3
"""
Real-time Supabase connection monitor and tester
This script continuously tests the Supabase connection and monitors database changes
"""

import sys
import os
import time
import threading
from datetime import datetime

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase
from telegramreferralpro.database import Database

class SupabaseMonitor:
    def __init__(self):
        self.db = Database()
        self.running = False
        self.connection_status = "Unknown"
        
    def test_connection(self):
        """Test the Supabase connection"""
        try:
            # Test basic connection by querying settings table
            response = supabase.table("settings").select("key, value").limit(1).execute()
            return True, "Connected successfully"
        except Exception as e:
            return False, str(e)
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            stats = {}
            
            # Get user count
            try:
                response = supabase.table("users").select("count", count="exact").execute()
                stats['users'] = response.count
            except:
                stats['users'] = "Error"
            
            # Get referral count
            try:
                response = supabase.table("referrals").select("count", count="exact").execute()
                stats['referrals'] = response.count
            except:
                stats['referrals'] = "Error"
            
            # Get referral targets
            try:
                response = supabase.table("referral_targets").select("id, target_level, is_active").execute()
                stats['referral_targets'] = len(response.data)
                stats['active_targets'] = sum(1 for target in response.data if target.get('is_active'))
            except:
                stats['referral_targets'] = "Error"
                stats['active_targets'] = "Error"
            
            # Get settings
            try:
                response = supabase.table("settings").select("key, value").execute()
                stats['settings'] = {item['key']: item['value'] for item in response.data}
            except:
                stats['settings'] = "Error"
                
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def monitor_changes(self):
        """Monitor database changes in real-time"""
        print("🔍 Setting up real-time monitoring...")
        
        try:
            # This is a simplified monitoring approach
            # In a full implementation, you would use Supabase real-time subscriptions
            print("✅ Real-time monitoring initialized")
            print("💡 Note: This script polls for changes. For true real-time, implement Supabase Realtime subscriptions.")
            return True
        except Exception as e:
            print(f"❌ Error setting up real-time monitoring: {e}")
            return False
    
    def run_monitoring_loop(self):
        """Run the continuous monitoring loop"""
        print("🚀 Starting real-time Supabase monitoring...")
        print("=" * 60)
        
        last_stats = None
        
        while self.running:
            try:
                # Test connection
                connected, message = self.test_connection()
                self.connection_status = "✅ Connected" if connected else f"❌ Disconnected: {message}"
                
                # Get database stats
                stats = self.get_database_stats()
                
                # Clear screen (works on Windows and Unix)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Display current status
                print(f"📊 Supabase Real-time Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 60)
                print(f"📡 Connection Status: {self.connection_status}")
                print()
                
                if "error" in stats:
                    print(f"❌ Error getting database stats: {stats['error']}")
                else:
                    print("📈 Database Statistics:")
                    print(f"   Users: {stats.get('users', 'N/A')}")
                    print(f"   Referrals: {stats.get('referrals', 'N/A')}")
                    print(f"   Referral Targets: {stats.get('referral_targets', 'N/A')} (Active: {stats.get('active_targets', 'N/A')})")
                    print()
                    
                    if stats.get('settings') and isinstance(stats['settings'], dict):
                        print("⚙️  Settings:")
                        for key, value in stats['settings'].items():
                            print(f"   {key}: {value}")
                        print()
                
                # Show instructions
                print("💡 Press Ctrl+C to stop monitoring")
                print("=" * 60)
                
                # Wait before next update
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(5)
    
    def start(self):
        """Start the monitoring"""
        # Test initial connection
        print("🔍 Testing initial Supabase connection...")
        connected, message = self.test_connection()
        if not connected:
            print(f"❌ Initial connection failed: {message}")
            return False
        
        print("✅ Initial connection successful!")
        
        # Setup monitoring
        if not self.monitor_changes():
            print("⚠️  Continuing without real-time monitoring...")
        
        # Start monitoring loop
        self.running = True
        try:
            self.run_monitoring_loop()
            return True
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            return True
        except Exception as e:
            print(f"❌ Error in monitoring: {e}")
            return False
    
    def stop(self):
        """Stop the monitoring"""
        self.running = False

def main():
    """Main function"""
    print("🚀 Supabase Real-time Connection Monitor")
    print("=" * 50)
    
    # Create monitor instance
    monitor = SupabaseMonitor()
    
    try:
        # Start monitoring
        success = monitor.start()
        if success:
            print("\n✅ Monitoring completed successfully")
        else:
            print("\n❌ Monitoring encountered errors")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()