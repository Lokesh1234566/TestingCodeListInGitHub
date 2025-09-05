import asyncio
from fastmcp import FastMCP, Context

mcp = FastMCP("ProgressDemo")


@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []

    for i, item in enumerate(items, start=1):
        # Report progress with an optional message
        await ctx.report_progress(progress=i, total=total, message=f"processing {item}")
        await asyncio.sleep(0.5)  # simulate work
        results.append(item.upper())

    # Ensure we end at 100%
    await ctx.report_progress(progress=total, total=total, message="done")

    return {"processed": len(results), "results": results}


if __name__ == "__main__":
    print("🚀 Starting ProgressDemo server on http://127.0.0.1:8000/mcp ...")
    # Be explicit about host/port so the client URL matches
    mcp.run(transport="http", host="127.0.0.1", port=8000)
