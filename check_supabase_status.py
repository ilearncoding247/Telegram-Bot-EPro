#!/usr/bin/env python3
"""
Simple Supabase status checker
Continuously checks Supabase connection and database status
"""

import sys
import os
import time
from datetime import datetime

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.supabase_client import supabase

def check_supabase_status():
    """Check Supabase connection and database status"""
    try:
        # Test 1: Basic connection
        response = supabase.table("settings").select("count").execute()
        
        # Test 2: Check all required tables
        tables = ["users", "referrals", "referral_targets", "settings"]
        table_status = {}
        
        for table in tables:
            try:
                resp = supabase.table(table).select("count", count="exact").execute()
                table_status[table] = {
                    "accessible": True,
                    "count": resp.count
                }
            except Exception as e:
                table_status[table] = {
                    "accessible": False,
                    "error": str(e)
                }
        
        return True, "Connected", table_status
        
    except Exception as e:
        return False, str(e), {}

def main():
    """Main function"""
    print("🔍 Supabase Status Checker")
    print("=" * 30)
    print("Press Ctrl+C to stop")
    print()
    
    check_count = 0
    
    try:
        while True:
            check_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            connected, message, table_status = check_supabase_status()
            
            # Clear screen (works on Windows and Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"📊 Supabase Status Check #{check_count}")
            print(f"🕒 Last checked: {timestamp}")
            print("=" * 40)
            
            if connected:
                print("✅ Supabase: CONNECTED")
                print()
                print("📋 Table Status:")
                for table, status in table_status.items():
                    if status["accessible"]:
                        print(f"   ✅ {table:20} | Records: {status['count']:4}")
                    else:
                        print(f"   ❌ {table:20} | Error: {status['error']}")
            else:
                print("❌ Supabase: DISCONNECTED")
                print(f"   Error: {message}")
            
            print()
            print("💡 Press Ctrl+C to stop")
            print("=" * 40)
            
            # Wait 5 seconds before next check
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Status checking stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()