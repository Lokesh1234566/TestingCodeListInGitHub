from fastapi import FastAPI, UploadFile
from fastmcp import Client
import json
import uvicorn

app = FastAPI()
MCP_URL = "http://127.0.0.1:8000/mcp"


async def send_to_mcp(payload: dict):
    async with Client(MCP_URL) as client:
        result = await client.call_tool("createEmployee", payload)
        return result


@app.post("/upload-json/")
async def upload_json(file: UploadFile):
    content = await file.read()
    data = json.loads(content)
    return await send_to_mcp(data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
