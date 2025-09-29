-- Create a view for referral statistics
CREATE OR REPLACE VIEW referral_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.referral_code,
    COUNT(r.id) as total_referrals,
    COUNT(r.id) as active_referrals,  -- Temporarily use total count since is_active column doesn't exist yet
    rt.target_level as target,
    CASE 
        WHEN COUNT(r.id) >= rt.target_level THEN true 
        ELSE false 
    END as target_reached,
    u.target_reached_at
FROM users u
LEFT JOIN referrals r ON u.id = r.referrer_id
LEFT JOIN referral_targets rt ON u.referral_target_id = rt.id
WHERE u.referral_code IS NOT NULL
GROUP BY u.id, u.email, u.referral_code, rt.target_level, u.target_reached_at;

-- Add comment to explain the view purpose
COMMENT ON VIEW referral_stats IS 'View to get referral statistics for all users';