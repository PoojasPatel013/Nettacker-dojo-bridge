import requests
import sys

DOJO_URL = "http://localhost:8080/api/v2"
API_KEY = "01b42d0c9fec74472fe2cff259f6fb0d0022d761"
HEADERS = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}
ENGAGEMENT_ID = 7

def check_findings():
    print(f"[*] Checking findings for Engagement {ENGAGEMENT_ID}...")
    r = requests.get(f"{DOJO_URL}/findings/?engagement={ENGAGEMENT_ID}", headers=HEADERS)
    
    if r.status_code == 200:
        data = r.json()
        count = data['count']
        print(f"✅ Found {count} findings!")
        if count > 0:
            for f in data['results']:
                print(f"   - [{f['severity']}] {f['title']}")
        else:
            print("❌ No findings found. Import might have failed or data mapping is wrong.")
    else:
        print(f"❌ Error fetching findings: {r.text}")

if __name__ == "__main__":
    check_findings()
