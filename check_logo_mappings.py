"""
Upload logos to Supabase using MCP - bypasses auth issues
"""
import csv
from pathlib import Path

LOGOS_DIR = Path('downloaded_logos')
MAPPING_FILE = 'logo_company_mapping.csv'

def main():
    """Read the mapping file and generate upload commands"""
    print("=" * 80)
    print("Logo Upload Helper - Generating Company IDs")
    print("=" * 80)
    
    # Read mapping file
    if not Path(MAPPING_FILE).exists():
        print(f"❌ Mapping file '{MAPPING_FILE}' not found!")
        return
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        mappings = list(reader)
    
    # Filter for entries with company names
    mappings_to_process = [m for m in mappings if m['company_name'].strip()]
    
    print(f"\n📊 Found {len(mappings_to_process)} logos with company names assigned\n")
    
    # Company name to ID mapping (from your database)
    company_ids = {
        "Abbott Philippines": 1,
        "Accenture": 2,
        "Access Healthcare": 3,
        "ADEC Healthcare": 4,
        "Afni": 5,
        "Alorica": 6,
        "Atos (Former Syntel)": 7,
        "AWS": 8,
        "Capstone": 9,
        "Carelon": 10,
        "Cliniqon": 11,
        "Cognizant": 12,
        "Concentrix": 13,
        "Conifer": 14,
        "Connext": 15,
        "Datamatics": 16,
        "Dexcom": 17,
        "DME Serve": 18,
        "Dynaquest": 19,
        "eDat Services": 20,
        "Everise": 21,
        "Evolent Health": 22,
        "EXL": 23,
        "Fresenius": 24,
        "Genfinity": 25,
        "Ibex": 26,
        "Infinit-O": 27,
        "Inspiro": 28,
        "IQVIA": 29,
        "iReply Back Office Services": 30,
        "iRHYTHM": 31,
        "Johnson & Johnson": 32,
        "LKN Strategies": 33,
        "Lyric": 34,
        "MedCheck": 35,
        "MedCode": 36,
        "Medical Abstract": 37,
        "MEDMETRIX": 38,
        "Microsourcing": 39,
        "MiraMed": 40,
        "Nordic": 41,
        "Office Symmetry": 42,
        "Omega Healthcare": 43,
        "Optimum TransSchool": 44,
        "Optum": 45,
        "Passelande": 46,
        "Pointwest": 47,
        "R1RCM": 48,
        "Sagility": 49,
        "Savant Technologies": 50,
        "Shearwater": 51,
        "SMS Global": 52,
        "Staywell": 53,
        "Tata Consultancy": 54,
        "Teleperformance": 55,
        "Tenet Health": 56,
        "TTSI": 57,
        "UST Global": 58,
        "Vector Outsourcing": 59,
        "VISAYA": 60,
        "VXI Global": 61,
        "Wagmi": 62,
        "Wipro": 63,
        "WorldSource": 64
    }
    
    # Generate output with matched IDs
    print("Company Name | Logo File | BPO ID | Status")
    print("-" * 80)
    
    matched = 0
    unmatched = []
    
    for mapping in mappings_to_process:
        company_name = mapping['company_name'].strip()
        logo_file = mapping['logo_file']
        file_path = LOGOS_DIR / logo_file
        
        if not file_path.exists():
            print(f"{company_name} | {logo_file} | N/A | ❌ File not found")
            continue
        
        bpo_id = company_ids.get(company_name)
        
        if bpo_id:
            print(f"{company_name} | {logo_file} | {bpo_id} | ✅ Matched")
            matched += 1
        else:
            print(f"{company_name} | {logo_file} | ??? | ⚠️  Not in database")
            unmatched.append(company_name)
    
    print(f"\n{'='*80}")
    print(f"✅ Matched: {matched} companies")
    print(f"⚠️  Unmatched: {len(unmatched)} companies")
    
    if unmatched:
        print(f"\nUnmatched companies:")
        for name in unmatched:
            print(f"  - {name}")
    
    print(f"{'='*80}")
    print("\nℹ️  Please ask Antigravity to upload these logos using the MCP Supabase tool")

if __name__ == '__main__':
    main()
