"""
Slack MCP Server using FastMCP

Simulates Slack workspace data for the OOO summarizer.
Provides access to messages, mentions, channel activity, and direct messages.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("slack-server")

@mcp.tool()
def get_messages(start_date: str, end_date: str, channel: Optional[str] = None) -> str:
    """Get Slack messages for a specific date range"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, channel, user, message, timestamp, thread_id, is_mention
    FROM messages 
    WHERE timestamp BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if channel:
        query += " AND channel = ?"
        params.append(channel)
    
    query += " ORDER BY timestamp DESC"
    
    cursor.execute(query, params)
    messages = cursor.fetchall()
    conn.close()
    
    result = []
    for message in messages:
        message_data = {
            "id": message[0],
            "channel": message[1],
            "user": message[2],
            "message": message[3],
            "timestamp": message[4],
            "thread_id": message[5],
            "is_mention": bool(message[6])
        }
        result.append(message_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_mentions(start_date: str, end_date: str) -> str:
    """Get messages where the user was mentioned"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, channel, user, message, timestamp, thread_id
    FROM messages 
    WHERE timestamp BETWEEN ? AND ?
    AND message LIKE '%@john.doe%'
    ORDER BY timestamp DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    mentions = cursor.fetchall()
    conn.close()
    
    result = []
    for mention in mentions:
        mention_data = {
            "id": mention[0],
            "channel": mention[1],
            "user": mention[2],
            "message": mention[3],
            "timestamp": mention[4],
            "thread_id": mention[5]
        }
        result.append(mention_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_direct_messages(start_date: str, end_date: str) -> str:
    """Get direct messages and private conversations"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, channel, user, message, timestamp, thread_id, is_mention
    FROM messages 
    WHERE timestamp BETWEEN ? AND ?
    AND channel LIKE 'D%'
    ORDER BY timestamp DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    dms = cursor.fetchall()
    conn.close()
    
    result = []
    for dm in dms:
        dm_data = {
            "id": dm[0],
            "channel": dm[1],
            "user": dm[2],
            "message": dm[3],
            "timestamp": dm[4],
            "thread_id": dm[5],
            "is_mention": bool(dm[6])
        }
        result.append(dm_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_channel_activity(start_date: str, end_date: str, channels: Optional[List[str]] = None) -> str:
    """Get activity summary for specific channels"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    if channels:
        placeholders = ",".join(["?" for _ in channels])
        query = f"""
        SELECT channel, COUNT(*) as message_count, 
               COUNT(DISTINCT user) as unique_users,
               MIN(timestamp) as first_message,
               MAX(timestamp) as last_message
        FROM messages 
        WHERE timestamp BETWEEN ? AND ?
        AND channel IN ({placeholders})
        GROUP BY channel
        ORDER BY message_count DESC
        """
        params = [start_date, end_date] + channels
    else:
        query = """
        SELECT channel, COUNT(*) as message_count, 
               COUNT(DISTINCT user) as unique_users,
               MIN(timestamp) as first_message,
               MAX(timestamp) as last_message
        FROM messages 
        WHERE timestamp BETWEEN ? AND ?
        GROUP BY channel
        ORDER BY message_count DESC
        """
        params = [start_date, end_date]
    
    cursor.execute(query, params)
    activity = cursor.fetchall()
    conn.close()
    
    result = []
    for channel_activity in activity:
        activity_data = {
            "channel": channel_activity[0],
            "message_count": channel_activity[1],
            "unique_users": channel_activity[2],
            "first_message": channel_activity[3],
            "last_message": channel_activity[4]
        }
        result.append(activity_data)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
