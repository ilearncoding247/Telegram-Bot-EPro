-- Add is_active column to referrals table
ALTER TABLE referrals ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Add index for better performance
CREATE INDEX idx_referrals_is_active ON referrals(is_active);

-- Update existing referrals to be active by default
UPDATE referrals SET is_active = TRUE WHERE is_active IS NULL;

-- Add a comment to explain the column purpose
COMMENT ON COLUMN referrals.is_active IS 'Indicates if the referral is still active (user is still in the channel)';