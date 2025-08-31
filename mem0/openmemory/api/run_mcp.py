#!/usr/bin/env python3
"""
Standalone MCP Server for OpenMemory.

This runs FastMCP as a separate HTTP server on port 8031.
"""

import os
import sys
import asyncio

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.mcp_server import mcp

async def main():
    """Run the MCP server."""
    print("Starting MCP server on port 8031...")
    # Run with streamable_http_async method
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())