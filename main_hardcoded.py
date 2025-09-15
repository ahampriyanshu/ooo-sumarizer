"""
OOO Summarizer Agent - Main Orchestrator using FastMCP

This is the main orchestrator agent that coordinates multiple FastMCP servers
to create comprehensive Out-of-Office summaries.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import openai
from openai import AsyncOpenAI
from fastmcp import Client

# Import FastMCP servers
from mcp_servers import (
    email_mcp,
    calendar_mcp,
    slack_mcp,
    kanban_mcp,
    github_mcp
)

# Import configuration
from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    DEFAULT_OOO_START,
    DEFAULT_OOO_END
)

class OOOSummarizerAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.mcp_servers = {
            "email": email_mcp,
            "calendar": calendar_mcp,
            "slack": slack_mcp,
            "kanban": kanban_mcp,
            "github": github_mcp
        }
        
    async def load_prompt(self, prompt_file: str) -> str:
        """Load prompt from file"""
        with open(f"prompts/{prompt_file}", "r") as f:
            return f.read()
    
    async def collect_data_from_servers(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Collect data from all FastMCP servers"""
        print(f"📊 Collecting data from {start_date} to {end_date}...")
        
        collected_data = {
            "emails": [],
            "calendar": [],
            "slack": [],
            "kanban": [],
            "github": []
        }
        
        # Collect email data
        try:
            print("📧 Collecting email data...")
            async with Client(self.mcp_servers["email"]) as client:
                # Get all emails
                emails = await client.call_tool("get_emails", {
                    "start_date": start_date,
                    "end_date": end_date,
                    "priority": "all"
                })
                collected_data["emails"].append(emails[0].text)
                
                # Get meeting requests
                meetings = await client.call_tool("get_meeting_requests", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["emails"].append(meetings[0].text)
                
                # Get important emails
                important = await client.call_tool("get_important_emails", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["emails"].append(important[0].text)
                
        except Exception as e:
            print(f"❌ Error collecting email data: {e}")
        
        # Collect calendar data
        try:
            print("📅 Collecting calendar data...")
            async with Client(self.mcp_servers["calendar"]) as client:
                # Get all events
                events = await client.call_tool("get_events", {
                    "start_date": start_date,
                    "end_date": end_date,
                    "event_type": "all"
                })
                collected_data["calendar"].append(events[0].text)
                
                # Get conflicts
                conflicts = await client.call_tool("get_conflicts", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["calendar"].append(conflicts[0].text)
                
                # Get deadlines
                deadlines = await client.call_tool("get_deadlines", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["calendar"].append(deadlines[0].text)
                
        except Exception as e:
            print(f"❌ Error collecting calendar data: {e}")
        
        # Collect Slack data
        try:
            print("💬 Collecting Slack data...")
            async with Client(self.mcp_servers["slack"]) as client:
                # Get messages
                messages = await client.call_tool("get_messages", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["slack"].append(messages[0].text)
                
                # Get mentions
                mentions = await client.call_tool("get_mentions", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["slack"].append(mentions[0].text)
                
                # Get DMs
                dms = await client.call_tool("get_direct_messages", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["slack"].append(dms[0].text)
                
                # Get channel activity
                activity = await client.call_tool("get_channel_activity", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["slack"].append(activity[0].text)
                
        except Exception as e:
            print(f"❌ Error collecting Slack data: {e}")
        
        # Collect Kanban data
        try:
            print("📋 Collecting Kanban data...")
            async with Client(self.mcp_servers["kanban"]) as client:
                # Get tasks
                tasks = await client.call_tool("get_tasks", {
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": "all"
                })
                collected_data["kanban"].append(tasks[0].text)
                
                # Get task updates
                updates = await client.call_tool("get_task_updates", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["kanban"].append(updates[0].text)
                
                # Get project progress
                progress = await client.call_tool("get_project_progress", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["kanban"].append(progress[0].text)
                
                # Get blocked tasks
                blocked = await client.call_tool("get_blocked_tasks", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["kanban"].append(blocked[0].text)
                
        except Exception as e:
            print(f"❌ Error collecting Kanban data: {e}")
        
        # Collect GitHub data
        try:
            print("🐙 Collecting GitHub data...")
            async with Client(self.mcp_servers["github"]) as client:
                # Get commits
                commits = await client.call_tool("get_commits", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["github"].append(commits[0].text)
                
                # Get pull requests
                prs = await client.call_tool("get_pull_requests", {
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": "all"
                })
                collected_data["github"].append(prs[0].text)
                
                # Get issues
                issues = await client.call_tool("get_issues", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["github"].append(issues[0].text)
                
                # Get code reviews
                reviews = await client.call_tool("get_code_reviews", {
                    "start_date": start_date,
                    "end_date": end_date
                })
                collected_data["github"].append(reviews[0].text)
                
        except Exception as e:
            print(f"❌ Error collecting GitHub data: {e}")
        
        print("✅ Data collection completed!")
        return collected_data
    
    async def generate_summary(self, data: Dict[str, Any], start_date: str, end_date: str) -> Dict[str, Any]:
        """Generate comprehensive OOO summary using LLM"""
        print("🤖 Generating comprehensive summary...")
        
        # Load the summary prompt
        prompt_template = await self.load_prompt("summary_prompt.txt")
        
        # Prepare the data for the LLM
        data_summary = f"""
OOO Period: {start_date} to {end_date}

EMAIL DATA:
{json.dumps(data['emails'], indent=2)}

CALENDAR DATA:
{json.dumps(data['calendar'], indent=2)}

SLACK DATA:
{json.dumps(data['slack'], indent=2)}

KANBAN DATA:
{json.dumps(data['kanban'], indent=2)}

GITHUB DATA:
{json.dumps(data['github'], indent=2)}
"""
        
        # Create the full prompt
        full_prompt = f"{prompt_template}\n\n{data_summary}"
        
        try:
            response = await self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert assistant that creates concise Out-of-Office summaries. Return only valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print(f"Raw content: {content}")
            return {"summary": f"JSON decode error: {e}"}
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return {"summary": f"Error generating summary: {e}"}
    
    async def extract_action_items(self, data: Dict[str, Any], start_date: str, end_date: str) -> Dict[str, Any]:
        """Extract and categorize action items using LLM"""
        print("📝 Extracting action items...")
        
        # Load the action items prompt
        prompt_template = await self.load_prompt("action_items_prompt.txt")
        
        # Prepare the data for the LLM
        data_summary = f"""
OOO Period: {start_date} to {end_date}

EMAIL DATA:
{json.dumps(data['emails'], indent=2)}

CALENDAR DATA:
{json.dumps(data['calendar'], indent=2)}

SLACK DATA:
{json.dumps(data['slack'], indent=2)}

KANBAN DATA:
{json.dumps(data['kanban'], indent=2)}

GITHUB DATA:
{json.dumps(data['github'], indent=2)}
"""
        
        # Create the full prompt
        full_prompt = f"{prompt_template}\n\n{data_summary}"
        
        try:
            response = await self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert assistant that extracts and categorizes action items from OOO data. Return only valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"❌ Error extracting action items: {e}")
            return {"action_items": {"P0": [], "P1": [], "P2": []}}
    
    async def analyze_priorities(self, data: Dict[str, Any], start_date: str, end_date: str) -> Dict[str, Any]:
        """Analyze and prioritize items using LLM"""
        print("⚡ Analyzing priorities...")
        
        # Load the priority analysis prompt
        prompt_template = await self.load_prompt("priority_analysis_prompt.txt")
        
        # Prepare the data for the LLM
        data_summary = f"""
OOO Period: {start_date} to {end_date}

EMAIL DATA:
{json.dumps(data['emails'], indent=2)}

CALENDAR DATA:
{json.dumps(data['calendar'], indent=2)}

SLACK DATA:
{json.dumps(data['slack'], indent=2)}

KANBAN DATA:
{json.dumps(data['kanban'], indent=2)}

GITHUB DATA:
{json.dumps(data['github'], indent=2)}
"""
        
        # Create the full prompt
        full_prompt = f"{prompt_template}\n\n{data_summary}"
        
        try:
            response = await self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": data_summary}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"❌ Error analyzing priorities: {e}")
            return {"updates": {"email": {"P0": [], "P1": []}, "calendar": {"P0": [], "P1": []}, "slack": {"P0": [], "P1": []}, "kanban": {"P0": [], "P1": []}, "github": {"P0": [], "P1": []}}}
    
    async def generate_ooo_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate complete OOO report"""
        # Use default dates if not provided
        if not start_date:
            start_date = DEFAULT_OOO_START
        if not end_date:
            end_date = DEFAULT_OOO_END
        
        print(f"🚀 Starting OOO Summarizer Agent...")
        print(f"📅 OOO Period: {start_date} to {end_date}")
        print()
        
        # Collect data from all sources
        data = await self.collect_data_from_servers(start_date, end_date)
        
        # Generate summary
        summary = await self.generate_summary(data, start_date, end_date)
        
        # Extract action items
        action_items = await self.extract_action_items(data, start_date, end_date)
        
        # Analyze priorities
        updates = await self.analyze_priorities(data, start_date, end_date)
        
        # Combine into final report
        report = {
            "summary": summary.get("summary", ""),
            "action_items": action_items.get("action_items", {"P0": [], "P1": [], "P2": []}),
            "updates": updates.get("updates", {})
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save the report to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ooo_report_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {filename}")
        return filename

async def main():
    """Main function to run the OOO Summarizer Agent"""
    # Check if databases exist
    if not os.path.exists("data/databases/emails.db"):
        print("❌ Databases not found. Please run 'python data/seed_data.py' first.")
        return
    
    # Create the agent
    agent = OOOSummarizerAgent()
    
    # Generate the report
    report = await agent.generate_ooo_report()
    
    # Save the report
    filename = agent.save_report(report)
    
    print("\n" + "="*50)
    print("🎉 OOO Summary Report Generated Successfully!")
    print("="*50)
    print(f"📄 Report saved to: {filename}")
    print("\n📊 Report Contents:")
    print("   - Summary: Executive summary")
    print("   - Action Items: P0, P1, P2 priorities")
    print("   - Updates: Source-wise categorized updates")
    print("\n💡 Next Steps:")
    print("   1. Review P0 action items (critical)")
    print("   2. Check important updates by source")
    print("   3. Plan P1 and P2 items for the week")

if __name__ == "__main__":
    asyncio.run(main())
