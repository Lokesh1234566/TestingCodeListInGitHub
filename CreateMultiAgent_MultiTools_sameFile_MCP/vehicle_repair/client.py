# import asyncio
# from fastmcp import Client


# async def process_tool():
#     client = Client("http://127.0.0.1:8000/mcp")
#     async with client:
#         await client.ping()

#         # Agent 1 → Service Inserted
#         inserted = await client.call_tool(
#             "service_inserted",
#             {
#                 "service_id": "S001",
#                 "vehicle_no": "KA01AB1234",
#                 "description": "Oil change",
#             },
#         )
#         print(inserted)

#         # Agent 1 → Service Updated
#         updated = await client.call_tool(
#             "service_updated", {"service_id": "S001", "status": "In Progress"}
#         )
#         print(updated)

#         # Agent 1 → Service Paid
#         paid = await client.call_tool(
#             "service_paid",
#             {"service_id": "S001", "amount": 2500.00, "payment_mode": "UPI"},
#         )
#         print(paid)

#         # Agent 2 → Invoice Generated
#         invoice = await client.call_tool(
#             "invoice_generated",
#             {"invoice_id": "INV1001", "customer": "John Doe", "amount": 4500.00},
#         )
#         print(invoice)

#         # Agent 2 → Invoice Paid
#         invoice_paid = await client.call_tool(
#             "invoice_paid",
#             {"invoice_id": "INV1001", "payment_mode": "Card"},
#         )
#         print(invoice_paid)


# if __name__ == "__main__":
#     asyncio.run(process_tool())


import asyncio
from fastmcp import Client


async def process_tool():
    client = Client("http://127.0.0.1:8000/mcp")
    async with client:
        await client.ping()
        print("✅ MCP Server reachable")

        # Service Inserted
        inserted = await client.call_tool(
            "service_inserted",
            {
                "service_id": "S001",
                "vehicle_no": "KA01AB1234",
                "description": "Oil change",
            },
        )
        print(inserted)

        # Service Updated
        updated = await client.call_tool(
            "service_updated", {"service_id": "S001", "status": "In Progress"}
        )
        print(updated)

        # Service Paid → triggers invoice generation automatically
        paid = await client.call_tool(
            "service_paid",
            {"service_id": "S001", "amount": 2500.00, "payment_mode": "UPI"},
        )
        print(paid)

        # Pay the invoice
        invoice_paid = await client.call_tool(
            "invoice_paid", {"invoice_id": "INV-S001", "payment_mode": "Card"}
        )
        print(invoice_paid)


if __name__ == "__main__":
    asyncio.run(process_tool())
