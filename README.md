You're returning from vacation with hundreds of emails, calendar invites, and Slack messages. Build an AI agent that automatically processes your out-of-office (OOO) communications and generates a structured summary with prioritized action items.

### Task

Build an AI-powered OOO summarizer that:
- Collects data from multiple sources (emails, calendar events, Slack messages)
- Analyzes and summarizes key events and updates
- Extracts action items requiring your attention
- Prioritizes items by urgency (P0, P1, P2)
- Generates a structured JSON report

### Requirements

To complete the system, you need to implement the following:

#### 1. MCP Utilities

Implement MCP server configuration in `mcp_utils.py`:
- Configure email, calendar, and Slack server connections
- Set up proper server initialization

#### 2. Prompt Files

Write prompt files that define agent behavior in `prompts/`:

- `data_collection_prompt.txt` - Collects data from multiple sources
- `summary_prompt.txt` - Generates executive summary
- `action_items_prompt.txt` - Extracts actionable items
- `priority_analysis_prompt.txt` - Prioritizes items by urgency

#### 3. Data Collection Format

The data collection prompt receives:
- `start_date`: ISO 8601 datetime for OOO period start
- `end_date`: ISO 8601 datetime for OOO period end

Expected output format:

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

### Test Scenarios

The system is tested across three scenarios:
- **Scenario 1**: 3-day OOO period
- **Scenario 2**: 7-day OOO period  
- **Scenario 3**: 14-day OOO period

### Best Practices

- **Prompt Engineering**: Write clear, deterministic prompts with examples for consistent behavior
- **JSON Compliance**: Ensure all outputs are valid JSON matching required structures
- **MCP Configuration**: Properly configure and initialize all MCP servers
- **Prioritization**: Correctly classify items as P0 (critical), P1 (high), P2 (medium)
- **Content Quality**: Generate relevant, actionable summaries and action items
- **Interactive Testing**: Use the Streamlit UI to test your agent in real time
