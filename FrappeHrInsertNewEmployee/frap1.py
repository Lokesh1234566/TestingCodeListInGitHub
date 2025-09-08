import requests
from base64 import b64encode

api_key = "dceeaf60bdd6251"
api_secret = "03e78b3b06283ce"
frappe_instance_url = "https://hrms-nzz-yhg.frappehr.com"

# Create a session
session = requests.Session()


def login(username: str, password: str):
    """Login using username and password (session-based auth)"""
    try:
        response = session.post(
            f"{frappe_instance_url}/api/method/login",
            data={"usr": username, "pwd": password},
        )
        response.raise_for_status()
        if response.json().get("message") == "Logged In":
            print("Login successful")
            return True
        else:
            print("Login failed:", response.json())
            return False
    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {e}")
        return False


def authenticate_with_api_key(api_key: str, api_secret: str):
    """Authenticate using API Key and Secret (Basic Auth)"""
    token = b64encode(f"{api_key}:{api_secret}".encode()).decode()
    session.headers.update({"Authorization": f"Basic {token}"})
    print("Authenticated with API Key/Secret")


def get_list(doctype: str, fields=None, limit=10):
    """Fetch list of records for a given DocType"""
    if fields is None:
        fields = ["name"]
    try:
        response = session.get(
            f"{frappe_instance_url}/api/resource/{doctype}",
            params={
                "fields": str(fields),
                "limit_page_length": limit,
            },
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        print(f"{doctype} records:")
        for row in data:
            print(row)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Get list failed: {e}")
        return []


def logout():
    """Logout current session (only works for login, not API key auth)"""
    try:
        response = session.get(f"{frappe_instance_url}/api/method/logout")
        response.raise_for_status()
        print("Logged out:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Logout failed: {e}")


# ----------------------------
# Example usage:
# ----------------------------
if __name__ == "__main__":
    # Option 1: Username/Password login
    # login("user@example.com", "password")

    # Option 2: API Key + Secret
    authenticate_with_api_key(api_key, api_secret)

    # Get list of Users
    get_list("User", fields=["first_name", "email", "birth_date"], limit=5)

    # Logout (only valid if used login(), not API key)
    # logout()
