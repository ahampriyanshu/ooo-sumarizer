"""
Test Case 1: OOO for 3 days from January 1-3, 2024
This script creates mock data for a 3-day OOO period with realistic scenarios.
"""

import sqlite3
import os
from datetime import datetime, timedelta

def create_email_database():
    """Create and populate email database for test case 1"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    # Drop and recreate emails table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS emails")
    cursor.execute("""
        CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            received_date TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            thread_id TEXT,
            meeting_date TEXT,
            meeting_duration INTEGER,
            attendees TEXT
        )
    """)
    
    # Test Case 1: 3-day OOO period (Jan 1-3, 2024) - 20% important, 80% noise
    emails = [
        # IMPORTANT EMAILS (20% - 2 out of 10)
        {
            "id": "email_001",
            "sender": "client@external.com",
            "subject": "URGENT: Production Issue - API Down",
            "body": "Our production API is down and customers are affected. Need immediate attention.",
            "received_date": "2024-01-02 09:00:00",
            "is_read": 0,
            "thread_id": "urgent_001"
        },
        {
            "id": "email_002",
            "sender": "manager@company.com",
            "subject": "Q1 Planning Meeting - Reschedule Request",
            "body": "We need to reschedule the Q1 planning meeting. Please confirm your availability for next week.",
            "received_date": "2024-01-03 14:30:00",
            "is_read": 0,
            "thread_id": "planning_001"
        },
        
        # NOISE EMAILS (80% - 8 out of 10)
        # New Year greetings
        {
            "id": "email_003",
            "sender": "hr@company.com",
            "subject": "Happy New Year 2024!",
            "body": "Wishing everyone a prosperous and successful new year!",
            "received_date": "2024-01-01 00:01:00",
            "is_read": 1,
            "thread_id": "greetings_001"
        },
        {
            "id": "email_004",
            "sender": "ceo@company.com",
            "subject": "New Year Message from Leadership",
            "body": "Thank you for your hard work in 2023. Looking forward to an amazing 2024!",
            "received_date": "2024-01-01 08:00:00",
            "is_read": 1,
            "thread_id": "ceo_message_001"
        },
        
        # Meeting reminders
        {
            "id": "email_005",
            "sender": "calendar@company.com",
            "subject": "Reminder: Team Standup Tomorrow",
            "body": "Don't forget about tomorrow's team standup at 9 AM.",
            "received_date": "2024-01-02 17:00:00",
            "is_read": 0,
            "thread_id": "reminder_001"
        },
        {
            "id": "email_006",
            "sender": "calendar@company.com",
            "subject": "Reminder: All Hands Meeting",
            "body": "Monthly all hands meeting scheduled for next Friday.",
            "received_date": "2024-01-03 10:00:00",
            "is_read": 0,
            "thread_id": "reminder_002"
        },
        
        # Product promotions
        {
            "id": "email_007",
            "sender": "marketing@company.com",
            "subject": "New Year Special: 50% Off Premium Features",
            "body": "Start 2024 with our premium features at half price!",
            "received_date": "2024-01-01 12:00:00",
            "is_read": 0,
            "thread_id": "promo_001"
        },
        {
            "id": "email_008",
            "sender": "sales@company.com",
            "subject": "Q1 Sales Targets and Incentives",
            "body": "New Q1 sales targets and incentive structure announced.",
            "received_date": "2024-01-02 11:00:00",
            "is_read": 0,
            "thread_id": "sales_001"
        },
        
        # IT notifications
        {
            "id": "email_009",
            "sender": "it@company.com",
            "subject": "System Maintenance Completed",
            "body": "Scheduled system maintenance has been completed successfully.",
            "received_date": "2024-01-03 06:00:00",
            "is_read": 1,
            "thread_id": "maintenance_001"
        },
        {
            "id": "email_010",
            "sender": "security@company.com",
            "subject": "Security Awareness Training - January",
            "body": "Monthly security awareness training materials are now available.",
            "received_date": "2024-01-03 15:00:00",
            "is_read": 0,
            "thread_id": "security_001"
        }
    ]
    
    for email in emails:
        cursor.execute("""
            INSERT INTO emails (custom_id, sender, subject, body, received_date, is_read, thread_id, meeting_date, meeting_duration, attendees)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email["id"], email["sender"], email["subject"], email["body"], email["received_date"],
            email["is_read"], email["thread_id"], 
            email.get("meeting_date"), email.get("meeting_duration"), 
            email.get("attendees")
        ))
    
    conn.commit()
    conn.close()
    print("✅ Email database created and seeded for Test Case 1")

def create_calendar_database():
    """Create and populate calendar database for test case 1"""
    conn = sqlite3.connect("data/databases/calendar.db")
    cursor = conn.cursor()
    
    # Drop and recreate events table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS events")
    cursor.execute("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            location TEXT,
            attendees TEXT,
            event_type TEXT DEFAULT 'meeting',
            is_all_day BOOLEAN DEFAULT 0,
            reminder_set BOOLEAN DEFAULT 1,
            project_name TEXT
        )
    """)
    
    # Test Case 1: 3-day OOO period (Jan 1-3, 2024) - 20% important, 80% noise
    events = [
        # IMPORTANT EVENTS (20% - 2 out of 10)
        {
            "id": "event_001",
            "title": "Production Issue Resolution",
            "description": "Critical production issue needs immediate attention",
            "start_time": "2024-01-02 10:00:00",
            "end_time": "2024-01-02 12:00:00",
            "location": "War Room",
            "attendees": "dev-team@company.com,manager@company.com",
            "event_type": "meeting"
        },
        {
            "id": "event_002",
            "title": "Q1 Planning Deadline",
            "description": "Final deadline for Q1 planning documents",
            "start_time": "2024-01-03 17:00:00",
            "end_time": "2024-01-03 17:00:00",
            "event_type": "deadline",
            "project_name": "Q1 Planning"
        },
        
        # NOISE EVENTS (80% - 8 out of 10)
        # New Year events
        {
            "id": "event_003",
            "title": "New Year Holiday",
            "description": "Company holiday for New Year",
            "start_time": "2024-01-01 00:00:00",
            "end_time": "2024-01-01 23:59:59",
            "event_type": "holiday",
            "is_all_day": 1
        },
        {
            "id": "event_004",
            "title": "New Year Team Lunch",
            "description": "Team lunch to celebrate the new year",
            "start_time": "2024-01-02 12:00:00",
            "end_time": "2024-01-02 13:30:00",
            "location": "Company Cafeteria",
            "attendees": "team@company.com",
            "event_type": "social"
        },
        
        # Regular meetings
        {
            "id": "event_005",
            "title": "Weekly Team Standup",
            "description": "Daily standup meeting for the development team",
            "start_time": "2024-01-02 09:00:00",
            "end_time": "2024-01-02 09:30:00",
            "location": "Conference Room A",
            "attendees": "dev-team@company.com",
            "event_type": "meeting"
        },
        {
            "id": "event_006",
            "title": "Weekly Team Standup",
            "description": "Daily standup meeting for the development team",
            "start_time": "2024-01-03 09:00:00",
            "end_time": "2024-01-03 09:30:00",
            "location": "Conference Room A",
            "attendees": "dev-team@company.com",
            "event_type": "meeting"
        },
        
        # Training sessions
        {
            "id": "event_007",
            "title": "New Year Security Training",
            "description": "Annual security awareness training session",
            "start_time": "2024-01-02 14:00:00",
            "end_time": "2024-01-02 15:00:00",
            "location": "Training Room",
            "attendees": "all@company.com",
            "event_type": "training"
        },
        {
            "id": "event_008",
            "title": "Q1 Goals Setting Workshop",
            "description": "Workshop to set Q1 individual and team goals",
            "start_time": "2024-01-03 10:00:00",
            "end_time": "2024-01-03 11:30:00",
            "location": "Conference Room B",
            "attendees": "team@company.com",
            "event_type": "workshop"
        },
        
        # Company events
        {
            "id": "event_009",
            "title": "New Year All Hands",
            "description": "Company-wide all hands meeting to kick off 2024",
            "start_time": "2024-01-03 15:00:00",
            "end_time": "2024-01-03 16:00:00",
            "location": "Main Auditorium",
            "attendees": "all@company.com",
            "event_type": "meeting"
        },
        {
            "id": "event_010",
            "title": "IT Infrastructure Review",
            "description": "Monthly IT infrastructure review meeting",
            "start_time": "2024-01-03 11:00:00",
            "end_time": "2024-01-03 12:00:00",
            "location": "IT Conference Room",
            "attendees": "it-team@company.com",
            "event_type": "meeting"
        }
    ]
    
    for event in events:
        cursor.execute("""
            INSERT INTO events (custom_id, title, description, start_time, end_time, location, attendees, event_type, project_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["id"], event["title"], event["description"], event["start_time"], event["end_time"],
            event.get("location"), event.get("attendees"), event["event_type"],
            event.get("project_name")
        ))
    
    conn.commit()
    conn.close()
    print("✅ Calendar database created and seeded for Test Case 1")

def create_slack_database():
    """Create and populate Slack database for test case 1"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    # Drop and recreate messages table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS messages")
    cursor.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            channel TEXT NOT NULL,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            is_mention BOOLEAN DEFAULT 0,
            thread_id TEXT
        )
    """)
    
    # Test Case 1: 3-day OOO period (Jan 1-3, 2024) - 20% important, 80% noise
    messages = [
        # IMPORTANT MESSAGES (20% - 2 out of 10)
        {
            "id": "slack_001",
            "channel": "#dev-team",
            "user": "manager@company.com",
            "message": "@john.doe URGENT: Production API is down. Need you to investigate immediately when you're back.",
            "timestamp": "2024-01-02 09:15:00",
            "is_mention": 1,
            "thread_id": "urgent_001"
        },
        {
            "id": "slack_002",
            "channel": "#general",
            "user": "cto@company.com",
            "message": "@john.doe We need to discuss the Q1 technical roadmap. Please schedule a meeting when you return.",
            "timestamp": "2024-01-03 16:00:00",
            "is_mention": 1,
            "thread_id": "roadmap_001"
        },
        
        # NOISE MESSAGES (80% - 8 out of 10)
        # New Year messages
        {
            "id": "slack_003",
            "channel": "#general",
            "user": "ceo@company.com",
            "message": "Happy New Year everyone! 🎉 Looking forward to an amazing 2024!",
            "timestamp": "2024-01-01 00:05:00",
            "is_mention": 0,
            "thread_id": "newyear_001"
        },
        {
            "id": "slack_004",
            "channel": "#random",
            "user": "alice@company.com",
            "message": "Anyone else excited about 2024? I have so many goals! 💪",
            "timestamp": "2024-01-01 10:30:00",
            "is_mention": 0,
            "thread_id": "goals_001"
        },
        
        # General chatter
        {
            "id": "slack_005",
            "channel": "#dev-team",
            "user": "bob@company.com",
            "message": "Good morning team! Hope everyone had a great New Year break.",
            "timestamp": "2024-01-02 08:30:00",
            "is_mention": 0,
            "thread_id": "morning_001"
        },
        {
            "id": "slack_006",
            "channel": "#general",
            "user": "sarah@company.com",
            "message": "The office coffee machine is working great today! ☕",
            "timestamp": "2024-01-02 09:45:00",
            "is_mention": 0,
            "thread_id": "coffee_001"
        },
        
        # Meeting discussions
        {
            "id": "slack_007",
            "channel": "#meetings",
            "user": "hr@company.com",
            "message": "Reminder: Q1 Goals Setting Workshop tomorrow at 10 AM",
            "timestamp": "2024-01-02 17:00:00",
            "is_mention": 0,
            "thread_id": "workshop_001"
        },
        {
            "id": "slack_008",
            "channel": "#announcements",
            "user": "it@company.com",
            "message": "System maintenance completed successfully. All services are back online.",
            "timestamp": "2024-01-03 06:30:00",
            "is_mention": 0,
            "thread_id": "maintenance_001"
        },
        
        # Team updates
        {
            "id": "slack_009",
            "channel": "#dev-team",
            "user": "alice@company.com",
            "message": "Just finished reviewing the new API documentation. Looks good!",
            "timestamp": "2024-01-03 11:00:00",
            "is_mention": 0,
            "thread_id": "docs_001"
        },
        {
            "id": "slack_010",
            "channel": "#general",
            "user": "marketing@company.com",
            "message": "New Year promotion is live! Check out our latest features 🚀",
            "timestamp": "2024-01-03 14:00:00",
            "is_mention": 0,
            "thread_id": "promo_001"
        }
    ]
    
    for message in messages:
        cursor.execute("""
            INSERT INTO messages (custom_id, channel, user, message, timestamp, is_mention, thread_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            message["id"], message["channel"], message["user"], message["message"], message["timestamp"],
            message["is_mention"], message["thread_id"]
        ))
    
    conn.commit()
    conn.close()
    print("✅ Slack database created and seeded for Test Case 1")

def create_kanban_database():
    """Create and populate Kanban database for test case 1"""
    conn = sqlite3.connect("data/databases/kanban.db")
    cursor = conn.cursor()
    
    # Drop and recreate tasks table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'medium',
            assignee TEXT,
            due_date TEXT,
            project_name TEXT,
            story_points INTEGER,
            created_date TEXT,
            updated_date TEXT,
            blocker_reason TEXT,
            blocked_by TEXT
        )
    """)
    
    # Drop and recreate task_updates table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS task_updates")
    cursor.execute("""
        CREATE TABLE task_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            task_id INTEGER,
            update_type TEXT,
            description TEXT,
            updated_by TEXT,
            updated_date TEXT,
            new_status TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    """)
    
    # Drop and recreate project_progress table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS project_progress")
    cursor.execute("""
        CREATE TABLE project_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_id TEXT UNIQUE,
            project_name TEXT NOT NULL,
            milestone TEXT,
            progress_percentage INTEGER,
            status TEXT,
            due_date TEXT,
            updated_date TEXT
        )
    """)
    
    # Test Case 1: 3-day OOO period (Jan 1-3, 2024) - 20% important, 80% noise
    tasks = [
        # IMPORTANT TASKS (20% - 2 out of 10)
        {
            "id": "task_001",
            "title": "Fix Production API Issue",
            "description": "Critical production API is down, affecting customers",
            "status": "in_progress",
            "priority": "high",
            "assignee": "john.doe@company.com",
            "due_date": "2024-01-02",
            "project_name": "Production Support",
            "story_points": 8,
            "created_date": "2024-01-02 09:00:00",
            "updated_date": "2024-01-02 09:00:00",
            "blocker_reason": "Waiting for database access",
            "blocked_by": "dba@company.com"
        },
        {
            "id": "task_002",
            "title": "Complete Q1 Planning Document",
            "description": "Finalize Q1 technical roadmap and planning document",
            "status": "todo",
            "priority": "high",
            "assignee": "john.doe@company.com",
            "due_date": "2024-01-03",
            "project_name": "Q1 Planning",
            "story_points": 5,
            "created_date": "2024-01-01 10:00:00",
            "updated_date": "2024-01-01 10:00:00"
        },
        
        # NOISE TASKS (80% - 8 out of 10)
        # Regular development tasks
        {
            "id": "task_003",
            "title": "Update API Documentation",
            "description": "Update API documentation with latest changes",
            "status": "done",
            "priority": "medium",
            "assignee": "alice@company.com",
            "due_date": "2024-01-02",
            "project_name": "Documentation",
            "story_points": 3,
            "created_date": "2023-12-30 14:00:00",
            "updated_date": "2024-01-02 11:00:00"
        },
        {
            "id": "task_004",
            "title": "Code Review: User Authentication",
            "description": "Review the new user authentication implementation",
            "status": "in_progress",
            "priority": "medium",
            "assignee": "bob@company.com",
            "due_date": "2024-01-03",
            "project_name": "Authentication",
            "story_points": 2,
            "created_date": "2024-01-02 10:00:00",
            "updated_date": "2024-01-02 10:00:00"
        },
        {
            "id": "task_005",
            "title": "Setup New Development Environment",
            "description": "Configure new development environment for the team",
            "status": "todo",
            "priority": "low",
            "assignee": "sarah@company.com",
            "due_date": "2024-01-05",
            "project_name": "Infrastructure",
            "story_points": 5,
            "created_date": "2024-01-01 15:00:00",
            "updated_date": "2024-01-01 15:00:00"
        },
        {
            "id": "task_006",
            "title": "Write Unit Tests for Payment Module",
            "description": "Add comprehensive unit tests for the payment processing module",
            "status": "todo",
            "priority": "medium",
            "assignee": "alice@company.com",
            "due_date": "2024-01-04",
            "project_name": "Testing",
            "story_points": 8,
            "created_date": "2024-01-02 13:00:00",
            "updated_date": "2024-01-02 13:00:00"
        },
        {
            "id": "task_007",
            "title": "Update Dependencies",
            "description": "Update project dependencies to latest versions",
            "status": "in_progress",
            "priority": "low",
            "assignee": "bob@company.com",
            "due_date": "2024-01-06",
            "project_name": "Maintenance",
            "story_points": 3,
            "created_date": "2024-01-03 09:00:00",
            "updated_date": "2024-01-03 09:00:00"
        },
        {
            "id": "task_008",
            "title": "Design New Dashboard UI",
            "description": "Create mockups for the new admin dashboard",
            "status": "todo",
            "priority": "medium",
            "assignee": "sarah@company.com",
            "due_date": "2024-01-08",
            "project_name": "UI/UX",
            "story_points": 5,
            "created_date": "2024-01-03 11:00:00",
            "updated_date": "2024-01-03 11:00:00"
        },
        {
            "id": "task_009",
            "title": "Performance Optimization",
            "description": "Optimize database queries for better performance",
            "status": "todo",
            "priority": "medium",
            "assignee": "alice@company.com",
            "due_date": "2024-01-10",
            "project_name": "Performance",
            "story_points": 8,
            "created_date": "2024-01-03 14:00:00",
            "updated_date": "2024-01-03 14:00:00"
        },
        {
            "id": "task_010",
            "title": "Security Audit Preparation",
            "description": "Prepare documentation for upcoming security audit",
            "status": "todo",
            "priority": "low",
            "assignee": "bob@company.com",
            "due_date": "2024-01-12",
            "project_name": "Security",
            "story_points": 3,
            "created_date": "2024-01-03 16:00:00",
            "updated_date": "2024-01-03 16:00:00"
        }
    ]
    
    for task in tasks:
        cursor.execute("""
            INSERT INTO tasks (custom_id, title, description, status, priority, assignee, due_date, project_name, story_points, created_date, updated_date, blocker_reason, blocked_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["id"], task["title"], task["description"], task["status"], task["priority"],
            task["assignee"], task["due_date"], task["project_name"], task["story_points"],
            task["created_date"], task["updated_date"], task.get("blocker_reason"), task.get("blocked_by")
        ))
    
    # Add some task updates
    task_updates = [
        {
            "id": "update_001",
            "task_id": 1,
            "update_type": "status_change",
            "description": "Task moved to in_progress due to production issue",
            "updated_by": "manager@company.com",
            "updated_date": "2024-01-02 09:00:00",
            "new_status": "in_progress"
        },
        {
            "id": "update_002",
            "task_id": 1,
            "update_type": "comment",
            "description": "Waiting for database access to proceed",
            "updated_by": "john.doe@company.com",
            "updated_date": "2024-01-02 09:30:00",
            "new_status": "in_progress"
        },
        {
            "id": "update_003",
            "task_id": 3,
            "update_type": "status_change",
            "description": "Documentation update completed",
            "updated_by": "alice@company.com",
            "updated_date": "2024-01-02 11:00:00",
            "new_status": "done"
        }
    ]
    
    for update in task_updates:
        cursor.execute("""
            INSERT INTO task_updates (custom_id, task_id, update_type, description, updated_by, updated_date, new_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            update["id"], update["task_id"], update["update_type"], update["description"],
            update["updated_by"], update["updated_date"], update["new_status"]
        ))
    
    # Add project progress
    project_progress = [
        {
            "id": "progress_001",
            "project_name": "Production Support",
            "milestone": "API Issue Resolution",
            "progress_percentage": 30,
            "status": "in_progress",
            "due_date": "2024-01-02",
            "updated_date": "2024-01-02 09:00:00"
        },
        {
            "id": "progress_002",
            "project_name": "Q1 Planning",
            "milestone": "Technical Roadmap",
            "progress_percentage": 75,
            "status": "in_progress",
            "due_date": "2024-01-03",
            "updated_date": "2024-01-03 10:00:00"
        },
        {
            "id": "progress_003",
            "project_name": "Documentation",
            "milestone": "API Documentation Update",
            "progress_percentage": 100,
            "status": "completed",
            "due_date": "2024-01-02",
            "updated_date": "2024-01-02 11:00:00"
        }
    ]
    
    for progress in project_progress:
        cursor.execute("""
            INSERT INTO project_progress (custom_id, project_name, milestone, progress_percentage, status, due_date, updated_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            progress["id"], progress["project_name"], progress["milestone"], progress["progress_percentage"],
            progress["status"], progress["due_date"], progress["updated_date"]
        ))
    
    conn.commit()
    conn.close()
    print("✅ Kanban database created and seeded for Test Case 1")

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
    cursor.executemany("INSERT INTO code_reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_reviews + noise_reviews)
    
    conn.commit()
    conn.close()
    print("✅ GitHub database created and seeded for Test Case 1")

def main():
    """Main function to create all databases for Test Case 1"""
    print("🚀 Starting Test Case 1 database creation and seeding...")
    print("📅 OOO Period: 2024-01-01 to 2024-01-03 (3 days)")
    print()
    
    # Create databases directory if it doesn't exist
    os.makedirs("data/databases", exist_ok=True)
    
    create_email_database()
    create_calendar_database()
    create_slack_database()
    create_kanban_database()
    print("🔧 Creating GitHub database...")
    create_github_database()
    
    print()
    print("✅ Test Case 1 databases created and seeded successfully!")
    print("📊 Summary:")
    print("   - Email database: 10 emails (2 important, 8 noise) - 80% noise ratio")
    print("   - Calendar database: 10 events (2 important, 8 noise) - 80% noise ratio")
    print("   - Slack database: 10 messages (2 important, 8 noise) - 80% noise ratio")
    print("   - Kanban database: 10 tasks (2 important, 8 noise) - 80% noise ratio")
    print("   - GitHub database: 8 commits, 4 PRs, 3 issues, 2 code reviews (2 important, 6 noise) - 75% noise ratio")
    print()
    print("🎯 Test Case 1: 3-day OOO period with New Year context and production issues")

if __name__ == "__main__":
    main()
