import asyncio
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client   
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

llm = ChatOpenAI()
stdio_server_params = StdioServerParameters(command="python", args=["C:/tolga/mcp/mcp/servers/math_server.py"])
async def main():
    print("Hello from mcp!")
    print("Starting MCP server as subprocess...")
    async with stdio_client(stdio_server_params) as (read, write):
        print("✓ Server subprocess started and connected via stdio")
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("✓ Session initialized")
            tools = await session.list_tools()
            print(f"\n✓ Found {len(tools.tools)} tools from the server:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description.strip()}")
            
            # Example: Call a tool to show the server is actually working
            print("\n--- Testing the server by calling 'add' tool ---")
            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            print(f"Result: {result.content}")
            
    print("\n✓ Server subprocess terminated (connection closed)")

if __name__ == "__main__":
    asyncio.run(main())
