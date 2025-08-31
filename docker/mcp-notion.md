# 출처

<https://github.com/makenotion/notion-mcp-server>

## MCP 서버 Config

```json
"notionApi": {
    "command": "docker",
    "args": [
        "run",
        "--rm",
        "-i",
        "-e", "NOTION_TOKEN",
        "mcp/notion"
    ],
    "env": {
        "NOTION_TOKEN": "ntn_****"
    }
}
```
