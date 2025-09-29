-- Check if the users table has uuid or bigint id column
-- This migration handles both cases

-- First, add is_active column to referrals table
-- We need to handle the type mismatch between users.id (uuid) and referrals.referrer_id (bigint)

-- Drop the existing foreign key constraints if they exist
ALTER TABLE referrals DROP CONSTRAINT IF EXISTS referrals_referrer_id_fkey;
ALTER TABLE referrals DROP CONSTRAINT IF EXISTS referrals_referrer_id_fkey1;
ALTER TABLE referrals DROP CONSTRAINT IF EXISTS referrals_referred_id_fkey;
ALTER TABLE referrals DROP CONSTRAINT IF EXISTS referrals_referred_id_fkey1;

-- Check if referrer_id column exists and has correct type
-- If not, we need to recreate it with the correct type
DO $$
BEGIN
    -- Try to alter the column type
    ALTER TABLE referrals ALTER COLUMN referrer_id TYPE uuid USING referrer_id::uuid;
EXCEPTION WHEN undefined_column THEN
    -- If column doesn't exist, add it
    ALTER TABLE referrals ADD COLUMN referrer_id uuid REFERENCES users(id);
WHEN datatype_mismatch THEN
    -- If there's a type mismatch, drop and recreate the column
    ALTER TABLE referrals DROP COLUMN IF EXISTS referrer_id;
    ALTER TABLE referrals ADD COLUMN referrer_id uuid REFERENCES users(id);
END $$;

-- Do the same for referred_id column
DO $$
BEGIN
    -- Try to alter the column type
    ALTER TABLE referrals ALTER COLUMN referred_id TYPE uuid USING referred_id::uuid;
EXCEPTION WHEN undefined_column THEN
    -- If column doesn't exist, add it
    ALTER TABLE referrals ADD COLUMN referred_id uuid REFERENCES users(id);
WHEN datatype_mismatch THEN
    -- If there's a type mismatch, drop and recreate the column
    ALTER TABLE referrals DROP COLUMN IF EXISTS referred_id;
    ALTER TABLE referrals ADD COLUMN referred_id uuid REFERENCES users(id);
END $$;

-- Add is_active column to referrals table
ALTER TABLE referrals ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;

-- Add index for better performance
CREATE INDEX IF NOT EXISTS idx_referrals_is_active ON referrals(is_active);

-- Update existing referrals to be active by default
UPDATE referrals SET is_active = TRUE WHERE is_active IS NULL;

-- Add a comment to explain the column purpose
COMMENT ON COLUMN referrals.is_active IS 'Indicates if the referral is still active (user is still in the channel)';

-- Drop the existing views
DROP VIEW IF EXISTS referral_stats;
DROP VIEW IF EXISTS referral_stats_basic;

-- Create the referral_stats view
CREATE OR REPLACE VIEW referral_stats AS
SELECT 
    users.id as user_id,
    users.email,
    users.referral_code,
    COUNT(referrals.id) as total_referrals,
    COUNT(CASE WHEN referrals.is_active THEN 1 END) as active_referrals,
    COALESCE(referral_targets.target_level, 0) as target,
    CASE 
        WHEN COUNT(CASE WHEN referrals.is_active THEN 1 END) >= COALESCE(referral_targets.target_level, 0) THEN true 
        ELSE false 
    END as target_reached,
    users.target_reached_at
FROM users
LEFT JOIN referrals ON users.id = referrals.referrer_id
LEFT JOIN referral_targets ON users.referral_target_id = referral_targets.id
WHERE users.referral_code IS NOT NULL
GROUP BY users.id, users.email, users.referral_code, referral_targets.target_level, users.target_reached_at;

-- Add comment to explain the view purpose
COMMENT ON VIEW referral_stats IS 'View to get referral statistics for all users';