import subprocess
from eventure import Event, EventBus, EventLog, EventQuery


class AdventureGame:
    """A simple text-based adventure game simulation using eventure."""

    def __init__(self) -> None:
        """Initialize the adventure game with event system."""
        self.event_log: EventLog = EventLog()
        self.event_bus: EventBus = EventBus(self.event_log)

        # Subscribe to events

        self.event_bus.subscribe("eventbus.send", self._handle_eventbus_send)
        self.game_over = False

    def start_game(self) -> None:

        # Start the game - this will trigger the subscribed handler
        self.event_bus.publish(
            "eventbus.send", {"message": "Welcome to the Adventure Game!"}
        )

    def _handle_eventbus_send(self, event: Event) -> None:

        if self.game_over:  # prevent loop
            return

        self.game_over = True  # mark finished

        output = subprocess.check_output(
            ["python", "./client.py", "this is from event bus"], text=True
        )
        print("Output OUTPUT OUTPUT :", output)

        outcome: str = "game finished"

        # publish a *different event* instead of "eventbus.send"
        self.event_bus.publish(
            "game.final_score",
            {"outcome": outcome},
            parent_event=event,
        )


if __name__ == "__main__":
    # Create and run the adventure game
    game: AdventureGame = AdventureGame()
    game.start_game()
