-- ============================================
-- HIMAP User Management & Authentication System
-- ============================================
-- This migration adds user management tables and RLS policies
-- for admin and member authentication

-- ============================================
-- 1. USER PROFILES TABLE
-- ============================================
-- Links Supabase Auth users to BPO companies and roles

CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    bpo_id UUID REFERENCES bpos(id) ON DELETE SET NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'member')),
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id),
    
    UNIQUE(user_id),
    UNIQUE(email)
);

-- Index for faster lookups
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_bpo_id ON user_profiles(bpo_id);
CREATE INDEX idx_user_profiles_role ON user_profiles(role);
CREATE INDEX idx_user_profiles_email ON user_profiles(email);

-- ============================================
-- 2. AUDIT LOGS TABLE
-- ============================================
-- Track all data modifications for compliance

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for querying logs
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_table_name ON audit_logs(table_name);
CREATE INDEX idx_audit_logs_record_id ON audit_logs(record_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- ============================================
-- 3. RLS POLICIES FOR USER_PROFILES
-- ============================================

-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Admin can see all profiles
CREATE POLICY "Admins can view all user profiles"
ON user_profiles FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.role = 'admin'
        AND up.is_active = true
    )
);

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
ON user_profiles FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- Only admins can create new profiles
CREATE POLICY "Admins can create user profiles"
ON user_profiles FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.role = 'admin'
        AND up.is_active = true
    )
);

-- Admins can update all profiles, users can update their own
CREATE POLICY "Admins can update all profiles, users can update own"
ON user_profiles FOR UPDATE
TO authenticated
USING (
    user_id = auth.uid()
    OR EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.role = 'admin'
        AND up.is_active = true
    )
);

-- ============================================
-- 4. RLS POLICIES FOR AUDIT_LOGS
-- ============================================

ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Only admins can view audit logs
CREATE POLICY "Admins can view audit logs"
ON audit_logs FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.role = 'admin'
        AND up.is_active = true
    )
);

-- System can insert audit logs (will be done via triggers)
CREATE POLICY "System can insert audit logs"
ON audit_logs FOR INSERT
TO authenticated
WITH CHECK (true);

-- ============================================
-- 5. UPDATE RLS POLICIES FOR BPOS TABLE
-- ============================================

-- Allow members to update their assigned company
CREATE POLICY "Members can update their assigned company"
ON bpos FOR UPDATE
TO authenticated
USING (
    -- User must be an active member assigned to this company
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpos.id
        AND up.role = 'member'
        AND up.is_active = true
    )
    -- OR user is an admin
    OR EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.role = 'admin'
        AND up.is_active = true
    )
);

-- ============================================
-- 6. UPDATE RLS POLICIES FOR RELATED TABLES
-- ============================================

-- BPO Services
CREATE POLICY "Members can update their company services"
ON bpo_services FOR UPDATE
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_services.bpo_id
        AND up.is_active = true
    )
);

CREATE POLICY "Members can insert their company services"
ON bpo_services FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_services.bpo_id
        AND up.is_active = true
    )
);

-- BPO Media (for logo uploads)
CREATE POLICY "Members can update their company media"
ON bpo_media FOR UPDATE
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_media.bpo_id
        AND up.is_active = true
    )
);

CREATE POLICY "Members can insert their company media"
ON bpo_media FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_media.bpo_id
        AND up.is_active = true
    )
);

-- BPO Locations
CREATE POLICY "Members can update their company locations"
ON bpo_locations FOR UPDATE
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_locations.bpo_id
        AND up.is_active = true
    )
);

CREATE POLICY "Members can insert their company locations"
ON bpo_locations FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_locations.bpo_id
        AND up.is_active = true
    )
);

-- BPO Certifications
CREATE POLICY "Members can update their company certifications"
ON bpo_certifications FOR UPDATE
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_certifications.bpo_id
        AND up.is_active = true
    )
);

CREATE POLICY "Members can insert their company certifications"
ON bpo_certifications FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_certifications.bpo_id
        AND up.is_active = true
    )
);

-- BPO Personnel
CREATE POLICY "Members can update their company personnel"
ON bpo_personnel FOR UPDATE
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_personnel.bpo_id
        AND up.is_active = true
    )
);

CREATE POLICY "Members can insert their company personnel"
ON bpo_personnel FOR INSERT
TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM user_profiles up
        WHERE up.user_id = auth.uid()
        AND up.bpo_id = bpo_personnel.bpo_id
        AND up.is_active = true
    )
);

-- ============================================
-- 7. HELPER FUNCTIONS
-- ============================================

-- Function to check if current user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
        AND is_active = true
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user's assigned BPO
CREATE OR REPLACE FUNCTION get_user_bpo_id()
RETURNS UUID AS $$
BEGIN
    RETURN (
        SELECT bpo_id FROM user_profiles
        WHERE user_id = auth.uid()
        AND is_active = true
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- 8. TRIGGER FOR AUDIT LOGGING
-- ============================================

-- Function to log changes
CREATE OR REPLACE FUNCTION log_audit()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        user_id,
        table_name,
        record_id,
        action,
        old_values,
        new_values
    ) VALUES (
        auth.uid(),
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply audit trigger to important tables
CREATE TRIGGER audit_bpos
    AFTER INSERT OR UPDATE OR DELETE ON bpos
    FOR EACH ROW EXECUTE FUNCTION log_audit();

CREATE TRIGGER audit_bpo_services
    AFTER INSERT OR UPDATE OR DELETE ON bpo_services
    FOR EACH ROW EXECUTE FUNCTION log_audit();

CREATE TRIGGER audit_bpo_media
    AFTER INSERT OR UPDATE OR DELETE ON bpo_media
    FOR EACH ROW EXECUTE FUNCTION log_audit();

-- ============================================
-- MIGRATION COMPLETE
-- ============================================
-- Next steps:
-- 1. Enable email/password auth in Supabase dashboard
-- 2. Configure email templates for password reset
-- 3. Create initial admin user via Supabase dashboard
