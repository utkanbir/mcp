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
    
    # Build server configuration
    # Math server path can be set via MATH_SERVER_PATH environment variable
    math_server_path = os.getenv("MATH_SERVER_PATH", "C:/tolga/mcp/mcp/servers/math_server.py")
    
    # Weather server URL can be set via WEATHER_SERVER_URL environment variable
    # Set to empty string or None to disable weather server
    weather_server_url = os.getenv("WEATHER_SERVER_URL", "")
    
    # Playwright MCP server (stdio transport)
    # Will be started as a subprocess automatically
    # Note: For stdio transport, do NOT use --port flag (that's only for HTTP/SSE mode)
    # The command will be: npx @playwright/mcp@latest (no port argument)
    playwright_command = os.getenv("PLAYWRIGHT_MCP_COMMAND", "npx")
    playwright_args_env = os.getenv("PLAYWRIGHT_MCP_ARGS", "@playwright/mcp@latest")
    
    # Ensure args is a list
    if isinstance(playwright_args_env, str):
        playwright_args = playwright_args_env.split()
    else:
        playwright_args = playwright_args_env if isinstance(playwright_args_env, list) else [playwright_args_env]
    
    # Configure all servers
    servers = {
        "math": { 
            "command": "python", 
            "args": [math_server_path],
            "transport": "stdio"
        },
        "playwright": {
            "command": playwright_command,
            "args": playwright_args,
            "transport": "stdio"
        }
    }
    
    # Add weather server only if URL is provided
    if weather_server_url:
        servers["weather"] = {
            "url": weather_server_url,
            "transport": "sse",
        }
    
    print(f"[INFO] Playwright MCP configured for stdio transport")
    print(f"       Command: {playwright_command} {' '.join(servers['playwright']['args'])}")
    print(f"       Will be started automatically as a subprocess")
    
    # Verify npx is available (for better error messages)
    if playwright_command == "npx":
        import shutil
        if not shutil.which("npx"):
            print(f"\n[WARNING] npx not found in PATH! Playwright MCP may fail to start.")
            print(f"          Make sure Node.js and npm are installed and in your PATH.")
    
    # Print server configuration
    server_names = list(servers.keys())
    print(f"\n[INFO] Creating MultiServerMCPClient with {len(servers)} server(s): {', '.join(server_names)}")
    print("\n[INFO] Server configuration:")
    print("  - math: stdio (will auto-start as subprocess)")
    if "weather" in servers:
        print(f"  - weather: sse ({servers['weather']['url']})")
    print(f"  - playwright: stdio (will auto-start as subprocess)")
    
    client = MultiServerMCPClient(servers)
    
    print("\n[INFO] Client created. Now fetching tools...")
    
    try:
        # Get tools from the client with a timeout
        tools = await asyncio.wait_for(client.get_tools(), timeout=60.0)
    except asyncio.TimeoutError:
        print("\n[ERROR] Timeout waiting for tools! One of the MCP servers might be hanging.")
        print("        Check if all servers are running and accessible.")
        return
    except Exception as e:
        print(f"\n[ERROR] Failed to get tools!")
        print(f"        Error type: {type(e).__name__}")
        print(f"        Error message: {str(e)}")
        print(f"\n[TROUBLESHOOTING] If Playwright tools are missing:")
        print(f"        1. Make sure npx is available in your PATH")
        print(f"        2. Verify @playwright/mcp package is accessible: npx @playwright/mcp@latest --help")
        print(f"        3. Check if the command is correct: {playwright_command} {' '.join(servers.get('playwright', {}).get('args', []))}")
        import traceback
        traceback.print_exc()
        return
    
    print(f"\n[OK] Total tools available: {len(tools)}")
    print("\n--- All Available Tools ---")
    
    # Count tools by prefix to see which server they come from
    playwright_tools = []
    math_tools = []
    weather_tools = []
    other_tools = []
    
    for tool in tools:
        tool_name = tool.name.lower()
        if 'browser' in tool_name or 'playwright' in tool_name:
            playwright_tools.append(tool.name)
        elif 'math' in tool_name or 'calculate' in tool_name or 'add' in tool_name:
            math_tools.append(tool.name)
        elif 'weather' in tool_name:
            weather_tools.append(tool.name)
        else:
            other_tools.append(tool.name)
        print(f"  - {tool.name}: {tool.description}")
    
    print("--- End of Tools ---\n")
    print(f"[DEBUG] Tools breakdown:")
    print(f"  - Playwright tools: {len(playwright_tools)} {playwright_tools}")
    print(f"  - Math tools: {len(math_tools)} {math_tools}")
    print(f"  - Weather tools: {len(weather_tools)} {weather_tools}")
    print(f"  - Other tools: {len(other_tools)} {other_tools}")
    
    if len(playwright_tools) == 0:
        print("\n[WARNING] No Playwright tools found! Check if Playwright MCP server started correctly.")
        print(f"          Command: {playwright_command} {' '.join(servers['playwright']['args'])}")
        print("          Check the error messages above for subprocess startup issues.")
        print("          Make sure npx and @playwright/mcp are available.\n")
    
    # Create agent with error handling enabled
    # The agent should be able to recover from tool errors and retry
    agent = create_react_agent(llm, tools)
    
    # Optional: Test with math (commented out to focus on Playwright)
    # result = await agent.ainvoke({"messages": [HumanMessage(content="What is (3 + 4) * 10?")]})
    # print(result)
    # print(result["messages"][-1].content)

    # Test with Playwright - visit oracle.com, grab a sentence, and display it
    print("\n--- Testing Playwright: Visit oracle.com and grab a sentence from the page ---")
    try:
        # Prompt to visit oracle.com, extract a sentence, and display it
        prompt = """Using Playwright MCP tools, visit oracle.com, grab one sentence from the page, and display it.

Steps:
1. Navigate to https://www.oracle.com using browser_navigate
2. Wait for the page to load
3. Use browser_evaluate to extract a sentence from the page. Use this JavaScript code:
   ```javascript
   () => {
     // Get the first visible paragraph or heading text from the main content
     const paragraphs = document.querySelectorAll('main p, main h2');
     for (const el of Array.from(paragraphs)) {
       const text = el.innerText?.trim() || el.textContent?.trim();
       if (text && text.length > 30 && text.length < 200) {
         return text;
       }
     }
     return 'No sentence found';
   }
   ```
4. Display the sentence you extracted
5. Close the page using browser_close"""
        
        result = await agent.ainvoke({
            "messages": [HumanMessage(content=prompt)]
        })
        print("\n--- Result ---")
        print(result["messages"][-1].content)
        
        # Extract and display the sentence if found in the response
        response_text = result["messages"][-1].content
        print("\n--- Extracted Sentence from Oracle.com ---")
        # Try to find a sentence in quotes or after keywords
        if "sentence" in response_text.lower() or "extracted" in response_text.lower():
            # The agent should have included the sentence in its response
            print(response_text)
        else:
            print(response_text)
    except Exception as e:
        error_msg = str(e)
        print(f"\n[ERROR] Failed to visit oracle.com and see page content")
        print(f"        Error: {error_msg}")
        
        if "Ref" in error_msg and "not found" in error_msg:
            print("\n        This error means the agent tried to use a stale page reference.")
            print("        The agent should:")
            print("        1. Navigate to the page")
            print("        2. Capture a FRESH snapshot")
            print("        3. Then extract content from that snapshot")
            print("\n        Try running again - the agent may need multiple attempts to get the workflow right.")
        
        import traceback
        traceback.print_exc()
    



if __name__ == "__main__":
    asyncio.run(main())
