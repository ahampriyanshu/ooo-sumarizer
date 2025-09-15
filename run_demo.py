#!/usr/bin/env python3
"""
Demo Script for OOO Summarizer Agent

This script demonstrates the complete workflow:
1. Seeds the databases with mock data
2. Runs the OOO Summarizer Agent
3. Displays the results
"""

import asyncio
import os
import sys
from datetime import datetime

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # Check if required packages are installed
    try:
        import openai
        import sqlite3
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    return True

def seed_databases():
    """Seed the databases with mock data"""
    print("🌱 Seeding databases with mock data...")
    
    try:
        # Import and run the seeding script
        from data.seed_data import main as seed_main
        seed_main()
        return True
    except Exception as e:
        print(f"❌ Error seeding databases: {e}")
        return False

async def run_agent():
    """Run the OOO Summarizer Agent"""
    print("🤖 Running OOO Summarizer Agent...")
    
    try:
        from main import OOOSummarizerAgent
        
        # Create the agent
        agent = OOOSummarizerAgent()
        
        # Generate the report
        report = await agent.generate_ooo_report()
        
        # Save the report
        filename = agent.save_report(report)
        
        return report, filename
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        return None, None

def display_summary(report):
    """Display a summary of the report"""
    if not report:
        return
    
    print("\n" + "="*60)
    print("📊 OOO SUMMARY REPORT")
    print("="*60)
    print(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Display executive summary
    print("📋 EXECUTIVE SUMMARY:")
    print("-" * 30)
    print(report.get('summary', 'No summary available'))
    print()
    
    # Display action items count
    action_items = report.get('action_items', {})
    p0_count = len(action_items.get('P0', []))
    p1_count = len(action_items.get('P1', []))
    p2_count = len(action_items.get('P2', []))
    print(f"📝 ACTION ITEMS: P0({p0_count}) P1({p1_count}) P2({p2_count})")
    print()
    
    # Display updates count
    updates = report.get('updates', {})
    total_p0_updates = sum(len(v.get('P0', [])) for v in updates.values())
    total_p1_updates = sum(len(v.get('P1', [])) for v in updates.values())
    print(f"⚡ UPDATES: P0({total_p0_updates}) P1({total_p1_updates}) across all sources")
    print()
    
    print("💡 Full JSON report saved to file for detailed review")

async def main():
    """Main demo function"""
    print("🚀 OOO Summarizer Agent Demo")
    print("=" * 40)
    print()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Seed databases
    if not seed_databases():
        sys.exit(1)
    
    # Run the agent
    report, filename = await run_agent()
    
    if report and filename:
        # Display summary
        display_summary(report)
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📄 Full report saved to: {filename}")
        print("\n📚 What you learned:")
        print("   ✅ MCP server implementation")
        print("   ✅ Multi-source data aggregation")
        print("   ✅ LLM-powered JSON analysis")
        print("   ✅ Structured report generation")
        print("\n🔗 Next steps:")
        print("   1. Review the JSON report structure")
        print("   2. Explore the MCP server code")
        print("   3. Modify prompts for different analysis")
        print("   4. Add new data sources")
        print("   5. Integrate with real APIs")
        
    else:
        print("❌ Demo failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
