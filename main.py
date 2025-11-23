import asyncio
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerTransport
from mcp.client.stdio import stdio_client   
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

llm = ChatOpenAI()
stdio_server_params = StdioServerParameter(command="python",args=["C/tolga/mcp/mcpservers/math_server.py"])
async def main():
    print("Hello from mcp!")

if __name__ == "__main__":
    asyncio.run(main())
