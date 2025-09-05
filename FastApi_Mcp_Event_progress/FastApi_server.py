import asyncio
from fastmcp import FastMCP, Context
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
import threading
import json

mcp = FastMCP("ProgressDemo")
app = FastAPI()

# Store results so FastAPI can serve them
results_store = {}


# ---------- Core processing generator ----------
async def process_items_generator(items: list[str]):
    """Async generator that yields progress and final result."""
    total = len(items)
    results = []

    for i, item in enumerate(items, start=1):
        await asyncio.sleep(0.5)  # simulate work
        results.append(item.upper())
        yield {"progress": i, "total": total, "message": f"processing {item}"}

    final = {"processed": len(results), "results": results}
    if items:
        key = items[0].split("-")[0]
        results_store[key] = final
    yield {"done": True, **final}


# ---------- MCP tool ----------
@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """MCP tool that reports progress just like FastAPI."""
    async for update in process_items_generator(items):
        if "progress" in update:
            await ctx.report_progress(
                progress=update["progress"],
                total=update["total"],
                message=update["message"],
            )
        elif update.get("done"):
            return update
    return {"done": True, "processed": 0, "results": []}


# ---------- FastAPI endpoints ----------
@app.post("/process")
async def process_via_fastapi(data: dict = Body(...)):
    """Simple run (no progress)."""
    items = data.get("items", [])
    final = None
    async for update in process_items_generator(items):
        if update.get("done"):
            final = update
    return JSONResponse(content=final)


@app.post("/process/stream")
async def process_via_stream(data: dict = Body(...)):
    """Run processing and stream progress via SSE."""
    items = data.get("items", [])

    async def event_generator():
        async for update in process_items_generator(items):
            yield f"data: {json.dumps(update)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/results")
async def get_results():
    return JSONResponse(content=results_store)


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=5001, log_level="info")


if __name__ == "__main__":
    print("🚀 Starting ProgressDemo MCP server on http://127.0.0.1:8000/mcp ...")
    print("🚀 Starting FastAPI on http://127.0.0.1:5001 ...")

    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    mcp.run(transport="http", host="127.0.0.1", port=8000)
