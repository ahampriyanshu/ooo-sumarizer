"""
Data Seeding Script for OOO Summarizer

Creates SQLite databases and populates them with realistic mock data
for the OOO period (2024-01-15 to 2024-01-22).
"""

import sqlite3
import os

# Ensure databases directory exists
os.makedirs("data/databases", exist_ok=True)

def create_email_database():
    """Create and populate email database"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    # Drop and recreate emails table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS emails")
    cursor.execute("""
        CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    # Sample email data with 80% noise, 20% important
    emails = [
        # IMPORTANT EMAILS (20% - 4 out of 20)
        {
            "sender": "ceo@company.com",
            "subject": "Q1 Strategy Review Meeting",
            "body": "Hi John, we need to schedule a Q1 strategy review meeting. Please let me know your availability for next week.",
            "received_date": "2024-01-16 09:30:00",
            "is_read": 0,
            "thread_id": "thread_001"
        },
        {
            "sender": "cto@company.com",
            "subject": "Technical Architecture Discussion",
            "body": "John, we need to discuss the new microservices architecture. Can we meet this week?",
            "received_date": "2024-01-17 14:15:00",
            "is_read": 0,
            "thread_id": "thread_002"
        },
        {
            "sender": "client@external.com",
            "subject": "Urgent: API Integration Issue",
            "body": "Hi John, we're experiencing issues with the API integration. Can you please look into this ASAP?",
            "received_date": "2024-01-20 08:45:00",
            "is_read": 0,
            "thread_id": "thread_005"
        },
        {
            "sender": "manager@company.com",
            "subject": "Project Status Update Required",
            "body": "Hi John, please provide an update on the API project status. We have a client meeting on Friday.",
            "received_date": "2024-01-18 11:00:00",
            "is_read": 0,
            "thread_id": "thread_003"
        },
        
        # NOISE EMAILS (80% - 16 out of 20)
        # Meeting Reminders
        {
            "sender": "calendar@company.com",
            "subject": "Reminder: Weekly Team Standup in 15 minutes",
            "body": "This is a reminder that your Weekly Team Standup meeting is starting in 15 minutes.",
            "received_date": "2024-01-16 08:45:00",
            "is_read": 1,
            "thread_id": "reminder_001"
        },
        {
            "sender": "calendar@company.com",
            "subject": "Reminder: 1:1 with Sarah in 30 minutes",
            "body": "This is a reminder that your 1:1 meeting with Sarah is starting in 30 minutes.",
            "received_date": "2024-01-17 09:30:00",
            "is_read": 1,
            "thread_id": "reminder_002"
        },
        
        # Product Promotions
        {
            "sender": "marketing@company.com",
            "subject": "New Product Launch: Check out our latest features!",
            "body": "We're excited to announce our new product features. Click here to learn more!",
            "received_date": "2024-01-16 10:00:00",
            "is_read": 0,
            "thread_id": "promo_001"
        },
        {
            "sender": "sales@company.com",
            "subject": "Special Offer: 50% off Premium Plan",
            "body": "Limited time offer! Get 50% off our premium plan. Offer expires soon!",
            "received_date": "2024-01-18 14:00:00",
            "is_read": 0,
            "thread_id": "promo_002"
        },
        
        # Finance Emails
        {
            "sender": "finance@company.com",
            "subject": "Monthly Expense Report Due",
            "body": "Please submit your monthly expense report by the end of the week.",
            "received_date": "2024-01-19 09:00:00",
            "is_read": 0,
            "thread_id": "finance_001"
        },
        {
            "sender": "payroll@company.com",
            "subject": "Payroll Processing Notice",
            "body": "Payroll will be processed on Friday. Please ensure your timesheet is submitted.",
            "received_date": "2024-01-20 11:00:00",
            "is_read": 0,
            "thread_id": "payroll_001"
        },
        
        # Legal & Compliance
        {
            "sender": "legal@company.com",
            "subject": "Updated Privacy Policy",
            "body": "Our privacy policy has been updated. Please review the changes.",
            "received_date": "2024-01-16 15:00:00",
            "is_read": 0,
            "thread_id": "legal_001"
        },
        {
            "sender": "compliance@company.com",
            "subject": "Security Training Reminder",
            "body": "Please complete your quarterly security training by month-end.",
            "received_date": "2024-01-17 10:00:00",
            "is_read": 0,
            "thread_id": "compliance_001"
        },
        
        # IT Emails
        {
            "sender": "it@company.com",
            "subject": "Scheduled Maintenance: Sunday 2-4 AM",
            "body": "We will be performing scheduled maintenance on Sunday from 2-4 AM. Some services may be unavailable.",
            "received_date": "2024-01-19 16:00:00",
            "is_read": 0,
            "thread_id": "it_001"
        },
        {
            "sender": "it@company.com",
            "subject": "Password Expiry Notice",
            "body": "Your password will expire in 7 days. Please update it before then.",
            "received_date": "2024-01-20 09:00:00",
            "is_read": 0,
            "thread_id": "it_002"
        },
        
        # POSH Meetings
        {
            "sender": "hr@company.com",
            "subject": "POSH Committee Meeting - All Hands",
            "body": "The Prevention of Sexual Harassment committee will hold an all-hands meeting next week. Attendance is mandatory.",
            "received_date": "2024-01-18 13:00:00",
            "is_read": 0,
            "thread_id": "posh_001"
        },
        
        # Company Events
        {
            "sender": "events@company.com",
            "subject": "Company All Hands - Q1 Results",
            "body": "Join us for our Q1 all-hands meeting where we'll discuss quarterly results and upcoming initiatives.",
            "received_date": "2024-01-21 10:00:00",
            "is_read": 0,
            "thread_id": "event_001"
        },
        {
            "sender": "hr@company.com",
            "subject": "Farewell Party for Mike - Friday 5 PM",
            "body": "Join us in celebrating Mike's contributions to the company. Farewell party at 5 PM in the cafeteria.",
            "received_date": "2024-01-19 14:00:00",
            "is_read": 0,
            "thread_id": "farewell_001"
        },
        
        # Newsletter & Updates
        {
            "sender": "newsletter@company.com",
            "subject": "Weekly Company Newsletter",
            "body": "This week's highlights: New hires, project updates, and company announcements.",
            "received_date": "2024-01-17 08:00:00",
            "is_read": 0,
            "thread_id": "newsletter_001"
        },
        {
            "sender": "hr@company.com",
            "subject": "New Employee Onboarding - Welcome Sarah!",
            "body": "Please welcome Sarah to our team! She joins us as a Senior Developer.",
            "received_date": "2024-01-20 12:00:00",
            "is_read": 0,
            "thread_id": "onboarding_001"
        }
    ]
    
    for email in emails:
        cursor.execute("""
            INSERT INTO emails (sender, subject, body, received_date, is_read, thread_id, meeting_date, meeting_duration, attendees)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email["sender"], email["subject"], email["body"], email["received_date"],
            email["is_read"], email["thread_id"], 
            email.get("meeting_date"), email.get("meeting_duration"), 
            email.get("attendees")
        ))
    
    conn.commit()
    conn.close()
    print("✅ Email database created and seeded")

def create_calendar_database():
    """Create and populate calendar database"""
    conn = sqlite3.connect("data/databases/calendar.db")
    cursor = conn.cursor()
    
    # Drop and recreate events table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS events")
    cursor.execute("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    # Sample calendar events with 80% noise, 20% important
    events = [
        # IMPORTANT EVENTS (20% - 2 out of 10)
        {
            "title": "Q1 Strategy Review",
            "description": "Quarterly strategy review meeting with leadership team",
            "start_time": "2024-01-16 10:00:00",
            "end_time": "2024-01-16 11:30:00",
            "location": "Conference Room A",
            "attendees": "ceo@company.com,cto@company.com,john.doe@company.com",
            "event_type": "meeting"
        },
        {
            "title": "API Project Deadline",
            "description": "Final deadline for API project delivery",
            "start_time": "2024-01-18 17:00:00",
            "end_time": "2024-01-18 17:00:00",
            "event_type": "deadline",
            "project_name": "API Integration"
        },
        
        # NOISE EVENTS (80% - 8 out of 10)
        # Farewell Meetings
        {
            "title": "Farewell Party for Mike",
            "description": "Join us in celebrating Mike's contributions to the company",
            "start_time": "2024-01-19 17:00:00",
            "end_time": "2024-01-19 19:00:00",
            "location": "Cafeteria",
            "attendees": "all@company.com",
            "event_type": "social",
        },
        
        # POSH Meetings
        {
            "title": "POSH Committee Meeting",
            "description": "Prevention of Sexual Harassment committee meeting",
            "start_time": "2024-01-22 14:00:00",
            "end_time": "2024-01-22 15:00:00",
            "location": "Conference Room B",
            "attendees": "posh-committee@company.com",
            "event_type": "meeting",
        },
        
        # Company All Hands
        {
            "title": "Company All Hands - Q1 Results",
            "description": "Quarterly all-hands meeting to discuss Q1 results",
            "start_time": "2024-01-23 10:00:00",
            "end_time": "2024-01-23 11:00:00",
            "location": "Main Auditorium",
            "attendees": "all@company.com",
            "event_type": "meeting",
        },
        
        # 1:1s (not with John)
        {
            "title": "1:1 with Sarah",
            "description": "Weekly 1:1 meeting with Sarah",
            "start_time": "2024-01-17 10:00:00",
            "end_time": "2024-01-17 10:30:00",
            "location": "Sarah's Office",
            "attendees": "sarah@company.com,manager@company.com",
            "event_type": "meeting",
        },
        {
            "title": "1:1 with Alex",
            "description": "Weekly 1:1 meeting with Alex",
            "start_time": "2024-01-18 11:00:00",
            "end_time": "2024-01-18 11:30:00",
            "location": "Alex's Office",
            "attendees": "alex@company.com,manager@company.com",
            "event_type": "meeting",
        },
        
        # Team Events
        {
            "title": "Team Building Event",
            "description": "Monthly team building activity",
            "start_time": "2024-01-20 15:00:00",
            "end_time": "2024-01-20 17:00:00",
            "location": "Recreation Center",
            "attendees": "team@company.com",
            "event_type": "social",
        },
        
        # Training Sessions
        {
            "title": "Security Training Session",
            "description": "Quarterly security awareness training",
            "start_time": "2024-01-24 09:00:00",
            "end_time": "2024-01-24 10:00:00",
            "location": "Training Room",
            "attendees": "all@company.com",
            "event_type": "training",
        },
        
        # Recurring Meetings
        {
            "title": "Weekly Team Standup",
            "description": "Daily standup meeting for the development team",
            "start_time": "2024-01-16 09:00:00",
            "end_time": "2024-01-16 09:30:00",
            "location": "Team Room",
            "attendees": "dev-team@company.com",
            "event_type": "meeting",
        }
    ]
    
    for event in events:
        cursor.execute("""
            INSERT INTO events (title, description, start_time, end_time, location, attendees, event_type, project_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["title"], event["description"], event["start_time"], event["end_time"],
            event.get("location"), event.get("attendees"), event["event_type"],
            event.get("project_name")
        ))
    
    conn.commit()
    conn.close()
    print("✅ Calendar database created and seeded")

def create_slack_database():
    """Create and populate Slack database"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    # Drop and recreate messages table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS messages")
    cursor.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            thread_ts TEXT,
            is_reply BOOLEAN DEFAULT 0,
            reactions TEXT,
            is_private BOOLEAN DEFAULT 0
        )
    """)
    
    # Sample Slack messages with 80% noise, 20% important
    messages = [
        # IMPORTANT MESSAGES (20% - 2 out of 10)
        {
            "channel": "D1234567890",
            "user": "manager@company.com",
            "message": "Hi John, just wanted to check in on the project status. Everything on track?",
            "timestamp": "2024-01-18 14:20:00",
            "is_private": 1
        },
        {
            "channel": "urgent",
            "user": "cto@company.com",
            "message": "@john.doe we need to discuss the security audit findings ASAP. Can you join a call in 30 mins?",
            "timestamp": "2024-01-21 13:00:00",
        },
        
        # NOISE MESSAGES (80% - 8 out of 10)
        # General Channel Noise
        {
            "channel": "general",
            "user": "alice.smith",
            "message": "Good morning everyone! Hope you all have a great day!",
            "timestamp": "2024-01-16 09:00:00"
        },
        {
            "channel": "general",
            "user": "bob.johnson",
            "message": "Anyone know where the coffee machine is? The one in the kitchen seems to be broken.",
            "timestamp": "2024-01-16 10:15:00"
        },
        
        # New Customer Messages
        {
            "channel": "customer-support",
            "user": "support@company.com",
            "message": "New customer inquiry from acme-corp. They're asking about enterprise pricing.",
            "timestamp": "2024-01-17 11:00:00"
        },
        {
            "channel": "sales-team",
            "user": "sales@company.com",
            "message": "Big deal closed! $50K ARR from TechCorp. Great work team!",
            "timestamp": "2024-01-18 15:30:00"
        },
        
        # New Employee Messages
        {
            "channel": "general",
            "user": "hr@company.com",
            "message": "Please welcome Sarah to our team! She joins us as a Senior Developer. Say hi! 👋",
            "timestamp": "2024-01-19 10:00:00"
        },
        {
            "channel": "general",
            "user": "sarah.new",
            "message": "Hi everyone! Excited to be part of the team. Looking forward to working with you all!",
            "timestamp": "2024-01-19 10:05:00"
        },
        
        # Reminders
        {
            "channel": "hr-announcements",
            "user": "hr@company.com",
            "message": "Reminder: Performance reviews are due by end of month. Please complete your self-assessments.",
            "timestamp": "2024-01-20 09:00:00"
        },
        
        # Release Channel
        {
            "channel": "releases",
            "user": "devops@company.com",
            "message": "Version 2.1.0 has been deployed to production. Release notes available in Confluence.",
            "timestamp": "2024-01-21 16:00:00"
        }
    ]
    
    for message in messages:
        cursor.execute("""
            INSERT INTO messages (channel, user, message, timestamp, thread_ts, is_reply, reactions, is_private)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message["channel"], message["user"], message["message"], message["timestamp"],
            message.get("thread_ts"), message.get("is_reply", 0), message.get("reactions"),
            message.get("is_private", 0)
        ))
    
    conn.commit()
    conn.close()
    print("✅ Slack database created and seeded")

def create_kanban_database():
    """Create and populate Kanban database"""
    conn = sqlite3.connect("data/databases/kanban.db")
    cursor = conn.cursor()
    
    # Drop and recreate tasks table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'medium',
            assignee TEXT,
            created_date TEXT NOT NULL,
            due_date TEXT,
            project TEXT,
            labels TEXT,
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
            task_id INTEGER,
            update_type TEXT,
            description TEXT,
            updated_by TEXT,
            updated_date TEXT,
            old_status TEXT,
            new_status TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    """)
    
    # Drop and recreate project_progress table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS project_progress")
    cursor.execute("""
        CREATE TABLE project_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            milestone TEXT,
            progress_percentage INTEGER,
            status TEXT,
            updated_date TEXT,
            description TEXT
        )
    """)
    
    # Sample tasks with 80% noise, 20% important
    tasks = [
        # IMPORTANT TASKS (20% - 2 out of 10)
        {
            "title": "Implement OAuth2 Authentication",
            "description": "Add OAuth2 authentication to the API endpoints",
            "status": "in_progress",
            "priority": "high",
            "assignee": "john.doe",
            "created_date": "2024-01-15",
            "due_date": "2024-01-20",
            "project": "API Integration",
            "labels": "backend,security",
            "updated_date": "2024-01-18"
        },
        {
            "title": "Fix Database Connection Pool",
            "description": "Resolve connection pool issues causing timeouts",
            "status": "blocked",
            "priority": "high",
            "assignee": "john.doe",
            "created_date": "2024-01-16",
            "due_date": "2024-01-19",
            "project": "API Integration",
            "labels": "backend,database",
            "updated_date": "2024-01-17",
            "blocker_reason": "Waiting for infrastructure team",
            "blocked_by": "infrastructure@company.com"
        },
        
        # NOISE TASKS (80% - 8 out of 10)
        # Ticket Details Changed - Assignee Changes
        {
            "title": "Update User Profile UI",
            "description": "Redesign the user profile page with new layout",
            "status": "in_progress",
            "priority": "medium",
            "assignee": "alice.smith",
            "created_date": "2024-01-14",
            "due_date": "2024-01-25",
            "project": "Frontend Redesign",
            "labels": "frontend,ui",
            "updated_date": "2024-01-18"
        },
        {
            "title": "Database Migration Script",
            "description": "Create migration script for user table updates",
            "status": "todo",
            "priority": "medium",
            "assignee": "bob.johnson",
            "created_date": "2024-01-16",
            "due_date": "2024-01-30",
            "project": "Database Optimization",
            "labels": "database,migration",
            "updated_date": "2024-01-17"
        },
        
        # Story Points Changes
        {
            "title": "Add Email Notifications",
            "description": "Implement email notification system for user actions",
            "status": "todo",
            "priority": "medium",
            "assignee": "sarah.new",
            "created_date": "2024-01-15",
            "due_date": "2024-01-28",
            "project": "Notification System",
            "labels": "backend,notifications",
            "updated_date": "2024-01-18"
        },
        
        # Status Updates
        {
            "title": "Mobile App Bug Fixes",
            "description": "Fix critical bugs in the mobile application",
            "status": "done",
            "priority": "medium",
            "assignee": "mobile.team",
            "created_date": "2024-01-10",
            "due_date": "2024-01-15",
            "project": "Mobile App",
            "labels": "mobile,bugs",
            "updated_date": "2024-01-15"
        },
        {
            "title": "Performance Optimization",
            "description": "Optimize application performance for better load times",
            "status": "in_progress",
            "priority": "medium",
            "assignee": "devops.team",
            "created_date": "2024-01-12",
            "due_date": "2024-01-22",
            "project": "Performance",
            "labels": "performance,optimization",
            "updated_date": "2024-01-19"
        },
        
        # Comments Added
        {
            "title": "Security Audit Implementation",
            "description": "Implement security recommendations from audit report",
            "status": "todo",
            "priority": "medium",
            "assignee": "security.team",
            "created_date": "2024-01-17",
            "due_date": "2024-01-24",
            "project": "Security",
            "labels": "security,audit",
            "updated_date": "2024-01-18"
        },
        {
            "title": "API Rate Limiting",
            "description": "Implement rate limiting for API endpoints",
            "status": "todo",
            "priority": "medium",
            "assignee": "backend.team",
            "created_date": "2024-01-18",
            "due_date": "2024-01-26",
            "project": "API Security",
            "labels": "api,security,rate-limiting",
            "updated_date": "2024-01-19"
        }
    ]
    
    for task in tasks:
        cursor.execute("""
            INSERT INTO tasks (title, description, status, priority, assignee, created_date, due_date, project, labels, updated_date, blocker_reason, blocked_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["title"], task["description"], task["status"], task["priority"],
            task["assignee"], task["created_date"], task["due_date"], task["project"],
            task["labels"], task["updated_date"], task.get("blocker_reason"),
            task.get("blocked_by")
        ))
    
    # Sample task updates
    task_updates = [
        {
            "task_id": 1,
            "update_type": "status_change",
            "description": "Started working on OAuth2 implementation",
            "updated_by": "john.doe",
            "updated_date": "2024-01-16",
            "old_status": "todo",
            "new_status": "in_progress"
        },
        {
            "task_id": 2,
            "update_type": "blocked",
            "description": "Task blocked due to infrastructure dependency",
            "updated_by": "john.doe",
            "updated_date": "2024-01-17",
            "old_status": "in_progress",
            "new_status": "blocked"
        },
        {
            "task_id": 3,
            "update_type": "completed",
            "description": "Code review completed successfully",
            "updated_by": "john.doe",
            "updated_date": "2024-01-17",
            "old_status": "in_progress",
            "new_status": "done"
        }
    ]
    
    for update in task_updates:
        cursor.execute("""
            INSERT INTO task_updates (task_id, update_type, description, updated_by, updated_date, old_status, new_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            update["task_id"], update["update_type"], update["description"],
            update["updated_by"], update["updated_date"], update["old_status"],
            update["new_status"]
        ))
    
    # Sample project progress
    project_progress = [
        {
            "project_name": "API Integration",
            "milestone": "Authentication Module",
            "progress_percentage": 75,
            "status": "in_progress",
            "updated_date": "2024-01-18",
            "description": "OAuth2 implementation 75% complete, database issues blocking completion"
        },
        {
            "project_name": "Payment System",
            "milestone": "Code Review Phase",
            "progress_percentage": 100,
            "status": "completed",
            "updated_date": "2024-01-17",
            "description": "All code reviews completed successfully"
        }
    ]
    
    for progress in project_progress:
        cursor.execute("""
            INSERT INTO project_progress (project_name, milestone, progress_percentage, status, updated_date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            progress["project_name"], progress["milestone"], progress["progress_percentage"],
            progress["status"], progress["updated_date"], progress["description"]
        ))
    
    conn.commit()
    conn.close()
    print("✅ Kanban database created and seeded")

def create_github_database():
    """Create and populate GitHub database"""
    conn = sqlite3.connect("data/databases/github.db")
    cursor = conn.cursor()
    
    # Drop and recreate commits table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS commits")
    cursor.execute("""
        CREATE TABLE commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository TEXT NOT NULL,
            author TEXT NOT NULL,
            message TEXT NOT NULL,
            commit_hash TEXT NOT NULL,
            branch TEXT DEFAULT 'main',
            files_changed INTEGER,
            lines_added INTEGER,
            lines_deleted INTEGER,
            commit_date TEXT NOT NULL
        )
    """)
    
    # Drop and recreate pull_requests table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS pull_requests")
    cursor.execute("""
        CREATE TABLE pull_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT NOT NULL,
            merged_date TEXT,
            review_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0
        )
    """)
    
    # Drop and recreate issues table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS issues")
    cursor.execute("""
        CREATE TABLE issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            labels TEXT,
            priority TEXT DEFAULT 'medium',
            created_date TEXT NOT NULL,
            closed_date TEXT
        )
    """)
    
    # Drop and recreate code_reviews table to avoid duplication
    cursor.execute("DROP TABLE IF EXISTS code_reviews")
    cursor.execute("""
        CREATE TABLE code_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_id INTEGER,
            reviewer TEXT NOT NULL,
            comment TEXT NOT NULL,
            review_type TEXT DEFAULT 'comment',
            file_path TEXT,
            line_number INTEGER,
            created_date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (pr_id) REFERENCES pull_requests (id)
        )
    """)
    
    # Sample commits with 80% noise, 20% important
    commits = [
        # IMPORTANT COMMITS (20% - 1 out of 5)
        {
            "repository": "api-integration",
            "author": "john.doe",
            "message": "feat: implement OAuth2 authentication",
            "commit_hash": "a1b2c3d4e5f6",
            "branch": "feature/oauth2",
            "files_changed": 5,
            "lines_added": 120,
            "lines_deleted": 10,
            "commit_date": "2024-01-16 14:30:00"
        },
        
        # NOISE COMMITS (80% - 4 out of 5)
        # Every PR raised even though you are not the reviewer
        {
            "repository": "frontend-app",
            "author": "alice.smith",
            "message": "feat: add new user dashboard component",
            "commit_hash": "b2c3d4e5f6g7",
            "branch": "feature/dashboard",
            "files_changed": 8,
            "lines_added": 200,
            "lines_deleted": 15,
            "commit_date": "2024-01-16 10:00:00"
        },
        {
            "repository": "mobile-app",
            "author": "bob.johnson",
            "message": "fix: resolve crash on Android 14",
            "commit_hash": "c3d4e5f6g7h8",
            "branch": "bugfix/android-crash",
            "files_changed": 3,
            "lines_added": 45,
            "lines_deleted": 12,
            "commit_date": "2024-01-17 09:30:00"
        },
        {
            "repository": "data-pipeline",
            "author": "sarah.new",
            "message": "refactor: optimize database queries",
            "commit_hash": "d4e5f6g7h8i9",
            "branch": "optimization/queries",
            "files_changed": 6,
            "lines_added": 80,
            "lines_deleted": 30,
            "commit_date": "2024-01-18 11:15:00"
        },
        {
            "repository": "devops-tools",
            "author": "devops.team",
            "message": "ci: update deployment scripts",
            "commit_hash": "e5f6g7h8i9j0",
            "branch": "main",
            "files_changed": 4,
            "lines_added": 60,
            "lines_deleted": 20,
            "commit_date": "2024-01-19 14:20:00"
        }
    ]
    
    for commit in commits:
        cursor.execute("""
            INSERT INTO commits (repository, author, message, commit_hash, branch, files_changed, lines_added, lines_deleted, commit_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            commit["repository"], commit["author"], commit["message"], commit["commit_hash"],
            commit["branch"], commit["files_changed"], commit["lines_added"],
            commit["lines_deleted"], commit["commit_date"]
        ))
    
    # Sample pull requests with 80% noise, 20% important
    pull_requests = [
        # IMPORTANT PRs (20% - 1 out of 5)
        {
            "repository": "api-integration",
            "title": "Add OAuth2 Authentication Support",
            "description": "This PR adds OAuth2 authentication to the API endpoints. Includes JWT token validation and refresh token handling.",
            "author": "john.doe",
            "status": "open",
            "created_date": "2024-01-16 15:00:00",
            "review_count": 2,
            "comment_count": 5
        },
        
        # NOISE PRs (80% - 4 out of 5)
        # Every PR raised even though you are not the reviewer
        {
            "repository": "frontend-app",
            "title": "Add new user dashboard with analytics",
            "description": "Implements a new dashboard component with user analytics and metrics visualization.",
            "author": "alice.smith",
            "status": "open",
            "created_date": "2024-01-16 10:30:00",
            "review_count": 0,
            "comment_count": 1
        },
        {
            "repository": "mobile-app",
            "title": "Fix Android 14 compatibility issues",
            "description": "Resolves crashes and compatibility issues on Android 14 devices.",
            "author": "bob.johnson",
            "status": "merged",
            "created_date": "2024-01-17 09:45:00",
            "merged_date": "2024-01-18 14:20:00",
            "review_count": 3,
            "comment_count": 7
        },
        {
            "repository": "data-pipeline",
            "title": "Optimize database query performance",
            "description": "Improves query performance by adding indexes and optimizing joins.",
            "author": "sarah.new",
            "status": "open",
            "created_date": "2024-01-18 11:30:00",
            "review_count": 1,
            "comment_count": 2
        },
        {
            "repository": "devops-tools",
            "title": "Update CI/CD pipeline configuration",
            "description": "Updates deployment scripts and adds new environment configurations.",
            "author": "devops.team",
            "status": "merged",
            "created_date": "2024-01-19 14:45:00",
            "merged_date": "2024-01-20 10:15:00",
            "review_count": 2,
            "comment_count": 4
        }
    ]
    
    for pr in pull_requests:
        cursor.execute("""
            INSERT INTO pull_requests (repository, title, description, author, status, created_date, merged_date, review_count, comment_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pr["repository"], pr["title"], pr["description"], pr["author"],
            pr["status"], pr["created_date"], pr.get("merged_date"),
            pr["review_count"], pr["comment_count"]
        ))
    
    # Sample issues with 80% noise, 20% important
    issues = [
        # IMPORTANT ISSUES (20% - 1 out of 5)
        {
            "repository": "api-integration",
            "title": "API rate limiting not working correctly",
            "description": "The rate limiting middleware is not properly enforcing limits on API endpoints.",
            "author": "client@external.com",
            "status": "open",
            "labels": "bug,high-priority",
            "priority": "high",
            "created_date": "2024-01-20 08:30:00"
        },
        
        # NOISE ISSUES (80% - 4 out of 5)
        # Build failures
        {
            "repository": "frontend-app",
            "title": "Build failing on Node.js 18",
            "description": "The build process is failing when using Node.js version 18. Works fine with Node.js 16.",
            "author": "alice.smith",
            "status": "open",
            "labels": "bug,build",
            "priority": "medium",
            "created_date": "2024-01-16 09:00:00"
        },
        {
            "repository": "mobile-app",
            "title": "iOS build failing due to dependency conflicts",
            "description": "CocoaPods dependency resolution is failing for iOS build. Need to update podfile.",
            "author": "bob.johnson",
            "status": "open",
            "labels": "bug,ios,build",
            "priority": "medium",
            "created_date": "2024-01-17 11:30:00"
        },
        
        # Action failures
        {
            "repository": "data-pipeline",
            "title": "GitHub Actions workflow failing",
            "description": "The CI/CD pipeline is failing due to timeout issues in the test suite.",
            "author": "sarah.new",
            "status": "open",
            "labels": "bug,ci-cd",
            "priority": "medium",
            "created_date": "2024-01-18 13:15:00"
        },
        
        # Other team activity
        {
            "repository": "devops-tools",
            "title": "Docker container memory usage optimization",
            "description": "Need to optimize memory usage in production Docker containers to reduce costs.",
            "author": "devops.team",
            "status": "open",
            "labels": "enhancement,performance",
            "priority": "medium",
            "created_date": "2024-01-19 15:45:00"
        }
    ]
    
    for issue in issues:
        cursor.execute("""
            INSERT INTO issues (repository, title, description, author, status, labels, priority, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            issue["repository"], issue["title"], issue["description"], issue["author"],
            issue["status"], issue["labels"], issue["priority"], issue["created_date"]
        ))
    
    # Sample code reviews
    code_reviews = [
        {
            "pr_id": 1,
            "reviewer": "alice.smith",
            "comment": "Great implementation! Just need to add error handling for token expiration.",
            "review_type": "comment",
            "file_path": "src/auth/oauth2.py",
            "line_number": 45,
            "created_date": "2024-01-17 10:00:00",
            "status": "resolved"
        },
        {
            "pr_id": 1,
            "reviewer": "bob.johnson",
            "comment": "Consider adding unit tests for the new authentication flow.",
            "review_type": "suggestion",
            "file_path": "tests/auth/test_oauth2.py",
            "line_number": 1,
            "created_date": "2024-01-17 15:30:00",
            "status": "pending"
        }
    ]
    
    for review in code_reviews:
        cursor.execute("""
            INSERT INTO code_reviews (pr_id, reviewer, comment, review_type, file_path, line_number, created_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            review["pr_id"], review["reviewer"], review["comment"], review["review_type"],
            review["file_path"], review["line_number"], review["created_date"], review["status"]
        ))
    
    conn.commit()
    conn.close()
    print("✅ GitHub database created and seeded")

def main():
    """Main function to create all databases"""
    print("🚀 Starting database creation and seeding...")
    print("📅 OOO Period: 2024-01-15 to 2024-01-22")
    print()
    
    create_email_database()
    create_calendar_database()
    create_slack_database()
    create_kanban_database()
    create_github_database()
    
    print()
    print("✅ All databases created and seeded successfully!")
    print("📊 Summary:")
    print("   - Email database: 20 emails (4 important, 16 noise) - 80% noise ratio")
    print("   - Calendar database: 10 events (2 important, 8 noise) - 80% noise ratio")
    print("   - Slack database: 10 messages (2 important, 8 noise) - 80% noise ratio")
    print("   - Kanban database: 10 tasks (2 important, 8 noise) - 80% noise ratio")
    print("   - GitHub database: 5 commits, 5 PRs, 5 issues (1 important each) - 80% noise ratio")
    print()
    print("🎯 Challenge: LLM must filter through 80% noise to identify truly important items!")

if __name__ == "__main__":
    main()
