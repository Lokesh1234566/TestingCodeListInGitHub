from frappeclient import FrappeClient

# import os

# For demonstration purposes: NEVER store credentials directly in code.
# Instead, use environment variables or a secure configuration management system.
api_key = "dceeaf60bdd6251"
api_secret = "03e78b3b06283ce"
frappe_instance_url = (
    "https://hrms-nzz-yhg.frappehr.com"  # Replace with your instance URL
)

try:
    # Authenticate using API Key and Secret
    client = FrappeClient(frappe_instance_url)

    client.authenticate(api_key, api_secret)

    print("Successfully authenticated to Frappe instance.")

    # Example: Fetch a list of Users
    users = client.get_list("User")
    # users = client.get_list("User", fields=["first_name", "email"])
    print("\nUsers in the system:")
    for user in users:
        # print(f"- Name: {user.get('first_name')} | Email: {user.get('email')}")
        print(user)

except Exception as e:
    print(f"Authentication or API call failed: {e}")
