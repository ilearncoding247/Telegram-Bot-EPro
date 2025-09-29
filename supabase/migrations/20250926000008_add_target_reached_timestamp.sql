-- Add target_reached_at column to users table
ALTER TABLE users ADD COLUMN target_reached_at TIMESTAMPTZ;

-- Add index for better performance
CREATE INDEX idx_users_target_reached ON users(target_reached_at);

-- Add a comment to explain the column purpose
COMMENT ON COLUMN users.target_reached_at IS 'Timestamp when the user reached their referral target';