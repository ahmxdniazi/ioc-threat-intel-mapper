import re
import json

WHITELIST = [
    "twitter.com", "linkedin.com", "www.linkedin.com",
    "facebook.com", "youtube.com", "github.com",
    "microsoft.com", "google.com", "paloaltonetworks.com"
]


def extract_iocs(text):
    iocs = {
        "ips": [],
        "domains": [],
        "urls": [],
        "md5": [],
        "sha256": [],
        "emails": []
    }

    # IP addresses
    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
    iocs["ips"] = list(set(re.findall(ip_pattern, text)))

    # Domains
    domain_pattern = r'\b(?:[a-zA-Z0-9\-]+\.)+(?:com|net|org|ru|io|co|info|biz|xyz|top|tk)\b'
    all_domains = list(set(re.findall(domain_pattern, text)))
    iocs["domains"] = [d for d in all_domains if d not in WHITELIST]

    # URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    all_urls = list(set(re.findall(url_pattern, text)))
    iocs["urls"] = [u for u in all_urls if not any(w in u for w in WHITELIST)]

    # MD5 hashes
    md5_pattern = r'\b[a-fA-F0-9]{32}\b'
    iocs["md5"] = list(set(re.findall(md5_pattern, text)))

    # SHA256 hashes
    sha256_pattern = r'\b[a-fA-F0-9]{64}\b'
    iocs["sha256"] = list(set(re.findall(sha256_pattern, text)))

    # Emails
    email_pattern = r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b'
    iocs["emails"] = list(set(re.findall(email_pattern, text)))

    return iocs


def load_report(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


if __name__ == "__main__":
    text = load_report("report1.txt")
    results = extract_iocs(text)

    print("\n=== IOC Extraction Results ===")
    for ioc_type, values in results.items():
        print(f"\n[{ioc_type.upper()}] — {len(values)} found")
        for v in values:
            print(f"  {v}")

    with open("iocs_raw.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n[+] Saved to iocs_raw.json")