"""
Shared fixtures for all test modules to avoid running the agent multiple times.
This dramatically improves test performance by caching the agent report.
"""
import pytest
import asyncio
import json
import os
from datetime import datetime
from main import OOOSummarizerAgent


@pytest.fixture(scope="session")
def agent_report():
    """
    Session-scoped fixture that runs the agent once and caches the result.
    This prevents running the expensive agent multiple times across all tests.
    """
    # Check if we have a cached report from a recent run
    cache_file = "tests/cached_agent_report.json"
    cache_timeout = 300  # 5 minutes
    
    if os.path.exists(cache_file):
        cache_age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if cache_age < cache_timeout:
            print("📋 Using cached agent report (less than 5 minutes old)")
            with open(cache_file, 'r') as f:
                return json.load(f)
    
    print("🚀 Running OOO Summarizer Agent (this will be cached for future tests)...")
    
    # Run the agent
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        agent = OOOSummarizerAgent()
        report = loop.run_until_complete(agent.generate_report(
            start_date="2024-01-01",
            end_date="2024-01-03"
        ))
        
        # Cache the result
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Agent report cached for future test runs")
        return report
        
    finally:
        loop.close()


@pytest.fixture(scope="session")
def test_data_verification():
    """
    Session-scoped fixture for data verification tests.
    Ensures databases are seeded before running tests.
    """
    # Ensure test data is seeded
    import subprocess
    result = subprocess.run([
        "python", "data/seed_data_test1.py"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        pytest.fail(f"Failed to seed test data: {result.stderr}")
    
    return True
