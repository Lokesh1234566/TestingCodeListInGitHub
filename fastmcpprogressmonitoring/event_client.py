import sys
import asyncio
from fastmcp import Client


async def main(msg: str, count: int):
    # Progress handler prints a line your eventList.py can parse
    async def progress_handler(
        progress: float, total: float | None, message: str | None
    ):
        if total:
            pct = (progress / total) * 100
            step = f"{int(progress)}/{int(total)}"
        else:
            pct = 0.0
            step = f"{int(progress)}/?"
        print(
            f"[Client Progress] {pct:.1f}% - step {step}{' - ' + message if message else ''}",
            flush=True,
        )

    # Connect to the HTTP server started by progress_server.py
    client = Client("http://127.0.0.1:8000/mcp", progress_handler=progress_handler)

    async with client:
        items = [f"{msg}-{i+1}" for i in range(count)]

        # Call the tool; progress is streamed to progress_handler above
        ret = await client.call_tool("process_items", {"items": items})

        # Print final result (also parsed by eventList.py)
        print(f"[Client Result] {ret.data}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python event_client.py <message> <count>")
        sys.exit(1)

    message = sys.argv[1]
    count = int(sys.argv[2])
    asyncio.run(main(message, count))
