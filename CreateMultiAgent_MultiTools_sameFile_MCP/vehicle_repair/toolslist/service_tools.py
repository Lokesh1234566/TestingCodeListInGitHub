# from fastmcp import FastMCP
# from agent.service_agent import bus

# # Use a shared MCP instance
# mcp = FastMCP(name="Vehicle + Billing")


# @mcp.tool(annotations={"title": "Service Inserted"})
# def service_inserted(service_id: str, vehicle_no: str, description: str) -> str:
#     event = {
#         "service_id": service_id,
#         "vehicle": vehicle_no,
#         "description": description,
#     }
#     bus.publish("service_inserted", event)
#     return f"Service inserted: {event}"


# @mcp.tool(annotations={"title": "Service Updated"})
# def service_updated(service_id: str, status: str) -> str:
#     event = {"service_id": service_id, "status": status}
#     bus.publish("service_updated", event)
#     return f"Service updated: {event}"


# @mcp.tool(annotations={"title": "Service Paid"})
# def service_paid(service_id: str, amount: float, payment_mode: str) -> str:
#     event = {"service_id": service_id, "amount": amount, "mode": payment_mode}
#     bus.publish("service_paid", event)
#     return f"Service Paid: {event}"


from fastmcp import FastMCP

mcp = FastMCP(name="Vehicle + Billing")


@mcp.tool(annotations={"title": "Service Inserted"})
def service_inserted(service_id: str, vehicle_no: str, description: str) -> str:
    from agent.service_agent import bus

    event = {
        "service_id": service_id,
        "vehicle": vehicle_no,
        "description": description,
    }
    bus.publish("service_inserted", event)
    return f"Service inserted: {event}"


@mcp.tool(annotations={"title": "Service Updated"})
def service_updated(service_id: str, status: str) -> str:
    from agent.service_agent import bus

    event = {"service_id": service_id, "status": status}
    bus.publish("service_updated", event)
    return f"Service updated: {event}"


@mcp.tool(annotations={"title": "Service Paid"})
def service_paid(service_id: str, amount: float, payment_mode: str) -> str:
    from agent.service_agent import bus

    event = {"service_id": service_id, "amount": amount, "mode": payment_mode}
    bus.publish("service_paid", event)
    return f"Service Paid: {event}"
