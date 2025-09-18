"""
Calendar MCP Server using FastMCP

Simulates Google Calendar/Outlook calendar data for the OOO summarizer.
Provides access to meetings, appointments, deadlines, and schedule conflicts.
"""

import sqlite3
import json
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("calendar-server")

@mcp.tool()
def get_events(start_date: str, end_date: str, event_type: str = "all") -> str:
    """Get calendar events for a specific date range"""
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/calendar.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, title, description, start_time, end_time, location, attendees, event_type, is_all_day, reminder_set
    FROM events 
    WHERE start_time BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if event_type != "all":
        query += " AND event_type = ?"
        params.append(event_type)
    
    query += " ORDER BY start_time ASC"
    
    cursor.execute(query, params)
    events = cursor.fetchall()
    conn.close()
    
    result = []
    for event in events:
        event_data = {
            "id": event[0],
            "title": event[1],
            "description": event[2],
            "start_time": event[3],
            "end_time": event[4],
            "location": event[5],
            "attendees": event[6],
            "event_type": event[7],
            "is_all_day": bool(event[8]),
            "reminder_set": bool(event[9])
        }
        result.append(event_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_conflicts(start_date: str, end_date: str) -> str:
    """Get scheduling conflicts and overlapping events"""
    conn = sqlite3.connect("data/databases/calendar.db")
    cursor = conn.cursor()
    
    # Find overlapping events
    query = """
    SELECT e1.id, e1.title, e1.start_time, e1.end_time, e2.id, e2.title, e2.start_time, e2.end_time
    FROM events e1
    JOIN events e2 ON e1.id != e2.id
    WHERE e1.start_time BETWEEN ? AND ?
    AND e2.start_time BETWEEN ? AND ?
    AND (
        (e1.start_time < e2.end_time AND e1.end_time > e2.start_time)
    )
    ORDER BY e1.start_time
    """
    
    cursor.execute(query, [start_date, end_date, start_date, end_date])
    conflicts = cursor.fetchall()
    conn.close()
    
    result = []
    for conflict in conflicts:
        conflict_data = {
            "event1": {
                "id": conflict[0],
                "title": conflict[1],
                "start_time": conflict[2],
                "end_time": conflict[3]
            },
            "event2": {
                "id": conflict[4],
                "title": conflict[5],
                "start_time": conflict[6],
                "end_time": conflict[7]
            }
        }
        result.append(conflict_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_deadlines(start_date: str, end_date: str) -> str:
    """Get upcoming deadlines and important dates"""
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/calendar.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, title, description, start_time, end_time, project_name
    FROM events 
    WHERE start_time BETWEEN ? AND ?
    AND (event_type = 'deadline' OR title LIKE '%deadline%' OR title LIKE '%due%')
    ORDER BY start_time ASC
    """
    
    cursor.execute(query, [start_date, end_date])
    deadlines = cursor.fetchall()
    conn.close()
    
    result = []
    for deadline in deadlines:
        deadline_data = {
            "id": deadline[0],
            "title": deadline[1],
            "description": deadline[2],
            "start_time": deadline[3],
            "end_time": deadline[4],
            "project_name": deadline[5]
        }
        result.append(deadline_data)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
