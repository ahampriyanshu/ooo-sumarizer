#!/usr/bin/env python3
"""
OOO Summarizer Agent - Main Orchestrator using mcp-use for Dynamic Tool Discovery

This implementation demonstrates the correct way to use MCP by letting the LLM
discover and use tools dynamically, rather than hardcoding tool calls.
"""

import asyncio
import json
import os
import warnings
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.getLogger("mcp_use").setLevel(logging.ERROR)

class OOOSummarizerAgent:
    def __init__(self):
        # Initialize LangChain OpenAI client (required for mcp-use)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
            temperature=0.1
        )
        
        # Configure MCP servers for dynamic tool discovery
        self.mcp_config = {
            'mcpServers': {
                'email': {
                    'command': 'python',
                    'args': ['mcp_servers/email_server.py']
                },
                'calendar': {
                    'command': 'python', 
                    'args': ['mcp_servers/calendar_server.py']
                },
                'slack': {
                    'command': 'python',
                    'args': ['mcp_servers/slack_server.py']
                },
                'kanban': {
                    'command': 'python',
                    'args': ['mcp_servers/kanban_server.py']
                },
            }
        }
        
        # Create MCP client and agent for dynamic tool discovery
        self.mcp_client = MCPClient.from_dict(self.mcp_config)
        self.agent = MCPAgent(
            llm=self.llm,
            client=self.mcp_client
        )

    async def generate_report(self, start_date: str = "2024-01-15", end_date: str = "2024-01-22"):
        """Generate complete OOO summary report using dynamic tool discovery"""
        print("🚀 Starting OOO Summarizer Agent with dynamic tool discovery...")
        print(f"📅 OOO Period: {start_date} to {end_date}")
        print()
        
        try:
            # Create MCP sessions
            await self.mcp_client.create_all_sessions()
            print("✅ MCP server sessions created successfully!")
            
            # Let the LLM discover and use tools to collect data
            with open("prompts/data_collection_prompt.txt", "r") as f:
                data_collection_prompt = f.read()
            
            # Replace placeholders manually to avoid conflicts with JSON braces
            data_collection_prompt = data_collection_prompt.replace("{start_date}", start_date)
            data_collection_prompt = data_collection_prompt.replace("{end_date}", end_date)
            
            print("🔍 Discovering available tools and collecting data...")
            data_result = await self.agent.run(data_collection_prompt)
            print("✅ Data collection completed!")
            
            # Generate summary using LLM
            with open("prompts/summary_prompt.txt", "r") as f:
                summary_prompt = f.read()
            
            summary_prompt = f"{summary_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
            
            print("🤖 Generating comprehensive summary...")
            summary_result = await self.agent.run(summary_prompt)
            print("✅ Summary generated!")
            
            # Extract action items using LLM
            with open("prompts/action_items_prompt.txt", "r") as f:
                action_items_prompt = f.read()
            
            action_items_prompt = f"{action_items_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
            
            print("📝 Extracting action items...")
            action_items_result = await self.agent.run(action_items_prompt)
            print("✅ Action items extracted!")
            
            # Analyze priorities using LLM
            with open("prompts/priority_analysis_prompt.txt", "r") as f:
                priority_analysis_prompt = f.read()
            
            priority_analysis_prompt = f"{priority_analysis_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
            
            print("⚡ Analyzing priorities...")
            priority_result = await self.agent.run(priority_analysis_prompt)
            print("✅ Priority analysis completed!")
            
            # Parse results
            try:
                summary_data = json.loads(summary_result)
                action_items_data = json.loads(action_items_result)
                priority_data = json.loads(priority_result)
                
                # Create final report
                report = {
                    "summary": summary_data.get("summary", ""),
                    "action_items": action_items_data.get("action_items", {}),
                    "updates": priority_data.get("updates", {})
                }
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing error: {e}")
                # Fallback report structure
                report = {
                    "summary": summary_result,
                    "action_items": {"P0": [], "P1": [], "P2": []},
                    "updates": {
                        "email": {"P0": [], "P1": []},
                        "calendar": {"P0": [], "P1": []},
                        "slack": {"P0": [], "P1": []},
                        "kanban": {"P0": [], "P1": []},
                    }
                }
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"reports/ooo_report_{timestamp}.json"
            
            with open(report_filename, "w") as f:
                json.dump(report, f, indent=2)
            
            print("=" * 50)
            print("🎉 OOO Summary Report Generated Successfully!")
            print("=" * 50)
            print(f"📄 Report saved to: {report_filename}")
            print()
            print("📊 Report Contents:")
            print("   - Summary: Executive summary")
            print("   - Action Items: P0, P1, P2 priorities")
            print("   - Updates: Source-wise categorized updates")
            
            return report
            
        except Exception as e:
            print(f"❌ Error during report generation: {e}")
            raise
        finally:
            # Clean up MCP sessions
            try:
                await self.mcp_client.close_all_sessions()
            except Exception as e:
                print(f"⚠️ Warning during cleanup: {e}")

async def main():
    """Main function"""
    agent = OOOSummarizerAgent()
    await agent.generate_report()

if __name__ == "__main__":
    asyncio.run(main())
