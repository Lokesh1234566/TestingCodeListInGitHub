from fastmcp import FastMCP

mcp = FastMCP(name="InvoiceServer")


@mcp.tool(annotations={"title": "printFromBusServer"})
def printFromBusServer(message: str = "") -> str:
    print("📩 Call From Client with:", message)
    return f"✅ Server received: {message}"


if __name__ == "__main__":
    print("🚀 Starting InvoiceServer on http://127.0.0.1:8000/mcp ...")
    mcp.run(transport="http")
