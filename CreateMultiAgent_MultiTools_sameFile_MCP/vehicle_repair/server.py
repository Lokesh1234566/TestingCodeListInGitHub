# from toolslist.service_tools import mcp
# import toolslist.billing_tools  # ensures billing tools are registered

# if __name__ == "__main__":
#     print("🚀 Starting Unified Vehicle Repair + Billing MCP Server with EventBus...")
#     mcp.run(transport="http", host="127.0.0.1", port=8000)


from toolslist.service_tools import mcp
import toolslist.billing_tools

if __name__ == "__main__":
    print("🚀 Starting Unified Vehicle Repair + Billing MCP Server with EventBus...")
    mcp.run(transport="http", host="127.0.0.1", port=8000)
