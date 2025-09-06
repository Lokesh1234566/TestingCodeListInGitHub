import os, json
from fastmcp import FastMCP
from multicolumn import column_boxes
from utils import extract_and_read_pdf_text, validate_json_vs_text, extract

mcp = FastMCP(name="InvoiceServer")


# --- TOOL 1: Convert PDF → TXT ---
@mcp.tool(annotations={"title": "Convert PDF to TXT"})
def convert_pdf_to_txt(pdf_path: str, txt_path: str) -> str:
    return extract_and_read_pdf_text(pdf_path, txt_path, column_boxes)


# --- TOOL 2: Convert TXT → JSON ---
@mcp.tool(annotations={"title": "Convert TXT to JSON"})
def convert_txt_to_json(txt_path: str, json_path: str) -> dict:
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    supplier_details = {
        "name": lines[0].strip() if lines else "",
        "address": ", ".join(lines[1:6]).strip() if len(lines) > 5 else "",
        "gstin_uin": extract(r"GSTIN/UIN:\s*(\S+)", text),
    }

    output_data = {"supplier_details": supplier_details}

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(output_data, jf, indent=4)

    return output_data


# --- TOOL 3: Validate JSON vs TXT ---
@mcp.tool(annotations={"title": "Validate JSON vs TXT"})
def json_txt_validation(json_path: str, txt_path: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    validate_json_vs_text(json_path, txt_path, output_dir)
    return f"Validation saved in {output_dir}"


if __name__ == "__main__":
    print("🚀 Starting InvoiceServer...")
    mcp.run(transport="http")
