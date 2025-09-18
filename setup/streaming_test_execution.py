#!/usr/bin/env python3
"""
Streaming test execution: Run tests as soon as their corresponding agent reports are available.
This eliminates waiting for all reports to be generated before starting any tests.
"""

import os
import sys
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        print(f"📋 Using cached agent report for {test_case}")
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    print(f"🚀 Running OOO Summarizer Agent for {test_case}...")
    
    # Load test data to get date range
    test_data = load_test_data(test_case)
    
    # Run the agent using run_agent.py
    start_date = test_data["date_range"]["start"]
    end_date = test_data["date_range"]["end"]
    
    # Run run_agent.py with date parameters
    # Get the project root directory (parent of setup directory)
    if '__file__' in globals():
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        # Fallback when running with exec()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath('setup/streaming_test_execution.py')))
    
    result = subprocess.run([
        "python", "run_agent.py", start_date, end_date
    ], capture_output=True, text=True, cwd=project_root)
    
    if result.returncode != 0:
        raise RuntimeError(f"Agent failed with return code {result.returncode}: {result.stderr}")
    
    # Extract JSON from output
    output_lines = result.stdout.strip().split('\n')
    json_output = None
    
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
    
    print(f"✅ Agent report for {test_case} cached successfully")
    return report

def generate_single_report(test_case):
    """Generate a single agent report (for parallel execution)"""
    try:
        report = get_agent_report(test_case)
        p0_count = len(report.get('action_items', {}).get('P0', []))
        return test_case, report, p0_count, None
    except Exception as e:
        return test_case, None, 0, str(e)

def run_tests_for_case(test_case):
    """Run all tests for a specific test case"""
    print(f"🧪 Running tests for {test_case}...")
    
    # Run pytest for this specific test case
    if '__file__' in globals():
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath('setup/streaming_test_execution.py')))
    
    result = subprocess.run([
        "python", "-m", "pytest", 
        "tests/test_ooo_agent.py::TestOOOSummarizerAgent",
        "-k", test_case,
        "-v", "--tb=short"
    ], capture_output=True, text=True, cwd=project_root)
    
    if result.returncode == 0:
        print(f"✅ All tests passed for {test_case}")
        return test_case, True, result.stdout
    else:
        print(f"❌ Some tests failed for {test_case}")
        print(f"Error output: {result.stderr[:500]}...")
        return test_case, False, result.stderr

def main():
    """Streaming test execution: Generate reports and run tests as they become available"""
    print("🎯 Starting streaming test execution...")
    print("📋 Reports will be generated in parallel, tests will run as reports become available")
    
    test_cases = ["test_case_1", "test_case_2", "test_case_3"]
    start_time = time.time()
    
    # Use ThreadPoolExecutor for both report generation and test execution
    with ThreadPoolExecutor(max_workers=6) as executor:  # 3 for reports + 3 for tests
        # Submit report generation tasks
        report_futures = {
            executor.submit(generate_single_report, test_case): test_case 
            for test_case in test_cases
        }
        
        # Submit test execution tasks (they will wait for reports)
        test_futures = {}
        
        # Process completed reports and start tests immediately
        completed_reports = {}
        for future in as_completed(report_futures):
            test_case, report, p0_count, error = future.result()
            
            if error:
                print(f"❌ {test_case}: Failed to generate report - {error}")
                continue
            
            print(f"✅ {test_case}: Generated report with {p0_count} P0 items")
            completed_reports[test_case] = (report, p0_count)
            
            # Start tests for this case immediately
            test_future = executor.submit(run_tests_for_case, test_case)
            test_futures[test_future] = test_case
            print(f"🚀 Started tests for {test_case} (report available)")
        
        # Collect test results
        test_results = {}
        for future in as_completed(test_futures):
            test_case, success, output = future.result()
            test_results[test_case] = (success, output)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Summary
    print(f"\n🎉 Streaming test execution completed in {duration:.1f} seconds!")
    
    # Report generation summary
    print(f"\n📊 Report Generation Summary:")
    for test_case, (report, p0_count) in completed_reports.items():
        print(f"   ✅ {test_case}: {p0_count} P0 items")
    
    # Test execution summary
    print(f"\n🧪 Test Execution Summary:")
    passed_cases = 0
    for test_case, (success, output) in test_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_case}")
        if success:
            passed_cases += 1
    
    print(f"\n📈 Overall Results:")
    print(f"   Total test cases: {len(test_cases)}")
    print(f"   Passed: {passed_cases}")
    print(f"   Failed: {len(test_cases) - passed_cases}")
    print(f"   Success rate: {passed_cases/len(test_cases)*100:.1f}%")
    
    # Exit with error code if any tests failed
    if passed_cases < len(test_cases):
        sys.exit(1)

if __name__ == "__main__":
    main()
