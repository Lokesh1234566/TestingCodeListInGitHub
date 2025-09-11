import os
import json
import csv
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
from eventure import Event, EventBus, EventLog

# Load env vars
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
FRAPPE_INSTANCE_URL = os.getenv("FRAPPE_INSTANCE_URL")

# Event system
event_log = EventLog()
event_bus = EventBus(event_log)

mcp = FastMCP(name="FrappeEmployeeServer")


@mcp.tool(annotations={"title": "pingServer"})
def pingServer() -> str:
    """Simple ping check"""
    print("✅ Ping received from Client")
    return "pong"


@mcp.tool(annotations={"title": "createEmployee"})
def createEmployee(
    first_name: str,
    date_of_birth: str,
    date_of_joining: str,
    gender: str,
    status: str,
) -> str:
    """Creates an employee record in Frappe"""

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
        "Accept": "application/json",
        "Authorization": f"token {API_KEY}:{API_SECRET}",
    }

    try:
        response = requests.post(
            f"{FRAPPE_INSTANCE_URL}/api/resource/Employee",
            headers=headers,
            data=json.dumps(new_employee_data),
        )

        if response.status_code in (200, 201):
            employee = response.json()["data"]
            emp_name = employee.get("name")
            emp_fullname = employee.get("employee_name", "Unknown")

            folder_path = os.path.join("employees", "created")
            os.makedirs(folder_path, exist_ok=True)
            csv_file = os.path.join(folder_path, f"{emp_name}.csv")

            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=employee.keys())
                writer.writeheader()
                writer.writerow(employee)

            event_bus.publish(
                "employee.created", {"id": emp_name, "name": emp_fullname}
            )

            print(f"✅ Employee {emp_fullname} created (ID: {emp_name})")
            return f"Employee {emp_fullname} created (ID: {emp_name})"
        else:
            error_msg = f"❌ Failed: {response.status_code} - {response.text}"
            print(error_msg)
            return error_msg

    except Exception as e:
        error_msg = f"⚠️ Error creating employee: {e}"
        print(error_msg)
        return error_msg


@mcp.tool(annotations={"title": "HtmlFormSubmit"})
def htmlformsubmit(name: str, email: str) -> str:
    """Handle HTML form submission via MCP"""
    print(f"Received form data: {name} ({email})")

    return f"Received submission from {name} with email {email}"


def handle_employee_created(event: Event):
    print(f"📢 EventBus received: {event.name} -> {event.payload}")


event_bus.subscribe("employee.created", handle_employee_created)


if __name__ == "__main__":
    print("hello benning start of autoserver.py")
    print("🚀 Starting FrappeEmployeeServer MCP on http://127.0.0.1:8000/mcp ...")
    mcp.run(transport="http")
