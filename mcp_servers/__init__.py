"""
FastMCP Servers for OOO Summarizer Agent

This package contains multiple FastMCP servers that simulate real-world data sources:
- Email Server: Simulates Gmail/Outlook
- Calendar Server: Simulates Google Calendar/Outlook  
- Slack Server: Simulates Slack workspace
"""

from .email_server import mcp as email_mcp
from .calendar_server import mcp as calendar_mcp
from .slack_server import mcp as slack_mcp

__all__ = [
    "email_mcp",
    "calendar_mcp", 
    "slack_mcp",
]
