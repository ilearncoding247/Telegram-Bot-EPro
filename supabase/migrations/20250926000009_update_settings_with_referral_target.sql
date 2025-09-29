-- Update the settings table to reference the referral_targets table
INSERT INTO settings (key, value) VALUES ('active_referral_target_id', '1')
ON CONFLICT (key) DO UPDATE SET value = '1';

-- Add comment to explain the setting
COMMENT ON TABLE settings IS 'Application settings including the active referral target';