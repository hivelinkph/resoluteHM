"""
Download all logos from HIMAP members page and create a mapping CSV for manual assignment
"""
import os
import re
import requests
import csv
from pathlib import Path
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# Load environment variables
load_dotenv('brand-extractor/.env')

# Configuration
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
LOGOS_DIR = Path('downloaded_logos')
MAPPING_FILE = 'logo_company_mapping.csv'

# Initialize Firecrawl
firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def scrape_logos():
    """Scrape the HIMAP members page for all logos"""
    print("🔥 Scraping HIMAP members page...")
    
    try:
        result = firecrawl.scrape(
            url='https://himap.ph/members/list-of-members/',
            formats=['markdown']
        )
        
        markdown = result.markdown if hasattr(result, 'markdown') else ''
        
        # Extract all image URLs
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, markdown)
        
        # Filter for likely logo images
        logo_urls = []
        for alt_text, url in images:
            # Skip small icons, banners, etc.
            if 'logo' in url.lower() or 'website' in url.lower():
                logo_urls.append(url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_logos = []
        for url in logo_urls:
            if url not in seen:
                seen.add(url)
                unique_logos.append(url)
        
        print(f"✅ Found {len(unique_logos)} unique logo images")
        return unique_logos
        
    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return []

def download_logo(url, filename):
    """Download a logo image"""
    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error downloading {url}: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 80)
    print("HIMAP Logo Downloader")
    print("=" * 80)
    
    # Create logos directory
    LOGOS_DIR.mkdir(exist_ok=True)
    
    # Scrape logo URLs
    logo_urls = scrape_logos()
    
    if not logo_urls:
        print("❌ No logos found")
        return
    
    print(f"\n📥 Downloading {len(logo_urls)} logos...")
    
    # Download logos and create mapping data
    mapping_data = []
    
    for idx, url in enumerate(logo_urls, 1):
        print(f"\n[{idx}/{len(logo_urls)}] {url}")
        
        # Determine file extension
        if url.lower().endswith('.png'):
            ext = '.png'
        elif url.lower().endswith('.jpg') or url.lower().endswith('.jpeg'):
            ext = '.jpg'
        else:
            # Try to guess from URL
            ext = '.png'
        
        filename = f"logo_{idx:03d}{ext}"
        filepath = LOGOS_DIR / filename
        
        # Download
        if download_logo(url, filepath):
            print(f"  ✅ Saved as {filename}")
            mapping_data.append({
                'logo_file': filename,
                'logo_url': url,
                'company_name': '',  # To be filled manually
                'notes': ''
            })
        else:
            mapping_data.append({
                'logo_file': filename,
                'logo_url': url,
                'company_name': '',
                'notes': 'DOWNLOAD FAILED'
            })
    
    # Create CSV mapping file
    print(f"\n📝 Creating mapping file: {MAPPING_FILE}")
    
    with open(MAPPING_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['logo_file', 'logo_url', 'company_name', 'notes'])
        writer.writeheader()
        writer.writerows(mapping_data)
    
    print(f"\n{'='*80}")
    print(f"✅ Downloaded {len(mapping_data)} logos to '{LOGOS_DIR}/' directory")
    print(f"✅ Created mapping file: '{MAPPING_FILE}'")
    print(f"\n📋 Next steps:")
    print(f"   1. Open '{MAPPING_FILE}' in Excel or a text editor")
    print(f"   2. Look at each logo image in '{LOGOS_DIR}/'")
    print(f"   3. Fill in the 'company_name' column with the exact company name")
    print(f"   4. Run 'python upload_mapped_logos.py' to upload to Supabase")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
