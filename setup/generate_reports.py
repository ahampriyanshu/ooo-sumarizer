#!/usr/bin/env python3
"""
Generate agent reports for all test cases to enable fast parallel test execution.
This script runs the agent once for each test case and caches the results.
"""

import os
import sys
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def load_test_data(test_case):
    """Load test data for a specific test case"""
    test_data_file = f"tests/test_data/{test_case}.json"
    with open(test_data_file, 'r') as f:
        return json.load(f)

def get_agent_report(test_case):
    """Get agent report for a specific test case, with caching"""
    # Create cache file name based on test case with fixed constant ID
    cache_file = f"tests/test_data/reports/agent_report_{test_case}_v1.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    # Ensure test data is seeded for this test case
    seed_script = f"data/seed_data_{test_case.replace('test_case_', 'test')}.py"
    if not os.path.exists(seed_script):
        raise FileNotFoundError(f"Seed script not found: {seed_script}")
    
    # Run the seeding script
    result = subprocess.run(["python", seed_script], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to seed test data for {test_case}: {result.stderr}")
    
    # Load test data to get date range
    test_data = load_test_data(test_case)
    
    # Run the agent using run_agent.py
    start_date = test_data["date_range"]["start"]
    end_date = test_data["date_range"]["end"]
    
    # Run run_agent.py with date parameters
    # Get the project root directory (parent of setup directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run([
        "python", "run_agent.py", start_date, end_date
    ], capture_output=True, text=True, cwd=project_root)
    
    if result.returncode != 0:
        raise RuntimeError(f"Agent failed with return code {result.returncode}: {result.stderr}")
    
    # Extract JSON from output
    output_lines = result.stdout.strip().split('\n')
    json_output = None
    
    # Find the JSON output (it should be the last meaningful line)
    for line in reversed(output_lines):
        line = line.strip()
        if line and line.startswith('{') and line.endswith('}'):
            json_output = line
            break
    
    if not json_output:
        # If no JSON found in lines, look for JSON in the entire output
        start_idx = result.stdout.find('{')
        end_idx = result.stdout.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_output = result.stdout[start_idx:end_idx+1]
        else:
            json_output = result.stdout.strip()
    
    try:
        report = json.loads(json_output)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse agent output as JSON: {e}\nOutput: {result.stdout}")
    
    # Cache the result
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

def generate_single_report(test_case):
    """Generate a single agent report (for parallel execution)"""
    try:
        report = get_agent_report(test_case)
        p0_count = len(report.get('action_items', {}).get('P0', []))
        return test_case, report, p0_count, None
    except Exception as e:
        return test_case, None, 0, str(e)

def main():
    """Generate all agent reports in parallel"""
    
    test_cases = ["test_case_1", "test_case_2", "test_case_3"]
    start_time = time.time()
    
    # Use ThreadPoolExecutor to run agent calls in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_case = {
            executor.submit(generate_single_report, test_case): test_case 
            for test_case in test_cases
        }
        
        # Collect results as they complete
        results = {}
        for future in as_completed(future_to_case):
            test_case, report, p0_count, error = future.result()
            results[test_case] = (report, p0_count, error)
            
            if error:
                print(f"❌ {test_case}: Failed to generate report - {error}")
    
    # Check for any failures
    failed_cases = [case for case, (_, _, error) in results.items() if error]
    if failed_cases:
        print(f"\n❌ Failed to generate reports for: {', '.join(failed_cases)}")
        sys.exit(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 All agent reports generated successfully in {duration:.1f} seconds!")

if __name__ == "__main__":
    main()
