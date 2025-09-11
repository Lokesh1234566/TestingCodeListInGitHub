from fastmcp import FastMCP
import requests, json, os, csv
from dotenv import load_dotenv
from eventure import Event, EventBus, EventLog

# Load env variables (API_KEY, API_SECRET, FRAPPE_INSTANCE_URL)
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
frappe_instance_url = os.getenv("FRAPPE_INSTANCE_URL")

event_log = EventLog()
event_bus = EventBus(event_log)

mcp = FastMCP(name="FrappeEmployeeServer")


# Simple ping tool
@mcp.tool
def pingServer() -> str:
    print("Ping received")
    return "pong"


# Main Employee creation tool
@mcp.tool
def createEmployee(
    first_name: str, date_of_birth: str, date_of_joining: str, gender: str, status: str
) -> str:
    new_employee_data = {
        "doctype": "Employee",
        "series": "HR-EMP-",
        "first_name": first_name,
        "date_of_birth": date_of_birth,
        "date_of_joining": date_of_joining,
        "gender": gender,
        "status": status,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {api_key}:{api_secret}",
    }

    resp = requests.post(
        f"{frappe_instance_url}/api/resource/Employee",
        headers=headers,
        data=json.dumps(new_employee_data),
    )

    if resp.status_code in (200, 201):
        employee = resp.json()["data"]
        emp_name = employee.get("name")
        emp_fullname = employee.get("employee_name", "Unknown")

        folder_path = os.path.join("employees", "created")
        os.makedirs(folder_path, exist_ok=True)
        csv_file = os.path.join(folder_path, f"{emp_name}.csv")

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=employee.keys())
            writer.writeheader()
            writer.writerow(employee)

        event_bus.publish("employee.created", {"id": emp_name, "name": emp_fullname})
        return f"Employee {emp_fullname} created (ID: {emp_name})"
    else:
        return f"Failed: {resp.status_code} - {resp.text}"


# EventBus handler
def handle_employee_created(event: Event):
    print(f"EventBus: {event.name} -> {event.payload}")


event_bus.subscribe("employee.created", handle_employee_created)

if __name__ == "__main__":
    mcp.run(transport="http")  # default port 8000
