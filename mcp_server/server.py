"""
Standalone PaperTrail MCP Server Entry Point.
Run directly using: python mcp_server/server.py
"""
import sys
import os

# Ensure backend directory is in sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.mcp.server import mcp_server

if __name__ == "__main__":
    mcp_server.run()
