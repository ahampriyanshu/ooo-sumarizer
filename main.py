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

from mcp_utils import get_mcp_agent, get_mcp_client

load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*Event loop is closed.*")
warnings.filterwarnings("ignore", message=".*Exception ignored.*")
logging.getLogger("mcp_use").setLevel(logging.ERROR)


class OOOSummarizerAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
            temperature=0.1,
            base_url=base_url,
        )

        self.mcp_client = get_mcp_client()
        self.agent = get_mcp_agent(self.llm)

    async def generate_report(
        self, start_date: str = "2024-01-01", end_date: str = "2024-01-03"
    ):
        """Generate complete OOO summary report using dynamic tool discovery"""
        print("🚀 Starting OOO Summarizer Agent with dynamic tool discovery...")
        print(f"📅 OOO Period: {start_date} to {end_date}")
        print()

        try:
            # Create MCP sessions
            await self.mcp_client.create_all_sessions()

            # Let the LLM discover and use tools to collect data
            with open("prompts/data_collection_prompt.txt", "r") as f:
                data_collection_prompt = f.read()

            # Replace placeholders manually to avoid conflicts with JSON braces
            data_collection_prompt = data_collection_prompt.replace(
                "{{ start_date }}", start_date
            )
            data_collection_prompt = data_collection_prompt.replace(
                "{{ end_date }}", end_date
            )
            data_result = await self.agent.run(data_collection_prompt)

            async def generate_summary():
                with open("prompts/summary_prompt.txt", "r") as f:
                    summary_prompt = f.read()
                summary_prompt = f"{summary_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
                return await self.agent.run(summary_prompt)

            async def extract_action_items():
                with open("prompts/action_items_prompt.txt", "r") as f:
                    action_items_prompt = f.read()
                action_items_prompt = f"{action_items_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
                return await self.agent.run(action_items_prompt)

            async def analyze_priorities():
                with open("prompts/priority_analysis_prompt.txt", "r") as f:
                    priority_analysis_prompt = f.read()
                priority_analysis_prompt = f"{priority_analysis_prompt}\n\n## Data Collected\n```json\n{data_result}\n```"
                return await self.agent.run(priority_analysis_prompt)

            # Run all three LLM calls in parallel
            print(
                "🚀 Running summary, action items, and priority analysis in parallel..."
            )
            summary_result, action_items_result, priority_result = await asyncio.gather(
                generate_summary(), extract_action_items(), analyze_priorities()
            )
            print("✅ All LLM calls completed in parallel")

            # Parse results - extract JSON from markdown code blocks if present
            try:

                def extract_json_from_markdown(text):
                    """Extract JSON from markdown code blocks"""
                    import re

                    # Look for JSON in code blocks
                    json_match = re.search(
                        r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL
                    )
                    if json_match:
                        return json_match.group(1)
                    # If no code blocks, try parsing the whole text
                    return text

                summary_json = extract_json_from_markdown(summary_result)
                action_items_json = extract_json_from_markdown(action_items_result)
                priority_json = extract_json_from_markdown(priority_result)

                summary_data = json.loads(summary_json)
                action_items_data = json.loads(action_items_json)
                priority_data = json.loads(priority_json)

                # Create final report
                report = {
                    "summary": summary_data.get("summary", ""),
                    "action_items": action_items_data.get("action_items", {}),
                    "updates": priority_data.get("updates", {}),
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
                    },
                }

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"reports/ooo_report_{timestamp}.json"

            # Ensure reports directory exists
            os.makedirs("reports", exist_ok=True)

            with open(report_filename, "w") as f:
                json.dump(report, f, indent=2)

            # Output JSON to stdout for test suite
            print(json.dumps(report))

            return report

        except Exception as e:
            print(f"❌ Error during report generation: {e}")
            raise
        finally:
            # Clean up MCP sessions with proper error handling
            try:
                if hasattr(self, "mcp_client") and self.mcp_client:
                    await self.mcp_client.close_all_sessions()
            except Exception as e:
                # Don't print warnings for expected cleanup errors
                if "Event loop is closed" not in str(e) and "CancelledError" not in str(
                    e
                ):
                    print(f"⚠️ Warning during cleanup: {e}")


async def main():
    """Main function"""
    import sys

    # Parse command line arguments for date range
    start_date = "2024-01-01"
    end_date = "2024-01-03"

    if len(sys.argv) >= 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    elif len(sys.argv) == 2:
        print("Usage: python main.py <start_date> <end_date>")
        print("Example: python main.py 2024-02-01 2024-02-14")
        sys.exit(1)

    agent = OOOSummarizerAgent()
    try:
        await agent.generate_report(start_date, end_date)
    except asyncio.CancelledError:
        # Handle cancellation gracefully
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Note: Asyncio subprocess cleanup errors may appear after this point
        # These are harmless warnings that occur during garbage collection.
        # For clean output, use: python summarizer.py
        pass
