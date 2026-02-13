"""
Create the bpo-assets storage bucket in Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Initialize Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 80)
print("Creating Supabase Storage Bucket")
print("=" * 80)

try:
    # Create bucket
    print("\n📦 Creating 'bpo-assets' bucket...")
    
    result = supabase.storage.create_bucket(
        'bpo-assets',
        options={
            'public': True,
            'file_size_limit': 5242880,  # 5MB
            'allowed_mime_types': ['image/png', 'image/jpeg', 'image/jpg', 'image/webp']
        }
    )
    
    print(f"✅ Bucket created successfully!")
    print(f"   Bucket ID: {result}")
    
except Exception as e:
    error_str = str(e)
    if 'already exists' in error_str.lower() or '42P07' in error_str:
        print(f"ℹ️  Bucket 'bpo-assets' already exists - that's fine!")
    else:
        print(f"❌ Error creating bucket: {e}")
        print("\nTrying alternative method...")
        
        try:
            # Try to list buckets to see if it exists
            buckets = supabase.storage.list_buckets()
            bucket_names = [b['name'] for b in buckets]
            
            if 'bpo-assets' in bucket_names:
                print(f"✅ Bucket 'bpo-assets' already exists!")
            else:
                print(f"❌ Bucket doesn't exist and couldn't be created")
                print(f"   Available buckets: {bucket_names}")
                print(f"\n   Please create the bucket manually in the Supabase dashboard")
        except Exception as e2:
            print(f"❌ Error: {e2}")

print("\n" + "=" * 80)
print("✅ Setup complete! Now run: python final_upload_logos.py")
print("=" * 80)
