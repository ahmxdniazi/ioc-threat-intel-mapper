import requests
import json
import time

API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

HEADERS = {
    "x-apikey": API_KEY
}

def check_hash(hash_val):
    url = f"https://www.virustotal.com/api/v3/files/{hash_val}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        return {
            "ioc": hash_val,
            "type": "Hash",
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "verdict": "MALICIOUS" if stats.get("malicious", 0) > 0 else "CLEAN"
        }
    return {"ioc": hash_val, "type": "Hash", "verdict": "NOT FOUND"}

def enrich_all(iocs):
    enriched = []
    for h in iocs.get("sha256", [])[:5]:
        print(f"[*] Checking Hash: {h}")
        enriched.append(check_hash(h))
        time.sleep(15)
    return enriched

if __name__ == "__main__":
    with open("iocs_raw.json") as f:
        iocs = json.load(f)
    enriched = enrich_all(iocs)
    with open("iocs_enriched.json", "w") as f:
        json.dump(enriched, f, indent=2)
    print("\n[+] Enrichment complete. Saved to iocs_enriched.json")