-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at on referral_targets
CREATE TRIGGER update_referral_targets_updated_at 
    BEFORE UPDATE ON referral_targets 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();