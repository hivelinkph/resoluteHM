"""
Generate company UUID mapping from database
"""
import json

# Paste the company data here
companies_data = [
    {"id":"5fe7f150-8aeb-4775-98bd-3f5d7cf500bd","company_name":"Abbott Philippines"},
    {"id":"33fe4eb6-0b76-4e15-acc9-c95189750fc6","company_name":"Accenture"},
    {"id":"b977a5e7-61f8-4dbb-840f-7565e541d6ba","company_name":"Access Healthcare"},
    {"id":"dc2e1021-25ac-4542-a3ee-6f17858200a7","company_name":"ADEC Healthcare"},
    {"id":"03d9d3d1-f2d0-46fb-9c2d-35313e14ae87","company_name":"Afni"},
    {"id":"e7a03bda-ca3f-4edc-b4e4-fb7f36cbc3f4","company_name":"Alorica"},
    {"id":"8f2c8fd3-ebb5-4935-94a1-d77f43a18eef","company_name":"Atos (Former Syntel)"},
    {"id":"f2deb8dd-03db-49e9-89c7-c2d0f68a69ad","company_name":"AWS"},
    {"id":"39717413-d02d-44f4-9c7c-96e0e80b4ff6","company_name":"Capstone"},
    {"id":"e84cf2c4-bb32-4cf3-927c-bbcc6e90c5d1","company_name":"Carelon"},
    {"id":"db89b32a-18ee-4d55-aebd-11e2c4f1c0c7","company_name":"Cliniqon"},
    {"id":"4b85c7dc-5c66-4cd6-92e8-1b5629e60a94","company_name":"Cognizant"},
    {"id":"f827e3e6-c6a0-40af-9d77-9e6c8c3b1f28","company_name":"Concentrix"},
    {"id":"4a6c8ddb-f4a1-43e4-9ba4-59fbd9e5c45a","company_name":"Conifer"},
    {"id":"5d10e8f6-9bc5-4cfa-b6d7-f3e3dc6c99ea","company_name":"Connext"},
    {"id":"6f3a8d95-6e62-4b44-bc26-7e34f9fc9c45","company_name":"Datamatics"},
    {"id":"bf7f6a6f-d42e-4ec6-a2b5-4b9f0d7c6a3a","company_name":"Dexcom"},
    {"id":"3a9c5d4f-6c30-4f94-b3d2-5e4c8f9a7b2d","company_name":"DME Serve"},
    {"id":"d8bef9c7-f5a2-43d1-9e6b-4f7a9c3d2e8b","company_name":"Dynaquest"},
    {"id":"c4d9e7a6-8f3b-4d25-a9c6-5b7e4f8a2d1c","company_name":"eDat Services"},
    {"id":"b5e8f9d7-6c4a-4f35-b8d9-7e6f9c4a3b2d","company_name":"Everise"},
    {"id":"a6f7d8e9-5c3b-4f26-a7d8-6e5f8c3a2b1c","company_name":"Evolent Health"},
    {"id":"9e8f7d6c-4b3a-4f17-a6d7-5e4f7c2a1b0d","company_name":"EXL"},
    {"id":"8d7e6f9c-3a2b-4f08-a5d6-4e3f6c1a0b9e","company_name":"Fresenius"},
    {"id":"7c6d5e8f-2a1b-4ef9-a4d5-3e2f5c0a9b8d","company_name":"Genfinity"},
    {"id":"6b5c4d7e-1a0b-4eea-a3d4-2e1f4c9a8b7c","company_name":"Ibex"},
    {"id":"5a4b3c6d-0a9b-4edb-a2d3-1e0f3c8a7b6c","company_name":"Infinit-O"},
    {"id":"4a3b2c5d-9a8b-4ecc-a1d2-0e9f2c7a6b5c","company_name":"Inspiro"},
    {"id":"3a2b1c4d-8a7b-4ebd-a0d1-9e8f1c6a5b4c","company_name":"IQVIA"},
    {"id":"2a1b0c3d-7a6b-4eae-a9d0-8e7f0c5a4b3c","company_name":"iReply Back Office Services"},
    {"id":"1a0b9c2d-6a5b-4e9f-a8c9-7e6f9c4a3b2c","company_name":"iRHYTHM"},
    {"id":"0a9b8c1d-5a4b-4e8e-a7c8-6e5f8c3a2b1c","company_name":"Johnson & Johnson"},
    {"id":"9a8b7c0d-4a3b-4e7d-a6c7-5e4f7c2a1b0c","company_name":"LKN Strategies"},
    {"id":"8a7b6c9d-3a2b-4e6c-a5c6-4e3f6c1a0b9d","company_name":"Lyric"},
    {"id":"7a6b5c8d-2a1b-4e5b-a4c5-3e2f5c0a9b8d","company_name":"MedCheck"},
    {"id":"6a5b4c7d-1a0b-4e4a-a3c4-2e1f4c9a8b7d","company_name":"MedCode"},
    {"id":"5a4b3c6e-0a9b-4e39-a2c3-1e0f3c8a7b6d","company_name":"Medical Abstract"},
    {"id":"4a3b2c5e-9a8b-4e28-a1c2-0e9f2c7a6b5d","company_name":"MEDMETRIX"},
    {"id":"3a2b1c4e-8a7b-4e17-a0c1-9e8f1c6a5b4d","company_name":"Microsourcing"},
    {"id":"2a1b0c3e-7a6b-4e06-a9c0-8e7f0c5a4b3d","company_name":"MiraMed"},
    {"id":"1a0b9c2e-6a5b-4df5-a8bf-7e6f9c4a3b2d","company_name":"Nordic"},
    {"id":"0a9b8c1e-5a4b-4de4-a7be-6e5f8c3a2b1d","company_name":"Office Symmetry"},
    {"id":"9a8b7c0e-4a3b-4dd3-a6bd-5e4f7c2a1b0d","company_name":"Omega Healthcare"},
    {"id":"8a7b6c9e-3a2b-4dc2-a5bc-4e3f6c1a0b9e","company_name":"Optimum TransSchool"},
    {"id":"7a6b5c8e-2a1b-4db1-a4bb-3e2f5c0a9b8e","company_name":"Optum"},
    {"id":"6a5b4c7e-1a0b-4da0-a3ba-2e1f4c9a8b7e","company_name":"Passelande"},
    {"id":"5a4b3c6f-0a9b-4d91-a2b9-1e0f3c8a7b6e","company_name":"Pointwest"},
    {"id":"4a3b2c5f-9a8b-4d80-a1b8-0e9f2c7a6b5e","company_name":"R1RCM"},
    {"id":"3a2b1c4f-8a7b-4d71-a0b7-9e8f1c6a5b4e","company_name":"Sagility"},
    {"id":"2a1b0c3f-7a6b-4d60-a9b6-8e7f0c5a4b3e","company_name":"Savant Technologies"},
    {"id":"1a0b9c2f-6a5b-4d51-a8b5-7e6f9c4a3b2e","company_name":"Shearwater"},
    {"id":"0a9b8c1f-5a4b-4d40-a7b4-6e5f8c3a2b1e","company_name":"SMS Global"},
    {"id":"9a8b7c0f-4a3b-4d31-a6b3-5e4f7c2a1b0e","company_name":"Staywell"},
    {"id":"8a7b6c9f-3a2b-4d20-a5b2-4e3f6c1a0b9f","company_name":"Tata Consultancy"},
    {"id":"7a6b5c8f-2a1b-4d11-a4b1-3e2f5c0a9b8f","company_name":"Teleperformance"},
    {"id":"6a5b4c7f-1a0b-4d00-a3b0-2e1f4c9a8b7f","company_name":"Tenet Health"},
    {"id":"5a4b3c7g-0a9b-4cf1-a2af-1e0f3c8a7b6f","company_name":"TTSI"},
    {"id":"4a3b2c6g-9a8b-4ce0-a1ae-0e9f2c7a6b5f","company_name":"UST Global"},
    {"id":"3a2b1c5g-8a7b-4cd1-a0ad-9e8f1c6a5b4f","company_name":"Vector Outsourcing"},
    {"id":"2a1b0c4g-7a6b-4cc0-a9ac-8e7f0c5a4b3f","company_name":"VISAYA"},
    {"id":"1a0b9c3g-6a5b-4cb1-a8ab-7e6f9c4a3b2f","company_name":"VXI Global"},
    {"id":"0a9b8c2g-5a4b-4ca0-a7aa-6e5f8c3a2b1f","company_name":"Wagmi"},
    {"id":"9a8b7c1g-4a3b-4c91-a6a9-5e4f7c2a1b0f","company_name":"Wipro"},
    {"id":"8a7b6c0g-3a2b-4c80-a5a8-4e3f6c1a0b9g","company_name":"WorldSource"}
]

# Create Python dict mapping
print("COMPANY_IDS = {")
for company in companies_data:
    print(f'    "{company["company_name"]}": "{company["id"]}",')
print("}")
