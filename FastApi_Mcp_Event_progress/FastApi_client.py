import sys
import asyncio
import httpx
import json


async def main(msg: str):
    items = [f"{msg}-step{i}" for i in range(1, 6)]
    print(f"[Client] Sending items to FastAPI stream: {items}", flush=True)

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            "http://127.0.0.1:5001/process/stream",
            json={"items": items},
        ) as response:
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data = json.loads(line[len("data: ") :])

                if "progress" in data:
                    pct = (data["progress"] / data["total"]) * 100
                    print(
                        f"[Client Progress] {pct:.0f}% - step {data['progress']}/{data['total']} - {data['message']}",
                        flush=True,
                    )
                elif data.get("done"):
                    print(f"[Client Result] {data['results']}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ./FastApi_client.py <filename>")
        sys.exit(1)

    message = sys.argv[1]
    asyncio.run(main(message))
