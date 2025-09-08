import requests
import base64


# Define headers if necessary (e.g., Content-Type for JSON data)
headers = {"Content-Type": "application/json"}
userpass = "dceeaf60bdd6251" + ":" + "03e78b3b06283ce"
encoded_userpass = base64.b64encode(userpass.encode()).decode()

testurl = (
    "https://hrms-nzz-yhg.frappehr.com/app/hr/api/method/frappe.auth.get_logged_user"
)
try:
    # Send the GET request
    headers = {"Authorization": "Basic %s" % encoded_userpass}
    response = requests.request("GET", testurl, headers=headers)
    # Check if the request was successful (status code 200)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Get Request Successful:")
        print(data)
    else:
        print(f"Get Request Failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the GET request: {e}")


#

try:
    # Send the GET request

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic cG9zdG1hbjpwYXNzd29yZA==",
    }
    # headers = {"Authorization": "token dceeaf60bdd6251:03e78b3b06283ce"}
    response = requests.request("POST", testurl, headers=headers)
    # Check if the request was successful (status code 200)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Get Request Successful:")
        print(data)
    else:
        print(f"Get Request Failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the GET request: {e}")
