import requests
import json

# -------------------------
# Config
# -------------------------
api_key = "dceeaf60bdd6251"
api_secret = "03e78b3b06283ce"
frappe_instance_url = "https://hrms-nzz-yhg.frappehr.com"

# Employee data
new_employee_data = {
    "doctype": "Employee",
    "series": "HR-EMP-",
    "first_name": "Test Not Assigned",
    "date_of_birth": "1992-01-01",
    "date_of_joining": "2023-01-01",
    "gender": "Male",
    "status": "Active",
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"token {api_key}:{api_secret}",
}

try:
    # Correct API endpoint
    response = requests.post(
        f"{frappe_instance_url}/api/resource/Employee",
        headers=headers,
        data=json.dumps(new_employee_data),
    )

    if response.status_code in (200, 201):
        employee = response.json()["data"]
        print(
            f"New Employee Created: {employee['employee_name']} (Name: {employee['name']})"
        )
    else:
        print(f"Failed to create employee: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
