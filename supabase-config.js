// Supabase Configuration and API Helpers
// Get your anon key from: Supabase Dashboard > Project Settings > API

const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

// Initialize Supabase client (using CDN in HTML files)
let supabase;

function initSupabase() {
    if (typeof window.supabase === 'undefined') {
        console.error('Supabase library not loaded. Make sure to include the Supabase CDN script.');
        return null;
    }
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return supabase;
}

// ============================================
// DATA FETCHING FUNCTIONS
// ============================================

/**
 * Fetch all active BPO companies with their basic info and primary logo
 */
async function fetchAllBPOs() {
    const { data, error } = await supabase
        .from('bpos')
        .select(`
            id,
            company_name,
            trade_name,
            city,
            province,
            total_employees,
            healthcare_fte_count,
            company_description,
            website_url
        `)
        .eq('is_active', true)
        .order('company_name');

    if (error) {
        console.error('Error fetching BPOs:', error);
        return [];
    }

    // Fetch primary logos for each company
    const bposWithLogos = await Promise.all(data.map(async (bpo) => {
        const { data: logo } = await supabase
            .from('bpo_media')
            .select('file_url')
            .eq('bpo_id', bpo.id)
            .eq('media_type', 'logo')
            .eq('is_primary', true)
            .single();

        return {
            ...bpo,
            logo_url: logo?.file_url || null
        };
    }));

    return bposWithLogos;
}

/**
 * Fetch complete details for a single BPO company
 */
async function fetchBPODetails(bpoId) {
    // Main company info
    const { data: company, error: companyError } = await supabase
        .from('bpos')
        .select('*')
        .eq('id', bpoId)
        .single();

    if (companyError) {
        console.error('Error fetching company:', companyError);
        return null;
    }

    // Fetch all related data in parallel
    const [
        { data: services },
        { data: clientProfile },
        { data: operations },
        { data: locations },
        { data: certifications },
        { data: personnel },
        { data: media },
        { data: financial },
        { data: technology }
    ] = await Promise.all([
        supabase.from('bpo_services').select('*').eq('bpo_id', bpoId),
        supabase.from('bpo_clients_profile').select('*').eq('bpo_id', bpoId).single(),
        supabase.from('bpo_operations').select('*').eq('bpo_id', bpoId).single(),
        supabase.from('bpo_locations').select('*').eq('bpo_id', bpoId),
        supabase.from('bpo_certifications').select('*').eq('bpo_id', bpoId),
        supabase.from('bpo_personnel').select('*').eq('bpo_id', bpoId),
        supabase.from('bpo_media').select('*').eq('bpo_id', bpoId),
        supabase.from('bpo_financial').select('*').eq('bpo_id', bpoId).single(),
        supabase.from('bpo_technology').select('*').eq('bpo_id', bpoId)
    ]);

    return {
        company,
        services: services || [],
        clientProfile: clientProfile || {},
        operations: operations || {},
        locations: locations || [],
        certifications: certifications || [],
        personnel: personnel || [],
        media: media || [],
        financial: financial || {},
        technology: technology || []
    };
}

/**
 * Search BPOs by name, city, or services
 */
async function searchBPOs(query) {
    const { data, error } = await supabase
        .from('bpos')
        .select(`
            id,
            company_name,
            trade_name,
            city,
            province,
            total_employees,
            healthcare_fte_count,
            company_description
        `)
        .eq('is_active', true)
        .or(`company_name.ilike.%${query}%,trade_name.ilike.%${query}%,city.ilike.%${query}%`)
        .order('company_name');

    if (error) {
        console.error('Error searching BPOs:', error);
        return [];
    }

    return data;
}

/**
 * Filter BPOs by service category
 */
async function filterBPOsByService(serviceCategory) {
    const { data, error } = await supabase
        .from('bpo_services')
        .select(`
            bpo_id,
            bpos (
                id,
                company_name,
                trade_name,
                city,
                province,
                total_employees,
                healthcare_fte_count,
                company_description
            )
        `)
        .eq('service_category', serviceCategory);

    if (error) {
        console.error('Error filtering BPOs:', error);
        return [];
    }

    return data.map(item => item.bpos);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get URL parameter by name
 */
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    if (!num) return '—';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Truncate text to specified length
 */
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}
