# from eventure import EventLog, EventBus

# # Initialize EventBus + Log
# log = EventLog()
# bus = EventBus(log)


# # Example subscribers
# def on_service_inserted(event):
#     print(f"[Listener] Service Inserted Event Received: {event}")


# def on_service_updated(event):
#     print(f"[Listener] Service Updated Event Received: {event}")


# def on_service_paid(event):
#     print(f"[Listener] Service Paid Event Received: {event}")


# # Subscribe listeners
# bus.subscribe("service_inserted", on_service_inserted)
# bus.subscribe("service_updated", on_service_updated)
# bus.subscribe("service_paid", on_service_paid)


from eventure import EventLog, EventBus
from agent.db import conn, cursor

log = EventLog()
bus = EventBus(log)


def on_service_inserted(event):
    data = event.data
    cursor.execute(
        "INSERT INTO services (service_id, vehicle_no, description) VALUES (%s, %s, %s)",
        (data["service_id"], data["vehicle"], data["description"]),
    )
    conn.commit()
    print(f"[DB] Service Inserted: {data}")


def on_service_updated(event):
    data = event.data
    cursor.execute(
        "UPDATE services SET status=%s WHERE service_id=%s",
        (data["status"], data["service_id"]),
    )
    conn.commit()
    print(f"[DB] Service Updated: {data}")


def on_service_paid(event):
    data = event.data
    cursor.execute(
        "UPDATE services SET amount=%s, payment_mode=%s WHERE service_id=%s",
        (data["amount"], data["mode"], data["service_id"]),
    )
    conn.commit()
    print(f"[DB] Service Paid: {data}")

    # generate invoice
    from agent.billing_agent import billing_bus

    invoice = {
        "invoice_id": f"INV-{data['service_id']}",
        "service_id": data["service_id"],
        "customer": "John Doe",
        "amount": data["amount"],
        "payment_mode": data["mode"],
    }
    billing_bus.publish("invoice_generated", invoice)


# Subscribe listeners
bus.subscribe("service_inserted", on_service_inserted)
bus.subscribe("service_updated", on_service_updated)
bus.subscribe("service_paid", on_service_paid)
