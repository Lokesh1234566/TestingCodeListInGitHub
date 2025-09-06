import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue
import threading

INPUT_DIR = "./allinvoices"
os.makedirs(INPUT_DIR, exist_ok=True)


class PDFHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        super().__init__()
        self.event_queue = event_queue

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".pdf"):
            self.event_queue.put(event)
            # print("len of queue", len(self.event_queue))


def process_batch(events):
    """
    Process a batch of PDF events:
    - Print details
    - Launch client.py for each detected PDF
    """
    print(f"\n📦 Processing batch of {len(events)} event(s):")
    for event in events:
        pdf_path = event.src_path
        base_name = os.path.basename(pdf_path)
        # print(f"📂 New PDF detected: {pdf_path}")

        # 🚀 Launch client.py for this PDF
        process = subprocess.Popen(["python", "client.py", pdf_path])
        print(f"✅ Started client.py for {base_name} (PID: {process.pid})")


def consumer_thread(event_queue, batch_size=20, batch_timeout=0):
    """
    Collects events in a batch and processes them.
    """
    batch = []
    last_processed_time = time.time()
    while True:
        try:
            event = event_queue.get(timeout=1)
            batch.append(event)
        except Exception:  # queue.Empty
            pass
        current_time = time.time()
        if len(batch) >= batch_size:
            process_batch(batch)
            batch = []
            last_processed_time = current_time
        current_time = time.time()

        if (
            len(batch) <= batch_size
            and batch
            and current_time - last_processed_time >= 10
        ):
            process_batch(batch)
            batch = []
            last_processed_time = current_time
        # elif len(batch) <= batch_size:
        #     process_batch(batch)
        #     batch = []

        time.sleep(1)  # Prevent busy-waiting


if __name__ == "__main__":
    print(f"👀 Watching {INPUT_DIR} for new PDFs...")

    event_queue = Queue()
    event_handler = PDFHandler(event_queue)

    observer = Observer()
    observer.schedule(event_handler, path=INPUT_DIR, recursive=False)
    observer.start()

    # Start consumer thread
    consumer = threading.Thread(target=consumer_thread, args=(event_queue,))
    consumer.daemon = True
    consumer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping observer...")
        observer.stop()

    observer.join()
    print("👋 Exited cleanly.")
