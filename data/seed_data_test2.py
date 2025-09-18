import sqlite3
import os

os.makedirs("data/databases", exist_ok=True)

def create_email_database():
    """Create and populate email database for Test Case 2"""
    conn = sqlite3.connect("data/databases/emails.db")
    cursor = conn.cursor()
    
    # Create emails table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
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
    
    # Important emails (20% of total - 4 out of 20)
    important_emails = [
        ("email_001", "security@company.com", "URGENT: Production Security Breach Detected", "A critical security vulnerability has been detected in our production API. Immediate action is required to prevent data loss. See incident #987.", "2024-01-08 10:00:00", 0, "thread_sec_001", None, None, "security@company.com,cto@company.com"),
        ("email_002", "product@company.com", "Q1 Roadmap Review Meeting", "Please review the Q1 product roadmap document attached. Meeting scheduled for Jan 10th to discuss priorities.", "2024-01-07 14:30:00", 0, "thread_q1_001", "2024-01-10 10:00:00", 90, "product@company.com,architects@company.com"),
        ("email_003", "devops@company.com", "High Priority: Database Performance Degradation", "We're seeing significant performance degradation on the main customer database. Investigate and fix ASAP.", "2024-01-09 11:45:00", 0, "thread_perf_001", None, None, "devops@company.com,ops-team@company.com"),
        ("email_004", "hr@company.com", "Annual Performance Review Cycle Starts", "The annual performance review cycle has officially started. Please submit your self-assessments by Jan 12th.", "2024-01-07 09:00:00", 0, "thread_hr_001", None, None, "hr@company.com,all@company.com"),
    ]
    
    # Noise emails (80% of total - 16 out of 20)
    noise_emails = [
        ("email_005", "marketing@company.com", "Weekly Newsletter - Company Updates", "Check out our latest company newsletter with exciting updates and team highlights!", "2024-01-07 08:00:00", 0, "thread_news_001", None, None, "marketing@company.com,all@company.com"),
        ("email_006", "support@company.com", "Customer Feedback Summary", "Weekly customer feedback summary is now available. Some interesting insights this week!", "2024-01-07 11:00:00", 0, "thread_feedback_001", None, None, "support@company.com,product@company.com"),
        ("email_007", "finance@company.com", "December Budget Report", "December budget report is ready for review. Please check your department allocations.", "2024-01-08 09:00:00", 0, "thread_budget_001", None, None, "finance@company.com,managers@company.com"),
        ("email_008", "events@company.com", "Team Building Event Invitation", "Join us for a fun team building event at the escape room this Friday! RSVP required.", "2024-01-08 15:00:00", 0, "thread_event_001", "2024-01-12 18:00:00", 120, "events@company.com,all@company.com"),
        ("email_009", "it@company.com", "Software Update Reminder", "Reminder: Please update your software to the latest version for security patches.", "2024-01-09 10:00:00", 0, "thread_update_001", None, None, "it@company.com,all@company.com"),
        ("email_010", "admin@company.com", "Office Supplies Update", "Office supplies have been ordered and will arrive next week. Thanks for your patience!", "2024-01-09 13:00:00", 0, "thread_supplies_001", None, None, "admin@company.com,all@company.com"),
        ("email_011", "legal@company.com", "Service Agreement Review", "Updated service agreements are ready for review. Please provide feedback by end of week.", "2024-01-10 11:00:00", 0, "thread_contract_001", None, None, "legal@company.com,managers@company.com"),
        ("email_012", "training@company.com", "New Employee Onboarding", "Welcome our new team members! Onboarding sessions are scheduled throughout the week.", "2024-01-10 14:00:00", 0, "thread_onboarding_001", None, None, "training@company.com,hr@company.com"),
        ("email_013", "research@company.com", "Market Research Findings", "Latest market research findings are now available in the shared drive. Some interesting trends!", "2024-01-11 10:00:00", 0, "thread_research_001", None, None, "research@company.com,product@company.com"),
        ("email_014", "compliance@company.com", "Quarterly Compliance Review", "Quarterly compliance review is due. Please ensure all documentation is up to date.", "2024-01-11 12:00:00", 0, "thread_compliance_001", None, None, "compliance@company.com,all@company.com"),
        ("email_015", "sales@company.com", "Q1 Sales Targets Update", "Q1 sales targets have been updated based on current market conditions. Let's crush these goals!", "2024-01-12 08:00:00", 0, "thread_sales_001", None, None, "sales@company.com,managers@company.com"),
        ("email_016", "product@company.com", "Feature Request Summary", "Feature request summary from customer feedback sessions is now available. Great insights!", "2024-01-12 15:00:00", 0, "thread_features_001", None, None, "product@company.com,dev-team@company.com"),
        ("email_017", "operations@company.com", "Weekly Operations Report", "Weekly operations report: System uptime at 99.8% this week. Great job team!", "2024-01-13 10:00:00", 0, "thread_ops_001", None, None, "operations@company.com,managers@company.com"),
        ("email_018", "quality@company.com", "QA Metrics Update", "QA metrics show improvement in bug detection rates. Keep up the excellent work!", "2024-01-13 14:00:00", 0, "thread_qa_001", None, None, "quality@company.com,dev-team@company.com"),
        ("email_019", "analytics@company.com", "User Analytics Dashboard", "Updated user analytics dashboard with new metrics and visualizations. Check it out!", "2024-01-14 09:00:00", 0, "thread_analytics_001", None, None, "analytics@company.com,product@company.com"),
        ("email_020", "communications@company.com", "Internal Communication Policies", "Internal communication policies have been updated. Please review the new guidelines.", "2024-01-14 16:00:00", 0, "thread_comm_001", None, None, "communications@company.com,all@company.com"),
    ]
    
    # Insert all emails (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("INSERT OR IGNORE INTO emails (custom_id, sender, subject, body, received_date, is_read, thread_id, meeting_date, meeting_duration, attendees) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_emails + noise_emails)
    
    conn.commit()
    conn.close()

def create_calendar_database():
    """Create and populate calendar database for Test Case 2"""
    conn = sqlite3.connect("data/databases/calendar.db")
    cursor = conn.cursor()
    
    # Drop and recreate events table to ensure correct schema
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
    
    # Important events (20% of total - 4 out of 20)
    important_events = [
        ("event_001", "Security Incident Response", "Emergency response meeting for security breach investigation", "2024-01-08 11:00:00", "2024-01-08 12:30:00", "War Room", "security@company.com,cto@company.com,dev-team@company.com", "meeting", 0, 1, "Security"),
        ("event_002", "Q1 Technical Roadmap Review", "Review and finalize Q1 technical roadmap with architecture team", "2024-01-09 15:00:00", "2024-01-09 16:30:00", "Conference Room A", "cto@company.com,architects@company.com,lead-dev@company.com", "meeting", 0, 1, "Architecture"),
        ("event_003", "Production Performance Crisis", "Urgent meeting to address production system performance issues", "2024-01-10 10:00:00", "2024-01-10 11:30:00", "Operations Center", "ops@company.com,dev-team@company.com,manager@company.com", "meeting", 0, 1, "Operations"),
        ("event_004", "Annual Performance Review Deadline", "Deadline for submitting annual performance review materials", "2024-01-12 17:00:00", "2024-01-12 17:00:00", None, "hr@company.com,all@company.com", "deadline", 0, 1, "HR"),
    ]
    
    # Noise events (80% of total - 16 out of 20)
    noise_events = [
        ("event_005", "Weekly Team Standup", "Regular weekly team standup meeting", "2024-01-07 09:00:00", "2024-01-07 09:30:00", "Conference Room B", "dev-team@company.com", "meeting", 0, 1, "Development"),
        ("event_006", "Lunch with Colleagues", "Casual lunch with team members", "2024-01-07 12:00:00", "2024-01-07 13:00:00", "Company Cafeteria", "colleagues@company.com", "social", 0, 0, None),
        ("event_007", "Software Training Session", "Training session on new software tools", "2024-01-08 14:00:00", "2024-01-08 15:00:00", "Training Room", "it@company.com,all@company.com", "training", 0, 1, "Training"),
        ("event_008", "Office Maintenance", "Scheduled office maintenance and cleaning", "2024-01-08 18:00:00", "2024-01-08 20:00:00", "Office", "maintenance@company.com", "maintenance", 0, 0, "Maintenance"),
        ("event_009", "Product Demo Preparation", "Prepare for upcoming product demonstration", "2024-01-09 10:00:00", "2024-01-09 11:00:00", "Demo Room", "product@company.com", "preparation", 0, 1, "Product"),
        ("event_010", "Code Review Session", "Regular code review session with team", "2024-01-09 13:00:00", "2024-01-09 14:00:00", "Conference Room C", "dev-team@company.com", "meeting", 0, 1, "Development"),
        ("event_011", "Client Meeting Preparation", "Prepare materials for upcoming client meeting", "2024-01-10 14:00:00", "2024-01-10 15:00:00", "Conference Room A", "sales@company.com", "preparation", 0, 1, "Sales"),
        ("event_012", "Team Building Activity", "Monthly team building activity", "2024-01-10 16:00:00", "2024-01-10 17:30:00", "Recreation Room", "hr@company.com,all@company.com", "social", 0, 0, "HR"),
        ("event_013", "Documentation Review", "Review and update project documentation", "2024-01-11 09:00:00", "2024-01-11 10:30:00", "Office", "dev-team@company.com", "work", 0, 1, "Development"),
        ("event_014", "Vendor Meeting", "Meeting with external vendor for service review", "2024-01-11 11:00:00", "2024-01-11 12:00:00", "Conference Room B", "vendor@external.com,procurement@company.com", "meeting", 0, 1, "Procurement"),
        ("event_015", "Budget Planning Session", "Plan budget allocation for next quarter", "2024-01-12 10:00:00", "2024-01-12 11:30:00", "Conference Room A", "finance@company.com,managers@company.com", "meeting", 0, 1, "Finance"),
        ("event_016", "Equipment Maintenance", "Scheduled maintenance for office equipment", "2024-01-12 14:00:00", "2024-01-12 15:00:00", "Office", "it@company.com", "maintenance", 0, 0, "IT"),
        ("event_017", "Project Status Update", "Weekly project status update meeting", "2024-01-13 09:30:00", "2024-01-13 10:30:00", "Conference Room C", "project-managers@company.com", "meeting", 0, 1, "Project Management"),
        ("event_018", "Skills Development Workshop", "Workshop on professional skills development", "2024-01-13 13:00:00", "2024-01-13 15:00:00", "Training Room", "hr@company.com,all@company.com", "training", 0, 1, "HR"),
        ("event_019", "Office Cleanup Day", "Monthly office cleanup and organization", "2024-01-14 10:00:00", "2024-01-14 12:00:00", "Office", "admin@company.com,all@company.com", "maintenance", 0, 0, "Admin"),
        ("event_020", "Weekend Planning Meeting", "Plan activities and priorities for next week", "2024-01-14 15:00:00", "2024-01-14 16:00:00", "Conference Room B", "managers@company.com", "meeting", 0, 1, "Management"),
    ]
    
    # Insert all events (use OR IGNORE to avoid conflicts when appending)
    # Note: id is auto-increment, so we don't specify it
    cursor.executemany("INSERT OR IGNORE INTO events (custom_id, title, description, start_time, end_time, location, attendees, event_type, is_all_day, reminder_set, project_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_events + noise_events)
    
    conn.commit()
    conn.close()

def create_slack_database():
    """Create and populate Slack database for Test Case 2"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    # Create messages table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            is_private BOOLEAN DEFAULT 0,
            thread_id TEXT,
            is_mention BOOLEAN DEFAULT 0,
            custom_id TEXT UNIQUE
        )
    """)
    
    # Important messages (20% of total - 4 out of 20)
    important_messages = [
        ("slack_001", "#security", "security@company.com", "@john.doe URGENT: Security breach detected in auth system. Need immediate investigation and response.", "2024-01-08 10:45:00", 0, "security_thread_001"),
        ("slack_002", "#architecture", "cto@company.com", "@john.doe Please review the Q1 technical roadmap. Your input on the proposed architecture changes is critical.", "2024-01-09 14:30:00", 0, "roadmap_thread_001"),
        ("slack_003", "#production", "ops@company.com", "@john.doe Production system performance is severely degraded. Customers reporting timeouts. Need your expertise ASAP.", "2024-01-10 09:15:00", 0, "performance_thread_001"),
        ("slack_004", "#hr", "hr@company.com", "@john.doe Annual performance review deadline is approaching. Please submit your self-assessment by Friday.", "2024-01-11 16:15:00", 0, "review_thread_001"),
    ]
    
    # Noise messages (80% of total - 16 out of 20)
    noise_messages = [
        (5, "#general", "marketing@company.com", "Check out our latest newsletter! Great updates on product features and company news.", "2024-01-07 08:15:00", 0, "newsletter_thread_001", 0, "slack_005"),
        (6, "#support", "support@company.com", "Weekly customer feedback summary is now available. Some interesting insights this week!", "2024-01-07 11:45:00", 0, "feedback_thread_001", 0, "slack_006"),
        (7, "#finance", "finance@company.com", "December budget report is ready for review. Please check your department allocations.", "2024-01-08 09:30:00", 0, "budget_thread_001", 0, "slack_007"),
        (8, "#events", "events@company.com", "Team building event at the escape room this Friday! Who's in? 🎉", "2024-01-08 16:00:00", 0, "event_thread_001", 0, "slack_008"),
        (9, "#it", "it@company.com", "Reminder: Please update your software to the latest version for security patches.", "2024-01-09 10:15:00", 0, "update_thread_001", 0, "slack_009"),
        (10, "#admin", "admin@company.com", "Office supplies have been ordered and will arrive next week. Thanks for your patience!", "2024-01-09 13:30:00", 0, "supplies_thread_001", 0, "slack_010"),
        (11, "#legal", "legal@company.com", "Updated service agreements are ready for review. Please provide feedback by end of week.", "2024-01-10 11:15:00", 0, "contract_thread_001", 0, "slack_011"),
        (12, "#onboarding", "training@company.com", "Welcome our new team members! Onboarding sessions are scheduled throughout the week.", "2024-01-10 14:45:00", 0, "onboarding_thread_001", 0, "slack_012"),
        (13, "#research", "research@company.com", "Latest market research findings are now available in the shared drive. Some interesting trends!", "2024-01-11 10:00:00", 0, "research_thread_001", 0, "slack_013"),
        (14, "#compliance", "compliance@company.com", "Quarterly compliance review is due. Please ensure all documentation is up to date.", "2024-01-11 12:30:00", 0, "compliance_thread_001", 0, "slack_014"),
        (15, "#sales", "sales@company.com", "Q1 sales targets have been updated based on current market conditions. Let's crush these goals! 💪", "2024-01-12 08:45:00", 0, "sales_thread_001", 0, "slack_015"),
        (16, "#product", "product@company.com", "Feature request summary from customer feedback sessions is now available. Great insights!", "2024-01-12 15:15:00", 0, "features_thread_001", 0, "slack_016"),
        (17, "#operations", "operations@company.com", "Weekly operations report: System uptime at 99.8% this week. Great job team! 📊", "2024-01-13 10:30:00", 0, "ops_thread_001", 0, "slack_017"),
        (18, "#qa", "quality@company.com", "QA metrics show improvement in bug detection rates. Keep up the excellent work! 🐛", "2024-01-13 14:00:00", 0, "qa_thread_001", 0, "slack_018"),
        (19, "#analytics", "analytics@company.com", "Updated user analytics dashboard with new metrics and visualizations. Check it out!", "2024-01-14 09:45:00", 0, "analytics_thread_001", 0, "slack_019"),
        (20, "#communications", "communications@company.com", "Internal communication policies have been updated. Please review the new guidelines.", "2024-01-14 16:30:00", 0, "comm_thread_001", 0, "slack_020"),
    ]
    
    # Insert all messages (use OR IGNORE to avoid conflicts when appending)
    # Note: id is auto-increment, so we don't specify it
    cursor.executemany("INSERT OR IGNORE INTO messages (custom_id, channel, user, message, timestamp, is_mention, thread_id) VALUES (?, ?, ?, ?, ?, ?, ?)", important_messages)
    
    conn.commit()
    conn.close()

def create_kanban_database():
    """Create and populate Kanban database for Test Case 2"""
    conn = sqlite3.connect("data/databases/kanban.db")
    cursor = conn.cursor()
    
    # Create kanban_tasks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kanban_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            assignee TEXT,
            created_date TEXT NOT NULL,
            due_date TEXT,
            project_name TEXT,
            labels TEXT,
            updated_date TEXT,
            custom_id TEXT UNIQUE
        )
    """)
    
    # Important tasks (20% of total - 4 out of 20)
    important_tasks = [
        (1, "Investigate Security Breach", "Critical security breach in authentication system requires immediate investigation and remediation", "in_progress", "high", "john.doe@company.com", "2024-01-08 10:00:00", "2024-01-08", "Security", "security,urgent,critical", "2024-01-08 10:00:00", "task_001"),
        (2, "Review Q1 Technical Roadmap", "Review and provide feedback on Q1 technical roadmap and architecture changes", "todo", "high", "john.doe@company.com", "2024-01-09 14:00:00", "2024-01-10", "Architecture", "roadmap,planning,architecture", "2024-01-09 14:00:00", "task_002"),
        (3, "Fix Production Performance Issues", "Address critical production system performance degradation affecting customers", "in_progress", "high", "john.doe@company.com", "2024-01-10 09:00:00", "2024-01-10", "Production", "performance,urgent,production", "2024-01-10 09:00:00", "task_003"),
        (4, "Complete Annual Performance Review", "Submit annual performance review self-assessment and team feedback", "todo", "medium", "john.doe@company.com", "2024-01-11 16:00:00", "2024-01-12", "HR", "review,hr,deadline", "2024-01-11 16:00:00", "task_004"),
    ]
    
    # Noise tasks (80% of total - 16 out of 20)
    noise_tasks = [
        (5, "Update Documentation", "Update project documentation with latest changes", "todo", "low", "alice@company.com", "2024-01-07 09:00:00", "2024-01-15", "Documentation", "docs,maintenance", "2024-01-07 09:00:00", "task_005"),
        (6, "Code Review Session", "Conduct code review for recent pull requests", "in_progress", "medium", "bob@company.com", "2024-01-07 10:00:00", "2024-01-08", "Development", "code-review,development", "2024-01-07 10:00:00", "task_006"),
        (7, "Prepare Training Materials", "Prepare materials for upcoming software training session", "todo", "low", "charlie@company.com", "2024-01-08 08:00:00", "2024-01-10", "Training", "training,preparation", "2024-01-08 08:00:00", "task_007"),
        (8, "Update User Interface", "Minor UI improvements based on user feedback", "in_progress", "medium", "diana@company.com", "2024-01-08 11:00:00", "2024-01-12", "Frontend", "ui,frontend,improvement", "2024-01-08 11:00:00", "task_008"),
        (9, "Database Optimization", "Optimize database queries for better performance", "todo", "medium", "eve@company.com", "2024-01-09 09:00:00", "2024-01-16", "Backend", "database,optimization", "2024-01-09 09:00:00", "task_009"),
        (10, "API Documentation Update", "Update API documentation with new endpoints", "in_progress", "low", "frank@company.com", "2024-01-09 13:00:00", "2024-01-14", "API", "api,docs", "2024-01-09 13:00:00", "task_010"),
        (11, "Client Demo Preparation", "Prepare demo materials for upcoming client presentation", "todo", "medium", "grace@company.com", "2024-01-10 08:00:00", "2024-01-11", "Sales", "demo,client,presentation", "2024-01-10 08:00:00", "task_011"),
        (12, "Bug Fix: Login Issue", "Fix minor login issue reported by users", "in_progress", "medium", "henry@company.com", "2024-01-10 14:00:00", "2024-01-12", "Bug Fixes", "bug,login,fix", "2024-01-10 14:00:00", "task_012"),
        (13, "Feature Enhancement: Search", "Enhance search functionality with better filters", "todo", "low", "iris@company.com", "2024-01-11 10:00:00", "2024-01-18", "Features", "search,enhancement", "2024-01-11 10:00:00", "task_013"),
        (14, "Performance Monitoring Setup", "Set up monitoring for new application features", "in_progress", "medium", "jack@company.com", "2024-01-11 15:00:00", "2024-01-15", "Monitoring", "monitoring,performance", "2024-01-11 15:00:00", "task_014"),
        (15, "User Testing Session", "Conduct user testing for new features", "todo", "medium", "kate@company.com", "2024-01-12 09:00:00", "2024-01-16", "Testing", "testing,user-feedback", "2024-01-12 09:00:00", "task_015"),
        (16, "Security Audit Preparation", "Prepare for upcoming security audit", "in_progress", "medium", "leo@company.com", "2024-01-12 11:00:00", "2024-01-17", "Security", "security,audit", "2024-01-12 11:00:00", "task_016"),
        (17, "Backup System Update", "Update backup system with latest configurations", "todo", "low", "mary@company.com", "2024-01-13 08:00:00", "2024-01-20", "Infrastructure", "backup,infrastructure", "2024-01-13 08:00:00", "task_017"),
        (18, "Mobile App Testing", "Test mobile app compatibility with new features", "in_progress", "medium", "nick@company.com", "2024-01-13 13:00:00", "2024-01-19", "Mobile", "mobile,testing", "2024-01-13 13:00:00", "task_018"),
        (19, "Analytics Dashboard Update", "Update analytics dashboard with new metrics", "todo", "low", "olivia@company.com", "2024-01-14 09:00:00", "2024-01-21", "Analytics", "analytics,dashboard", "2024-01-14 09:00:00", "task_019"),
        (20, "Weekly Report Generation", "Generate weekly progress report for stakeholders", "in_progress", "low", "peter@company.com", "2024-01-14 14:00:00", "2024-01-14", "Reporting", "report,weekly", "2024-01-14 14:00:00", "task_020"),
    ]
    
    # Insert all tasks (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("INSERT OR IGNORE INTO kanban_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_tasks + noise_tasks)
    
    conn.commit()
    conn.close()

def create_github_database():
    """Create and populate GitHub database for Test Case 2"""
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
            labels TEXT,
            priority TEXT,
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
        (1, "company/security", "john@company.com", "Fix critical security vulnerability in authentication", "sec001", "main", 5, 25, 12, "2024-01-08 11:30:00", "commit_001"),
        (2, "company/architecture", "john@company.com", "Implement Q1 roadmap architecture changes", "arch001", "feature/q1-roadmap", 8, 45, 20, "2024-01-09 15:30:00", "commit_002"),
    ]
    
    noise_commits = [
        (3, "company/frontend", "alice@company.com", "Update UI components styling", "ui001", "main", 3, 15, 8, "2024-01-07 10:00:00", "commit_003"),
        (4, "company/backend", "bob@company.com", "Add new API endpoint for user management", "api001", "feature/user-mgmt", 4, 30, 5, "2024-01-08 14:00:00", "commit_004"),
        (5, "company/docs", "charlie@company.com", "Update README with installation instructions", "doc001", "main", 1, 10, 2, "2024-01-09 09:00:00", "commit_005"),
        (6, "company/tests", "diana@company.com", "Add unit tests for payment module", "test001", "feature/tests", 2, 25, 0, "2024-01-10 11:00:00", "commit_006"),
        (7, "company/infrastructure", "eve@company.com", "Update Docker configuration", "docker001", "main", 2, 8, 3, "2024-01-11 13:00:00", "commit_007"),
        (8, "company/mobile", "frank@company.com", "Fix mobile app navigation issue", "mobile001", "feature/mobile-fix", 3, 12, 6, "2024-01-12 15:00:00", "commit_008"),
    ]
    
    important_prs = [
        (1, "company/security", "Critical Security Fix", "Fixes critical security vulnerability in authentication system", "john@company.com", "merged", "main", "fix/security-vuln", "2024-01-08 11:00:00", "2024-01-08 12:00:00", "2024-01-08 12:30:00", "pr_001"),
        (2, "company/architecture", "Q1 Roadmap Implementation", "Implements architecture changes from Q1 technical roadmap", "john@company.com", "open", "main", "feature/q1-roadmap", "2024-01-09 15:00:00", "2024-01-09 16:00:00", None, "pr_002"),
    ]
    
    noise_prs = [
        (3, "company/frontend", "UI Component Updates", "Updates styling for various UI components", "alice@company.com", "merged", "main", "feature/ui-updates", "2024-01-07 09:00:00", "2024-01-07 10:00:00", "2024-01-07 10:30:00", "pr_003"),
        (4, "company/backend", "User Management API", "Adds new API endpoints for user management", "bob@company.com", "open", "main", "feature/user-api", "2024-01-08 13:00:00", "2024-01-08 14:00:00", None, "pr_004"),
    ]
    
    important_issues = [
        (1, "company/security", "Critical Security Vulnerability", "Authentication system has critical security vulnerability requiring immediate attention", "john@company.com", "closed", "security,critical,urgent", "high", "2024-01-08 10:00:00", "2024-01-08 12:30:00", "2024-01-08 12:30:00", "issue_001"),
        (2, "company/performance", "Production Performance Degradation", "Production system experiencing severe performance issues affecting customers", "john@company.com", "open", "performance,production,urgent", "high", "2024-01-10 08:00:00", "2024-01-10 09:00:00", None, "issue_002"),
    ]
    
    noise_issues = [
        (3, "company/frontend", "Button hover effect not working", "The hover effect on submit button is not displaying correctly", "alice@company.com", "open", "ui,bug", "low", "2024-01-07 15:00:00", "2024-01-07 16:00:00", None, "issue_003"),
    ]
    
    important_reviews = [
        (1, "company/security", 1, "john@company.com", "This security fix looks good. The authentication logic is now properly secured.", "src/auth.py", 45, "2024-01-08 12:00:00", "approved", "review_001"),
    ]
    
    noise_reviews = [
        (2, "company/frontend", 3, "alice@company.com", "UI updates look great! Consider adding some animations.", "components/Button.js", 12, "2024-01-07 10:30:00", "approved", "review_002"),
    ]
    
    # Insert data (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("INSERT OR IGNORE INTO commits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_commits + noise_commits)
    cursor.executemany("INSERT OR IGNORE INTO pull_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_prs + noise_prs)
    cursor.executemany("INSERT OR IGNORE INTO issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_issues + noise_issues)
    cursor.executemany("INSERT OR IGNORE INTO code_reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_reviews + noise_reviews)
    
    conn.commit()
    conn.close()

def main():
    """Main function to create all databases for Test Case 2"""
    
    create_email_database()
    create_calendar_database()
    create_slack_database()
    create_kanban_database()
    create_github_database()
    

if __name__ == "__main__":
    main()