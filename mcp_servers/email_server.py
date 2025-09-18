"""
Email MCP Server using FastMCP

Simulates Gmail/Outlook email data for the OOO summarizer.
Provides access to emails, meeting requests, and important communications.
"""

import sqlite3
import json
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("email-server")

@mcp.tool()
def get_emails(start_date: str, end_date: str, limit: int = 50) -> str:
    """Get emails for a specific date range"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, sender, subject, body, received_date, is_read, thread_id
    FROM emails 
    WHERE received_date BETWEEN ? AND ?
    ORDER BY received_date DESC LIMIT ?
    """
    params = [start_date, end_date, limit]
    
    cursor.execute(query, params)
    emails = cursor.fetchall()
    conn.close()
    
    result = []
    for email in emails:
        email_data = {
            "id": email[0],
            "sender": email[1],
            "subject": email[2],
            "body": email[3],
            "received_date": email[4],
            "is_read": bool(email[5]),
            "thread_id": email[6]
        }
        result.append(email_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_meeting_requests(start_date: str, end_date: str) -> str:
    """Get meeting requests and calendar invites"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, sender, subject, body, received_date, meeting_date, meeting_duration, attendees
    FROM emails 
    WHERE received_date BETWEEN ? AND ? 
    AND (subject LIKE '%meeting%' OR subject LIKE '%invite%' OR body LIKE '%calendar%')
    ORDER BY received_date DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    meetings = cursor.fetchall()
    conn.close()
    
    result = []
    for meeting in meetings:
        meeting_data = {
            "id": meeting[0],
            "sender": meeting[1],
            "subject": meeting[2],
            "body": meeting[3],
            "received_date": meeting[4],
            "meeting_date": meeting[5],
            "meeting_duration": meeting[6],
            "attendees": meeting[7]
        }
        result.append(meeting_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_important_emails(start_date: str, end_date: str) -> str:
    """Get emails marked as important or from key contacts"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, sender, subject, body, received_date, is_read, thread_id
    FROM emails 
    WHERE received_date BETWEEN ? AND ? 
    AND sender IN (
        'ceo@company.com', 'cto@company.com', 'manager@company.com'
    )
    ORDER BY received_date DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    important_emails = cursor.fetchall()
    conn.close()
    
    result = []
    for email in important_emails:
        email_data = {
            "id": email[0],
            "sender": email[1],
            "subject": email[2],
            "body": email[3],
            "received_date": email[4],
            "is_read": bool(email[5]),
            "thread_id": email[6]
        }
        result.append(email_data)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
