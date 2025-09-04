import sys
import asyncio
import io
from fastmcp import Client

# Force UTF-8 output (Windows fix for emoji/unicode)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


async def main(msg: str):
    client = Client("http://127.0.0.1:8000/mcp")
    async with client:
        response = await client.call_tool("printFromBusServer", {"message": msg})
        print("Server Response:", response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ./client.py <message>")
        sys.exit(1)

    message = sys.argv[1]
    asyncio.run(main(message))
