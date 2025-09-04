import os
import time
import subprocess
import threading
from flask import Flask, request, jsonify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from eventure import Event, EventBus, EventLog

WATCH_FOLDER = "watched_folder"


# ------------------ EventBus Game ------------------
class AdventureGame:
    def __init__(self, last_runs):
        self.event_log = EventLog()
        self.event_bus = EventBus(self.event_log)
        self.last_runs = last_runs

        # subscribe events
        self.event_bus.subscribe("eventbus.3de_event", self.handle_3de)
        self.event_bus.subscribe("eventbus.vee_event", self.handle_vee)

    def handle_3de(self, event: Event):
        filename = event.data.get("filename", "")
        print(f"🔥 Handling 3DE Event for {filename}")
        out = subprocess.check_output(
            ["python", "./client.py", f"Processing 3DE file {filename}"],
            text=True,
            encoding="utf-8",
        )
        print(out)
        self.last_runs.append(
            {"type": "3de", "filename": filename, "output": out.strip()}
        )

    def handle_vee(self, event: Event):
        filename = event.data.get("filename", "")
        print(f"🔥 Handling Vee Event for {filename}")
        out = subprocess.check_output(
            ["python", "./client.py", f"Processing Vee file {filename}"],
            text=True,
            encoding="utf-8",
        )
        print(out)
        self.last_runs.append(
            {"type": "vee", "filename": filename, "output": out.strip()}
        )


# ------------------ Watchdog ------------------
class PDFHandler(FileSystemEventHandler):
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path).lower()
            if filename.startswith("3de") and filename.endswith(".pdf"):
                self.event_bus.publish("eventbus.3de_event", {"filename": filename})
            elif filename.startswith("vee") and filename.endswith(".pdf"):
                self.event_bus.publish("eventbus.vee_event", {"filename": filename})
            else:
                print(f"Ignored: {filename}")


def start_watch(event_bus):
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)
    handler = PDFHandler(event_bus)
    observer = Observer()
    observer.schedule(handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching {WATCH_FOLDER} for 3DE and Vee PDFs...")
    return observer


# ------------------ Flask Web API ------------------
app = Flask(__name__)

# shared run history
last_runs = []
game = AdventureGame(last_runs)


@app.route("/api/start", methods=["POST"])
def start_process():
    """Manually trigger runs by POST body"""
    data = request.json or {}
    num_3de = int(data.get("num_3de", 0))
    num_vee = int(data.get("num_vee", 0))

    responses = []
    for i in range(num_3de):
        out = subprocess.check_output(
            ["python", "./client.py", f"Triggered 3DE run {i+1}"],
            text=True,
            encoding="utf-8",
        )
        responses.append({"type": "3de", "output": out.strip()})

    for i in range(num_vee):
        out = subprocess.check_output(
            ["python", "./client.py", f"Triggered Vee run {i+1}"],
            text=True,
            encoding="utf-8",
        )
        responses.append({"type": "vee", "output": out.strip()})

    last_runs.extend(responses)  # keep history
    return jsonify({"status": "ok", "runs": responses})


@app.route("/api/start", methods=["GET"])
def start_process_get():
    """Fetch the collected results"""
    if not last_runs:
        return jsonify({"message": "No runs triggered yet."})
    return jsonify({"last_runs": last_runs})


def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)


# ------------------ Main ------------------
if __name__ == "__main__":
    observer = start_watch(game.event_bus)

    # Run Flask API in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("🚀 Event system + Watchdog + WebAPI started.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped.")
    observer.join()
