import requests
import json
from dotenv import load_dotenv
import os
import csv


# Load environment variables
load_dotenv()
API_Key = "dc90ce7525c448d"
API_SECRET = "3a833e29be642a0"
FRAPPE_INSTANCE_URL = "https://hrms-zkz-wjk.frappehr.com"

api_key = "dc90ce7525c448d"
api_secret = "3a833e29be642a0"
frappe_instance_url = "https://hrms-zkz-wjk.frappehr.com"


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"token {api_key}:{api_secret}",
}
response = requests.get(
    f"{FRAPPE_INSTANCE_URL}/api/resource/DocType?limit_start=0&limit_page_length=1500",  # space, not underscore
    headers=headers,
)

print(response.json())
