"""
Test runner for OOO Summariser Agent
Runs the agent with Test Case 1 data and then executes the test suite
"""

import asyncio
import subprocess
import sys
import os
from main import OOOSummarizerAgent


async def run_agent_test():
    """Run the OOO Summariser Agent with Test Case 1 data"""
    print("🚀 Running OOO Summariser Agent with Test Case 1 data...")
    print("📅 OOO Period: 2024-01-01 to 2024-01-03")
    print()
    
    # Ensure test data exists
    if not os.path.exists("data/databases/emails.db"):
        print("❌ Test data not found. Please run 'python data/seed_data_test1.py' first.")
        return False
    
    try:
        # Run the agent
        agent = OOOSummarizerAgent()
        await agent.generate_report("2024-01-01", "2024-01-03")
        print("✅ Agent report generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        return False


def run_pytest_tests():
    """Run the pytest test suite"""
    print("\n🧪 Running pytest test suite...")
    print("=" * 60)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_ooo_agent.py", 
            "-v", 
            "--tb=short"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            return True
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False


async def main():
    """Main function to run agent and tests"""
    print("🎯 OOO Summariser Agent Test Suite")
    print("=" * 60)
    
    # Step 1: Run the agent
    agent_success = await run_agent_test()
    if not agent_success:
        print("❌ Agent test failed. Exiting.")
        return
    
    # Step 2: Run pytest tests
    test_success = run_pytest_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Agent Execution: {'✅ PASSED' if agent_success else '❌ FAILED'}")
    print(f"   Test Suite: {'✅ PASSED' if test_success else '❌ FAILED'}")
    
    if agent_success and test_success:
        print("\n🎉 All tests passed! The OOO Summariser Agent is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")


if __name__ == "__main__":
    asyncio.run(main())
