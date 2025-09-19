# OOO Summariser Agent Challenge

## Problem Statement

You're returning from a vacation and your inbox is flooded with hundreds of emails, calendar invites, and Slack messages. Your team has been working on critical projects, and there are urgent issues that need your immediate attention.

You need to quickly understand what happened while you were away and identify the most important items that require your action. However, manually sifting through all this information would take hours, and you need to prioritize your time effectively.

## Your Task

Build an AI agent that can automatically process your out-of-office (OOO) communications and generate a structured summary with prioritized action items.

The agent should:

-   **Collect data** from multiple sources (emails, calendar events, Slack messages)
-   **Analyze and summarize** the key events and updates
-   **Extract action items** that require your attention
-   **Prioritize items** by urgency (P0, P1, P2)
-   **Generate a structured report** in JSON format

### Input Data Sources

The agent must integrate with three data sources:

-   **Email system** - Retrieve emails from your inbox
-   **Calendar system** - Access calendar events and meetings
-   **Slack workspace** - Read messages from relevant channels

### Output Format

The agent must return a JSON report with the following structure:

```json
{
	"summary": "Critical production system outage requires immediate attention, along with security vulnerability patches and Q1 planning sessions. Multiple client escalations and compliance deadlines are approaching. Team coordination needed for infrastructure migration and product launch approvals.",
	"action_items": {
		"P0": [
			{
				"id": "email_001",
				"title": "CRITICAL: Production System Outage",
				"due_date": "2024-01-02",
				"source": "email",
				"context": "Production API is down and customers are affected. Immediate attention required."
			},
			{
				"id": "slack_001",
				"title": "URGENT: Security Vulnerability Patch",
				"due_date": "2024-01-02",
				"source": "slack",
				"context": "Critical security vulnerability detected. Patch deployment required immediately."
			},
			{
				"id": "event_001",
				"title": "Emergency Incident Response",
				"due_date": "2024-01-02",
				"source": "calendar",
				"context": "Emergency response meeting for production outage. All hands on deck."
			}
		],
		"P1": [
			{
				"id": "email_005",
				"title": "Q1 Strategic Planning Session",
				"due_date": "2024-01-03",
				"source": "email",
				"context": "Q1 strategic planning session scheduled. Your input required for roadmap decisions."
			},
			{
				"id": "slack_007",
				"title": "Client Escalation Review",
				"due_date": "2024-01-04",
				"source": "slack",
				"context": "Major client escalation needs technical review and response plan."
			},
			{
				"id": "event_003",
				"title": "Infrastructure Migration Planning",
				"due_date": "2024-01-05",
				"source": "calendar",
				"context": "Infrastructure migration planning session. Technical oversight required."
			}
		],
		"P2": [
			{
				"id": "email_012",
				"title": "Team Building Event",
				"due_date": "2024-01-10",
				"source": "email",
				"context": "Optional team building event. RSVP if interested in attending."
			},
			{
				"id": "slack_015",
				"title": "Weekly Tech Talk",
				"due_date": "2024-01-08",
				"source": "slack",
				"context": "Weekly tech talk on new framework. Educational session for the team."
			}
		]
	},
	"updates": {
		"email": {
			"P0": [
				{
					"id": "email_001",
					"title": "Production System Outage Alert",
					"due_date": "2024-01-02",
					"source": "email",
					"context": "Urgent system outage affecting multiple clients. Immediate response needed."
				},
				{
					"id": "email_002",
					"title": "Security Vulnerability Notification",
					"due_date": "2024-01-02",
					"source": "email",
					"context": "Critical security patch required for authentication system."
				}
			],
			"P1": [
				{
					"id": "email_005",
					"title": "Q1 Planning Meeting Invite",
					"due_date": "2024-01-03",
					"source": "email",
					"context": "Strategic planning session for Q1 roadmap and resource allocation."
				},
				{
					"id": "email_008",
					"title": "Compliance Review Reminder",
					"due_date": "2024-01-05",
					"source": "email",
					"context": "Quarterly compliance review documentation due. Please prepare materials."
				}
			]
		},
		"calendar": {
			"P0": [
				{
					"id": "event_001",
					"title": "Emergency Incident Response",
					"due_date": "2024-01-02",
					"source": "calendar",
					"context": "Emergency response meeting for production system outage."
				}
			],
			"P1": [
				{
					"id": "event_003",
					"title": "Infrastructure Migration Planning",
					"due_date": "2024-01-05",
					"source": "calendar",
					"context": "Planning session for upcoming infrastructure migration project."
				},
				{
					"id": "event_004",
					"title": "Product Launch Review",
					"due_date": "2024-01-07",
					"source": "calendar",
					"context": "Final review meeting for product launch. Go/no-go decision required."
				}
			]
		},
		"slack": {
			"P0": [
				{
					"id": "slack_001",
					"title": "Security Vulnerability Alert",
					"due_date": "2024-01-02",
					"source": "slack",
					"context": "Critical security vulnerability detected. Immediate patch deployment required."
				}
			],
			"P1": [
				{
					"id": "slack_007",
					"title": "Client Escalation Discussion",
					"due_date": "2024-01-04",
					"source": "slack",
					"context": "Major client escalation requires technical review and response strategy."
				},
				{
					"id": "slack_010",
					"title": "Team Standup Reminder",
					"due_date": "2024-01-03",
					"source": "slack",
					"context": "Daily standup meeting. Please prepare status updates for your projects."
				}
			]
		}
	}
}
```

### Prioritization Logic

-   **P0 (Critical)**: Urgent issues requiring immediate attention (system outages, security issues, critical deadlines)
-   **P1 (Important)**: Important items that need attention soon (meetings, project updates, client requests)
-   **P2 (Nice to have)**: Lower priority items (general updates, non-urgent requests)

## Deliverables

The following files and code sections need to be completed:

### 1. Prompt Files (`prompts/` directory)

### 2. Main Agent Logic (`main.py`)

-   LLM model configuration and setup
-   Generate executive summary using LLM
-   Extract action items using LLM
-   Prioritize items using LLM

### 3. Framework Already Provided

-   **MCP Servers** - Email, calendar, and Slack data access
-   **Data Collection** - Automatic data gathering from all sources
-   **Infrastructure** - Database setup, parallel processing, error handling

## Success Criteria

Your solution will be evaluated on:

-   **Prompt Quality** - Effective prompts that guide LLM to produce accurate results
-   **Method Implementation** - Correct logic for processing and integrating LLM responses
-   **Output Accuracy** - Correctly identifies and prioritizes important items
-   **JSON Compliance** - Produces valid JSON matching the required structure

## Test Scenarios

1. Scenario 1: 3-Day OOO
2. Scenario 2: 7-Day OOO
3. Scenario 3: 14-Day OOO

## Evaluation

Your solution will be tested against multiple scenarios with varying data volumes and complexity. The test suite will verify:

-   **JSON Structure Compliance** - Output matches the required format exactly
-   **Prioritization Accuracy** - Items are correctly classified as P0, P1, P2
-   **Content Quality** - Summary and action items are relevant and actionable
-   **Data Completeness** - All important information is captured and processed
-   **Error Handling** - Graceful handling of edge cases and invalid data

## Tips for Success

-   **Focus on prompt writing** - Clear, specific prompts lead to better LLM outputs
-   **Test incrementally** - Run tests after implementing each method
-   **Use the provided examples** - Study the test data to understand expected outputs
-   **Handle edge cases** - Consider empty data, malformed inputs, and error scenarios
