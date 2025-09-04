# from toolslist.service_tools import mcp  # import shared instance
# from agent.billing_agent import billing_bus


# @mcp.tool(annotations={"title": "Invoice Generated"})
# def invoice_generated(invoice_id: str, customer: str, amount: float) -> str:
#     event = {"invoice_id": invoice_id, "customer": customer, "amount": amount}
#     billing_bus.publish("invoice_generated", event)
#     return f"Invoice Generated: {event}"


# @mcp.tool(annotations={"title": "Invoice Paid"})
# def invoice_paid(invoice_id: str, payment_mode: str) -> str:
#     event = {"invoice_id": invoice_id, "mode": payment_mode}
#     billing_bus.publish("invoice_paid", event)
#     return f"Invoice Paid: {event}"


from toolslist.service_tools import mcp


@mcp.tool(annotations={"title": "Invoice Generated"})
def invoice_generated(invoice_id: str, customer: str, amount: float) -> str:
    from agent.billing_agent import billing_bus

    event = {"invoice_id": invoice_id, "customer": customer, "amount": amount}
    billing_bus.publish("invoice_generated", event)
    return f"Invoice Generated: {event}"


@mcp.tool(annotations={"title": "Invoice Paid"})
def invoice_paid(invoice_id: str, payment_mode: str) -> str:
    from agent.billing_agent import billing_bus

    event = {"invoice_id": invoice_id, "mode": payment_mode}
    billing_bus.publish("invoice_paid", event)
    return f"Invoice Paid: {event}"
