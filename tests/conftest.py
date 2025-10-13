"""
Shared fixtures for all test modules to avoid running the agent multiple times.
This dramatically improves test performance by caching the agent report.
"""

import pytest
import asyncio
import json
import os
from main import OOOSummarizerAgent
from .test_ooo_agent import TEST_CASES


def load_test_data(test_case="test_case_1"):
    """Load test data from JSON file"""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "test_data", f"{test_case}.json"
    )
    with open(test_data_path, "r") as f:
        return json.load(f)


@pytest.fixture(scope="session", params=TEST_CASES)
def test_case_data(request):
    """Parameterized fixture that provides test case data for both test cases"""
    return load_test_data(request.param)


def get_agent_report(test_case):
    """
    Get agent report for a specific test case, with caching.
    This prevents running the expensive agent multiple times for the same test case.
    Uses a fixed constant ID system for cache identification.
    """
    # Create cache file name based on test case with fixed constant ID
    cache_file = f"tests/test_data/reports/agent_report_{test_case}_v1.json"

    if os.path.exists(cache_file):
        print(f"📋 Using cached agent report for {test_case} (fixed constant ID: v1)")
        with open(cache_file, "r") as f:
            return json.load(f)

    print(
        f"🚀 Running OOO Summarizer Agent for {test_case} (this will be cached for future tests)..."
    )

    # Ensure test data is seeded for this test case
    seed_script = f"data/seed_data_{test_case.replace('test_case_', 'test')}.py"
    if not os.path.exists(seed_script):
        raise FileNotFoundError(f"Seed script not found: {seed_script}")

    # Run the seeding script
    import subprocess

    result = subprocess.run(["python", seed_script], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to seed test data for {test_case}: {result.stderr}")

    # Load test data to get date range
    test_data = load_test_data(test_case)

    # Run the agent
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        agent = OOOSummarizerAgent()
        report = loop.run_until_complete(
            agent.generate_report(
                start_date=test_data["date_range"]["start"],
                end_date=test_data["date_range"]["end"],
            )
        )

        # Cache the result
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"✅ Agent report for {test_case} cached for future test runs")
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

    result = subprocess.run(
        ["python", "data/seed_data_test1.py"], capture_output=True, text=True
    )

    if result.returncode != 0:
        pytest.fail(f"Failed to seed test data: {result.stderr}")

    return True
