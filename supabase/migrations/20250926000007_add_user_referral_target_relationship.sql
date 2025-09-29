-- Add referral_target_id column to users table
ALTER TABLE users ADD COLUMN referral_target_id BIGINT REFERENCES referral_targets(id) DEFAULT 1;

-- Add index for better performance
CREATE INDEX idx_users_referral_target ON users(referral_target_id);

-- Update existing users to use the default referral target
UPDATE users SET referral_target_id = 1 WHERE referral_target_id IS NULL;

-- Add a comment to explain the column purpose
COMMENT ON COLUMN users.referral_target_id IS 'Reference to the referral target this user is working toward';