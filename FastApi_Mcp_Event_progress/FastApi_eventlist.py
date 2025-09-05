import sys
import subprocess
import time
import os
from eventure import Event, EventBus, EventLog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "watched_folder"


class InvoicePdf:
    def __init__(self) -> None:
        self.event_log: EventLog = EventLog()
        self.event_bus: EventBus = EventBus(self.event_log)

        self.event_bus.subscribe("eventbus.file_detected", self._handle_file)
        self.event_bus.subscribe("eventbus.progress", self._handle_progress)
        self.event_bus.subscribe("eventbus.result", self._handle_result)

    def start_watch(self):
        ensure_folder(WATCH_FOLDER)
        event_handler = PDFHandler(self.event_bus)
        observer = Observer()
        observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
        observer.start()

        print(f"Watching folder: {WATCH_FOLDER} for '3DE*.pdf' or 'Vee*.pdf' files...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("Stopped watching.")
        observer.join()

    def _handle_file(self, event: Event):
        filename = event.data["filename"]
        print(f"[Event] Processing PDF: {filename}")
        self._run_client(filename)

    def _run_client(self, msg: str) -> None:
        process = subprocess.Popen(
            ["python", "./FastApi_client.py", msg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        assert process.stdout is not None
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            print(line)

            if line.startswith("[Client Progress]"):
                try:
                    percent = float(line.split("%")[0].split()[-1])
                except Exception:
                    percent = 0.0
                self.event_bus.publish(
                    "eventbus.progress",
                    {"stage": msg, "progress": percent, "response": line},
                )
            elif line.startswith("[Client Result]"):
                self.event_bus.publish(
                    "eventbus.result",
                    {"stage": msg, "response": line},
                )

        process.wait()
        if process.returncode != 0:
            err = process.stderr.read()
            print(f"Client subprocess failed: {err}")

    def _handle_progress(self, event: Event) -> None:
        print(
            f"[Progress Event] {event.data['stage']}: "
            f"{event.data['progress']:.1f}% | {event.data['response']}"
        )

    def _handle_result(self, event: Event) -> None:
        print(
            f"[Result Event] {event.data['stage']} finished → {event.data['response']}"
        )


class PDFHandler(FileSystemEventHandler):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            lower = filename.lower()
            if (lower.startswith("3de") and lower.endswith(".pdf")) or (
                lower.startswith("vee") and lower.endswith(".pdf")
            ):
                print(f"New matching PDF detected: {filename}")
                self.event_bus.publish("eventbus.file_detected", {"filename": filename})
            else:
                print(f"Ignored file: {filename}")


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")


if __name__ == "__main__":
    pdfview = InvoicePdf()
    pdfview.start_watch()
