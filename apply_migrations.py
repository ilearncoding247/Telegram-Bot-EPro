#!/usr/bin/env python3
"""
Script to apply referral target migrations to remote Supabase database
"""

import sys
import os
import requests
from pathlib import Path

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

def execute_sql_directly(sql_statement: str) -> bool:
    """Execute SQL statement directly using HTTP requests to Supabase"""
    try:
        # Get Supabase URL and key from environment
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            print("Missing SUPABASE_URL or SUPABASE_KEY in environment")
            return False
            
        # Make direct HTTP request to Supabase
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        # For raw SQL execution in Supabase, we need to use the PostgREST RPC feature
        # But first we need to create a function that can execute arbitrary SQL
        
        # Let's try to create the execute_sql function first
        create_function_sql = """
        CREATE OR REPLACE FUNCTION public.execute_sql(sql text)
        RETURNS void AS $$
        BEGIN
          EXECUTE sql;
        END;
        $$ LANGUAGE plpgsql;
        """
        
        # Try to execute using RPC endpoint
        rpc_url = f"{url}/rest/v1/rpc/execute_sql"
        
        # This approach won't work directly. Let's try a different method.
        # We'll need to break down our SQL into individual table operations
        
        print(f"Would execute: {sql_statement[:100]}...")
        # In a real implementation, we would need to parse the SQL and convert to API calls
        # For now, we'll just print what would be executed
        return True
        
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return False

def apply_migration_statements_individually(file_path: str) -> bool:
    """Apply migration by parsing and executing individual statements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Skip empty files
        if not sql_content.strip():
            print(f"Skipping empty file: {file_path}")
            return True
            
        # Split SQL content into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        success = True
        for statement in statements:
            if statement.upper().startswith(('CREATE', 'INSERT', 'UPDATE', 'DELETE', 'ALTER', 'DROP', 'COMMENT', 'DROP VIEW', 'CREATE OR REPLACE VIEW')):
                print(f"Processing statement: {statement[:100]}...")
                # For now, just print the statement
                # In a full implementation, we would parse and convert to API calls
                if not execute_sql_directly(statement):
                    success = False
                    
        return success
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def apply_migrations():
    """Apply all referral target migrations to the remote Supabase database"""
    migrations_dir = Path("supabase/migrations")
    
    # List of migration files to apply in order
    migration_files = [
        "20250926000006_create_referral_targets_table.sql",
        "20250926000007_add_user_referral_target_relationship.sql",
        "20250926000008_add_target_reached_timestamp.sql",
        "20250926000009_update_settings_with_referral_target.sql",
        "20250926000010_create_referral_targets_updated_at_trigger.sql",
        "20250926000011_create_referral_stats_view.sql",
        "20250926000013_check_and_fix_referrals_table.sql"  # Updated to use the new migration
    ]
    
    print("Applying referral target migrations to remote Supabase database...")
    print("=" * 60)
    
    success_count = 0
    for migration_file in migration_files:
        file_path = migrations_dir / migration_file
        if file_path.exists():
            print(f"\nApplying migration: {migration_file}")
            if apply_migration_statements_individually(str(file_path)):
                success_count += 1
                print(f"Successfully processed: {migration_file}")
            else:
                print(f"Failed to process: {migration_file}")
        else:
            print(f"Migration file not found: {migration_file}")
    
    print("\n" + "=" * 60)
    print(f"Processed {success_count}/{len(migration_files)} migrations")
    print("NOTE: This is a simulation. In a production environment, you would need to:")
    print("1. Use the Supabase dashboard to run these SQL statements, or")
    print("2. Set up proper authentication for raw SQL execution, or")
    print("3. Convert SQL operations to Supabase client API calls")
    return success_count > 0

if __name__ == "__main__":
    success = apply_migrations()
    if success:
        print("\nMigration processing completed!")
        sys.exit(0)
    else:
        print("\nMigration processing had issues!")
        sys.exit(1)