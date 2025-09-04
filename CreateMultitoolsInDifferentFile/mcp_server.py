from mcp.server.fastmcp import FastMCP

# Create shared MCP server instance
mcp = FastMCP("mix_server")

# Import tools so they register automatically
import toolslist.csv_tools
import toolslist.parquet_tools

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()
