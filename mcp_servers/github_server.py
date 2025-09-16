"""
GitHub MCP Server using FastMCP

Simulates GitHub activity data for the OOO summarizer.
Provides access to commits, pull requests, issues, and code reviews.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("github-server")

@mcp.tool()
def get_commits(start_date: str, end_date: str, repository: Optional[str] = None) -> str:
    """Get commits for a specific date range"""
    print(f"🔍 [GITHUB] get_commits called with start_date={start_date}, end_date={end_date}, repository={repository}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/github.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, repository, author, message, commit_hash, branch, files_changed, lines_added, lines_deleted, commit_date
    FROM commits 
    WHERE commit_date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if repository:
        query += " AND repository = ?"
        params.append(repository)
    
    query += " ORDER BY commit_date DESC"
    
    cursor.execute(query, params)
    commits = cursor.fetchall()
    conn.close()
    
    result = []
    for commit in commits:
        commit_data = {
            "id": commit[0],
            "repository": commit[1],
            "author": commit[2],
            "message": commit[3],
            "commit_hash": commit[4],
            "branch": commit[5],
            "files_changed": commit[6],
            "lines_added": commit[7],
            "lines_deleted": commit[8],
            "commit_date": commit[9]
        }
        result.append(commit_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_pull_requests(start_date: str, end_date: str, status: str = "all") -> str:
    """Get pull requests and their status"""
    print(f"🔍 [GITHUB] get_pull_requests called with start_date={start_date}, end_date={end_date}, status={status}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/github.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, repository, title, description, author, status, created_date, updated_date, merged_date
    FROM pull_requests 
    WHERE created_date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if status != "all":
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY created_date DESC"
    
    cursor.execute(query, params)
    prs = cursor.fetchall()
    conn.close()
    
    result = []
    for pr in prs:
        pr_data = {
            "id": pr[0],
            "repository": pr[1],
            "title": pr[2],
            "description": pr[3],
            "author": pr[4],
            "status": pr[5],
            "created_date": pr[6],
            "updated_date": pr[7],
            "merged_date": pr[8]
        }
        result.append(pr_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_issues(start_date: str, end_date: str, labels: Optional[List[str]] = None) -> str:
    """Get issues and bug reports"""
    print(f"🔍 [GITHUB] get_issues called with start_date={start_date}, end_date={end_date}, labels={labels}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/github.db")
    cursor = conn.cursor()
    
    query = """
    SELECT custom_id, repository, title, description, author, status, labels, priority, created_date, closed_date
    FROM issues 
    WHERE created_date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if labels:
        # Simple label filtering - in real implementation, you'd use a proper join
        label_conditions = " OR ".join(["labels LIKE ?" for _ in labels])
        query += f" AND ({label_conditions})"
        params.extend([f"%{label}%" for label in labels])
    
    query += " ORDER BY priority DESC, created_date DESC"
    
    cursor.execute(query, params)
    issues = cursor.fetchall()
    conn.close()
    
    result = []
    for issue in issues:
        issue_data = {
            "id": issue[0],
            "repository": issue[1],
            "title": issue[2],
            "description": issue[3],
            "author": issue[4],
            "status": issue[5],
            "labels": issue[6],
            "priority": issue[7],
            "created_date": issue[8],
            "closed_date": issue[9]
        }
        result.append(issue_data)
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_code_reviews(start_date: str, end_date: str) -> str:
    """Get code review comments and feedback"""
    print(f"🔍 [GITHUB] get_code_reviews called with start_date={start_date}, end_date={end_date}")
    conn = sqlite3.connect("/Users/karan/hr/ai-agents/ooo-summariser/data/databases/github.db")
    cursor = conn.cursor()
    
    query = """
    SELECT id, pr_id, reviewer, comment, review_type, file_path, line_number, created_date, status
    FROM code_reviews 
    WHERE created_date BETWEEN ? AND ?
    ORDER BY created_date DESC
    """
    
    cursor.execute(query, [start_date, end_date])
    reviews = cursor.fetchall()
    conn.close()
    
    result = []
    for review in reviews:
        review_data = {
            "id": review[0],
            "pr_id": review[1],
            "reviewer": review[2],
            "comment": review[3],
            "review_type": review[4],
            "file_path": review[5],
            "line_number": review[6],
            "created_date": review[7],
            "status": review[8]
        }
        result.append(review_data)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
