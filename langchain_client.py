import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI()

async def main():
    print("Hello from mcp!")
    # MultiServerMCPClient cannot be used as a context manager in version 0.1.0+
    client = MultiServerMCPClient({
        "math": { 
            "command": "python", 
            "args": ["C:/tolga/mcp/mcp/servers/math_server.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        },
    })
    
    # Get tools from the client
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({"messages": [HumanMessage(content="What is (3 + 4) * 10?")]})
    print(result)
    print(result["messages"][-1].content)
    result= await agent.ainvoke({"messages": [HumanMessage(content="What is the weather in Tokyo?")]})
    print(result)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
    