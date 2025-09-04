# from eventure import EventLog, EventBus

# # Initialize EventBus + Log for Billing Agent
# billing_log = EventLog()
# billing_bus = EventBus(billing_log)


# # Example subscribers
# def on_invoice_generated(event):
#     print(f"[Billing Listener] Invoice Generated Event Received: {event}")


# def on_invoice_paid(event):
#     print(f"[Billing Listener] Invoice Paid Event Received: {event}")


# # Subscribe listeners
# billing_bus.subscribe("invoice_generated", on_invoice_generated)
# billing_bus.subscribe("invoice_paid", on_invoice_paid)


from eventure import EventLog, EventBus
from agent.db import conn, cursor

billing_log = EventLog()
billing_bus = EventBus(billing_log)


def on_invoice_generated(event):
    data = event.data
    cursor.execute(
        "INSERT INTO invoices (invoice_id, service_id, customer, amount, payment_mode) VALUES (%s, %s, %s, %s, %s)",
        (
            data["invoice_id"],
            data.get("service_id"),
            data["customer"],
            data["amount"],
            data.get("payment_mode"),
        ),
    )
    conn.commit()
    print(f"[DB] Invoice Generated: {data}")


def on_invoice_paid(event):
    data = event.data
    cursor.execute(
        "UPDATE invoices SET payment_mode=%s WHERE invoice_id=%s",
        (data["mode"], data["invoice_id"]),
    )
    conn.commit()
    print(f"[DB] Invoice Paid: {data}")


# Subscribe listeners
billing_bus.subscribe("invoice_generated", on_invoice_generated)
billing_bus.subscribe("invoice_paid", on_invoice_paid)
