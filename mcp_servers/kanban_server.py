"""
Kanban MCP Server using FastMCP

Simulates Jira/Trello/Asana kanban board data for the OOO summarizer.
Provides access to task updates, project progress, and workflow changes.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("kanban-server")

@mcp.tool()
def get_tasks(start_date: str, end_date: str, status: str = "all") -> str:
    """Get tasks and tickets for a specific date range"""
    print(f"🔍 [KANBAN] get_tasks called with start_date={start_date}, end_date={end_date}, status={status}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/kanban.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, title, description, status, priority, assignee, created_date, due_date, project_name, story_points
    FROM tasks 
    WHERE created_date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if status != "all":
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY priority DESC, created_date DESC"
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    
    result = []
    for task in tasks:
        task_data = {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3],
            "priority": task[4],
            "assignee": task[5],
            "created_date": task[6],
            "due_date": task[7],
            "project_name": task[8],
            "story_points": task[9]
        }
        result.append(task_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_task_updates(start_date: str, end_date: str) -> str:
    """Get task updates, comments, and status changes"""
    print(f"🔍 [KANBAN] get_task_updates called with start_date={start_date}, end_date={end_date}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/kanban.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, task_id, update_type, description, updated_by, updated_date, old_status, new_status
    FROM task_updates 
    WHERE updated_date BETWEEN ? AND ?
    ORDER BY updated_date DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    updates = cursor.fetchall()
    conn.close()
    
    result = []
    for update in updates:
        update_data = {
            "id": update[0],
            "task_id": update[1],
            "update_type": update[2],
            "description": update[3],
            "updated_by": update[4],
            "updated_date": update[5],
            "old_status": update[6],
            "new_status": update[7]
        }
        result.append(update_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_project_progress(start_date: str, end_date: str) -> str:
    """Get project progress and milestone updates"""
    print(f"🔍 [KANBAN] get_project_progress called with start_date={start_date}, end_date={end_date}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/kanban.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, project_name, milestone, progress_percentage, status, updated_date, description
    FROM project_progress 
    WHERE updated_date BETWEEN ? AND ?
    ORDER BY updated_date DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    progress = cursor.fetchall()
    conn.close()
    
    result = []
    for prog in progress:
        progress_data = {
            "id": prog[0],
            "project_name": prog[1],
            "milestone": prog[2],
            "progress_percentage": prog[3],
            "status": prog[4],
            "updated_date": prog[5],
            "description": prog[6]
        }
        result.append(progress_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_blocked_tasks(start_date: str, end_date: str) -> str:
    """Get blocked tasks and dependencies"""
    print(f"🔍 [KANBAN] get_blocked_tasks called with start_date={start_date}, end_date={end_date}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/kanban.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, title, description, status, blocker_reason, blocked_by, project_name, priority
    FROM tasks 
    WHERE status = 'blocked' 
    AND (created_date BETWEEN ? AND ? OR updated_date BETWEEN ? AND ?)
    ORDER BY priority DESC, created_date DESC
    """
    
    cursor.execute(query, [start_date, end_date, start_date, end_date])
    blocked_tasks = cursor.fetchall()
    conn.close()
    
    result = []
    for task in blocked_tasks:
        task_data = {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3],
            "blocker_reason": task[4],
            "blocked_by": task[5],
            "project_name": task[6],
            "priority": task[7]
        }
        result.append(task_data)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
