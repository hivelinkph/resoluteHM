import os
import json

logo_dir = r"c:\AntiGravity\HIMAP\downloaded_logos"
logos = []
try:
    for filename in os.listdir(logo_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            logos.append(f"downloaded_logos/{filename}")
    
    # Sort for consistency
    logos.sort()
    
    print(json.dumps(logos, indent=2))
except Exception as e:
    print(f"Error: {e}")
