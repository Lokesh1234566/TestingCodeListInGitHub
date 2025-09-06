import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue

INPUT_DIR = "./allinvoices"
os.makedirs(INPUT_DIR, exist_ok=True)


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        super().__init__()
        self.event_queue = event_queue

    """def on_any_event(self, event):
        # Add event details to the queue
        self.event_queue.put(event)"""

    def on_created(self, event):
        # Add event details to the queue
        self.event_queue.put(event)


def process_batch(events):
    # This function processes a batch of events
    print(f"Processing batch of {len(events)} events:")
    for event in events:
        print(f"  {event.event_type}: {event.src_path}")
    # Add your batch processing logic here (e.g., database updates, file operations)


def consumer_thread(event_queue, batch_size=10, batch_timeout=2):
    batch = []
    last_processed_time = time.time()
    while True:
        try:
            event = event_queue.get(timeout=1)  # Non-blocking wait for 1 second
            batch.append(event)
        except Exception:  # queue.Empty
            pass

        current_time = time.time()
        if len(batch) >= batch_size or (
            batch and (current_time - last_processed_time >= batch_timeout)
        ):
            process_batch(batch)
            batch = []
            last_processed_time = current_time
        time.sleep(0.1)  # Small delay to prevent busy-waiting


if __name__ == "__main__":
    event_queue = Queue()
    event_handler = MyEventHandler(event_queue)
    observer = Observer()
    observer.schedule(
        event_handler,
        path=INPUT_DIR,
        recursive=True,
    )  # Monitor current directory
    observer.start()

    # Start the consumer thread
    import threading

    consumer = threading.Thread(target=consumer_thread, args=(event_queue,))
    consumer.daemon = True  # Allow main program to exit even if this thread is running
    consumer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
