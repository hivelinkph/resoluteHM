"""
Create massive INSERT statement for all logos at once
"""
import csv
from pathlib import Path
import re

MAPPING_FILE = 'logo_company_mapping.csv'

# Company name to UUID mapping
COMPANY_UUIDs = {
    "Abbott Philippines": "5fe7f150-8aeb-4775-98bd-3f5d7cf500bd",
    "Accenture": "33fe4eb6-0b76-4e15-acc9-c95189750fc6",
    "Access Healthcare": "b977a5e7-61f8-4dbb-840f-7565e541d6ba",
    "ADEC Healthcare": "dc2e1021-25ac-4542-a3ee-6f17858200a7",
    "Afni": "03d9d3d1-f2d0-46fb-9c2d-35313e14ae87",
    "Alorica": "f64f653c-9947-48f9-bcfd-c12e13919fb7",
    "Atos (Former Syntel)": "ef1a1145-34b3-48bb-9f18-b7b7296a1539",
    "AWS": "8293fa99-8a1f-464d-93f9-44a518298212",
    "Capstone": "be629de4-a02e-4b15-b447-5910f8762828",
    "Carelon": "6378efe4-ab21-4269-8746-9a3810f1ee96",
    "Cliniqon": "a3379d3f-bb15-465b-ad2a-318085c9c16c",
    "Cognizant": "b2b8c897-56db-40a9-914e-62459578a707",
    "Concentrix": "cbfa00be-e35a-4b08-89dd-f740c918bc44",
    "Conifer": "12dcc5ce-03bd-46f1-a76b-d16dd266f2e3",
    "Connext": "9d55ec3e-05ff-492b-ae42-59b7c96f6188",
    "Datamatics": "80e7b289-c792-4db1-9d0a-0beae4025b41",
    "Dexcom": "fab9c3be-783b-4233-939f-a7fc0a6c401d",
    "DME Serve": "8d920926-6490-4aa8-8a96-ba1988a70d1e",
    "Dynaquest": "c29841ef-7b91-4c3f-8d14-cabf1088f77b",
    "eDat Services": "ad9ff725-242c-43e9-b97b-a21f62cb6823",
    "Everise": "0fbc4d4c-d19a-4bd3-8589-18f5d7a04215",
    "Evolent Health": "1a782feb-843f-40dc-ae2c-1d23a58c7322",
    "EXL": "2b30bd61-f9bd-4c97-a5d1-0ea4af3068dc",
    "Fresenius": "101b2d62-bd2d-4bf2-b645-c7116a1140f1",
    "Genfinity": "4b15d38c-7d2e-44b9-93ef-1e480a0b7b4c",
    "Ibex": "9a454421-3685-41b7-a742-861e790e3eeb",
    "Infinit-O": "7617bf2e-547b-49b2-bb49-7023df5c7a56",
    "Inspiro": "dfa248ae-deab-4db9-b09c-ee9d93de59c2",
    "IQVIA": "9c151d34-9c12-4d59-a7b5-a786f98f0ae2",
    "iReply Back Office Services": "77b32207-c2c6-42de-b93e-43725de9aedb",
    "iRHYTHM": "fbe7f290-6195-4b05-be26-a5b583b8443c",
    "Johnson & Johnson": "a9c52594-75e0-4d1d-b0d0-1b0b30f60d33",
    "LKN Strategies": "c0525cc2-2164-47ef-8f96-c45808778f88",
    "Lyric": "8a60619c-78d4-4271-8b1a-5494573a8d6e",
    "MedCheck": "3ec35c7b-2cea-41c1-80b7-ad2237e42791",
    "MedCode": "96b09de3-e66a-4fd7-af9f-6d751640aa12",
    "Medical Abstract": "a0a06fea-f3fb-481d-90ad-324384dfc8bd",
    "MEDMETRIX": "ba2d683a-f068-439a-a966-f4f9f208485e",
    "Microsourcing": "4d4f55a4-7ee3-4e5e-ad97-2512879ecfb3",
    "MiraMed": "4ec710c2-a2b0-4ffc-b5f1-2cc6bc5714f0",
    "Nordic": "7f6b57cd-1409-474f-b8ce-1be7b2371bc9",
    "Office Symmetry": "599550e1-79dd-483b-a6be-7c9782e170c8",
    "Omega Healthcare": "f6a44e30-cbae-42b4-8cea-254cba26c8b5",
    "Optimum TransSchool": "67950e54-6071-4f57-be1d-3c558cb5c5a2",
    "Optum": "ea74ef07-96b3-40f9-89c1-c8b133308cff",
    "Passelande": "b9aa9951-8ba1-4c51-ad40-2cb0cbea8865",
    "Pointwest": "f84e1d7a-3059-4b83-8e31-28a8ad72cd76",
    "R1RCM": "93b754a3-9f19-4163-88ef-0ceb013a8411",
    "Sagility": "8e1652e0-2c2f-4aad-b2ab-5962198c4e46",
    "Savant Technologies": "66949c76-c22f-4fc0-a0e8-a167cd2d1e56",
    "Shearwater": "51a3e261-7a9e-4599-bfc5-9b298394218f",
    "SMS Global": "dfba415e-d005-45f9-b985-5e188652e905",
    "Staywell": "382bf7dc-7785-41fc-977d-c03fbafe4ce8",
    "Tata Consultancy": "0aa66ba3-5892-4d56-b7ac-1f67b53df155",
    "Teleperformance": "ffbad00c-3a6c-4d7c-b784-f07f22a9301d",
    "Tenet Health": "5aaad344-ce25-4826-8133-41d48d62ba77",
    "TTSI": "36713954-f91f-465f-be04-e748c2676c26",
    "UST Global": "87f0ea5c-9a8b-4a2a-aef8-70297579f3b2",
    "Vector Outsourcing": "d676d184-7980-48b0-916c-9ae617f63628",
    "VISAYA": "e7973845-5602-48b3-881a-d6a37ecaa2ac",
    "VXI Global": "17e53a6b-b6a8-4849-a7a2-01e591aab21a",
    "Wagmi": "1856022c-5945-4999-bc88-ff8aec2560f",
    "Wipro": "bfe76eff-445a-49f7-ac18-ccde0d340f2f",
    "WorldSource": "9b620150-e585-4115-bc4b-ff466caa3b0e"
}

# Read CSV
with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    mappings = [m for m in reader if m['company_name'].strip()]

# Generate VALUES list
values = []
for mapping in mappings:
    company_name = mapping['company_name'].strip()
    uuid = COMPANY_UUIDs.get(company_name)
    
    if uuid:
        # Create storage URL
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', company_name.lower())
        file_ext = Path(mapping['logo_file']).suffix
        storage_path = f"logos/{safe_name}{file_ext}"
        public_url = f"https://llvsayyfvwkqbmhnmumh.supabase.co/storage/v1/object/public/bpo-assets/{storage_path}"
        
        values.append(f"('{uuid}', 'logo', '{public_url}', true)")

# Create single INSERT
sql = "INSERT INTO bpo_media (bpo_id, media_type, file_url, is_primary) VALUES\n  " + ",\n  ".join(values) + "\nON CONFLICT DO NOTHING;"

print(sql)
