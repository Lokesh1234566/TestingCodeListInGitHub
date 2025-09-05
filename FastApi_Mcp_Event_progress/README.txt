📘 Project README

This project demonstrates a FastAPI + MCP + Event-driven system that
processes PDF files, streams progress updates, and reports results using
an event bus.

✨ Features

-   FastAPI server (/process, /process/stream, /results) for item
    processing
-   MCP (Model Context Protocol) tool integration with progress updates
-   Client (FastApi_client.py) to stream processing results from FastAPI
-   Event-driven workflow using EventBus and Watchdog for file
    monitoring
-   Automatic detection of PDF files (3DE*.pdf and Vee*.pdf) in a
    watched folder
-   Real-time progress and result event publishing

⚙️ How It Works

1.  Start the MCP + FastAPI server (python main.py).
2.  The FastAPI server listens on port 5001 for processing requests.
3.  Client (FastApi_client.py) sends items to /process/stream and prints
    progress.
4.  The InvoicePdf class monitors watched_folder for new PDF files.
5.  When a matching PDF appears, an event triggers the client to process
    it.
6.  Progress and results are published via the EventBus.

📦 Requirements

-   Python 3.9+
-   fastapi
-   uvicorn
-   httpx
-   watchdog
-   eventure
-   fastmcp
-   reportlab

🚀 Usage

1.  Install dependencies: pip install -r requirements.txt
2.  Run the main server: python main.py
3.  Run the folder watcher: python invoice_watcher.py
4.  Drop a PDF file (3DE*.pdf or Vee*.pdf) into watched_folder.
5.  Monitor terminal logs for progress and results.

✅ You now have a working FastAPI + Event-driven PDF processor!


progress is generated on the server side and streamed to the client:

Server side (FastAPI + MCP):

The function process_items_generator yields progress updates ({"progress": i, "total": total, "message": ...}) as it processes each item.

In FastAPI’s /process/stream endpoint, these updates are streamed back to the client using Server-Sent Events (SSE).

In the MCP tool (process_items), progress is reported via ctx.report_progress.

Client side (FastApi_client.py):

The client doesn’t calculate progress itself.

It listens to the streamed messages from the server and simply prints/logs the progress updates it receives (e.g., [Client Progress] 40% - step 2/5 - processing ...).

👉 So the server is responsible for generating progress, and the client only displays it.
