import requests
import json
import os
import csv
from dotenv import load_dotenv

# Load environment variables (optional if already hardcoding)
load_dotenv()

# API credentials & instance URL
API_KEY = "dc90ce7525c448d"
API_SECRET = "3a833e29be642a0"
FRAPPE_INSTANCE_URL = "https://hrms-zkz-wjk.frappehr.com"

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"token {API_KEY}:{API_SECRET}",
}

# Request data
response = requests.get(
    f"{FRAPPE_INSTANCE_URL}/api/resource/DocType?limit_start=0&limit_page_length=1500",
    headers=headers,
)

data = response.json()

# === Create output folder if not exists ===
output_folder = "output_data"
os.makedirs(output_folder, exist_ok=True)

# === Save JSON file ===
json_path = os.path.join(output_folder, "doctype_data.json")
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"JSON data saved to {json_path}")

# === Save CSV file ===
csv_path = os.path.join(output_folder, "doctype_data.csv")

# Extract "data" key from frappe response (usually in `data`)
if "data" in data:
    records = data["data"]
else:
    records = data  # fallback

if records and isinstance(records, list):
    keys = records[0].keys()  # take keys from first record

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)

    print(f"CSV data saved to {csv_path}")
else:
    print("No records found in response for CSV export.")
