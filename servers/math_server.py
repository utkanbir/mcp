from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers
    Args:
        a: The first number
        b: The second number
    Returns:
        The sum of the two numbers
    """
    print(f"Adding {a} and {b}")
    return a + b


@mcp.prompt()
def get_research_prompt(topic: str) -> str:
    """
    Get a research prompt for a topic
    Args:
        topic: The topic to get a research prompt for
    Returns:
        A research prompt for the topic
    """
    return f"Research the topic {topic}"

@mcp.tool()
def get_research_result(prompt: str) -> str:
    """
    Get a research result for a prompt
    Args:
        prompt: The prompt to get a research result for
    Returns:
        A research result for the prompt
    """
    return f"The research result for the prompt {prompt}"
    
    
@mcp.tool() 
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers
    Args:
        a: The first number
        b: The second number
    Returns:
        The product of the two numbers
    """
    print(f"Multiplying {a} and {b}")
    return a * b

if __name__ == "__main__":
    # Transport options:
    # - "stdio" (default) - for Claude Desktop and stdio-based clients
    # - "sse" - Server-Sent Events (for web clients)
    # - "streamable-http" - HTTP transport (for HTTP clients)
    # Note: Claude Desktop ONLY supports "stdio" transport
    #mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")
