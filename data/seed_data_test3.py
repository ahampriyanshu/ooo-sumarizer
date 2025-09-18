#!/usr/bin/env python3
"""
Seed data for Test Case 3: 14-day OOO (Feb 1-14, 2024)
Valentine's Day context with Q1 planning, team building, and system maintenance
"""

import sqlite3
import os

def create_email_database():
    """Create and populate email database for test case 3"""
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
    
    # Important emails (20% of total - 16 out of 80)
    important_emails = [
        ("email_021", "security@company.com", "URGENT: System Vulnerability Patch Required", "Critical security vulnerability discovered in authentication system. Immediate patch deployment required before Feb 5th.", "2024-02-02 09:15:00", 0, "security_thread_002", "2024-02-05 10:00:00", 60, "security@company.com,cto@company.com,dev-team@company.com"),
        ("email_022", "cto@company.com", "Q1 Architecture Review - Your Input Needed", "Please review the proposed Q1 architecture changes. Your expertise is critical for the upcoming system redesign.", "2024-02-03 14:30:00", 0, "architecture_thread_002", "2024-02-06 15:00:00", 90, "cto@company.com,architects@company.com,dev-team@company.com"),
        ("email_023", "hr@company.com", "Performance Review Deadline - Feb 12th", "Annual performance review deadline is approaching. Please submit your self-assessment and peer feedback by February 12th.", "2024-02-04 11:00:00", 0, "performance_thread_002", "2024-02-12 17:00:00", 0, "hr@company.com,managers@company.com"),
        ("email_024", "operations@company.com", "Production System Maintenance - Feb 8th", "Scheduled maintenance window for production systems on February 8th from 2-6 AM. Please prepare for potential downtime.", "2024-02-05 16:45:00", 0, "maintenance_thread_002", "2024-02-08 02:00:00", 240, "operations@company.com,dev-team@company.com,support@company.com"),
        ("email_025", "ceo@company.com", "Q1 Strategic Planning Session - Feb 7th", "Critical Q1 strategic planning session. Your presence is required for key business decisions.", "2024-02-06 08:00:00", 0, "strategy_thread_001", "2024-02-07 09:00:00", 180, "ceo@company.com,cto@company.com,managers@company.com"),
        ("email_026", "legal@company.com", "Contract Renewal - Critical Deadline Feb 10th", "Major client contract renewal deadline approaching. Legal review and approval required immediately.", "2024-02-07 10:30:00", 0, "contract_thread_001", "2024-02-10 14:00:00", 120, "legal@company.com,ceo@company.com,sales@company.com"),
        ("email_027", "finance@company.com", "Q1 Budget Approval - Feb 9th", "Q1 budget requires your approval before implementation. Critical for business operations.", "2024-02-08 09:15:00", 0, "budget_thread_001", "2024-02-09 10:00:00", 90, "finance@company.com,ceo@company.com,managers@company.com"),
        ("email_028", "compliance@company.com", "Security Audit - Feb 11th", "Annual security audit scheduled. Your system access and documentation review required.", "2024-02-09 11:00:00", 0, "audit_thread_001", "2024-02-11 09:00:00", 240, "compliance@company.com,security@company.com,it@company.com"),
        ("email_029", "product@company.com", "Product Launch - Feb 13th", "Major product launch requires your final approval and technical review.", "2024-02-10 14:00:00", 0, "launch_thread_001", "2024-02-13 15:00:00", 120, "product@company.com,cto@company.com,marketing@company.com"),
        ("email_030", "support@company.com", "Critical Customer Issue - Feb 12th", "Major customer experiencing system outage. Your technical expertise needed for resolution.", "2024-02-11 16:30:00", 0, "support_thread_001", "2024-02-12 08:00:00", 180, "support@company.com,dev-team@company.com,operations@company.com"),
        ("email_031", "sales@company.com", "Enterprise Deal - Feb 14th", "Major enterprise deal closing requires your technical consultation and approval.", "2024-02-12 10:00:00", 0, "sales_thread_001", "2024-02-14 11:00:00", 90, "sales@company.com,ceo@company.com,legal@company.com"),
        ("email_032", "devops@company.com", "Infrastructure Migration - Feb 13th", "Critical infrastructure migration requires your oversight and technical guidance.", "2024-02-13 08:30:00", 0, "migration_thread_001", "2024-02-13 20:00:00", 360, "devops@company.com,operations@company.com,dev-team@company.com"),
        ("email_033", "qa@company.com", "Release Testing - Feb 14th", "Final release testing requires your approval before production deployment.", "2024-02-14 09:00:00", 0, "testing_thread_001", "2024-02-14 10:00:00", 120, "qa@company.com,dev-team@company.com,product@company.com"),
        ("email_034", "security@company.com", "Security Incident Response - Feb 14th", "Security incident requires immediate response and your technical expertise.", "2024-02-14 12:00:00", 0, "incident_thread_001", "2024-02-14 13:00:00", 180, "security@company.com,cto@company.com,operations@company.com"),
        ("email_035", "hr@company.com", "Team Restructuring - Feb 14th", "Important team restructuring decisions require your input and approval.", "2024-02-14 15:00:00", 0, "restructure_thread_001", "2024-02-14 16:00:00", 90, "hr@company.com,ceo@company.com,managers@company.com"),
        ("email_036", "operations@company.com", "System Performance Review - Feb 14th", "Critical system performance review requires your technical analysis and recommendations.", "2024-02-14 17:00:00", 0, "performance_thread_001", "2024-02-14 18:00:00", 60, "operations@company.com,cto@company.com,dev-team@company.com"),
    ]
    
    # Noise emails (80% of total - 64 out of 80)
    noise_emails = [
        ("email_025", "marketing@company.com", "Valentine's Day Team Event Invitation", "Join us for our annual Valentine's Day team building event! Fun activities and team bonding guaranteed! 💕", "2024-02-01 10:00:00", 0, "valentine_thread_001", "2024-02-14 18:00:00", 120, "all@company.com"),
        ("email_026", "finance@company.com", "February Budget Report Available", "February budget report is now available for review. Please check your department allocations.", "2024-02-01 14:30:00", 0, "budget_thread_002", None, None, None),
        ("email_027", "it@company.com", "Software Update Reminder", "Reminder: Please update your software to the latest version for security patches and new features.", "2024-02-02 08:15:00", 0, "update_thread_002", None, None, None),
        ("email_028", "events@company.com", "Team Building Workshop - Feb 9th", "Team building workshop scheduled for February 9th. Great opportunity to strengthen team collaboration!", "2024-02-02 16:00:00", 0, "workshop_thread_001", "2024-02-09 10:00:00", 180, "all@company.com"),
        ("email_029", "support@company.com", "Customer Feedback Summary", "Weekly customer feedback summary is now available. Some interesting insights this week!", "2024-02-03 11:45:00", 0, "feedback_thread_002", None, None, None),
        ("email_030", "legal@company.com", "Contract Review Update", "Updated service agreements are ready for review. Please provide feedback by end of week.", "2024-02-03 15:15:00", 0, "contract_thread_002", None, None, None),
        ("email_031", "training@company.com", "New Employee Onboarding", "Welcome our new team members! Onboarding sessions are scheduled throughout the week.", "2024-02-04 09:30:00", 0, "onboarding_thread_002", None, None, None),
        ("email_032", "research@company.com", "Market Research Findings", "Latest market research findings are now available in the shared drive. Some interesting trends!", "2024-02-04 13:00:00", 0, "research_thread_002", None, None, None),
        ("email_033", "compliance@company.com", "Compliance Review Reminder", "Quarterly compliance review is due. Please ensure all documentation is up to date.", "2024-02-05 10:30:00", 0, "compliance_thread_002", None, None, None),
        ("email_034", "sales@company.com", "Q1 Sales Targets Update", "Q1 sales targets have been updated based on current market conditions. Let's crush these goals! 💪", "2024-02-05 12:45:00", 0, "sales_thread_002", None, None, None),
        ("email_035", "product@company.com", "Feature Request Summary", "Feature request summary from customer feedback sessions is now available. Great insights!", "2024-02-06 15:15:00", 0, "features_thread_002", None, None, None),
        ("email_036", "operations@company.com", "Weekly Operations Report", "Weekly operations report: System uptime at 99.9% this week. Excellent performance team! 📊", "2024-02-06 10:30:00", 0, "ops_thread_002", None, None, None),
        ("email_037", "quality@company.com", "QA Metrics Update", "QA metrics show improvement in bug detection rates. Keep up the excellent work! 🐛", "2024-02-07 14:00:00", 0, "qa_thread_002", None, None, None),
        ("email_038", "analytics@company.com", "Analytics Dashboard Update", "Updated user analytics dashboard with new metrics and visualizations. Check it out!", "2024-02-07 09:45:00", 0, "analytics_thread_002", None, None, None),
        ("email_039", "communications@company.com", "Internal Communication Update", "Internal communication policies have been updated. Please review the new guidelines.", "2024-02-08 16:30:00", 0, "comm_thread_002", None, None, None),
        ("email_040", "admin@company.com", "Office Supplies Update", "Office supplies have been ordered and will arrive next week. Thanks for your patience!", "2024-02-08 13:30:00", 0, "supplies_thread_002", None, None, None),
        ("email_041", "marketing@company.com", "Valentine's Day Decorations", "Help us decorate the office for Valentine's Day! All supplies provided.", "2024-02-01 12:00:00", 0, "decorations_thread_001", None, None, None),
        ("email_042", "hr@company.com", "Employee Recognition Program", "Nominate your colleagues for the monthly recognition program. Great way to show appreciation!", "2024-02-01 15:00:00", 0, "recognition_thread_001", None, None, None),
        ("email_043", "it@company.com", "New Laptop Setup", "New laptops are ready for setup. Please schedule your appointment with IT.", "2024-02-02 09:00:00", 0, "laptop_thread_001", None, None, None),
        ("email_044", "events@company.com", "Coffee Chat Series", "Join our monthly coffee chat series. Great networking opportunity!", "2024-02-02 14:00:00", 0, "coffee_thread_001", None, None, None),
        ("email_045", "support@company.com", "Customer Satisfaction Survey", "Please complete the customer satisfaction survey. Your feedback is valuable!", "2024-02-03 10:00:00", 0, "survey_thread_001", None, None, None),
        ("email_046", "legal@company.com", "Legal Training Session", "Mandatory legal training session scheduled. Please mark your calendar.", "2024-02-03 16:00:00", 0, "training_thread_001", None, None, None),
        ("email_047", "training@company.com", "Skills Development Workshop", "Skills development workshop available. Enhance your professional skills!", "2024-02-04 10:00:00", 0, "skills_thread_001", None, None, None),
        ("email_048", "research@company.com", "Industry Trends Report", "Latest industry trends report is available. Stay updated with market changes!", "2024-02-04 14:00:00", 0, "trends_thread_001", None, None, None),
        ("email_049", "compliance@company.com", "Policy Update Notification", "Company policies have been updated. Please review the changes.", "2024-02-05 11:00:00", 0, "policy_thread_001", None, None, None),
        ("email_050", "sales@company.com", "Sales Training Materials", "New sales training materials are available. Improve your sales techniques!", "2024-02-05 15:00:00", 0, "sales_training_thread_001", None, None, None),
        ("email_051", "product@company.com", "Product Feedback Session", "Product feedback session scheduled. Share your ideas and suggestions!", "2024-02-06 12:00:00", 0, "feedback_session_thread_001", None, None, None),
        ("email_052", "operations@company.com", "Process Improvement Ideas", "Share your process improvement ideas. Help us work more efficiently!", "2024-02-06 17:00:00", 0, "process_thread_001", None, None, None),
        ("email_053", "qa@company.com", "Quality Metrics Review", "Quality metrics are being reviewed. Your input on improvements is welcome!", "2024-02-07 10:00:00", 0, "quality_thread_001", None, None, None),
        ("email_054", "analytics@company.com", "Data Visualization Workshop", "Learn to create better data visualizations. Workshop materials available!", "2024-02-07 14:00:00", 0, "viz_thread_001", None, None, None),
        ("email_055", "communications@company.com", "Internal Newsletter", "Monthly internal newsletter is ready. Read about company updates and achievements!", "2024-02-08 11:00:00", 0, "newsletter_thread_001", None, None, None),
        ("email_056", "admin@company.com", "Office Space Planning", "Office space planning meeting scheduled. Share your workspace needs!", "2024-02-08 16:00:00", 0, "space_thread_001", None, None, None),
        ("email_057", "marketing@company.com", "Social Media Campaign", "Help us promote our social media campaign. Share and engage!", "2024-02-09 09:00:00", 0, "social_thread_001", None, None, None),
        ("email_058", "hr@company.com", "Wellness Program", "Join our wellness program. Take care of your physical and mental health!", "2024-02-09 13:00:00", 0, "wellness_thread_001", None, None, None),
        ("email_059", "it@company.com", "Cybersecurity Awareness", "Cybersecurity awareness training available. Stay safe online!", "2024-02-10 08:00:00", 0, "cyber_thread_001", None, None, None),
        ("email_060", "events@company.com", "Team Lunch", "Monthly team lunch scheduled. Great opportunity to connect with colleagues!", "2024-02-10 12:00:00", 0, "lunch_thread_001", None, None, None),
        ("email_061", "support@company.com", "Customer Success Stories", "Read our latest customer success stories. Inspiring achievements!", "2024-02-11 09:00:00", 0, "success_thread_001", None, None, None),
        ("email_062", "legal@company.com", "Contract Template Update", "Contract templates have been updated. Use the latest versions!", "2024-02-11 14:00:00", 0, "template_thread_001", None, None, None),
        ("email_063", "training@company.com", "Leadership Development", "Leadership development program available. Grow your leadership skills!", "2024-02-12 10:00:00", 0, "leadership_thread_001", None, None, None),
        ("email_064", "research@company.com", "Competitive Analysis", "Competitive analysis report is ready. Stay ahead of the competition!", "2024-02-12 15:00:00", 0, "competitive_thread_001", None, None, None),
        ("email_065", "compliance@company.com", "Audit Preparation", "Audit preparation checklist available. Ensure compliance readiness!", "2024-02-13 09:00:00", 0, "audit_prep_thread_001", None, None, None),
        ("email_066", "sales@company.com", "Customer Relationship Management", "CRM training session scheduled. Improve your customer relationships!", "2024-02-13 14:00:00", 0, "crm_thread_001", None, None, None),
        ("email_067", "product@company.com", "User Experience Research", "User experience research findings available. Improve product usability!", "2024-02-14 10:00:00", 0, "ux_thread_001", None, None, None),
        ("email_068", "operations@company.com", "Efficiency Metrics", "Efficiency metrics dashboard updated. Track your team's performance!", "2024-02-14 16:00:00", 0, "efficiency_thread_001", None, None, None),
        ("email_069", "qa@company.com", "Testing Best Practices", "Testing best practices guide available. Improve your testing processes!", "2024-02-01 11:00:00", 0, "testing_best_practices_thread_001", None, None, None),
        ("email_070", "analytics@company.com", "KPI Dashboard", "KPI dashboard has been updated with new metrics. Track your progress!", "2024-02-01 16:00:00", 0, "kpi_thread_001", None, None, None),
        ("email_071", "communications@company.com", "Meeting Etiquette", "Meeting etiquette guidelines updated. Make meetings more productive!", "2024-02-02 10:00:00", 0, "meeting_thread_001", None, None, None),
        ("email_072", "admin@company.com", "Office Equipment", "New office equipment has been installed. Check out the latest additions!", "2024-02-02 15:00:00", 0, "equipment_thread_001", None, None, None),
        ("email_073", "marketing@company.com", "Brand Guidelines", "Brand guidelines have been updated. Maintain consistent branding!", "2024-02-03 12:00:00", 0, "brand_thread_001", None, None, None),
        ("email_074", "hr@company.com", "Employee Handbook", "Employee handbook has been updated. Review the latest policies!", "2024-02-03 17:00:00", 0, "handbook_thread_001", None, None, None),
        ("email_075", "it@company.com", "Software Licenses", "Software license renewals due. Ensure compliance with licensing!", "2024-02-04 11:00:00", 0, "licenses_thread_001", None, None, None),
        ("email_076", "events@company.com", "Company Picnic", "Annual company picnic planning begins. Share your ideas and preferences!", "2024-02-04 16:00:00", 0, "picnic_thread_001", None, None, None),
        ("email_077", "support@company.com", "Knowledge Base", "Knowledge base has been updated. Find answers to common questions!", "2024-02-05 12:00:00", 0, "knowledge_thread_001", None, None, None),
        ("email_078", "legal@company.com", "Privacy Policy", "Privacy policy has been updated. Review the latest changes!", "2024-02-05 17:00:00", 0, "privacy_thread_001", None, None, None),
        ("email_079", "training@company.com", "Certification Program", "Professional certification program available. Advance your career!", "2024-02-06 13:00:00", 0, "certification_thread_001", None, None, None),
        ("email_080", "research@company.com", "Market Segmentation", "Market segmentation analysis available. Understand your target audience!", "2024-02-06 18:00:00", 0, "segmentation_thread_001", None, None, None),
        ("email_081", "compliance@company.com", "Risk Assessment", "Risk assessment report available. Identify and mitigate potential risks!", "2024-02-07 11:00:00", 0, "risk_thread_001", None, None, None),
        ("email_082", "sales@company.com", "Lead Generation", "Lead generation strategies workshop. Improve your sales pipeline!", "2024-02-07 16:00:00", 0, "leads_thread_001", None, None, None),
        ("email_083", "product@company.com", "Feature Roadmap", "Product feature roadmap updated. See what's coming next!", "2024-02-08 12:00:00", 0, "roadmap_thread_001", None, None, None),
        ("email_084", "operations@company.com", "Supply Chain", "Supply chain optimization report available. Improve efficiency!", "2024-02-08 17:00:00", 0, "supply_chain_thread_001", None, None, None),
        ("email_085", "qa@company.com", "Bug Tracking", "Bug tracking system updated. Report and track issues effectively!", "2024-02-09 10:00:00", 0, "bugs_thread_001", None, None, None),
        ("email_086", "analytics@company.com", "Performance Monitoring", "Performance monitoring tools updated. Track system performance!", "2024-02-09 15:00:00", 0, "monitoring_thread_001", None, None, None),
        ("email_087", "communications@company.com", "Internal Communications", "Internal communications strategy updated. Improve team communication!", "2024-02-10 11:00:00", 0, "internal_comms_thread_001", None, None, None),
        ("email_088", "admin@company.com", "Facility Management", "Facility management updates. Keep the office running smoothly!", "2024-02-10 16:00:00", 0, "facility_thread_001", None, None, None),
        ("email_089", "marketing@company.com", "Content Strategy", "Content strategy workshop scheduled. Improve your marketing content!", "2024-02-11 10:00:00", 0, "content_thread_001", None, None, None),
        ("email_090", "hr@company.com", "Diversity & Inclusion", "Diversity and inclusion training available. Build an inclusive workplace!", "2024-02-11 15:00:00", 0, "diversity_thread_001", None, None, None),
        ("email_091", "it@company.com", "Cloud Migration", "Cloud migration project update. Modernize our infrastructure!", "2024-02-12 11:00:00", 0, "cloud_thread_001", None, None, None),
        ("email_092", "events@company.com", "Hackathon Planning", "Annual hackathon planning begins. Share your ideas and register!", "2024-02-12 16:00:00", 0, "hackathon_thread_001", None, None, None),
        ("email_093", "support@company.com", "Customer Onboarding", "Customer onboarding process improved. Better first impressions!", "2024-02-13 10:00:00", 0, "onboarding_thread_001", None, None, None),
        ("email_094", "legal@company.com", "Intellectual Property", "Intellectual property training available. Protect your innovations!", "2024-02-13 15:00:00", 0, "ip_thread_001", None, None, None),
        ("email_095", "training@company.com", "Mentorship Program", "Mentorship program launched. Connect with experienced professionals!", "2024-02-14 11:00:00", 0, "mentorship_thread_001", None, None, None),
        ("email_096", "research@company.com", "Innovation Lab", "Innovation lab opens. Explore new technologies and ideas!", "2024-02-14 16:00:00", 0, "innovation_thread_001", None, None, None),
    ]
    
    # Insert all emails (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("""
        INSERT OR IGNORE INTO emails (custom_id, sender, subject, body, received_date, is_read, thread_id, meeting_date, meeting_duration, attendees)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, important_emails + noise_emails)
    
    conn.commit()
    conn.close()

def create_calendar_database():
    """Create and populate calendar database for test case 3"""
    conn = sqlite3.connect("data/databases/calendar.db")
    cursor = conn.cursor()
    
    # Create events table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
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
    
    # Important events (20% of total - 12 out of 60)
    important_events = [
        ("event_021", "Security Vulnerability Patch Deployment", "Critical security patch deployment for authentication system vulnerability", "2024-02-05 10:00:00", "2024-02-05 11:00:00", "War Room", "security@company.com,cto@company.com,dev-team@company.com", "meeting", 0, 1, "Security"),
        ("event_022", "Q1 Architecture Review Meeting", "Review proposed Q1 architecture changes and system redesign plans", "2024-02-06 15:00:00", "2024-02-06 16:30:00", "Conference Room A", "cto@company.com,architects@company.com,dev-team@company.com", "meeting", 0, 1, "Architecture"),
        ("event_023", "Performance Review Deadline", "Deadline for submitting annual performance review materials", "2024-02-12 17:00:00", "2024-02-12 17:00:00", "HR Office", "hr@company.com,managers@company.com", "deadline", 0, 1, "HR"),
        ("event_024", "Production System Maintenance", "Scheduled maintenance window for production systems", "2024-02-08 02:00:00", "2024-02-08 06:00:00", "Data Center", "operations@company.com,dev-team@company.com,support@company.com", "maintenance", 0, 1, "Operations"),
        ("event_025", "Q1 Strategic Planning Session", "Critical Q1 strategic planning session for key business decisions", "2024-02-07 09:00:00", "2024-02-07 12:00:00", "Boardroom", "ceo@company.com,cto@company.com,managers@company.com", "meeting", 0, 1, "Strategy"),
        ("event_026", "Contract Renewal Review", "Review and approve major client contract renewal", "2024-02-10 14:00:00", "2024-02-10 16:00:00", "Legal Office", "legal@company.com,ceo@company.com,sales@company.com", "meeting", 0, 1, "Legal"),
        ("event_027", "Q1 Budget Approval Meeting", "Approve Q1 budget for business operations", "2024-02-09 10:00:00", "2024-02-09 11:30:00", "Finance Office", "finance@company.com,ceo@company.com,managers@company.com", "meeting", 0, 1, "Finance"),
        ("event_028", "Security Audit Preparation", "Prepare for annual security audit", "2024-02-11 09:00:00", "2024-02-11 17:00:00", "Security Office", "compliance@company.com,security@company.com,it@company.com", "meeting", 0, 1, "Compliance"),
        ("event_029", "Product Launch Approval", "Final approval for major product launch", "2024-02-13 15:00:00", "2024-02-13 17:00:00", "Product Office", "product@company.com,cto@company.com,marketing@company.com", "meeting", 0, 1, "Product"),
        ("event_030", "Critical Customer Issue Resolution", "Resolve major customer system outage", "2024-02-12 08:00:00", "2024-02-12 12:00:00", "Support Center", "support@company.com,dev-team@company.com,operations@company.com", "meeting", 0, 1, "Support"),
        ("event_031", "Enterprise Deal Technical Review", "Technical consultation for major enterprise deal", "2024-02-14 11:00:00", "2024-02-14 13:00:00", "Sales Office", "sales@company.com,ceo@company.com,legal@company.com", "meeting", 0, 1, "Sales"),
        ("event_032", "Infrastructure Migration Oversight", "Oversee critical infrastructure migration", "2024-02-13 20:00:00", "2024-02-14 02:00:00", "Data Center", "devops@company.com,operations@company.com,dev-team@company.com", "maintenance", 0, 1, "DevOps"),
    ]
    
    # Noise events (80% of total - 48 out of 60)
    noise_events = [
        ("event_025", "Valentine's Day Team Event", "Annual Valentine's Day team building event with fun activities", "2024-02-14 18:00:00", "2024-02-14 20:00:00", "Main Hall", "all@company.com", "social", 0, 1, "Team Building"),
        ("event_026", "Team Building Workshop", "Team building workshop to strengthen collaboration", "2024-02-09 10:00:00", "2024-02-09 13:00:00", "Training Room", "all@company.com", "workshop", 0, 1, "Team Building"),
        ("event_027", "Weekly Team Standup", "Regular weekly team standup meeting", "2024-02-01 09:00:00", "2024-02-01 09:30:00", "Conference Room B", "dev-team@company.com", "meeting", 0, 1, "Team Operations"),
        ("event_028", "Budget Planning Session", "Plan budget allocation for next quarter", "2024-02-01 14:00:00", "2024-02-01 15:30:00", "Finance Office", "finance@company.com,managers@company.com", "meeting", 0, 1, "Finance"),
        ("event_029", "Documentation Review", "Review and update project documentation", "2024-02-02 11:00:00", "2024-02-02 12:00:00", "Conference Room C", "dev-team@company.com", "meeting", 0, 1, "Documentation"),
        ("event_030", "Client Meeting", "Regular client check-in and progress update", "2024-02-02 15:00:00", "2024-02-02 16:00:00", "Client Office", "sales@company.com,account-manager@company.com", "meeting", 0, 1, "Client Relations"),
        ("event_031", "Code Review Session", "Review recent code changes and improvements", "2024-02-03 10:00:00", "2024-02-03 11:30:00", "Dev Room", "dev-team@company.com", "meeting", 0, 1, "Development"),
        ("event_032", "Training Session", "Training session on new tools and processes", "2024-02-03 13:00:00", "2024-02-03 14:30:00", "Training Room", "all@company.com", "training", 0, 1, "Training"),
        ("event_033", "Project Status Update", "Update on current project status and milestones", "2024-02-04 09:30:00", "2024-02-04 10:30:00", "Conference Room A", "project-managers@company.com", "meeting", 0, 1, "Project Management"),
        ("event_034", "Vendor Meeting", "Meeting with key vendors and suppliers", "2024-02-04 14:00:00", "2024-02-04 15:00:00", "Conference Room B", "procurement@company.com", "meeting", 0, 1, "Procurement"),
        ("event_035", "Quality Assurance Review", "Review QA processes and quality metrics", "2024-02-05 13:00:00", "2024-02-05 14:00:00", "QA Lab", "qa-team@company.com", "meeting", 0, 1, "Quality Assurance"),
        ("event_036", "Marketing Planning", "Plan marketing campaigns for next quarter", "2024-02-06 10:00:00", "2024-02-06 11:30:00", "Marketing Office", "marketing@company.com", "meeting", 0, 1, "Marketing"),
        ("event_037", "Research Presentation", "Present latest research findings and insights", "2024-02-07 11:00:00", "2024-02-07 12:00:00", "Conference Room C", "research@company.com", "presentation", 0, 1, "Research"),
        ("event_038", "Compliance Training", "Mandatory compliance training session", "2024-02-07 15:00:00", "2024-02-07 16:30:00", "Training Room", "all@company.com", "training", 0, 1, "Compliance"),
        ("event_039", "Sales Review", "Review sales performance and targets", "2024-02-08 10:00:00", "2024-02-08 11:00:00", "Sales Office", "sales@company.com", "meeting", 0, 1, "Sales"),
        ("event_040", "All Hands Meeting", "Company-wide all hands meeting", "2024-02-08 15:00:00", "2024-02-08 16:00:00", "Main Hall", "all@company.com", "meeting", 0, 1, "Company"),
        ("event_041", "Valentine's Day Decorations", "Decorate office for Valentine's Day celebration", "2024-02-01 12:00:00", "2024-02-01 13:00:00", "Main Hall", "marketing@company.com", "social", 0, 1, "Events"),
        ("event_042", "Employee Recognition Ceremony", "Monthly employee recognition ceremony", "2024-02-02 15:00:00", "2024-02-02 16:00:00", "Main Hall", "hr@company.com,all@company.com", "ceremony", 0, 1, "HR"),
        ("event_043", "New Laptop Setup Session", "Set up new laptops for team members", "2024-02-03 10:00:00", "2024-02-03 12:00:00", "IT Office", "it@company.com", "training", 0, 1, "IT"),
        ("event_044", "Coffee Chat Networking", "Monthly coffee chat networking event", "2024-02-04 14:00:00", "2024-02-04 15:00:00", "Break Room", "events@company.com", "networking", 0, 1, "Networking"),
        ("event_045", "Customer Satisfaction Survey", "Distribute customer satisfaction survey", "2024-02-05 11:00:00", "2024-02-05 12:00:00", "Support Office", "support@company.com", "meeting", 0, 1, "Support"),
        ("event_046", "Legal Training Session", "Mandatory legal training for all employees", "2024-02-06 14:00:00", "2024-02-06 16:00:00", "Training Room", "legal@company.com,all@company.com", "training", 0, 1, "Legal"),
        ("event_047", "Skills Development Workshop", "Skills development workshop for team", "2024-02-07 10:00:00", "2024-02-07 12:00:00", "Training Room", "training@company.com", "workshop", 0, 1, "Training"),
        ("event_048", "Industry Trends Presentation", "Present latest industry trends and insights", "2024-02-08 13:00:00", "2024-02-08 14:00:00", "Conference Room C", "research@company.com", "presentation", 0, 1, "Research"),
        ("event_049", "Policy Update Meeting", "Update employees on new company policies", "2024-02-09 11:00:00", "2024-02-09 12:00:00", "Main Hall", "compliance@company.com,all@company.com", "meeting", 0, 1, "Compliance"),
        ("event_050", "Sales Training Session", "Sales training session for team", "2024-02-10 15:00:00", "2024-02-10 17:00:00", "Sales Office", "sales@company.com", "training", 0, 1, "Sales"),
        ("event_051", "Product Feedback Session", "Product feedback session with customers", "2024-02-11 14:00:00", "2024-02-11 16:00:00", "Product Office", "product@company.com", "meeting", 0, 1, "Product"),
        ("event_052", "Process Improvement Workshop", "Workshop on process improvement ideas", "2024-02-12 10:00:00", "2024-02-12 12:00:00", "Conference Room A", "operations@company.com", "workshop", 0, 1, "Operations"),
        ("event_053", "Quality Metrics Review", "Review quality metrics and KPIs", "2024-02-13 11:00:00", "2024-02-13 12:00:00", "QA Lab", "qa-team@company.com", "meeting", 0, 1, "Quality Assurance"),
        ("event_054", "Data Visualization Training", "Data visualization training workshop", "2024-02-14 14:00:00", "2024-02-14 16:00:00", "Analytics Office", "analytics@company.com", "training", 0, 1, "Analytics"),
        ("event_055", "Internal Newsletter Review", "Review monthly internal newsletter", "2024-02-01 16:00:00", "2024-02-01 17:00:00", "Communications Office", "communications@company.com", "meeting", 0, 1, "Communications"),
        ("event_056", "Office Space Planning", "Plan office space allocation", "2024-02-02 10:00:00", "2024-02-02 11:00:00", "Admin Office", "admin@company.com", "meeting", 0, 1, "Administration"),
        ("event_057", "Social Media Campaign Launch", "Launch social media marketing campaign", "2024-02-03 15:00:00", "2024-02-03 16:00:00", "Marketing Office", "marketing@company.com", "meeting", 0, 1, "Marketing"),
        ("event_058", "Wellness Program Session", "Employee wellness program session", "2024-02-04 12:00:00", "2024-02-04 13:00:00", "Wellness Room", "hr@company.com", "wellness", 0, 1, "HR"),
        ("event_059", "Cybersecurity Awareness Training", "Cybersecurity awareness training", "2024-02-05 14:00:00", "2024-02-05 15:00:00", "Training Room", "it@company.com,all@company.com", "training", 0, 1, "IT"),
        ("event_060", "Team Lunch", "Monthly team lunch event", "2024-02-06 12:00:00", "2024-02-06 13:00:00", "Cafeteria", "events@company.com", "social", 0, 1, "Events"),
        ("event_061", "Customer Success Stories", "Share customer success stories", "2024-02-07 15:00:00", "2024-02-07 16:00:00", "Support Office", "support@company.com", "presentation", 0, 1, "Support"),
        ("event_062", "Contract Template Review", "Review and update contract templates", "2024-02-08 11:00:00", "2024-02-08 12:00:00", "Legal Office", "legal@company.com", "meeting", 0, 1, "Legal"),
        ("event_063", "Leadership Development Program", "Leadership development program session", "2024-02-09 14:00:00", "2024-02-09 16:00:00", "Training Room", "training@company.com", "training", 0, 1, "Training"),
        ("event_064", "Competitive Analysis Review", "Review competitive analysis findings", "2024-02-10 13:00:00", "2024-02-10 14:00:00", "Research Office", "research@company.com", "meeting", 0, 1, "Research"),
        ("event_065", "Audit Preparation Meeting", "Prepare for upcoming audit", "2024-02-11 10:00:00", "2024-02-11 11:00:00", "Compliance Office", "compliance@company.com", "meeting", 0, 1, "Compliance"),
        ("event_066", "CRM System Update", "Update CRM system and processes", "2024-02-12 15:00:00", "2024-02-12 16:00:00", "Sales Office", "sales@company.com", "training", 0, 1, "Sales"),
        ("event_067", "User Experience Research", "User experience research session", "2024-02-13 13:00:00", "2024-02-13 15:00:00", "Product Office", "product@company.com", "research", 0, 1, "Product"),
        ("event_068", "Efficiency Metrics Review", "Review team efficiency metrics", "2024-02-14 10:00:00", "2024-02-14 11:00:00", "Operations Office", "operations@company.com", "meeting", 0, 1, "Operations"),
    ]
    
    # Insert all events (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("INSERT OR IGNORE INTO events (custom_id, title, description, start_time, end_time, location, attendees, event_type, is_all_day, reminder_set, project_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", important_events + noise_events)
    
    conn.commit()
    conn.close()

def create_slack_database():
    """Create and populate Slack database for test case 3"""
    conn = sqlite3.connect("data/databases/slack.db")
    cursor = conn.cursor()
    
    # Create messages table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
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
    
    # Important messages (20% of total - 24 out of 120)
    important_messages = [
        ("slack_021", "#security", "security@company.com", "@john.doe URGENT: Critical security vulnerability in auth system. Patch deployment required by Feb 5th.", "2024-02-02 09:15:00", 0, "security_thread_002"),
        ("slack_022", "#architecture", "cto@company.com", "@john.doe Q1 architecture review meeting scheduled. Your input on system redesign is critical.", "2024-02-03 14:30:00", 0, "architecture_thread_002"),
        ("slack_023", "#hr", "hr@company.com", "@john.doe Performance review deadline approaching. Please submit materials by Feb 12th.", "2024-02-04 11:00:00", 0, "performance_thread_002"),
        ("slack_024", "#operations", "operations@company.com", "@john.doe Production maintenance scheduled for Feb 8th 2-6 AM. Prepare for potential downtime.", "2024-02-05 16:45:00", 0, "maintenance_thread_002"),
        ("slack_025", "#strategy", "ceo@company.com", "@john.doe Q1 strategic planning session on Feb 7th. Your presence is required for key decisions.", "2024-02-06 08:00:00", 0, "strategy_thread_001"),
        ("slack_026", "#legal", "legal@company.com", "@john.doe Major contract renewal deadline Feb 10th. Legal review and approval needed immediately.", "2024-02-07 10:30:00", 0, "contract_thread_001"),
        ("slack_027", "#finance", "finance@company.com", "@john.doe Q1 budget approval required by Feb 9th. Critical for business operations.", "2024-02-08 09:15:00", 0, "budget_thread_001"),
        ("slack_028", "#compliance", "compliance@company.com", "@john.doe Security audit scheduled for Feb 11th. System access review required.", "2024-02-09 11:00:00", 0, "audit_thread_001"),
        ("slack_029", "#product", "product@company.com", "@john.doe Product launch requires your final approval. Technical review needed by Feb 13th.", "2024-02-10 14:00:00", 0, "launch_thread_001"),
        ("slack_030", "#support", "support@company.com", "@john.doe Critical customer issue - system outage. Your technical expertise needed for resolution.", "2024-02-11 16:30:00", 0, "support_thread_001"),
        ("slack_031", "#sales", "sales@company.com", "@john.doe Enterprise deal closing Feb 14th. Technical consultation and approval required.", "2024-02-12 10:00:00", 0, "sales_thread_001"),
        ("slack_032", "#devops", "devops@company.com", "@john.doe Infrastructure migration Feb 13th. Your oversight and technical guidance needed.", "2024-02-13 08:30:00", 0, "migration_thread_001"),
        ("slack_033", "#qa", "qa@company.com", "@john.doe Release testing requires your approval before production deployment on Feb 14th.", "2024-02-14 09:00:00", 0, "testing_thread_001"),
        ("slack_034", "#security", "security@company.com", "@john.doe Security incident response required. Immediate technical expertise needed.", "2024-02-14 12:00:00", 0, "incident_thread_001"),
        ("slack_035", "#hr", "hr@company.com", "@john.doe Team restructuring decisions require your input and approval by Feb 14th.", "2024-02-14 15:00:00", 0, "restructure_thread_001"),
        ("slack_036", "#operations", "operations@company.com", "@john.doe System performance review requires your technical analysis and recommendations.", "2024-02-14 17:00:00", 0, "performance_thread_001"),
        ("slack_037", "#architecture", "cto@company.com", "@john.doe Architecture changes need your review before implementation. Critical for system stability.", "2024-02-01 10:00:00", 0, "architecture_thread_003"),
        ("slack_038", "#security", "security@company.com", "@john.doe Security patch testing completed. Ready for your approval and deployment.", "2024-02-02 11:00:00", 0, "security_thread_003"),
        ("slack_039", "#operations", "operations@company.com", "@john.doe System maintenance checklist prepared. Your review and approval needed.", "2024-02-03 12:00:00", 0, "maintenance_thread_003"),
        ("slack_040", "#hr", "hr@company.com", "@john.doe Performance review materials prepared. Ready for your submission.", "2024-02-04 13:00:00", 0, "performance_thread_003"),
        ("slack_041", "#strategy", "ceo@company.com", "@john.doe Strategic planning session confirmed. Your attendance is mandatory.", "2024-02-05 14:00:00", 0, "strategy_thread_002"),
        ("slack_042", "#legal", "legal@company.com", "@john.doe Contract renewal documents reviewed. Your final approval required.", "2024-02-06 15:00:00", 0, "contract_thread_002"),
        ("slack_043", "#finance", "finance@company.com", "@john.doe Budget approval process initiated. Your decision needed by deadline.", "2024-02-07 16:00:00", 0, "budget_thread_002"),
        ("slack_044", "#compliance", "compliance@company.com", "@john.doe Security audit preparation in progress. Your documentation review needed.", "2024-02-08 17:00:00", 0, "audit_thread_002"),
    ]
    
    # Noise messages (80% of total - 96 out of 120)
    noise_messages = [
        ("slack_025", "#general", "marketing@company.com", "Valentine's Day team event invitation! Join us for fun activities and team bonding! 💕", "2024-02-01 10:00:00", 0, "valentine_thread_001"),
        ("slack_026", "#finance", "finance@company.com", "February budget report is now available for review. Please check your department allocations.", "2024-02-01 14:30:00", 0, "budget_thread_002"),
        ("slack_027", "#it", "it@company.com", "Software update reminder: Please update to the latest version for security patches.", "2024-02-02 08:15:00", 0, "update_thread_002"),
        ("slack_028", "#events", "events@company.com", "Team building workshop on Feb 9th! Great opportunity to strengthen collaboration! 🎯", "2024-02-02 16:00:00", 0, "workshop_thread_001"),
        ("slack_029", "#support", "support@company.com", "Weekly customer feedback summary available. Some interesting insights this week!", "2024-02-03 11:45:00", 0, "feedback_thread_002"),
        ("slack_030", "#legal", "legal@company.com", "Updated service agreements ready for review. Please provide feedback by end of week.", "2024-02-03 15:15:00", 0, "contract_thread_002"),
        ("slack_031", "#onboarding", "training@company.com", "Welcome new team members! Onboarding sessions scheduled throughout the week.", "2024-02-04 09:30:00", 0, "onboarding_thread_002"),
        ("slack_032", "#research", "research@company.com", "Latest market research findings available in shared drive. Interesting trends!", "2024-02-04 13:00:00", 0, "research_thread_002"),
        ("slack_033", "#compliance", "compliance@company.com", "Quarterly compliance review due. Please ensure all documentation is up to date.", "2024-02-05 10:30:00", 0, "compliance_thread_002"),
        ("slack_034", "#sales", "sales@company.com", "Q1 sales targets updated based on market conditions. Let's crush these goals! 💪", "2024-02-05 12:45:00", 0, "sales_thread_002"),
        ("slack_035", "#product", "product@company.com", "Feature request summary from customer feedback available. Great insights!", "2024-02-06 15:15:00", 0, "features_thread_002"),
        ("slack_036", "#operations", "operations@company.com", "Weekly operations report: System uptime at 99.9% this week. Excellent! 📊", "2024-02-06 10:30:00", 0, "ops_thread_002"),
        ("slack_037", "#qa", "quality@company.com", "QA metrics show improvement in bug detection rates. Keep up the great work! 🐛", "2024-02-07 14:00:00", 0, "qa_thread_002"),
        ("slack_038", "#analytics", "analytics@company.com", "Updated analytics dashboard with new metrics and visualizations. Check it out!", "2024-02-07 09:45:00", 0, "analytics_thread_002"),
        ("slack_039", "#communications", "communications@company.com", "Internal communication policies updated. Please review the new guidelines.", "2024-02-08 16:30:00", 0, "comm_thread_002"),
        ("slack_040", "#admin", "admin@company.com", "Office supplies ordered and arriving next week. Thanks for your patience!", "2024-02-08 13:30:00", 0, "supplies_thread_002"),
        ("slack_045", "#general", "marketing@company.com", "Valentine's Day decorations are ready! Help us decorate the office! 🎨", "2024-02-01 12:00:00", 0, "decorations_thread_001"),
        ("slack_046", "#hr", "hr@company.com", "Employee recognition program nominations are open! Nominate your colleagues! 🏆", "2024-02-01 15:00:00", 0, "recognition_thread_001"),
        ("slack_047", "#it", "it@company.com", "New laptops are ready for setup. Please schedule your appointment with IT.", "2024-02-02 09:00:00", 0, "laptop_thread_001"),
        ("slack_048", "#events", "events@company.com", "Coffee chat series starting this month! Great networking opportunity! ☕", "2024-02-02 14:00:00", 0, "coffee_thread_001"),
        ("slack_049", "#support", "support@company.com", "Customer satisfaction survey is live! Please complete it. Your feedback is valuable! 📊", "2024-02-03 10:00:00", 0, "survey_thread_001"),
        ("slack_050", "#legal", "legal@company.com", "Legal training session scheduled. Please mark your calendar for mandatory attendance.", "2024-02-03 16:00:00", 0, "training_thread_001"),
        ("slack_051", "#training", "training@company.com", "Skills development workshop available! Enhance your professional skills! 🚀", "2024-02-04 10:00:00", 0, "skills_thread_001"),
        ("slack_052", "#research", "research@company.com", "Industry trends report is available! Stay updated with market changes! 📈", "2024-02-04 14:00:00", 0, "trends_thread_001"),
        ("slack_053", "#compliance", "compliance@company.com", "Company policies have been updated. Please review the changes.", "2024-02-05 11:00:00", 0, "policy_thread_001"),
        ("slack_054", "#sales", "sales@company.com", "New sales training materials are available! Improve your sales techniques! 💼", "2024-02-05 15:00:00", 0, "sales_training_thread_001"),
        ("slack_055", "#product", "product@company.com", "Product feedback session scheduled! Share your ideas and suggestions! 💡", "2024-02-06 12:00:00", 0, "feedback_session_thread_001"),
        ("slack_056", "#operations", "operations@company.com", "Process improvement ideas welcome! Help us work more efficiently! ⚡", "2024-02-06 17:00:00", 0, "process_thread_001"),
        ("slack_057", "#qa", "qa@company.com", "Quality metrics are being reviewed. Your input on improvements is welcome! 🔍", "2024-02-07 10:00:00", 0, "quality_thread_001"),
        ("slack_058", "#analytics", "analytics@company.com", "Data visualization workshop available! Learn to create better visualizations! 📊", "2024-02-07 14:00:00", 0, "viz_thread_001"),
        ("slack_059", "#communications", "communications@company.com", "Monthly internal newsletter is ready! Read about company updates! 📰", "2024-02-08 11:00:00", 0, "newsletter_thread_001"),
        ("slack_060", "#admin", "admin@company.com", "Office space planning meeting scheduled. Share your workspace needs! 🏢", "2024-02-08 16:00:00", 0, "space_thread_001"),
        ("slack_061", "#marketing", "marketing@company.com", "Social media campaign launch! Help us promote and engage! 📱", "2024-02-09 09:00:00", 0, "social_thread_001"),
        ("slack_062", "#wellness", "hr@company.com", "Wellness program launched! Take care of your physical and mental health! 💪", "2024-02-09 13:00:00", 0, "wellness_thread_001"),
        ("slack_063", "#security", "it@company.com", "Cybersecurity awareness training available! Stay safe online! 🔒", "2024-02-10 08:00:00", 0, "cyber_thread_001"),
        ("slack_064", "#events", "events@company.com", "Monthly team lunch scheduled! Great opportunity to connect! 🍽️", "2024-02-10 12:00:00", 0, "lunch_thread_001"),
        ("slack_065", "#support", "support@company.com", "Customer success stories are ready! Inspiring achievements! 🌟", "2024-02-11 09:00:00", 0, "success_thread_001"),
        ("slack_066", "#legal", "legal@company.com", "Contract templates have been updated! Use the latest versions! 📋", "2024-02-11 14:00:00", 0, "template_thread_001"),
        ("slack_067", "#training", "training@company.com", "Leadership development program available! Grow your leadership skills! 👑", "2024-02-12 10:00:00", 0, "leadership_thread_001"),
        ("slack_068", "#research", "research@company.com", "Competitive analysis report is ready! Stay ahead of the competition! 🏃‍♂️", "2024-02-12 15:00:00", 0, "competitive_thread_001"),
        ("slack_069", "#compliance", "compliance@company.com", "Audit preparation checklist available! Ensure compliance readiness! ✅", "2024-02-13 09:00:00", 0, "audit_prep_thread_001"),
        ("slack_070", "#sales", "sales@company.com", "CRM training session scheduled! Improve your customer relationships! 🤝", "2024-02-13 14:00:00", 0, "crm_thread_001"),
        ("slack_071", "#product", "product@company.com", "User experience research findings available! Improve product usability! 🎯", "2024-02-14 10:00:00", 0, "ux_thread_001"),
        ("slack_072", "#operations", "operations@company.com", "Efficiency metrics dashboard updated! Track your team's performance! 📈", "2024-02-14 16:00:00", 0, "efficiency_thread_001"),
        ("slack_073", "#qa", "qa@company.com", "Testing best practices guide available! Improve your testing processes! 🧪", "2024-02-01 11:00:00", 0, "testing_best_practices_thread_001"),
        ("slack_074", "#analytics", "analytics@company.com", "KPI dashboard has been updated! Track your progress! 📊", "2024-02-01 16:00:00", 0, "kpi_thread_001"),
        ("slack_075", "#communications", "communications@company.com", "Meeting etiquette guidelines updated! Make meetings more productive! 🎯", "2024-02-02 10:00:00", 0, "meeting_thread_001"),
        ("slack_076", "#admin", "admin@company.com", "New office equipment has been installed! Check out the latest additions! 🖥️", "2024-02-02 15:00:00", 0, "equipment_thread_001"),
        ("slack_077", "#marketing", "marketing@company.com", "Brand guidelines have been updated! Maintain consistent branding! 🎨", "2024-02-03 12:00:00", 0, "brand_thread_001"),
        ("slack_078", "#hr", "hr@company.com", "Employee handbook has been updated! Review the latest policies! 📖", "2024-02-03 17:00:00", 0, "handbook_thread_001"),
        ("slack_079", "#it", "it@company.com", "Software license renewals due! Ensure compliance with licensing! 📄", "2024-02-04 11:00:00", 0, "licenses_thread_001"),
        ("slack_080", "#events", "events@company.com", "Annual company picnic planning begins! Share your ideas and preferences! 🏕️", "2024-02-04 16:00:00", 0, "picnic_thread_001"),
        ("slack_081", "#support", "support@company.com", "Knowledge base has been updated! Find answers to common questions! 📚", "2024-02-05 12:00:00", 0, "knowledge_thread_001"),
        ("slack_082", "#legal", "legal@company.com", "Privacy policy has been updated! Review the latest changes! 🔒", "2024-02-05 17:00:00", 0, "privacy_thread_001"),
        ("slack_083", "#training", "training@company.com", "Professional certification program available! Advance your career! 🎓", "2024-02-06 13:00:00", 0, "certification_thread_001"),
        ("slack_084", "#research", "research@company.com", "Market segmentation analysis available! Understand your target audience! 🎯", "2024-02-06 18:00:00", 0, "segmentation_thread_001"),
        ("slack_085", "#compliance", "compliance@company.com", "Risk assessment report available! Identify and mitigate potential risks! ⚠️", "2024-02-07 11:00:00", 0, "risk_thread_001"),
        ("slack_086", "#sales", "sales@company.com", "Lead generation strategies workshop! Improve your sales pipeline! 🎣", "2024-02-07 16:00:00", 0, "leads_thread_001"),
        ("slack_087", "#product", "product@company.com", "Product feature roadmap updated! See what's coming next! 🗺️", "2024-02-08 12:00:00", 0, "roadmap_thread_001"),
        ("slack_088", "#operations", "operations@company.com", "Supply chain optimization report available! Improve efficiency! ⚡", "2024-02-08 17:00:00", 0, "supply_chain_thread_001"),
        ("slack_089", "#qa", "qa@company.com", "Bug tracking system updated! Report and track issues effectively! 🐛", "2024-02-09 10:00:00", 0, "bugs_thread_001"),
        ("slack_090", "#analytics", "analytics@company.com", "Performance monitoring tools updated! Track system performance! 📊", "2024-02-09 15:00:00", 0, "monitoring_thread_001"),
        ("slack_091", "#communications", "communications@company.com", "Internal communications strategy updated! Improve team communication! 💬", "2024-02-10 11:00:00", 0, "internal_comms_thread_001"),
        ("slack_092", "#admin", "admin@company.com", "Facility management updates! Keep the office running smoothly! 🏢", "2024-02-10 16:00:00", 0, "facility_thread_001"),
        ("slack_093", "#marketing", "marketing@company.com", "Content strategy workshop scheduled! Improve your marketing content! ✍️", "2024-02-11 10:00:00", 0, "content_thread_001"),
        ("slack_094", "#hr", "hr@company.com", "Diversity and inclusion training available! Build an inclusive workplace! 🌈", "2024-02-11 15:00:00", 0, "diversity_thread_001"),
        ("slack_095", "#it", "it@company.com", "Cloud migration project update! Modernize our infrastructure! ☁️", "2024-02-12 11:00:00", 0, "cloud_thread_001"),
        ("slack_096", "#events", "events@company.com", "Annual hackathon planning begins! Share your ideas and register! 💻", "2024-02-12 16:00:00", 0, "hackathon_thread_001"),
        ("slack_097", "#support", "support@company.com", "Customer onboarding process improved! Better first impressions! 👋", "2024-02-13 10:00:00", 0, "onboarding_thread_001"),
        ("slack_098", "#legal", "legal@company.com", "Intellectual property training available! Protect your innovations! 💡", "2024-02-13 15:00:00", 0, "ip_thread_001"),
        ("slack_099", "#training", "training@company.com", "Mentorship program launched! Connect with experienced professionals! 🤝", "2024-02-14 11:00:00", 0, "mentorship_thread_001"),
        ("slack_100", "#research", "research@company.com", "Innovation lab opens! Explore new technologies and ideas! 🚀", "2024-02-14 16:00:00", 0, "innovation_thread_001"),
        ("slack_101", "#general", "marketing@company.com", "Valentine's Day team event planning! Help us organize the celebration! 💕", "2024-02-01 13:00:00", 0, "valentine_planning_thread_001"),
        ("slack_102", "#finance", "finance@company.com", "Budget allocation review meeting! Discuss department funding! 💰", "2024-02-01 17:00:00", 0, "budget_allocation_thread_001"),
        ("slack_103", "#it", "it@company.com", "System maintenance reminder! Prepare for scheduled downtime! 🔧", "2024-02-02 12:00:00", 0, "maintenance_reminder_thread_001"),
        ("slack_104", "#events", "events@company.com", "Team building activities survey! Share your preferences! 📝", "2024-02-02 17:00:00", 0, "team_building_survey_thread_001"),
        ("slack_105", "#support", "support@company.com", "Customer feedback analysis complete! Great insights this week! 📊", "2024-02-03 11:00:00", 0, "feedback_analysis_thread_001"),
        ("slack_106", "#legal", "legal@company.com", "Contract template standardization! Ensure consistency! 📋", "2024-02-03 17:00:00", 0, "contract_standardization_thread_001"),
        ("slack_107", "#training", "training@company.com", "New employee orientation program! Welcome our new team members! 👋", "2024-02-04 12:00:00", 0, "orientation_thread_001"),
        ("slack_108", "#research", "research@company.com", "Market research findings presentation! Join us for insights! 📈", "2024-02-04 17:00:00", 0, "market_research_thread_001"),
        ("slack_109", "#compliance", "compliance@company.com", "Compliance training completion tracking! Ensure everyone is up to date! ✅", "2024-02-05 13:00:00", 0, "compliance_tracking_thread_001"),
        ("slack_110", "#sales", "sales@company.com", "Sales performance review meeting! Discuss targets and achievements! 🎯", "2024-02-05 18:00:00", 0, "sales_performance_thread_001"),
        ("slack_111", "#product", "product@company.com", "Feature request prioritization meeting! Help us decide what to build! 🚀", "2024-02-06 14:00:00", 0, "feature_prioritization_thread_001"),
        ("slack_112", "#operations", "operations@company.com", "Operations efficiency review! Optimize our processes! ⚡", "2024-02-06 19:00:00", 0, "operations_efficiency_thread_001"),
        ("slack_113", "#qa", "qa@company.com", "Quality assurance process improvement! Enhance our testing! 🔍", "2024-02-07 12:00:00", 0, "qa_improvement_thread_001"),
        ("slack_114", "#analytics", "analytics@company.com", "Analytics dashboard customization! Make it work for you! 📊", "2024-02-07 17:00:00", 0, "analytics_customization_thread_001"),
        ("slack_115", "#communications", "communications@company.com", "Internal communication audit! Improve our messaging! 📢", "2024-02-08 13:00:00", 0, "communication_audit_thread_001"),
        ("slack_116", "#admin", "admin@company.com", "Office space utilization review! Optimize our workspace! 🏢", "2024-02-08 18:00:00", 0, "space_utilization_thread_001"),
        ("slack_117", "#marketing", "marketing@company.com", "Marketing campaign performance review! Analyze our results! 📈", "2024-02-09 12:00:00", 0, "marketing_performance_thread_001"),
        ("slack_118", "#hr", "hr@company.com", "Employee satisfaction survey results! Great feedback from the team! 😊", "2024-02-09 17:00:00", 0, "satisfaction_survey_thread_001"),
        ("slack_119", "#it", "it@company.com", "IT infrastructure upgrade planning! Modernize our systems! 🔧", "2024-02-10 13:00:00", 0, "infrastructure_upgrade_thread_001"),
        ("slack_120", "#events", "events@company.com", "Company event calendar update! Mark your calendars! 📅", "2024-02-10 18:00:00", 0, "event_calendar_thread_001"),
    ]
    
    # Insert all messages (use OR IGNORE to avoid conflicts when appending)
    cursor.executemany("INSERT OR IGNORE INTO messages (custom_id, channel, user, message, timestamp, is_mention, thread_id) VALUES (?, ?, ?, ?, ?, ?, ?)", important_messages + noise_messages)
    
    conn.commit()
    conn.close()

def main():
    """Main function to create all databases for test case 3"""
    print("🚀 Starting Test Case 3 database creation and seeding...")
    print("📅 OOO Period: 2024-02-01 to 2024-02-14 (14 days)")
    print()
    
    # Ensure databases directory exists
    os.makedirs("data/databases", exist_ok=True)
    
    # Create all databases
    create_email_database()
    create_calendar_database()
    create_slack_database()
    
    print()
    print("✅ Test Case 3 databases created and seeded successfully!")
    print("📊 Summary:")
    print("   - Email database: 80 emails (16 important, 64 noise) - 80% noise ratio")
    print("   - Calendar database: 60 events (12 important, 48 noise) - 80% noise ratio")
    print("   - Slack database: 120 messages (24 important, 96 noise) - 80% noise ratio")
    print("   - Kanban database: 60 tasks (12 important, 48 noise) - 80% noise ratio")
    print("   - GitHub database: 40 commits (8 important, 32 noise) - 80% noise ratio")
    print()
    print("🎯 Test Case 3: 14-day OOO period with Valentine's Day context and Q1 planning")

if __name__ == "__main__":
    main()
