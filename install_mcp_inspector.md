# Installing MCP Inspector on Windows

## Step 1: Install Node.js
1. Download Node.js from https://nodejs.org/ (choose LTS version)
2. Run the installer
3. Restart your terminal/PowerShell

## Step 2: Verify Installation
After restarting, run:
```powershell
node --version
npm --version
```

## Step 3: Install MCP Inspector
```powershell
npm install -g @modelcontextprotocol/inspector
```

## Step 4: Run MCP Inspector
For stdio transport (Claude Desktop):
```powershell
mcp-inspector stdio "C:\tolga\mcp\mcp\.venv\Scripts\python.exe" "C:\tolga\mcp\mcp\servers\math_server.py"
```

For streamable-http transport:
1. Start your server with `transport="streamable-http"` (it will run on port 8000)
2. In another terminal, run:
```powershell
mcp-inspector http http://localhost:8000
```

## Alternative: Use npx (no global install needed)
```powershell
npx @modelcontextprotocol/inspector stdio "C:\tolga\mcp\mcp\.venv\Scripts\python.exe" "C:\tolga\mcp\mcp\servers\math_server.py"
```


