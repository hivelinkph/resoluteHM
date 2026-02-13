# HIMAP Member Directory - Setup Guide

## Overview

A complete member directory system for HIMAP (Healthcare BPO association) with Supabase backend.

## Files Created

1. **database-schema.sql** - Complete Supabase schema with 10 tables
2. **supabase-config.js** - API configuration and helper functions
3. **himap-directory.html** - Member list page with search/filter
4. **member-detail.html** - Individual member profile page
5. **healthcare-bpo-landing.html** - Updated with directory link

## Setup Instructions

### Step 1: Set up Supabase Database

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Navigate to the SQL Editor in your Supabase dashboard
3. Copy the entire contents of `database-schema.sql`
4. Paste and execute in the SQL Editor
5. Verify all 10 tables were created successfully:
   - bpos
   - bpo_services
   - bpo_clients_profile
   - bpo_operations
   - bpo_locations
   - bpo_certifications
   - bpo_personnel
   - bpo_media
   - bpo_financial
   - bpo_technology

### Step 2: Configure Storage for Media Files

1. In Supabase dashboard, go to **Storage**
2. Create a new bucket named `bpo-media`
3. Set bucket to **Public** (for logo and image access)
4. Configure CORS if needed

### Step 3: Get Your Supabase Credentials

1. Go to **Project Settings** > **API**
2. Copy your:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (starts with `YOUR_ANON_KEY`)

### Step 4: Configure Frontend

1. Open `supabase-config.js`
2. Replace the placeholder values:
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```
3. Save the file

### Step 5: Add Sample Data (Optional)

To test the system, you can add sample BPO companies:

```sql
-- Example: Add a sample company
INSERT INTO bpos (
    company_name,
    trade_name,
    city,
    province,
    email,
    contact_number,
    company_description,
    total_employees,
    healthcare_fte_count,
    is_active
) VALUES (
    'Sample Healthcare BPO Inc.',
    'SampleBPO',
    'Manila',
    'Metro Manila',
    'contact@samplebpo.com',
    '+63 2 1234 5678',
    'Leading provider of healthcare BPO solutions',
    500,
    350,
    true
);
```

### Step 6: Upload Company Logos

1. Navigate to **Storage** > `bpo-media` bucket
2. Upload company logo files
3. Get the public URL for each logo
4. Insert into `bpo_media` table:
   ```sql
   INSERT INTO bpo_media (bpo_id, media_type, file_url, is_primary)
   VALUES (
       'YOUR_BPO_ID',
       'logo',
       'https://YOUR_PROJECT.supabase.co/storage/v1/object/public/bpo-media/logo.png',
       true
   );
   ```

## Testing

1. Open `healthcare-bpo-landing.html` in a browser
2. Click "View HIMAP Members" button
3. Verify member list loads with your sample data
4. Click on a member card to view details
5. Test all 7 tabs on the detail page

## Features

### Member Directory Page
- Search by company name or location
- Filter by service category  
- Responsive grid layout
- Company logo display
- Quick stats (employees, FTEs)

### Member Detail Page
- 7 information tabs:
  1. Overview
  2. Services & Capabilities
  3. Operations Details
  4. Locations
  5. Leadership Team
  6. Certifications
  7. Technology Stack
- Hero section with company branding
- Key statistics display

## Database Schema Highlights

- **UUID primary keys** for all tables
- **Foreign key relationships** maintain data integrity
- **Row Level Security (RLS)** policies for access control
- **Automatic timestamps** via triggers
- **Indexes** on foreign keys for performance
- **Public read access** configured (customize as needed)

## Customization

### Updating Branding
- Primary color: `--primary: #363F4D;` (Kyte Navy)
- Accent color: `--accent: #2DD1AC;` (Kyte Teal)
- Logo: `ResoluteTransparent.png` is the standard brand logo

### Adding More Filters
Edit `himap-directory.html` filter tags section to add service categories.

### Customizing RLS Policies
Modify the policies in `database-schema.sql` if you need authentication or restricted access.

## Troubleshooting

**Issue**: "Unable to load members"
- Check browser console for errors
- Verify Supabase credentials in `supabase-config.js`
- Ensure RLS policies allow public read access

**Issue**: Images not loading
- Verify storage bucket is public
- Check file URLs are correct in `bpo_media` table
- Ensure CORS is configured

**Issue**: Search not working
- Check that data exists in `bpos` table
- Verify Supabase client initialized correctly

## Next Steps

1. Add actual HIMAP member data to database
2. Upload company logos to Supabase Storage  
3. Configure custom domain (if needed)
4. Set up admin panel for data management (optional)
5. Deploy to production hosting
