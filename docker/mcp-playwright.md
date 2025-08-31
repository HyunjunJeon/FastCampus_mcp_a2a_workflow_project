# 출처

<https://github.com/microsoft/playwright-mcp>

## MCP 서버 Config

```json
{
  "mcpServers": {
    "playwright": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--init", "mcr.microsoft.com/playwright/mcp"]
    }
  }
}
```
