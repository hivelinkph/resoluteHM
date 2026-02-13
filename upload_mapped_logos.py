"""
Upload logos to Supabase based on manual mapping file
"""
import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
import re

# Load environment variables
load_dotenv('brand-extractor/.env')

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

LOGOS_DIR = Path('downloaded_logos')
MAPPING_FILE = 'logo_company_mapping.csv'

# Initialize Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def match_company_to_db(company_name):
    """Match company name to database ID"""
    try:
        response = supabase.table('bpos').select('id, company_name, trade_name').eq('is_active', True).execute()
        companies = response.data
        
        # Exact match
        for company in companies:
            if company['company_name'].lower() == company_name.lower():
                return company['id'], company['company_name']
            if company.get('trade_name') and company['trade_name'].lower() == company_name.lower():
                return company['id'], company['company_name']
        
        # Partial match
        for company in companies:
            if company_name.lower() in company['company_name'].lower():
                return company['id'], company['company_name']
            if company.get('trade_name') and company_name.lower() in company['trade_name'].lower():
                return company['id'], company['company_name']
        
        return None, None
        
    except Exception as e:
        print(f"  ❌ Error matching: {e}")
        return None, None

def upload_logo(file_path, company_name):
    """Upload logo to Supabase Storage"""
    try:
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', company_name.lower())
        file_ext = Path(file_path).suffix
        storage_path = f"logos/{safe_name}{file_ext}"
        
        # Read file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Upload to storage
        supabase.storage.from_('bpo-assets').upload(
            storage_path,
            file_content,
            {'content-type': f'image/{file_ext[1:]}', 'upsert': 'true'}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('bpo-assets').get_public_url(storage_path)
        
        return public_url
        
    except Exception as e:
        print(f"  ❌ Upload error: {e}")
        return None

def update_bpo_media(bpo_id, logo_url):
    """Update bpo_media table with logo"""
    try:
        # Check if exists
        existing = supabase.table('bpo_media').select('*').eq('bpo_id', bpo_id).eq('media_type', 'logo').execute()
        
        if existing.data:
            # Update
            supabase.table('bpo_media').update({
                'file_url': logo_url,
                'is_primary': True
            }).eq('id', existing.data[0]['id']).execute()
        else:
            # Insert
            supabase.table('bpo_media').insert({
                'bpo_id': bpo_id,
                'media_type': 'logo',
                'file_url': logo_url,
                'is_primary': True,
                'display_order': 1
            }).execute()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 80)
    print("HIMAP Logo Uploader")
    print("=" * 80)
    
    # Read mapping file
    if not Path(MAPPING_FILE).exists():
        print(f"❌ Mapping file '{MAPPING_FILE}' not found!")
        print(f"   Run 'python download_logos.py' first")
        return
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mappings = list(reader)
    
    # Filter for entries with company names
    mappings_to_process = [m for m in mappings if m['company_name'].strip()]
    
    print(f"\n📊 Found {len(mappings_to_process)} logos with company names assigned")
    print(f"    (Skipping {len(mappings) - len(mappings_to_process)} without names)\n")
    
    # Process each mapping
    processed = 0
    skipped = 0
    
    for idx, mapping in enumerate(mappings_to_process, 1):
        company_name = mapping['company_name'].strip()
        logo_file = mapping['logo_file']
        
        print(f"\n[{idx}/{len(mappings_to_process)}] {company_name}")
        print(f"    File: {logo_file}")
        
        # Match to database
        bpo_id, matched_name = match_company_to_db(company_name)
        
        if not bpo_id:
            print(f"    ⚠️  Company not found in database")
            skipped += 1
            continue
        
        if matched_name != company_name:
            print(f"    ℹ️  Matched to: {matched_name}")
        
        # Check if file exists
        file_path = LOGOS_DIR / logo_file
        if not file_path.exists():
            print(f"    ⚠️  Logo file not found")
            skipped += 1
            continue
        
        # Upload to Supabase
        print(f"    📤 Uploading...")
        public_url = upload_logo(file_path, company_name)
        
        if not public_url:
            skipped += 1
            continue
        
        # Update database
        if update_bpo_media(bpo_id, public_url):
            print(f"    ✅ Success! {public_url}")
            processed += 1
        else:
            skipped += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Uploaded {processed} logos")
    print(f"⚠️  Skipped {skipped} logos")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
