# Logo Upload Instructions

## ✅ What's Been Done

1. **Downloaded 89 company logos** from the HIMAP members page
2. **Created mapping spreadsheet** at `logo_company_mapping.csv`
3. **Prepared upload script** at `upload_mapped_logos.py`

All logos are saved in the `downloaded_logos/` folder with numbered filenames (logo_001.png, logo_002.jpg, etc.)

## 📋 Next Steps

### Step 1: Fill in the Mapping File

Open `logo_company_mapping.csv` in Excel or any text editor. You'll see 4 columns:

| Column | Description |
|--------|-------------|
| `logo_file` | The filename of the downloaded logo (e.g., logo_001.png) |
| `logo_url` | The original URL where the logo came from |
| `company_name` | **YOU NEED TO FILL THIS IN** - exact company name from database |
| `notes` | Optional notes field |

**Important:** The `company_name` must match a company name in the database EXACTLY (or at least closely). You can find all company names by running:

```powershell
# List all companies in the database
python -c "import os; from dotenv import load_dotenv; from supabase import create_client; load_dotenv(); s = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_ROLE_KEY')); print('\\n'.join([c['company_name'] for c in s.table('bpos').select('company_name').eq('is_active', True).execute().data]))"
```

### Step 2: Map the Logos

For each row in the CSV:
1. Open the image file from `downloaded_logos/` (e.g., double-click `logo_001.png`)
2. Look at the logo and identify which company it belongs to
3. Fill in the `company_name` column with the exact company name
4. Save the CSV file

**Tip:** You don't need to fill in ALL 89 logos at once. The upload script will only process rows where you've entered a company name.

### Step 3: Upload to Supabase

Once you've mapped some (or all) logos, run:

```powershell
python upload_mapped_logos.py
```

This script will:
- Read your mapping file
- Match company names to the database
- Upload logos to Supabase Storage
- Update the `bpo_media` table
- Show you a summary of what was uploaded

## 🔄 You Can Run Multiple Times

You can:
- Map a few logos, run the upload script
- Map more logos later, run it again
- The script will update existing logos if you re-upload

## 📁 File Structure

```
HIMAP/
├── downloaded_logos/          # All 89 logo images
│   ├── logo_001.png
│   ├── logo_002.jpg
│   └── ...
├── logo_company_mapping.csv   # THE FILE YOU NEED TO EDIT
├── download_logos.py           # Already executed
└── upload_mapped_logos.py      # Run after mapping
```

## ❓ Troubleshooting

**Q: Company name not matched?**
- Make sure spelling is exact
- Try using the company's trade name if different
- Check the list of companies using the command above

**Q: Want to see what's already been uploaded?**
```sql
SELECT b.company_name, m.file_url 
FROM bpos b 
JOIN bpo_media m ON b.id = m.bpo_id 
WHERE m.media_type = 'logo'
```

**Q: Made a mistake?**
- Just fix the CSV and run `upload_mapped_logos.py` again
- It will replace the old logo with the new one
