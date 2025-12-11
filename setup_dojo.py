import requests
import sys

DOJO_URL = "http://localhost:8080/api/v2"
API_KEY = "01b42d0c9fec74472fe2cff259f6fb0d0022d761"
HEADERS = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}

def create_product():
    print("[*] Creating 'Nettacker Scans' Product...")
    data = {
        "name": "Nettacker Automated Scans",
        "description": "Container for automated Nettacker scan results",
        "prod_type": 1  # Assuming 'Research and Development' exists, usually ID 1
    }
    r = requests.post(f"{DOJO_URL}/products/", headers=HEADERS, json=data)
    if r.status_code == 201:
        pid = r.json()['id']
        print(f"✅ Created Product ID: {pid}")
        return pid
    elif r.status_code == 400 and "already exists" in r.text:
         # Try to find it
         print("   Product already exists, fetching ID...")
         r = requests.get(f"{DOJO_URL}/products/?name=Nettacker+Automated+Scans", headers=HEADERS)
         return r.json()['results'][0]['id']
    else:
        print(f"❌ Failed to create product: {r.text}")
        sys.exit(1)

def create_engagement(product_id):
    print("[*] Creating 'Daily Scan' Engagement...")
    data = {
        "name": "Daily Nettacker Scan",
        "product": product_id,
        "target_start": "2025-01-01",
        "target_end": "2025-12-31",
        "status": "In Progress"
    }
    r = requests.post(f"{DOJO_URL}/engagements/", headers=HEADERS, json=data)
    if r.status_code == 201:
        eid = r.json()['id']
        print(f"✅ Created Engagement ID: {eid}")
        return eid
    else:
        print(f"❌ Failed to create engagement: {r.text}")
        # Try to list engagements for this product to return one
        r = requests.get(f"{DOJO_URL}/engagements/?product={product_id}", headers=HEADERS)
        if r.json()['count'] > 0:
             return r.json()['results'][0]['id']
        sys.exit(1)

if __name__ == "__main__":
    pid = create_product()
    eid = create_engagement(pid)
    print(f"\n🎉 USE THIS ID: {eid}")
