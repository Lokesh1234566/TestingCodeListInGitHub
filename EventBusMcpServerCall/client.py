import asyncio

from fastmcp import Client


class FastMCPClientTest:

    async def main():
        client = Client("http://127.0.0.1:8000/mcp")
        async with client:
            ret1 = await client.call_tool("printFromBusServer", "")
            print("ret1", ret1)

        print("Call From EventBus")

    asyncio.run(main())
