# OOO Summarizer Agent Challenge

This is a comprehensive real-world challenge for learning **Model Context Protocol (MCP)** implementation using the **FastMCP** library. The OOO (Out of Office) Summarizer Agent demonstrates how to build a multi-source data aggregation system using FastMCP servers to create intelligent summaries and action items.

## 🎯 Challenge Overview

The OOO Summarizer Agent pulls data from multiple sources during an employee's absence and creates detailed summaries with prioritized action items. This challenge teaches:

-   **FastMCP Server Implementation**: Building multiple FastMCP servers for different data sources
-   **Data Aggregation**: Combining data from multiple sources into coherent context
-   **LLM Integration**: Using AI to generate intelligent summaries and extract action items
-   **Real-world Architecture**: Production-ready patterns for agent systems

## 🏗️ Architecture

The system consists of multiple FastMCP servers that simulate real-world data sources:

### Dynamic Tool Discovery

This implementation demonstrates the correct way to use MCP by letting the LLM discover and use tools dynamically:

-   **Traditional Approach**: Hardcoded tool calls (defeats MCP purpose)
-   **Dynamic Approach**: LLM discovers available tools and chooses intelligently
-   **Benefits**: Context-aware tool selection, extensibility, true MCP implementation

See `DYNAMIC_TOOL_DISCOVERY.md` for detailed explanation and implementations.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Email Server   │    │ Calendar Server │    │  Slack Server   │
│ (Gmail/Outlook) │    │ (Google/Outlook)│    │   (Workspace)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────---┐
                    │  Main Orchestrator │
                    │        Agent       │
                    └─────────────────---┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Kanban Server   │    │  GitHub Server  │    │   LLM Engine    │
│ (Jira/Trello)   │    │   (Activity)    │    │  (OpenAI GPT)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### FastMCP Servers

1. **Email Server** (`email_server.py`)

    - Simulates Gmail/Outlook with emails, meeting requests, and important communications
    - Tools: `get_emails`, `get_meeting_requests`, `get_important_emails`

2. **Calendar Server** (`calendar_server.py`)

    - Simulates Google Calendar/Outlook with meetings, appointments, and deadlines
    - Tools: `get_events`, `get_conflicts`, `get_deadlines`

3. **Slack Server** (`slack_server.py`)

    - Simulates Slack workspace with messages, mentions, and channel activity
    - Tools: `get_messages`, `get_mentions`, `get_direct_messages`, `get_channel_activity`

4. **Kanban Server** (`kanban_server.py`)

    - Simulates Jira/Trello/Asana with task updates and project progress
    - Tools: `get_tasks`, `get_task_updates`, `get_project_progress`, `get_blocked_tasks`

5. **GitHub Server** (`github_server.py`)
    - Simulates GitHub with commits, PRs, issues, and code reviews
    - Tools: `get_commits`, `get_pull_requests`, `get_issues`, `get_code_reviews`

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   OpenAI API key
-   Git

### Installation

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd ooo-summariser
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    ```bash
    # Create .env file
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "OPENAI_MODEL=gpt-4" >> .env
    ```

4. **Seed the databases with mock data**

    ```bash
    python data/seed_data.py
    ```

5. **Run the OOO Summarizer Agent**

    **Dynamic Tool Discovery (Recommended):**

    ```bash
    # Clean output (recommended)
    python run_agent.py

    # Direct execution (shows harmless cleanup warnings)
    python main.py
    ```

    **Legacy Hardcoded Approach:**

    ```bash
    python main_hardcoded.py
    ```

## ⚠️ Runtime Error Fix

The agent may show asyncio cleanup errors when exiting. These are **harmless warnings** that don't affect functionality.

### **Solutions:**

1. **✅ Clean output (Recommended)**:

    ```bash
    python run_agent.py
    ```

2. **✅ Alternative**:

    ```bash
    python main.py 2>/dev/null
    ```

3. **⚠️ Direct execution (Shows warnings)**:
    ```bash
    python main.py
    ```

### **Why This Happens:**

The MCP library uses asyncio subprocesses. When the script exits, the event loop closes before subprocess cleanup completes, causing warnings during garbage collection. This is a known limitation of asyncio subprocess management.

    **Demo Script:**

    ```bash
    python run_demo.py
    ```

## 🔧 Implementation

### Dynamic Tool Discovery (`main.py`)

-   Uses mcp-use library for true MCP implementation
-   LLM discovers available tools automatically
-   Intelligent tool selection based on context
-   Production-ready approach
-   Demonstrates correct MCP principles

### Legacy Approach (`main_hardcoded.py`)

-   Hardcoded tool calls (for comparison)
-   Fixed sequence of operations
-   Defeats MCP purpose
-   Kept for educational purposes

## 📊 Mock Data

The system includes realistic mock data for the OOO period (2024-01-15 to 2024-01-22):

### Email Data (6 emails)

-   CEO strategy review meeting request
-   CTO technical architecture discussion
-   Manager project status update
-   HR performance review meeting
-   Client urgent API integration issue
-   Team weekly standup reminder

### Calendar Data (5 events)

-   Q1 Strategy Review meeting
-   API Project Deadline
-   Technical Architecture Discussion
-   Client Demo Preparation
-   Performance Review appointment

### Slack Data (6 messages)

-   Code review request with mention
-   Database connection issue
-   Private manager check-in
-   CEO praise for API project
-   Client timeline inquiry
-   Urgent security audit discussion

### Kanban Data (4 tasks + updates)

-   OAuth2 Authentication implementation
-   Database Connection Pool fix (blocked)
-   Payment Module code review (completed)
-   API Documentation update

### GitHub Data (3 commits, 2 PRs, 2 issues, 2 reviews)

-   OAuth2 authentication commits
-   Database connection fixes
-   API documentation updates
-   Pull request reviews and feedback
-   Bug reports and feature requests

## 🤖 AI-Powered Analysis

The system uses OpenAI GPT-4 to generate three types of analysis:

### 1. Executive Summary

-   Comprehensive overview of all activities
-   Key decisions and project status
-   Critical items requiring attention

### 2. Action Items

-   Categorized by priority (Immediate, High, Medium, Low)
-   Specific tasks with due dates and context
-   Dependencies and effort estimates

### 3. Priority Analysis

-   Urgency vs Impact matrix
-   Business critical items identification
-   Time management recommendations

## 📁 Project Structure

```
ooo-summariser/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                  # Main orchestrator agent
├── config/
│   └── settings.py          # Configuration settings
├── mcp_servers/
│   ├── __init__.py
│   ├── email_server.py      # Email MCP server
│   ├── calendar_server.py   # Calendar MCP server
│   ├── slack_server.py      # Slack MCP server
│   ├── kanban_server.py     # Kanban MCP server
│   └── github_server.py     # GitHub MCP server
├── data/
│   ├── __init__.py
│   ├── seed_data.py         # Database seeding script
│   └── databases/           # SQLite databases
│       ├── emails.db
│       ├── calendar.db
│       ├── slack.db
│       ├── kanban.db
│       └── github.db
└── prompts/
    ├── summary_prompt.txt      # LLM prompt for summaries
    ├── action_items_prompt.txt # LLM prompt for action items
    └── priority_analysis_prompt.txt # LLM prompt for priorities
```

## 🎓 Learning Objectives

This challenge teaches students:

### MCP Fundamentals

-   **Server Implementation**: How to build MCP servers with proper tool definitions
-   **Protocol Compliance**: Following MCP standards for data exchange
-   **Tool Integration**: Creating reusable tools for different data sources
-   **Error Handling**: Robust error handling and fallback strategies

### Data Management

-   **Multi-source Aggregation**: Combining data from different sources
-   **Context Management**: Managing large amounts of data within context limits
-   **Data Transformation**: Converting raw data into structured formats
-   **Database Design**: SQLite schema design for different data types

### AI Integration

-   **Prompt Engineering**: Creating effective prompts for different tasks
-   **LLM Orchestration**: Coordinating multiple LLM calls for complex analysis
-   **Output Formatting**: Structuring AI outputs for human consumption
-   **Context Optimization**: Managing token usage and context windows

### Production Patterns

-   **Agent Architecture**: Building scalable agent systems
-   **Configuration Management**: Environment-based configuration
-   **Logging and Monitoring**: Tracking system performance
-   **Error Recovery**: Handling failures gracefully

## 🔧 Customization

### Adding New Data Sources

1. **Create a new MCP server** in `mcp_servers/`
2. **Define tools** for data access
3. **Add to the orchestrator** in `main.py`
4. **Update prompts** if needed

### Modifying Analysis

1. **Edit prompt files** in `prompts/`
2. **Adjust LLM parameters** in `main.py`
3. **Add new analysis types** as needed

### Changing Data Period

1. **Update dates** in `config/settings.py`
2. **Re-seed databases** with new data
3. **Run the agent** with new parameters

## 🧪 Testing

### Manual Testing

```bash
# Test individual MCP servers
python -c "from mcp_servers.email_server import EmailMCPServer; print('Email server loaded successfully')"

# Test data collection
python -c "import asyncio; from main import OOOSummarizerAgent; asyncio.run(OOOSummarizerAgent().collect_data_from_servers('2024-01-15', '2024-01-22'))"
```

### Database Verification

```bash
# Check database contents
sqlite3 data/databases/emails.db "SELECT COUNT(*) FROM emails;"
sqlite3 data/databases/calendar.db "SELECT COUNT(*) FROM events;"
sqlite3 data/databases/slack.db "SELECT COUNT(*) FROM messages;"
sqlite3 data/databases/kanban.db "SELECT COUNT(*) FROM tasks;"
sqlite3 data/databases/github.db "SELECT COUNT(*) FROM commits;"
```

## 🚨 Troubleshooting

### Common Issues

1. **Database not found**

    ```bash
    python data/seed_data.py
    ```

2. **OpenAI API key missing**

    ```bash
    echo "OPENAI_API_KEY=your-key" > .env
    ```

3. **Import errors**

    ```bash
    pip install -r requirements.txt
    ```

4. **Permission errors**
    ```bash
    chmod +x data/seed_data.py
    ```

## 📈 Extensions

### Advanced Features

-   **Real API Integration**: Replace mock data with real APIs
-   **User Preferences**: Customizable summary depth and focus areas
-   **Export Formats**: PDF, email, or other output formats
-   **Scheduling**: Automated daily/weekly summaries
-   **Notifications**: Alert system for critical items

### Performance Optimizations

-   **Caching**: Cache frequently accessed data
-   **Parallel Processing**: Concurrent data collection
-   **Incremental Updates**: Only process new data
-   **Rate Limiting**: Respect API limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

-   **Model Context Protocol (MCP)** for the protocol specification
-   **OpenAI** for the GPT-4 API
-   **SQLite** for lightweight database storage
-   **Python asyncio** for concurrent operations

---

**Happy Learning!** 🎉

This challenge provides a comprehensive introduction to building real-world AI agents with MCP. The skills learned here can be applied to many other agent-building scenarios.
