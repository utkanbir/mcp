from typing import List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get the weather for a city
    Args:
        city: The city to get the weather for
    Returns:
        The weather for the city
    """     
    return f"The weather in {city} is sunny"

if __name__ == "__main__":
    mcp.run(transport="sse")