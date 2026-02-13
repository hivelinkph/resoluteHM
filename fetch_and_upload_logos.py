"""
Fetch company logos from HIMAP members page using Firecrawl and upload to Supabase
"""
import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
from firecrawl import FirecrawlApp
import time

# Load environment variables
load_dotenv()

# Configuration
FIRE_CRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Initialize clients
firecrawl = FirecrawlApp(api_key=FIRE_CRAWL_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape_himap_logos():
    """Scrape the HIMAP members page for company logos"""
    print("🔥 Scraping HIMAP members page...")
    
    try:
        result = firecrawl.scrape(
            url='https://himap.ph/members/list-of-members/',
            formats=['markdown']
        )
        
        # Get markdown content from Document object
        markdown = result.markdown if hasattr(result, 'markdown') else ''
        
        print(f"✅ Successfully scraped page")
        print(f"📝 Markdown length: {len(markdown)} characters")
        
        # Extract all image URLs from markdown
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, markdown)
        
        print(f"✅ Found {len(images)} images on the page")
        
        return result, images
        
    except Exception as e:
        print(f"❌ Error scraping page: {e}")
        import traceback
        traceback.print_exc()
        return None, []

def download_image(url, filename):
    """Download an image from a URL"""
    try:
        print(f"  📥 Downloading {url}...")
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✅ Saved to {filename}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error downloading {url}: {e}")
        return False

def upload_to_supabase(file_path, company_name):
    """Upload logo to Supabase Storage and return the public URL"""
    try:
        # Create a clean filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', company_name.lower())
        file_ext = Path(file_path).suffix
        storage_path = f"logos/{safe_name}{file_ext}"
        
        print(f"  📤 Uploading {file_path} to Supabase Storage...")
        
        # Read file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Upload to storage bucket (create 'bpo-assets' bucket if it doesn't exist)
        result = supabase.storage.from_('bpo-assets').upload(
            storage_path,
            file_content,
            {'content-type': f'image/{file_ext[1:]}'}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('bpo-assets').get_public_url(storage_path)
        
        print(f"  ✅ Uploaded! URL: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"  ❌ Error uploading to Supabase: {e}")
        return None

def match_company_to_db(company_name):
    """Try to match the company name from the scraped data to the database"""
    try:
        # Fetch all companies
        response = supabase.table('bpos').select('id, company_name, trade_name').eq('is_active', True).execute()
        companies = response.data
        
        # Try exact match first
        for company in companies:
            if company['company_name'].lower() == company_name.lower():
                return company['id']
            if company.get('trade_name') and company['trade_name'].lower() == company_name.lower():
                return company['id']
        
        # Try partial match
        for company in companies:
            if company_name.lower() in company['company_name'].lower() or company['company_name'].lower() in company_name.lower():
                print(f"  ⚠️  Partial match: '{company_name}' -> '{company['company_name']}'")
                return company['id']
            if company.get('trade_name'):
                if company_name.lower() in company['trade_name'].lower() or company['trade_name'].lower() in company_name.lower():
                    print(f"  ⚠️  Partial match: '{company_name}' -> '{company['trade_name']}'")
                    return company['id']
        
        print(f"  ⚠️  No match found for: {company_name}")
        return None
        
    except Exception as e:
        print(f"  ❌ Error matching company: {e}")
        return None

def update_bpo_media(bpo_id, logo_url):
    """Insert or update logo in bpo_media table"""
    try:
        # Check if logo already exists
        existing = supabase.table('bpo_media').select('*').eq('bpo_id', bpo_id).eq('media_type', 'logo').execute()
        
        if existing.data:
            # Update existing
            supabase.table('bpo_media').update({
                'file_url': logo_url,
                'is_primary': True
            }).eq('id', existing.data[0]['id']).execute()
            print(f"  ✅ Updated existing logo record")
        else:
            # Insert new
            supabase.table('bpo_media').insert({
                'bpo_id': bpo_id,
                'media_type': 'logo',
                'file_url': logo_url,
                'is_primary': True,
                'display_order': 1
            }).execute()
            print(f"  ✅ Created new logo record")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating media table: {e}")
        return False

def main():
    """Main execution flow"""
    print("=" * 80)
    print("HIMAP Logo Scraper & Uploader")
    print("=" * 80)
    
    # Create temp directory for downloads
    temp_dir = Path('temp_logos')
    temp_dir.mkdir(exist_ok=True)
    
    # Step 1: Scrape the page
    result, images = scrape_himap_logos()
    
    if not result:
        print("❌ Failed to scrape page. Exiting.")
        return
    
    print(f"\n📊 Processing {len(images)} images...")
    
    # Step 2: Process each image
    processed = 0
    for alt_text, image_url in images:
        print(f"\n{'='*60}")
        print(f"Processing: {alt_text or 'Unnamed'}")
        print(f"URL: {image_url}")
        
        # Skip if not a company logo (based on alt text or URL patterns)
        if not alt_text or len(alt_text) < 3:
            print("  ⏭️  Skipping - no alt text")
            continue
        
        # Download image
        file_ext = '.png' if 'png' in image_url.lower() else '.jpg'
        temp_file = temp_dir / f"logo_{processed}{file_ext}"
        
        if not download_image(image_url, temp_file):
            continue
        
        # Upload to Supabase
        public_url = upload_to_supabase(temp_file, alt_text)
        
        if not public_url:
            continue
        
        # Match to database company
        bpo_id = match_company_to_db(alt_text)
        
        if bpo_id:
            # Update database
            update_bpo_media(bpo_id, public_url)
            processed += 1
        
        # Clean up temp file
        temp_file.unlink()
        
        # Rate limiting
        time.sleep(0.5)
    
    print(f"\n{'='*80}")
    print(f"✅ Completed! Processed {processed} logos")
    print(f"{'='*80}")
    
    # Cleanup
    try:
        temp_dir.rmdir()
    except:
        pass

if __name__ == '__main__':
    main()
