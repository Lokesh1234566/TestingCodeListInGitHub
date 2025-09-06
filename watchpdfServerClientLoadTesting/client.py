import asyncio
import os
import sys
from fastmcp import Client
import win32com.client
from eventure import Event, EventBus, EventLog, EventQuery


OUTPUT_TXT_DIR = "./txtfiles"
OUTPUT_JSON_DIR = "./jsonfiles"
VALIDATION_DIR = "./validations"

os.makedirs(OUTPUT_TXT_DIR, exist_ok=True)
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
os.makedirs(VALIDATION_DIR, exist_ok=True)


class FastMCPClientTest:
    def __init__(self) -> None:
        """Initialize the adventure game with event system."""
        self.event_log: EventLog = EventLog()
        self.event_bus: EventBus = EventBus(self.event_log)

    async def process_pdf(pdf_path: str):
        client = Client("http://127.0.0.1:8000/mcp")
        async with client:
            await client.ping()

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_path = os.path.join(OUTPUT_TXT_DIR, f"{base_name}.txt")
        json_path = os.path.join(OUTPUT_JSON_DIR, f"{base_name}.json")
        validation_file = os.path.join(VALIDATION_DIR, f"{base_name}.txt")

        print(f"\n📂 Processing: {pdf_path}")
        # self.event_log.save_to_file("E:\HRInterviewProject\examplescodes\Eventure.log")

        # Convert PDF → TXT
        await client.call_tool(
            "convert_pdf_to_txt", {"pdf_path": pdf_path, "txt_path": txt_path}
        )
        # print(f"   ✅ TXT saved: {txt_path}")
        # send_msmq_by_correlation_id(txt_path, "convert_pdf_to_txt")

        # Convert TXT → JSON
        # invoice_json = await client.call_tool(
        #     "convert_txt_to_json", {"txt_path": txt_path, "json_path": json_path}
        # )
        # print(f"   ✅ JSON saved: {json_path}")
        # print(f"   Extracted JSON: {invoice_json}")
        # send_msmq_by_correlation_id(json_path, "convert_txt_to_json")

        # Validate JSON vs TXT
        # await client.call_tool(
        #     "json_txt_validation",
        #     {
        #         "json_path": json_path,
        #         "txt_path": txt_path,
        #         "output_dir": VALIDATION_DIR,
        #     },
        # )
        # print(f"   ✅ Validation saved: {validation_file}")
        # send_msmq_by_correlation_id(json_path, "json_txt_validation")


def printFromBus():
    print("abcdef")


def send_msmq_by_correlation_id(pdf_path: str, actionName: str):
    """Send MSMQ message with a padded correlation ID."""
    try:
        qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
        qinfo.PathName = ".\\private$\\test_in"  # Replace with your queue path
        queue = qinfo.Open(2, 0)  # Open for send (2=MQ_SEND_ACCESS)
        msg = win32com.client.Dispatch("MSMQ.MSMQMessage")
        msg.Body = actionName

        # padded_correlation_id = bytes(pdf_path.ljust(20), "utf-8")
        # msg.CorrelationId = padded_correlation_id
        msg.Label = actionName + " " + pdf_path
        # print("padded_correlation_id", padded_correlation_id)
        msg.Send(queue)
        queue.Close()
    except Exception as e:
        print(f"Error sending MSMQ message: {e}")
        return None
    finally:
        if "queue" in locals() and queue:
            queue.Close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python client.py <pdf_path>")
        sys.exit(1)

        pdf_path = sys.argv[1]
        asyncio.run(process_pdf(pdf_path))
