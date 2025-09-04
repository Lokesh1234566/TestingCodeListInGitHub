from fastmcp import FastMCP


mcp = FastMCP(name="InvoiceServer")


# --- TOOL 1:
@mcp.tool(annotations={"title": "printFromBusServer"})
def printFromBusServer() -> str:
    print("call From Client")
    return "From server"


if __name__ == "__main__":
    print("🚀 Starting InvoiceServer...")
    mcp.run(transport="http")
