

This project demonstrates an event-driven architecture using:

FastMCP (server + client communication)

Eventure (event bus + event log)

Watchdog (file system monitoring)

Flask (web API for manual triggers and result fetching)

It combines file watching, server communication, and an API layer for handling PDF processing events.

📂 Project Structure
.
├── server.py       # FastMCP server (InvoiceServer)
├── client.py       # FastMCP client to call server tools
├── app.py          # Main event system with Watchdog + Flask API
├── watched_folder/ # Folder monitored for incoming PDFs

⚡ Features

FastMCP Server (server.py)

Exposes a tool printFromBusServer for remote calls.

Listens at http://127.0.0.1:8000/mcp.

Client (client.py)

Sends messages to the MCP server.

Prints the server’s response.

Event Bus System (app.py)

Uses Eventure to manage events (3DE and Vee).

Subscribes to events and triggers client calls.

File Watching

Any new file in watched_folder/ starting with:

3de...pdf → triggers a 3DE event.

vee...pdf → triggers a Vee event.

Other files are ignored.

Flask Web API

POST /api/start → manually trigger runs (num_3de, num_vee).

GET /api/start → fetch history of triggered runs.

▶️ How to Run
1. Start the MCP Server
python server.py


You should see:

🚀 Starting InvoiceServer on http://127.0.0.1:8000/mcp ...

2. Start the Event System
python app.py


This will:

Start Flask API on port 5000.

Watch watched_folder/ for new PDF files.

3. Test the Client Directly
python client.py "Hello from Client"


Expected output:

📩 Call From Client with: Hello from Client
Server Response: ✅ Server received: Hello from Client

🌐 API Usage
Trigger Runs (POST)
curl -X POST http://127.0.0.1:5000/api/start \
     -H "Content-Type: application/json" \
     -d '{"num_3de": 2, "num_vee": 1}'


Response:

{
  "status": "ok",
  "runs": [
    {"type": "3de", "output": "✅ Server received: Triggered 3DE run 1"},
    {"type": "3de", "output": "✅ Server received: Triggered 3DE run 2"},
    {"type": "vee", "output": "✅ Server received: Triggered Vee run 1"}
  ]
}

Fetch Results (GET)
curl http://127.0.0.1:5000/api/start


Response:

{
  "last_runs": [
    {"type": "3de", "filename": "3de_test.pdf", "output": " Server received: Processing 3DE file 3de_test.pdf"},
    {"type": "vee", "filename": "vee_test.pdf", "output": " Server received: Processing Vee file vee_test.pdf"}
  ]
}

📊 Workflow Summary

Drop a PDF into watched_folder/.

If it starts with 3de → 3DE event → client call → MCP server.

If it starts with vee → Vee event → client call → MCP server.

Manual triggers available via API.

Results stored in memory (last_runs) and can be queried with GET /api/start.

✅ Requirements

Install dependencies:

pip install fastmcp flask watchdog eventure