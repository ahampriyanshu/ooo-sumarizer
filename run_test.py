"""
Test Runner for OOO Summarizer
Allows running different test cases with different seeding data
"""

import asyncio
import sys
import os
from main import OOOSummarizerAgent

def run_seed_script(script_name):
    """Run a specific seeding script"""
    print(f"🌱 Running seeding script: {script_name}")
    os.system(f"python {script_name}")
    print()

async def run_test_case(test_name, start_date, end_date, seed_script):
    """Run a complete test case"""
    print(f"🧪 Running Test Case: {test_name}")
    print(f"📅 OOO Period: {start_date} to {end_date}")
    print("=" * 60)
    
    # Run the seeding script
    run_seed_script(seed_script)
    
    # Run the OOO summarizer
    print("🤖 Running OOO Summarizer Agent...")
    agent = OOOSummarizerAgent()
    await agent.generate_report(start_date, end_date)
    
    print("=" * 60)
    print(f"✅ Test Case '{test_name}' completed!")
    print()

async def main():
    """Main function to run test cases"""
    if len(sys.argv) < 2:
        print("Usage: python run_test.py <test_case>")
        print()
        print("Available test cases:")
        print("  test1    - 3-day OOO (Jan 1-3, 2024) with New Year context")
        print("  original - Original 7-day OOO (Jan 15-22, 2024)")
        print()
        print("Example: python run_test.py test1")
        return
    
    test_case = sys.argv[1].lower()
    
    if test_case == "test1":
        await run_test_case(
            "Test Case 1: 3-day OOO with New Year Context",
            "2024-01-01",
            "2024-01-03",
            "data/seed_data_test1.py"
        )
    elif test_case == "original":
        await run_test_case(
            "Original: 7-day OOO Period",
            "2024-01-15",
            "2024-01-22",
            "data/ref/seed_data_original.py"
        )
    else:
        print(f"❌ Unknown test case: {test_case}")
        print("Available test cases: test1, original")

if __name__ == "__main__":
    asyncio.run(main())
