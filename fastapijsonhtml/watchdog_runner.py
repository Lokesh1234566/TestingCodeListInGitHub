import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATH = "employees/incoming"  # folder to watch


class JSONHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            print(f"New JSON detected: {event.src_path}")

            # Notify FastAPI
            try:
                resp = requests.post(
                    "http://127.0.0.1:30000/json-found",
                    json={"path": event.src_path},
                    timeout=15,
                )
                print(f"FastAPI Response: {resp.json()}")
            except Exception as e:
                print(f"Error notifying FastAPI: {e}")


def main():
    os.makedirs(WATCH_PATH, exist_ok=True)

    observer = Observer()
    event_handler = JSONHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    observer.start()

    print(f"Watching folder: {WATCH_PATH} ... (drop JSON files here)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping services...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
