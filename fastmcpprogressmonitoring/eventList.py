import sys
import subprocess
from eventure import Event, EventBus, EventLog


class AdventureGame:
    def __init__(self) -> None:
        self.event_log: EventLog = EventLog()
        self.event_bus: EventBus = EventBus(self.event_log)

        self.event_bus.subscribe("eventbus.first_arg", self._handle_first_arg)
        self.event_bus.subscribe("eventbus.second_arg", self._handle_second_arg)
        self.event_bus.subscribe("eventbus.progress", self._handle_progress)
        self.event_bus.subscribe("eventbus.result", self._handle_result)

    def start_game(self, arg1: str, arg2: str) -> None:
        self.event_bus.publish("eventbus.first_arg", {"value": arg1})
        self.event_bus.publish("eventbus.second_arg", {"value": arg2})

    def _handle_first_arg(self, event: Event) -> None:
        self._run_client("FirstEvent", int(event.data["value"]))

    def _handle_second_arg(self, event: Event) -> None:
        self._run_client("SecondEvent", int(event.data["value"]))

    def _run_client(self, msg: str, count: int) -> None:
        process = subprocess.Popen(
            ["python", "./event_client.py", msg, str(count)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Stream client output
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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python eventList.py <arg1> <arg2>")
        sys.exit(1)

    arg1, arg2 = sys.argv[1], sys.argv[2]
    game = AdventureGame()
    game.start_game(arg1, arg2)
