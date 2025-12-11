import requests
import json
import argparse
import os
import sys

# Config
# -----------------------------------------------------------------------------
# In a real scenario, use environment variables:
# DOJO_API_KEY = os.environ.get('DD_API_KEY')
# -----------------------------------------------------------------------------
DOJO_URL = "http://localhost:8080/api/v2"
API_KEY = "01b42d0c9fec74472fe2cff259f6fb0d0022d761"  # User provided key

def import_scan(scan_file, engagement_id):
    print(f"[*] Reading scan file: {scan_file}")
    
    if not os.path.exists(scan_file):
        print(f"❌ Error: File {scan_file} not found.")
        return

    # Transformation Logic
    # -------------------------------------------------------------------------
    try:
        with open(scan_file, 'r') as f:
            raw_data = json.load(f)
            
        print(f"[*] Loaded {len(raw_data)} findings. Transforming for DefectDojo...")
        
        findings = []
        for item in raw_data:
            # Map fields to 'Generic Findings Import' format
            # Fallback to defaults if keys are missing
            finding = {
                "title": item.get("title", item.get("module_name", "Unknown Vulnerability")),
                "date": item.get("date", "2025-01-01"),
                "severity": item.get("severity", "Info"),
                "description": (
                    f"{item.get('description', 'No description provided.')}\n\n"
                    "--------------------------------------------------\n"
                    "**Origin:** Automated Import via Nettacker-DefectDojo Bridge\n"
                    "**Source Tool:** OWASP Nettacker\n"
                    f"**Scan ID:** {item.get('scan_id', 'Automated Scan')}\n"
                    f"**Raw Module:** {item.get('module_name', 'Unknown')}"
                ),
                "mitigation": item.get("mitigation", "No mitigation provided."),
                "impact": item.get("impact", "No impact provided."),
                "references": item.get("references", "https://github.com/OWASP/Nettacker"),
                "active": item.get("active", True),
                "verified": item.get("verified", True),
                "tags": ["nettacker", "automated", "defectdojo-bridge"]
            }
            findings.append(finding)
            
        # Save temporary transformed file
        temp_file = "dojo_import.json"
        with open(temp_file, 'w') as f:
            json.dump({"findings": findings, "date": "2025-01-01", "test": "Nettacker"}, f)
            # 'Generic Findings Import' often expects a list or specific wrapper. 
            # Actually, standard Generic Import expects a JSON list of findings.
            
    except json.JSONDecodeError as e:
        print(f"❌ Error: Failed to parse JSON. {e}")
        return

    print(f"[*] Uploading transformed data to DefectDojo at {DOJO_URL}...")
    
    # Upload the transformed file
    # Define DefectDojo parameters
    data = {
        'active': 'true',
        'verified': 'true',
        'scan_type': 'Generic Findings Import',
        'engagement': engagement_id
    }

    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    # Upload logic wrapped in try-finally to ensure cleanup
    try:
        with open(temp_file, 'rb') as f_upload:
            files = {'file': f_upload}
            
            try:
                response = requests.post(
                    f"{DOJO_URL}/import-scan/",
                    headers=headers,
                    data=data,
                    files=files
                )
                
                if response.status_code == 201:
                    print("✅ Success! Scan imported successfully.")
                    import_response = response.json()
                else:
                    print(f"❌ Failed to upload. Status Code: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except requests.exceptions.ConnectionError as e:
                print(f"❌ Connection Error: {e}")
                print("   Is DefectDojo running? (docker-compose up)")
                
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except PermissionError:
                print(f"⚠️ Warning: Could not remove temp file {temp_file} (it might be locked).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import Nettacker results to DefectDojo')
    parser.add_argument('--file', type=str, default="nettacker_results.json", help='Path to results file')
    parser.add_argument('--engagement', type=int, default=1, help='Engagement ID')
    args = parser.parse_args()
    
    import_scan(args.file, args.engagement)
