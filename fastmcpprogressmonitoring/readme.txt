The MCP specification includes a progress notification mechanism that allows communicating the progress of long-running operations. Progress updates are useful for:

- Providing feedback for long-running server operations
- Updating users about the status of operations that might take time to complete
- Enabling client applications to display progress indicators for better UX

An MCP (Model Context Protocol) server can communicate progress for a long-running task by utilizing the Context object, specifically its progress reporting capabilities. This allows the server to send updates back to the client application, providing real-time feedback on the task's advancement.

# Event-Driven Progress Monitoring Demo

This project demonstrates event-driven progress monitoring using:
- fastmcp (for server–client communication with progress updates)
- eventure (for event bus and event logging)

The system is split into three components:

1. event_server.py – Async server that processes items and streams progress updates.
2. event_client.py – Client that connects to the server, executes tasks, and prints progress + results.
3. eventList.py – Event manager/game orchestrator that spawns clients as subprocesses, parses their output, and publishes events to an in-process event bus.

------------------------------------------------------------
File Overview
------------------------------------------------------------

event_server.py
------------------
- Defines a FastMCP server with one tool: process_items.
- Simulates processing a list of items while reporting progress back to the client using ctx.report_progress.
- Runs on http://127.0.0.1:8000/mcp.

Usage:
    python event_server.py

------------------------------------------------------------

event_client.py
---------------
- Connects to the MCP server (http://127.0.0.1:8000/mcp).
- Sends a list of items (<msg>-1, <msg>-2, … <msg>-N) for processing.
- Prints:
  * Progress lines (parsed by eventList.py)
  * Final result

Usage:
    python event_client.py <message> <count>

Example:
    python event_client.py Hello 3

------------------------------------------------------------

eventList.py
------------
- Main orchestrator that sets up an EventBus.
- Subscribes to events: eventbus.first_arg, eventbus.second_arg, eventbus.progress, eventbus.result.
- Spawns event_client.py as a subprocess for each input argument.
- Parses client stdout and republishes as events.

Usage:
    python eventList.py <arg1> <arg2>

Example:
    python eventList.py 3 2

------------------------------------------------------------
Flow Summary
------------------------------------------------------------
1. eventList.py publishes first_arg and second_arg events.
2. Event handlers spawn event_client.py subprocesses.
3. Each client calls the MCP server’s process_items.
4. Server streams progress via ctx.report_progress.
5. Client prints [Client Progress] lines.
6. eventList.py reads stdout and republishes as eventbus.progress and eventbus.result.

------------------------------------------------------------
Requirements
------------------------------------------------------------
Install dependencies:
    pip install fastmcp eventure

Python 3.10+ recommended.

------------------------------------------------------------
Running the Demo
------------------------------------------------------------
1. Start the server:
    python event_server.py

2. In another terminal, run the orchestrator:
    python eventList.py 4 3

This will:
- Start two clients (FirstEvent, SecondEvent).
- Each processes items and streams progress back.
- The EventBus logs progress + results in real time.

------------------------------------------------------------
Notes
------------------------------------------------------------
- Progress source: The server (event_server.py) generates progress events.
- Progress handling: The client (event_client.py) formats and prints them.
- Progress consumption: The orchestrator (eventList.py) parses client stdout and republishes events for logging or other use.
