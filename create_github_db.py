#!/usr/bin/env python3
"""
Quick script to create GitHub database for testing
"""
import sqlite3
import os

def create_github_database():
    """Create and seed GitHub database for Test Case 1"""
    conn = sqlite3.connect("data/databases/github.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commits (
            id INTEGER PRIMARY KEY,
            repository TEXT NOT NULL,
            author TEXT NOT NULL,
            message TEXT NOT NULL,
            commit_hash TEXT NOT NULL,
            branch TEXT NOT NULL,
            files_changed INTEGER,
            lines_added INTEGER,
            lines_deleted INTEGER,
            commit_date TEXT NOT NULL,
            custom_id TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pull_requests (
            id INTEGER PRIMARY KEY,
            repository TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            status TEXT NOT NULL,
            base_branch TEXT NOT NULL,
            head_branch TEXT NOT NULL,
            created_date TEXT NOT NULL,
            updated_date TEXT,
            merged_date TEXT,
            custom_id TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
            repository TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT,
            labels TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT,
            closed_date TEXT,
            custom_id TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_reviews (
            id INTEGER PRIMARY KEY,
            repository TEXT NOT NULL,
            pull_request_id INTEGER,
            reviewer TEXT NOT NULL,
            comment TEXT NOT NULL,
            file_path TEXT,
            line_number INTEGER,
            created_date TEXT NOT NULL,
            status TEXT NOT NULL,
            custom_id TEXT UNIQUE
        )
    """)
    
    # Important GitHub data (20% of total)
    important_commits = [
        (1, "company/api", "john@company.com", "Fix production API authentication bug", "abc123", "main", 3, 15, 8, "2024-01-02 10:30:00", "commit_001"),
        (2, "company/frontend", "alice@company.com", "Update Q1 planning dashboard components", "def456", "feature/q1-planning", 5, 25, 12, "2024-01-03 14:15:00", "commit_002"),
    ]
    
    noise_commits = [
        (3, "company/docs", "bob@company.com", "Update README with new installation steps", "ghi789", "main", 1, 5, 2, "2024-01-01 16:20:00", "commit_003"),
        (4, "company/tests", "charlie@company.com", "Add unit tests for user service", "jkl012", "feature/tests", 2, 30, 0, "2024-01-02 11:45:00", "commit_004"),
        (5, "company/infrastructure", "diana@company.com", "Update Docker configuration", "mno345", "main", 2, 8, 3, "2024-01-02 13:30:00", "commit_005"),
        (6, "company/backend", "eve@company.com", "Refactor database connection pool", "pqr678", "feature/refactor", 4, 20, 15, "2024-01-03 09:15:00", "commit_006"),
        (7, "company/mobile", "frank@company.com", "Fix iOS build configuration", "stu901", "main", 1, 3, 1, "2024-01-03 10:00:00", "commit_007"),
        (8, "company/analytics", "grace@company.com", "Add logging for user events", "vwx234", "feature/analytics", 3, 12, 4, "2024-01-03 15:30:00", "commit_008"),
    ]
    
    important_prs = [
        (1, "company/api", "Fix production API authentication", "Critical fix for production API authentication bug affecting customers", "john@company.com", "merged", "main", "fix/auth-bug", "2024-01-02 10:00:00", "2024-01-02 12:00:00", "2024-01-02 12:30:00", "pr_001"),
    ]
    
    noise_prs = [
        (2, "company/frontend", "Update button styles", "Minor UI improvements for better user experience", "alice@company.com", "open", "main", "feature/ui-updates", "2024-01-01 14:00:00", "2024-01-01 14:00:00", None, "pr_002"),
        (3, "company/docs", "Add API documentation", "Comprehensive API documentation for new endpoints", "bob@company.com", "closed", "main", "docs/api", "2024-01-02 09:00:00", "2024-01-02 16:00:00", None, "pr_003"),
        (4, "company/tests", "Improve test coverage", "Add more unit tests to increase coverage", "charlie@company.com", "open", "main", "feature/tests", "2024-01-03 11:00:00", "2024-01-03 11:00:00", None, "pr_004"),
    ]
    
    important_issues = [
        (1, "company/api", "Production API authentication failing", "Users cannot authenticate with the production API. This is affecting customer access.", "john@company.com", "closed", "high", "bug,production", "2024-01-02 08:00:00", "2024-01-02 12:30:00", "2024-01-02 12:30:00", "issue_001"),
    ]
    
    noise_issues = [
        (2, "company/frontend", "Button hover effect not working", "The hover effect on the submit button is not displaying correctly", "alice@company.com", "open", "low", "ui,bug", "2024-01-01 15:00:00", "2024-01-01 15:00:00", None, "issue_002"),
        (3, "company/docs", "Update installation guide", "The installation guide needs to be updated with new dependencies", "bob@company.com", "open", "medium", "documentation", "2024-01-03 10:00:00", "2024-01-03 10:00:00", None, "issue_003"),
    ]
    
    important_reviews = [
        (1, "company/api", 1, "alice@company.com", "This fix looks good. The authentication logic is now properly handling edge cases.", "src/auth.py", 45, "2024-01-02 11:30:00", "approved", "review_001"),
    ]
    
    noise_reviews = [
        (2, "company/frontend", 2, "bob@company.com", "Consider using CSS variables for better maintainability.", "styles/buttons.css", 12, "2024-01-01 16:00:00", "pending", "review_002"),
    ]
    
    # Insert data
    cursor.executemany("INSERT INTO commits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_commits + noise_commits)
    cursor.executemany("INSERT INTO pull_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_prs + noise_prs)
    cursor.executemany("INSERT INTO issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_issues + noise_issues)
    cursor.executemany("INSERT INTO code_reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_reviews + noise_reviews)
    
    conn.commit()
    conn.close()
    print("✅ GitHub database created and seeded successfully!")

if __name__ == "__main__":
    print("🚀 Starting GitHub database creation...")
    os.makedirs("data/databases", exist_ok=True)
    create_github_database()
    print("✅ GitHub database creation completed!")
