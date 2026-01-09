import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    server = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as client:
            # Initialize the session
            await client.initialize()

            # 1. List tools
            tools = await client.list_tools()
            print("TOOLS:", tools)

            # 2. Call create_lead
            result = await client.call_tool(
                name="create_lead",
                arguments={
                    "input": {
                        "provider": "zoho",
                        "payload": {
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "john@example.com",
                            "last_name": "Doe",
                            "company": "Example Inc",
                            "phone": "123-456-7890"
                        }
                    }
                }
            )

            print("RESULT:", result)

if __name__ == "__main__":
    asyncio.run(main())
