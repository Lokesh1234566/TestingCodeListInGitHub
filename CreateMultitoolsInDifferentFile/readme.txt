README – MCP CSV & Parquet Summarizer
📌 Overview

This project demonstrates a Micro Control Protocol (MCP) server that can summarize CSV and Parquet files. It uses:

fastmcp → to build the MCP server and expose tools.

pandas → to read and summarize CSV/Parquet files.

utils.file_reader → helper functions to read files from the /data directory.

toolslist → contains the MCP tool definitions.

⚙️ Project Structure
project/
│
├── data/
│   ├── sample.csv
│   └── sample.parquet
│
├── toolslist/
│   ├── csv_tools.py         # Tool to summarize CSV
│   ├── parquet_tools.py     # Tool to summarize Parquet
│
├── utils/
│   └── file_reader.py       # File reading helper functions
│
├── mcp_server.py            # FastMCP server instance
├── server.py                # Entry point to run server
└── README.txt               # Documentation

🚀 Components
1. toolslist/csv_tools.py

Defines the MCP tool summarize_csv_file:

Accepts a filename (e.g., sample.csv).

Calls read_csv_summary from utils/file_reader.py.

Returns number of rows and columns.

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    return read_csv_summary(filename)

2. toolslist/parquet_tools.py

Defines the MCP tool summarize_parquet_file:

Accepts a filename (e.g., sample.parquet).

Calls read_parquet_summary.

Returns number of rows and columns.

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    return read_parquet_summary(filename)

3. utils/file_reader.py

Helper functions using pandas:

read_csv_summary(filename: str)
Reads a CSV file and reports number of rows & columns.

read_parquet_summary(filename: str)
Reads a Parquet file and reports number of rows & columns.

4. mcp_server.py

Creates the shared MCP server instance:

from mcp.server.fastmcp import FastMCP
mcp = FastMCP("mix_server")

# Register tools by importing
import toolslist.csv_tools
import toolslist.parquet_tools

5. server.py

Runs the MCP server:

if __name__ == "__main__":
    mcp.run()

🔄 How It Works

Start the server:

python server.py


Client requests tool (example):

Call summarize_csv_file("sample.csv") → returns CSV summary.

Call summarize_parquet_file("sample.parquet") → returns Parquet summary.

Server responds with number of rows and columns.

✅ Example Output

If sample.csv has 100 rows and 5 columns:

CSV file 'sample.csv' has 100 rows and 5 columns.


If sample.parquet has 200 rows and 8 columns:

Parquet file 'sample.parquet' has 200 rows and 8 columns.

📖 Requirements

Python 3.9+

Install dependencies:

pip install pandas fastmcp