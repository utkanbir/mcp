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
    
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers
    Args:
        a: The first number
        b: The second number
    Returns:
        The difference of the two numbers
    """
    print(f"Subtracting {a} and {b}")
    return a - b
    
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
    mcp.run(transport="stdio")

