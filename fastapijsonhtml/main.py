# main.py
from fastapi import FastAPI, Request, BackgroundTasks, Form
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import subprocess
import os
import time
import psutil

app = FastAPI()
server_process = None  # global reference for autoserver.py


# --------------------------------------------------
# Utility: check if autoserver.py already running
# --------------------------------------------------
def is_mcp_running() -> bool:
    global server_process
    if server_process and server_process.poll() is None:
        return True

    # double-check system process list
    for proc in psutil.process_iter(["cmdline"]):
        try:
            if proc.info["cmdline"] and "./autoserver.py" in proc.info["cmdline"]:
                return True
        except Exception:
            continue
    return False


# --------------------------------------------------
# Start MCP server (autoserver.py)
# --------------------------------------------------
def start_mcp_server():
    global server_process
    if not is_mcp_running():
        print("🚀 Starting MCP server (autoserver.py)...")
        server_process = subprocess.Popen(
            ["python", "./autoserver.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(3)  # allow server to boot
        print(f"✅ autoserver.py started with PID {server_process.pid}")


# --------------------------------------------------
# Stop MCP server gracefully
# --------------------------------------------------
def stop_mcp_server():
    global server_process
    if server_process and server_process.poll() is None:
        print("🛑 Stopping autoserver.py...")
        server_process.terminate()
        server_process.wait()
        print("✅ autoserver.py stopped")


# --------------------------------------------------
# FastAPI routes
# --------------------------------------------------
@app.get("/healthcheck/")
def healthcheck():
    return {"status": "ok"}


@app.post("/json-found")
async def json_found(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    json_path = body.get("path")

    if not json_path or not os.path.exists(json_path):
        return JSONResponse(content={"error": "Invalid JSON path"}, status_code=400)

    # Ensure MCP server is running
    start_mcp_server()

    # Start autoclient.py in background
    background_tasks.add_task(
        subprocess.Popen, ["python", "./autoclient.py", json_path]
    )

    return JSONResponse(
        content={"message": f"📂 JSON found → processing {os.path.basename(json_path)}"}
    )


# --------------------------------------------------
# Lifespan events
# --------------------------------------------------
@app.on_event("shutdown")
def shutdown_event():
    stop_mcp_server()


@app.post("/submitdata", response_class=HTMLResponse)
async def handle_form_submission(
    request: Request, name: str = Form(...), email: str = Form(...)
):
    # Process the form data here
    message = f"Received submission from {name} with email {email}."
    return "Health - Great"


# --------------------------------------------------
# Run FastAPI
# --------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=30000)
