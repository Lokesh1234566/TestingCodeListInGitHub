README – Event-Driven Adventure Game with MCP Server & Client
📌 Overview

This project demonstrates an event-driven architecture using:

eventure for EventBus communication.

subprocess for external process execution (client.py).

fastmcp for building a Multi Context Protocol (MCP) server and client.

The system is composed of three parts:

AdventureGame → Publishes events and triggers client.py.

FastMCPClientTest → Connects to MCP server and calls tools.

InvoiceServer (FastMCP) → Runs an MCP server exposing tools.

⚙️ Project Structure
project/
│
├── adventure_game.py   # AdventureGame using EventBus + subprocess
├── client.py           # Called from AdventureGame (prints message)
├── server.py           # MCP Server (FastMCP)
└── README.txt          # Documentation

🚀 Components
1. AdventureGame (eventure + subprocess)

Uses EventBus and EventLog from eventure.

Subscribes to "eventbus.send" events.

When triggered, it:

Calls client.py via subprocess.check_output.

Publishes a new "game.final_score" event.

self.event_bus.subscribe("eventbus.send", self._handle_eventbus_send)
self.event_bus.publish("eventbus.send", {"message": "Welcome to the Adventure Game!"})

2. FastMCP Client (FastMCPClientTest)

Connects to the MCP server at http://127.0.0.1:8000/mcp.

Calls the registered tool "printFromBusServer".

Prints the result and confirms interaction.

ret1 = await client.call_tool("printFromBusServer", "")
print("ret1", ret1)

3. FastMCP Server (InvoiceServer)

Built using FastMCP.

Exposes a tool "printFromBusServer".

Responds to client calls and returns "From server".

@mcp.tool(annotations={"title": "printFromBusServer"})
def printFromBusServer() -> str:
    print("call From Client")
    return "From server"

🔄 Flow of Execution

Start the MCP Server

python server.py


Runs Server with the tool printFromBusServer.

Run Adventure Game

python adventure_game.py


Publishes "eventbus.send".

Runs client.py as subprocess.

Publishes "game.final_score".

Run MCP Client Test

python client.py


Connects to MCP server.

Calls "printFromBusServer" and prints the result.

📬 Event System

Subscribe: self.event_bus.subscribe("eventbus.send", handler)

Publish: self.event_bus.publish("eventbus.send", data)

Parent Event Linking: Used for chaining (parent_event=event).

✅ Example Output

When running all together:

🚀 Starting Server...
call From Client
From server

Output OUTPUT OUTPUT : this is from event bus
ret1 From server
Call From EventBus

📖 Requirements

Python 3.9+

Install dependencies:

pip install eventure fastmcp