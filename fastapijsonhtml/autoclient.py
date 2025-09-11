import sys
import json
import asyncio
import time
from fastmcp import Client


async def ping_server() -> bool:
    try:
        async with Client("http://127.0.0.1:8000/mcp") as client:
            pong = await client.ping()
            print(f"Ping result: {pong}")
            return True
    except Exception:
        print("Could not connect to MCP server")
        return False


async def send_to_server(data: dict):
    async with Client("http://127.0.0.1:8000/mcp") as client:
        ret = await client.call_tool("createEmployee", data)
        print(f"MCP Server Response: {ret}")


def process_json(json_path: str):
    for _ in range(5):  # retry if file is locked
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            asyncio.run(send_to_server(data))
            return
        except PermissionError:
            time.sleep(0.5)
        except Exception as e:
            print(f"Error handling file {json_path}: {e}")
            return


def main(json_path: str):
    if not asyncio.run(ping_server()):
        sys.exit(1)

    process_json(json_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python autoclient.py <json_file>")
        sys.exit(1)
    else:
        json_path = sys.argv[1]
        if json_path == "test":
            if not asyncio.run(ping_server()):
                sys.exit(1)
            else:
                print("MCP Server Running")
        else:
            json_path = sys.argv[1]
            main(json_path)
