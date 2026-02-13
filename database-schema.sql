-- HIMAP Member Directory Database Schema
-- Supabase / PostgreSQL Migration Script

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1️⃣ MAIN TABLE: BPOs (Core Company Information)
-- ============================================
CREATE TABLE bpos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL,
    trade_name TEXT,
    year_established INTEGER,
    registration_number TEXT,
    headquarters_address TEXT,
    city TEXT,
    province TEXT,
    country TEXT DEFAULT 'Philippines',
    website_url TEXT,
    linkedin_url TEXT,
    email TEXT,
    contact_number TEXT,
    company_description TEXT,
    mission TEXT,
    vision TEXT,
    total_employees INTEGER,
    healthcare_fte_count INTEGER,
    ownership_type TEXT,
    parent_company TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2️⃣ SERVICES & CAPABILITIES
-- ============================================
CREATE TABLE bpo_services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    service_category TEXT NOT NULL,
    service_name TEXT NOT NULL,
    description TEXT,
    certifications_required TEXT,
    tools_used TEXT,
    is_primary_service BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bpo_services_bpo_id ON bpo_services(bpo_id);

-- ============================================
-- 3️⃣ CLIENT & MARKET PROFILE
-- ============================================
CREATE TABLE bpo_clients_profile (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE UNIQUE,
    target_market TEXT,
    client_types TEXT,
    average_client_size TEXT,
    no_of_active_clients INTEGER,
    largest_client_type TEXT,
    years_serving_healthcare INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 4️⃣ OPERATIONS DETAILS
-- ============================================
CREATE TABLE bpo_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE UNIQUE,
    number_of_sites INTEGER,
    delivery_model TEXT,
    work_shifts TEXT,
    compliance_frameworks TEXT,
    data_security_measures TEXT,
    business_continuity_plan TEXT,
    disaster_recovery_site BOOLEAN,
    ehr_systems_supported TEXT,
    billing_platforms_supported TEXT,
    coding_systems_supported TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 5️⃣ LOCATIONS
-- ============================================
CREATE TABLE bpo_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    location_name TEXT,
    address TEXT,
    city TEXT,
    province TEXT,
    country TEXT,
    headcount INTEGER,
    is_headquarters BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bpo_locations_bpo_id ON bpo_locations(bpo_id);

-- ============================================
-- 6️⃣ CERTIFICATIONS & ACCREDITATIONS
-- ============================================
CREATE TABLE bpo_certifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    certification_name TEXT NOT NULL,
    issuing_body TEXT,
    valid_from DATE,
    valid_until DATE,
    certificate_number TEXT,
    certificate_file_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bpo_certifications_bpo_id ON bpo_certifications(bpo_id);

-- ============================================
-- 7️⃣ SENIOR MANAGEMENT & KEY PERSONNEL
-- ============================================
CREATE TABLE bpo_personnel (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    position_title TEXT,
    department TEXT,
    linkedin_profile TEXT,
    years_experience INTEGER,
    healthcare_experience_years INTEGER,
    bio TEXT,
    photo_url TEXT,
    is_executive BOOLEAN DEFAULT false,
    is_key_personnel BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bpo_personnel_bpo_id ON bpo_personnel(bpo_id);

-- ============================================
-- 8️⃣ MEDIA & IMAGES
-- ============================================
CREATE TABLE bpo_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    media_type TEXT NOT NULL, -- logo, operations_photo, office_photo, team_photo, certificate_scan
    file_url TEXT NOT NULL,
    caption TEXT,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_primary BOOLEAN DEFAULT false
);

CREATE INDEX idx_bpo_media_bpo_id ON bpo_media(bpo_id);
CREATE INDEX idx_bpo_media_type ON bpo_media(media_type);

-- ============================================
-- 9️⃣ FINANCIAL SNAPSHOT
-- ============================================
CREATE TABLE bpo_financial (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE UNIQUE,
    annual_revenue_range TEXT,
    growth_rate_percent NUMERIC(5,2),
    revenue_from_healthcare_percent NUMERIC(5,2),
    funding_stage TEXT,
    last_funding_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 🔟 TECHNOLOGY STACK
-- ============================================
CREATE TABLE bpo_technology (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bpo_id UUID REFERENCES bpos(id) ON DELETE CASCADE,
    system_type TEXT NOT NULL, -- EHR, Billing, CRM, RPA, AI
    system_name TEXT NOT NULL,
    version TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bpo_technology_bpo_id ON bpo_technology(bpo_id);

-- ============================================
-- UPDATE TIMESTAMP TRIGGER
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_bpos_updated_at BEFORE UPDATE ON bpos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================
-- Enable RLS on all tables
ALTER TABLE bpos ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_services ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_clients_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_operations ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_certifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_personnel ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_media ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_financial ENABLE ROW LEVEL SECURITY;
ALTER TABLE bpo_technology ENABLE ROW LEVEL SECURITY;

-- Public read access for all tables (adjust based on your needs)
CREATE POLICY "Allow public read access on bpos" ON bpos FOR SELECT USING (is_active = true);
CREATE POLICY "Allow public read access on services" ON bpo_services FOR SELECT USING (true);
CREATE POLICY "Allow public read access on clients" ON bpo_clients_profile FOR SELECT USING (true);
CREATE POLICY "Allow public read access on operations" ON bpo_operations FOR SELECT USING (true);
CREATE POLICY "Allow public read access on locations" ON bpo_locations FOR SELECT USING (true);
CREATE POLICY "Allow public read access on certifications" ON bpo_certifications FOR SELECT USING (true);
CREATE POLICY "Allow public read access on personnel" ON bpo_personnel FOR SELECT USING (true);
CREATE POLICY "Allow public read access on media" ON bpo_media FOR SELECT USING (true);
CREATE POLICY "Allow public read access on financial" ON bpo_financial FOR SELECT USING (true);
CREATE POLICY "Allow public read access on technology" ON bpo_technology FOR SELECT USING (true);

-- ============================================
-- SAMPLE DATA (Optional - Remove if not needed)
-- ============================================
-- INSERT INTO bpos (company_name, trade_name, city, email, is_active) 
-- VALUES ('Sample Healthcare BPO Inc.', 'SampleBPO', 'Manila', 'contact@samplebpo.com', true);
