import os
import random
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# HIMAP Members extracted from website
companies = [
    {"name": "Abbott Philippines", "website": "https://www.abbott.com/"},
    {"name": "Accenture", "website": "https://www.accenture.com/us-en"},
    {"name": "Access Healthcare", "website": "http://accesshealthcare.com/"},
    {"name": "ADEC Healthcare", "website": "https://www.healthcare.adec-innovations.com/"},
    {"name": "Alorica", "website": "http://alorica.com/"},
    {"name": "Concentrix", "website": "https://www.concentrix.com/"},
    {"name": "Connext", "website": "http://connextglobal.com/"},
    {"name": "Lyric", "website": "http://lyric.ai/"},
    {"name": "Dynaquest", "website": "https://dqtsi.com/"},
    {"name": "Passelande", "website": "http://www.passelande.com/"},
    {"name": "eDat Services", "website": "http://edataservices.com/"},
    {"name": "EXL", "website": "https://exlservice.com/"},
    {"name": "Genfinity", "website": "http://genfinity.net/"},
    {"name": "Sagility", "website": "http://sagilityhealth.com/"},
    {"name": "Infinit-O", "website": "http://infinit-o.com/"},
    {"name": "IQVIA", "website": "http://iqvia.com/"},
    {"name": "Omega Healthcare", "website": "http://omegahms.com/"},
    {"name": "Optum", "website": "http://optum.com/"},
    {"name": "Pointwest", "website": "https://pointwest.com.ph/"},
    {"name": "Shearwater", "website": "https://swhealth.com/"},
    {"name": "Staywell", "website": "http://staywellguam.com/"},
    {"name": "Atos (Former Syntel)", "website": "http://atos.net/"},
    {"name": "Tenet Health", "website": "http://tenethealth.com/"},
    {"name": "TTSI", "website": "http://ttsibpo.com/"},
    {"name": "Vector Outsourcing", "website": "https://www.vectoroutsourcing.com/"},
    {"name": "VISAYA", "website": "http://www.visayakpo.com/"},
    {"name": "Wipro", "website": "http://wipro.com/"},
    {"name": "WorldSource", "website": "http://worldsourceteam.com.ph/"},
    {"name": "MedCode", "website": "https://medcode.ph/"},
    {"name": "Capstone", "website": "http://www.capstone.ph/"},
    {"name": "Inspiro", "website": "http://inspiro.com/"},
    {"name": "Conifer", "website": "https://www.coniferhealth.com/"},
    {"name": "LKN Strategies", "website": "http://lknstrategies.us/"},
    {"name": "Carelon", "website": "http://www.carelonglobal.ph/"},
    {"name": "Afni", "website": "http://afni.com/"},
    {"name": "Cliniqon", "website": "http://cliniqon.com/"},
    {"name": "AWS", "website": "http://awsys-i.com/"},
    {"name": "Cognizant", "website": "http://cognizant.com/"},
    {"name": "Nordic", "website": "https://www.nordicglobal.com/"},
    {"name": "DME Serve", "website": "http://dmeserve.com/"},
    {"name": "SMS Global", "website": "https://smsgt.com/"},
    {"name": "Teleperformance", "website": "http://teleperformance.com/"},
    {"name": "UST Global", "website": "http://ust.com/"},
    {"name": "Office Symmetry", "website": "http://officesymmetry.com/"},
    {"name": "Evolent Health", "website": "https://www.evolent.com/"},
    {"name": "MEDMETRIX", "website": "http://med-metrix.com/"},
    {"name": "Wagmi", "website": "http://wagmisolutions.io/"},
    {"name": "VXI Global", "website": "http://vxi.com/"},
    {"name": "Medical Abstract", "website": "https://www.mdabstract.com/"},
    {"name": "Ibex", "website": "https://www.ibex.co/"},
    {"name": "MedCheck", "website": "https://www.medcheck.com.ph/"},
    {"name": "Datamatics", "website": "https://www.datamatics.com/"},
    {"name": "Dexcom", "website": "https://www.dexcom.com/"},
    {"name": "Everise", "website": "https://weareeverise.com/"},
    {"name": "Microsourcing", "website": "http://microsourcing.com/"},
    {"name": "Savant Technologies", "website": "http://savant.ph/"},
    {"name": "iRHYTHM", "website": "https://www.irhythmtech.com/us/en"},
    {"name": "MiraMed", "website": "https://www.coronishealth.com/"},
    {"name": "Johnson & Johnson", "website": "http://jnj.com/"},
    {"name": "R1RCM", "website": "https://www.r1rcm.com/"},
    {"name": "Tata Consultancy", "website": "https://www.tcs.com/"},
    {"name": "Fresenius", "website": "https://freseniusmedicalcare.com/en-us/"},
    {"name": "Optimum TransSchool", "website": "https://otsiinc.com/"},
    {"name": "iReply Back Office Services", "website": "http://www.ireplyservices.com/"},
]

# Service categories for healthcare BPO
service_categories = [
    "Medical Coding",
    "Medical Billing",
    "Revenue Cycle Management",
    "Claims Processing",
    "Healthcare IT",
    "Clinical Documentation",
    "Medical Transcription",
    "Prior Authorization",
    "Patient Support Services"
]

# Philippines cities
cities = [
    "Manila", "Makati", "Bonifacio Global City", "Quezon City", "Pasig",
    "Ortigas", "Alabang", "Cebu", "Davao", "Clark"
]

def create_mock_data(company):
    """Create mock data for a company"""
    return {
        "company_name": company["name"],
        "trade_name": company["name"].replace(" Philippines", "").replace(" Inc.", ""),
        "city": random.choice(cities),
        "province": "Metro Manila" if random.random() > 0.3 else "Cebu",
        "country": "Philippines",
        "website_url": company["website"],
        "email": f"info@{company['website'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]}",
        "company_description": f"Leading healthcare BPO provider specializing in {random.choice(service_categories).lower()} and related services.",
        "total_employees": random.randint(100, 5000),
        "healthcare_fte_count": random.randint(50, 3000),
        "is_active": True
    }

def create_services(bpo_id):
    """Create 2-4 services for each company"""
    num_services = random.randint(2, 4)
    selected_services = random.sample(service_categories, num_services)
    
    services = []
    for service in selected_services:
        services.append({
            "bpo_id": bpo_id,
            "service_category": service,
            "service_name": service,
            "description": f"Professional {service.lower()} services for healthcare providers",
            "is_primary_service": service == selected_services[0]
        })
    return services

def populate_database():
    """Populate the Supabase database with HIMAP member companies"""
    print("🚀 Starting HIMAP member data population...")
    print(f"📊 Total companies to insert: {len(companies)}\n")
    
    inserted_count = 0
    
    for idx, company in enumerate(companies, 1):
        try:
            # Create company data
            company_data = create_mock_data(company)
            
            # Insert company
            result = supabase.table("bpos").insert(company_data).execute()
            
            if result.data and len(result.data) > 0:
                bpo_id = result.data[0]['id']
                inserted_count += 1
                
                # Create services for this company
                services_data = create_services(bpo_id)
                supabase.table("bpo_services").insert(services_data).execute()
                
                # Create client profile with mock data
                client_profile = {
                    "bpo_id": bpo_id,
                    "target_market": "United States, Canada",
                    "client_types": "Hospitals, Physician Practices, Insurance Payers",
                    "no_of_active_clients": random.randint(5, 50),
                    "years_serving_healthcare": random.randint(3, 20)
                }
                supabase.table("bpo_clients_profile").insert(client_profile).execute()
                
                # Create operations data
                operations = {
                    "bpo_id": bpo_id,
                    "delivery_model": random.choice(["Onsite", "Offshore", "Hybrid"]),
                    "work_shifts": "24/7 Operations",
                    "compliance_frameworks": "HIPAA, SOC 2, ISO 27001",
                    "ehr_systems_supported": "Epic, Cerner, Meditech, Athenahealth"
                }
                supabase.table("bpo_operations").insert(operations).execute()
                
                print(f"✅ {idx}/{len(companies)} - {company['name']} - Inserted successfully")
            else:
                print(f"❌ {idx}/{len(companies)} - {company['name']} - Failed to insert")
                
        except Exception as e:
            print(f"❌ {idx}/{len(companies)} - {company['name']} - Error: {str(e)}")
            continue
    
    print(f"\n🎉 Data population completed!")
    print(f"✅ Successfully inserted: {inserted_count}/{len(companies)} companies")

if __name__ == "__main__":
    populate_database()
