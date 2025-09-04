README

Unified Vehicle Repair + Billing System (Event-Driven with MCP)
--------------------------------------------------------------

## Overview
This project demonstrates an **event-driven architecture** for a Vehicle Repair
and Billing System using Python, MySQL, and the `fastmcp` library.

The system connects multiple agents (service and billing) with an event bus
(`EventBus`) and provides MCP tools to interact with the database in a modular,
decoupled manner.

Events trigger actions automatically, such as updating services and generating invoices.

---

## Features
- Event-driven architecture using `EventBus` and `EventLog`.
- Service Management:
  - Insert service
  - Update service status
  - Record service payment
- Billing Management:
  - Generate invoices
  - Mark invoices as paid
- Database schema setup with MySQL.
- MCP Tools for service and billing exposed via HTTP server.
- Client script to simulate tool invocations.
- EventBus pattern with **publish** and **subscribe** for decoupling.

---

## Project Structure
```
project/
│
├── agent/
│   ├── db.py               # Database connection + schema creation
│   ├── service_agent.py    # Handles service-related events, publishes invoices
│   └── billing_agent.py    # Handles billing-related events
│
├── toolslist/
│   ├── service_tools.py    # MCP tools for service events
│   └── billing_tools.py    # MCP tools for billing events
│
├── server.py               # Unified MCP server entrypoint
├── client.py               # Test client to call MCP tools
└── README.txt              # Documentation
```

---

## Database Schema
### Table: `services`
- `id` (INT, Primary Key, Auto Increment)
- `service_id` (VARCHAR, Unique)
- `vehicle_no` (VARCHAR)
- `description` (VARCHAR)
- `status` (VARCHAR)
- `amount` (FLOAT)
- `payment_mode` (VARCHAR)

### Table: `invoices`
- `id` (INT, Primary Key, Auto Increment)
- `invoice_id` (VARCHAR, Unique)
- `service_id` (VARCHAR)
- `customer` (VARCHAR)
- `amount` (FLOAT)
- `payment_mode` (VARCHAR)

---

## EventBus Usage (Publish/Subscribe)

The system uses **EventBus** from `eventure` to decouple logic between agents.

### Service Agent Subscriptions
- `service_inserted` → Inserts new service into DB.
- `service_updated` → Updates service status in DB.
- `service_paid` → Updates payment info in DB and **publishes** `invoice_generated`.

### Billing Agent Subscriptions
- `invoice_generated` → Inserts invoice into DB.
- `invoice_paid` → Updates invoice payment mode in DB.

### Example Flow
1. **Tool call** `service_paid` publishes:
   ```
   bus.publish("service_paid", {"service_id": "S001", "amount": 2500.0, "mode": "UPI"})
   ```
   → Service Agent handles DB update.  
   → Publishes `invoice_generated` with invoice details.

2. **Billing Agent** subscribed to `invoice_generated`:
   ```
   billing_bus.subscribe("invoice_generated", on_invoice_generated)
   ```
   → Creates invoice in DB.

3. Later, **Tool call** `invoice_paid` publishes:
   ```
   billing_bus.publish("invoice_paid", {"invoice_id": "INV-S001", "mode": "Card"})
   ```
   → Updates DB to mark invoice as paid.

---

## Running the Project
1. Ensure MySQL is running and update `DB_CONFIG` in `db.py` with your credentials.
2. Install dependencies:
   ```
   pip install fastmcp mysql-connector-python eventure
   ```
3. Start the MCP server:
   ```
   python server.py
   ```
   Output:
   ```
   🚀 Starting Unified Vehicle Repair + Billing MCP Server with EventBus...
   ```

4. Run the client to simulate workflow:
   ```
   python client.py
   ```

---

## Example Client Run Output
```
✅ MCP Server reachable
Service inserted: {'service_id': 'S001', 'vehicle': 'KA01AB1234', 'description': 'Oil change'}
Service updated: {'service_id': 'S001', 'status': 'In Progress'}
Service Paid: {'service_id': 'S001', 'amount': 2500.0, 'mode': 'UPI'}
[DB] Service Paid: {...}
[DB] Invoice Generated: {...}
Invoice Paid: {'invoice_id': 'INV-S001', 'mode': 'Card'}
```

---

## Key Concepts
- **EventBus**: Enables decoupled communication between services and billing.
- **Subscribe**: Agents subscribe to events they need to handle.
- **Publish**: Agents/tools publish events that trigger subscribed listeners.
- **Event-Driven Design**: Actions are triggered by events, not direct calls.
- **MCP Tools**: Expose actions via APIs for external systems to interact with.
- **MySQL Database**: Persistent storage for services and invoices.

---

## Security Considerations
- Always validate event data before processing.
- Protect MCP server endpoints if exposed in production.
- Use environment variables for DB credentials instead of hardcoding.
