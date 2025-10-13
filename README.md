# OOO Summariser Agent Challenge

## Problem Statement

You're returning from a vacation and there are hundreds of emails, calendar invites, and Slack messages. You need to quickly understand what happened while you were away and identify the most important items that require your action.

Build an AI agent that can automatically process your out-of-office (OOO) communications and generate a structured summary with prioritized action items.

The agent should:

-   **Collect data** from multiple sources (emails, calendar events, Slack messages)
-   **Analyze and summarize** the key events and updates
-   **Extract action items** that require your attention
-   **Prioritize items** by urgency (P0, P1, P2)
-   **Generate a structured report** in JSON format

## Your Task

The following files and code sections need to be completed:

### 1. MCP utilities (`mcp_utils.py`)

-   MCP servers configuration and setup

### 2. Prompt Files (`prompts/` directory)

-   prompts/data_collection_prompt.txt
-   Input Format:
    -   start_date: ISO 8601 date or datetime string representing the beginning of the OOO period.
    -   end_date: ISO 8601 date or datetime string representing the end of the OOO period.
    -   Output Format for data collection prompt:

```json
{
	"emails": [
		{
			"id": "email_001",
			"sender": "john.doe@company.com",
			"subject": "URGENT: Production System Outage",
			"body": "The production API is down and customers are affected. Immediate attention required.",
			"received_date": "2024-01-02T10:30:00Z",
			"is_read": false,
			"thread_id": "thread_001"
		},
		{
			"id": "email_002",
			"sender": "security@company.com",
			"subject": "Security Vulnerability Notification",
			"body": "Critical security patch required for authentication system.",
			"received_date": "2024-01-02T14:15:00Z",
			"is_read": false,
			"thread_id": "thread_002"
		}
	],
	"calendar_events": [
		{
			"id": "event_001",
			"title": "Emergency Incident Response",
			"description": "Emergency response meeting for production system outage.",
			"start_time": "2024-01-02T15:00:00Z",
			"end_time": "2024-01-02T16:00:00Z",
			"location": "Conference Room A",
			"attendees": ["john.doe@company.com", "jane.smith@company.com"],
			"event_type": "meeting"
		},
		{
			"id": "event_002",
			"title": "Q1 Strategic Planning Session",
			"description": "Strategic planning session for Q1 roadmap and resource allocation.",
			"start_time": "2024-01-03T09:00:00Z",
			"end_time": "2024-01-03T11:00:00Z",
			"location": "Virtual",
			"attendees": [
				"john.doe@company.com",
				"jane.smith@company.com",
				"bob.wilson@company.com"
			],
			"event_type": "meeting"
		}
	],
	"slack_messages": [
		{
			"id": "slack_001",
			"channel": "#incidents",
			"user": "john.doe",
			"message": "Critical security vulnerability detected. Immediate patch deployment required.",
			"timestamp": "2024-01-02T11:45:00Z",
			"is_private": false
		},
		{
			"id": "slack_002",
			"channel": "#general",
			"user": "jane.smith",
			"message": "Major client escalation requires technical review and response strategy.",
			"timestamp": "2024-01-02T16:20:00Z",
			"is_private": false
		}
	]
}
```

### Evaluation Criteria

-   **Prompt Accurray** - Effective prompts that guide LLM to produce accurate results
-   **JSON Compliance** - Produces valid JSON matching the required structure
-   **Method Implementation** - Correct logic for setting up the MCP servers
-   **Output Accuracy** - Correctly identifies and prioritizes important items
-   **Prioritization Accuracy** - Items are correctly classified as P0, P1, P2
-   **Content Quality** - Summary and action items are relevant and actionable

### Test Scenarios

1. Scenario 1: 3-Day OOO
2. Scenario 2: 7-Day OOO
3. Scenario 3: 14-Day OOO

## Streamlit Web Interface

The project includes a web interface built with Streamlit for interactive testing and visualization:

### Run the web app

```bash
streamlit run app.py --server.port 8000
```
