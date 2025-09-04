from EventLogForEventure import EventLog1


class AdventureGame:
    """Simple DB test wrapper using EventLog1."""

    def __init__(self) -> None:
        """Initialize with DB operations."""
        test123 = EventLog1()
        print(test123.save_to_db())  # Insert hardcoded data

        showdbdata = EventLog1()
        print(showdbdata.show_db_data())  # Show data from DB


if __name__ == "__main__":
    game = AdventureGame()
