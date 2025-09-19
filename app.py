#!/usr/bin/env python3
"""
Streamlit App for OOO Summariser Agent
Provides a web interface to run test cases and visualize results
"""

import streamlit as st
import json
import subprocess
import re

# Page configuration
st.set_page_config(
    page_title="OOO Summariser Agent",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    /* Force override all Streamlit defaults */
    * {
        box-sizing: border-box;
    }
    
    /* Main app background */
    .stApp {
        background-color: #1A1D29 !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Hide ONLY the header toolbar, not the entire first div */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Hide toolbar elements */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide deploy and stop buttons */
    [data-testid="stDeployButton"], [data-testid="stStopButton"] {
        display: none !important;
    }
    
    /* Main content area - centered layout */
    .main .block-container {
        background-color: #1A1D29 !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    
    /* Center text content with better spacing */
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3 {
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    
    .main .block-container p {
        text-align: center !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Better section spacing */
    .main .block-container > div {
        margin: 1rem 0 !important;
    }
    
    /* Center the main header */
    .main-header {
        text-align: center !important;
        margin: 0 auto !important;
        color: white !important;
    }
    
    /* Center the subtitle */
    .main-subtitle {
        text-align: center !important;
        margin: 0 auto !important;
        color: white !important;
    }
    
    /* Header container with border */
    .header-container {
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem !important;
        padding: 2rem !important;
        margin: 2rem auto !important;
        max-width: 800px !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
        box-shadow: 0 4px 20px rgba(74, 137, 243, 0.2) !important;
        color: white !important;
    }
    
    /* Test cases header centering */
    .test-cases-header {
        text-align: center !important;
        margin: 2rem auto !important;
    }
    
    .test-cases-header h2 {
        color: #FFFFFF !important;
        margin-bottom: 0.5rem !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .test-cases-header p {
        color: #A0A3AD !important;
        margin: 0 !important;
        font-size: 1.1rem !important;
    }
    
    /* Hide sidebar completely */
    .stSidebar {
        display: none !important;
    }
    
    /* Form elements container - better spacing */
    .stSelectbox {
        margin: 1rem auto !important;
        max-width: 500px !important;
        height: auto;
    }
    
    .stCheckbox {
        margin: 1rem auto !important;
        max-width: 500px !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important
        margin: 1rem auto !important;
        max-width: 500px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* Center button and checkbox in nested column layout */
    .stColumns .stColumns .stButton {
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    .stColumns .stColumns .stCheckbox {
        margin: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 100% !important;
    }
    
    /* Ensure proper spacing in the gap column */
    .stColumns .stColumns .stEmpty {
        margin: 0 1rem !important;
    }
    
    /* Main content selectbox */
    .stSelectbox > div > div {
        background-color: #3B4257 !important;
        border: 1px solid #3B4257 !important;
        border-radius: 0.5rem !important;
        width: 100% !important;
        padding: 0.75rem !important;
        min-height: 2.5rem !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Selectbox text visibility */
    .stSelectbox > div > div > div {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        overflow: visible !important;
        white-space: nowrap !important;
    }
    
    .stSelectbox label {
        color: #A0A3AD !important;
        text-align: left !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown options styling */
    .stSelectbox [data-baseweb="select"] {
        min-height: 2.5rem !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        min-height: 2.5rem !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Ensure dropdown menu items are visible */
    .stSelectbox [role="listbox"] {
        background-color: #3B4257 !important;
        border: 1px solid #4A89F3 !important;
        border-radius: 0.5rem !important;
    }
    
    .stSelectbox [role="option"] {
        color: #FFFFFF !important;
        padding: 0.75rem !important;
        min-height: 2.5rem !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #4A89F3 !important;
    }
    
    /* Main content checkbox */
    .stCheckbox label {
        color: #A0A3AD !important;
        text-align: center !important;
        font-weight: 500 !important;
    }
    
    /* Main content button */
    .stButton > button {
        background-color: #4A89F3 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        max-width: 500px !important;
        font-size: 1rem !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        background-color: #3A79E3 !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button:focus {
        color: #FFFFFF !important;
    }
    
    .stButton > button:active {
        color: #FFFFFF !important;
    }
    
    /* Force button text to be white */
    .stButton > button * {
        color: #FFFFFF !important;
    }
    
    .stButton > button > div {
        color: #FFFFFF !important;
    }
    
    .stButton > button > div > div {
        color: #FFFFFF !important;
    }
    
    .stButton > button > div > div > div {
        color: #FFFFFF !important;
    }
    
    /* Main content styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .main-subtitle {
        color: #A0A3AD;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    /* Test case section styling */
    .test-case-section {
        background-color: #222736;
        padding: 2rem;
        border-radius: 0.75rem;
        margin: 2rem auto !important;
        border: 1px solid #3B4257;
        text-align: center !important;
        max-width: 700px !important;
    }
    
    /* Center columns within test case section */
    .test-case-section .stColumns {
        justify-content: center !important;
        gap: 2rem !important;
    }
    
    /* Better spacing for test case content */
    .test-case-section h3 {
        margin-bottom: 1.5rem !important;
    }
    
    .test-case-section ul, .test-case-section ol {
        text-align: left !important;
        margin: 1rem 0 !important;
    }
    
    /* Text colors and wrapping */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    p, div, span, li {
        color: #A0A3AD !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Fix text clipping in metrics and cards */
    .stMetric {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stMetric > div {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Fix text clipping in action items */
    .priority-p0, .priority-p1, .priority-p2 {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #222736;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #4A89F3;
        margin: 1rem 0;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    /* Priority sections */
    .priority-p0 {
        background-color: #3B4257;
        border-left: 4px solid #FF6B6B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    .priority-p1 {
        background-color: #3B4257;
        border-left: 4px solid #FFD93D;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    .priority-p2 {
        background-color: #3B4257;
        border-left: 4px solid #6BCF7F;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    
    /* Action items */
    .action-item {
        background-color: #222736;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        border: 1px solid #3B4257;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #222736 !important;
        color: #FFFFFF !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1A1D29 !important;
    }
    
    /* Remove only horizontal dividers, not all dividers */
    hr.stDivider {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript to hide the header and fix button text
st.markdown("""
<script>
    // Hide the Streamlit header and fix button text
    function fixUI() {
        // Hide only the header toolbar
        const header = document.querySelector('header[data-testid="stHeader"]');
        if (header) {
            header.style.display = 'none';
        }
        
        // Hide toolbar elements
        const toolbar = document.querySelector('[data-testid="stToolbar"]');
        if (toolbar) {
            toolbar.style.display = 'none';
        }
        
        // Hide deploy and stop buttons
        const deployButton = document.querySelector('[data-testid="stDeployButton"]');
        if (deployButton) {
            deployButton.style.display = 'none';
        }
        
        const stopButton = document.querySelector('[data-testid="stStopButton"]');
        if (stopButton) {
            stopButton.style.display = 'none';
        }
        
        // Fix button text visibility
        const mainButtons = document.querySelectorAll('.stButton > button');
        mainButtons.forEach(button => {
            button.style.color = '#FFFFFF';
            const textElements = button.querySelectorAll('*');
            textElements.forEach(element => {
                element.style.color = '#FFFFFF';
            });
        });
    }
    
    // Run immediately
    fixUI();
    
    // Run on page load
    document.addEventListener('DOMContentLoaded', fixUI);
    
    // Run on any DOM changes
    const observer = new MutationObserver(fixUI);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Run periodically to ensure fixes stick
    setInterval(fixUI, 1000);
</script>
""", unsafe_allow_html=True)

def extract_json_from_output(output, debug=False):
    """Extract JSON from agent output using multiple methods"""
    if not output or not output.strip():
        return None
    
    output = output.strip()
    
    if debug:
        print(f"DEBUG: Input output length: {len(output)}")
        print(f"DEBUG: First 200 chars: {output[:200]}")
    
    # Method 1: Look for markdown code blocks
    if "```json" in output:
        json_start = output.find("```json") + 7
        json_end = output.find("```", json_start)
        if json_end > json_start:
            json_str = output[json_start:json_end].strip()
            if debug:
                print(f"DEBUG: Method 1 - Found markdown JSON block: {json_str[:100]}...")
            try:
                result = json.loads(json_str)
                if debug:
                    print("DEBUG: Method 1 - Successfully parsed JSON")
                return result
            except json.JSONDecodeError as e:
                if debug:
                    print(f"DEBUG: Method 1 - JSON decode error: {e}")
                pass
    
    # Method 2: Look for JSON object starting with { and ending with }
    if "{" in output and "}" in output:
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        if json_end > json_start:
            json_str = output[json_start:json_end].strip()
            if debug:
                print(f"DEBUG: Method 2 - Found JSON object: {json_str[:100]}...")
            try:
                result = json.loads(json_str)
                if debug:
                    print("DEBUG: Method 2 - Successfully parsed JSON")
                return result
            except json.JSONDecodeError as e:
                if debug:
                    print(f"DEBUG: Method 2 - JSON decode error: {e}")
                pass
    
    # Method 3: Try to find JSON using regex
    json_pattern = r'\{.*\}'
    matches = re.findall(json_pattern, output, re.DOTALL)
    if debug:
        print(f"DEBUG: Method 3 - Found {len(matches)} regex matches")
    for i, match in enumerate(matches):
        if debug:
            print(f"DEBUG: Method 3 - Trying match {i+1}: {match[:100]}...")
        try:
            result = json.loads(match)
            if debug:
                print(f"DEBUG: Method 3 - Successfully parsed JSON from match {i+1}")
            return result
        except json.JSONDecodeError as e:
            if debug:
                print(f"DEBUG: Method 3 - JSON decode error for match {i+1}: {e}")
            continue
    
    # Method 4: Try the entire output as JSON
    if debug:
        print("DEBUG: Method 4 - Trying entire output as JSON")
    try:
        result = json.loads(output)
        if debug:
            print("DEBUG: Method 4 - Successfully parsed entire output as JSON")
        return result
    except json.JSONDecodeError as e:
        if debug:
            print(f"DEBUG: Method 4 - JSON decode error: {e}")
        pass
    
    if debug:
        print("DEBUG: All methods failed to parse JSON")
    return None

def run_test_case(test_case, debug=False):
    """Run a specific test case and return the agent report"""
    try:
        # Run the agent for the specific test case
        if test_case == "test_case_1":
            cmd = ["python3", "run_agent.py", "2024-01-01", "2024-01-03"]
        elif test_case == "test_case_2":
            cmd = ["python3", "run_agent.py", "2024-01-07", "2024-01-14"]
        elif test_case == "test_case_3":
            cmd = ["python3", "run_agent.py", "2024-02-01", "2024-02-14"]
        else:
            return None
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Parse the JSON output using the helper function
            parsed_json = extract_json_from_output(result.stdout, debug=debug)
            
            if parsed_json:
                # Ensure we return a dictionary
                if isinstance(parsed_json, dict):
                    return parsed_json
                else:
                    st.error(f"JSON parsing returned {type(parsed_json).__name__}, expected dict")
                    if debug:
                        st.text("Parsed JSON:")
                        st.text(str(parsed_json))
                    return None
            else:
                st.error("No valid JSON found in output")
                if debug:
                    st.text("Raw output:")
                    st.text(result.stdout)
                    st.text("Raw stderr:")
                    st.text(result.stderr)
                return None
        else:
            st.error(f"Command failed with return code {result.returncode}")
            st.text("Error output:")
            st.text(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        st.error("Test case execution timed out (5 minutes)")
        return None
    except Exception as e:
        st.error(f"Error running test case: {e}")
        return None

def run_all_test_cases(debug=False):
    """Run all test cases and return their reports"""
    reports = {}
    test_cases = ["test_case_1", "test_case_2", "test_case_3"]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, test_case in enumerate(test_cases):
        status_text.text(f"Running {test_case}...")
        report = run_test_case(test_case, debug=debug)
        reports[test_case] = report
        progress_bar.progress((i + 1) / len(test_cases))
    
    status_text.text("All test cases completed!")
    return reports

def display_report(report, test_case_name=None):
    """Display a beautiful UI for the JSON report"""
    if not report:
        st.error("No report data to display")
        return
    
    # Check if report is a dictionary (parsed JSON)
    if not isinstance(report, dict):
        st.error(f"Invalid report format. Expected dictionary, got {type(report).__name__}")
        if isinstance(report, str):
            st.text("Raw report data:")
            st.text(report)
        return
    
    # Header
    if test_case_name:
        st.markdown(f"<h2>📊 Report: {test_case_name.replace('_', ' ').title()}</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2>📊 OOO Summary Report</h2>", unsafe_allow_html=True)
    
    # Basic info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # OOO Period - extract from test case context since it's not in the JSON
        if test_case_name:
            if "Test Case 1" in test_case_name:
                start_date, end_date = "1st Jan 2024", "3rd Jan 2024"
            elif "Test Case 2" in test_case_name:
                start_date, end_date = "7th Jan 2024", "14th Jan 2024"
            elif "Test Case 3" in test_case_name:
                start_date, end_date = "1st Feb 2024", "14th Feb 2024"
            else:
                start_date, end_date = "N/A", "N/A"
        else:
            start_date, end_date = "N/A", "N/A"
        st.metric("OOO Period", f"{start_date} to {end_date}")
    
    with col2:
        # Handle different action_items structures
        if isinstance(report.get('action_items'), dict):
            # New structure: {"P0": [...], "P1": [...], "P2": [...]}
            total_items = sum(len(items) for items in report.get('action_items', {}).values())
        else:
            # Old structure: [...]
            total_items = len(report.get('action_items', []))
        st.metric("Total Action Items", total_items)
    
    with col3:
        # Handle different action_items structures
        if isinstance(report.get('action_items'), dict):
            p0_count = len(report.get('action_items', {}).get('P0', []))
        else:
            p0_count = len([item for item in report.get('action_items', []) if item.get('priority') == 'P0'])
        st.metric("P0 Items", p0_count)
    
    with col4:
        # Handle different action_items structures
        if isinstance(report.get('action_items'), dict):
            p1_count = len(report.get('action_items', {}).get('P1', []))
        else:
            p1_count = len([item for item in report.get('action_items', []) if item.get('priority') == 'P1'])
        st.metric("P1 Items", p1_count)
    
    st.divider()
    
    # Executive Summary
    st.markdown("### 📝 Summary")
    # Use the correct field name from README structure
    summary = report.get('summary', 'No summary available')
    st.markdown(f"<div class='metric-card'>{summary}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Action Items by Priority
    action_items = report.get('action_items', [])
    if action_items:
        st.markdown("### ✅ Action Items")
        
        # Handle different action_items structures
        if isinstance(action_items, dict):
            # New structure: {"P0": [...], "P1": [...], "P2": [...]}
            p0_items = action_items.get('P0', [])
            p1_items = action_items.get('P1', [])
            p2_items = action_items.get('P2', [])
        else:
            # Old structure: [...]
            p0_items = [item for item in action_items if item.get('priority') == 'P0']
            p1_items = [item for item in action_items if item.get('priority') == 'P1']
            p2_items = [item for item in action_items if item.get('priority') == 'P2']
        
        # P0 Items
        if p0_items:
            st.markdown("#### 🔴 P0 - Critical")
            for item in p0_items:
                title = item.get('title', 'Untitled')
                source = item.get('source', 'Unknown')
                due_date = item.get('due_date', 'Not specified')
                description = item.get('description', item.get('context', 'No description'))
                st.markdown(f"""
                <div class='priority-p0'>
                    <strong>{title}</strong><br>
                    <em>Source:</em> {source}<br>
                    <em>Due:</em> {due_date}<br>
                    <em>Description:</em> {description}
                </div>
                """, unsafe_allow_html=True)
        
        # P1 Items
        if p1_items:
            st.markdown("#### 🟡 P1 - Important")
            for item in p1_items:
                title = item.get('title', 'Untitled')
                source = item.get('source', 'Unknown')
                due_date = item.get('due_date', 'Not specified')
                description = item.get('description', item.get('context', 'No description'))
                st.markdown(f"""
                <div class='priority-p1'>
                    <strong>{title}</strong><br>
                    <em>Source:</em> {source}<br>
                    <em>Due:</em> {due_date}<br>
                    <em>Description:</em> {description}
                </div>
                """, unsafe_allow_html=True)
        
        # P2 Items
        if p2_items:
            st.markdown("#### 🟢 P2 - Nice to Have")
            for item in p2_items:
                title = item.get('title', 'Untitled')
                source = item.get('source', 'Unknown')
                due_date = item.get('due_date', 'Not specified')
                description = item.get('description', item.get('context', 'No description'))
                st.markdown(f"""
                <div class='priority-p2'>
                    <strong>{title}</strong><br>
                    <em>Source:</em> {source}<br>
                    <em>Due:</em> {due_date}<br>
                    <em>Description:</em> {description}
                </div>
                """, unsafe_allow_html=True)
    
    # Data Sources Summary (using updates structure from README)
    updates = report.get('updates', {})
    if updates:
        st.divider()
        st.markdown("### 📊 Data Sources Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            email_items = updates.get('email', {})
            email_count = len(email_items.get('P0', [])) + len(email_items.get('P1', []))
            st.metric("📧 Emails", email_count)
        
        with col2:
            calendar_items = updates.get('calendar', {})
            calendar_count = len(calendar_items.get('P0', [])) + len(calendar_items.get('P1', []))
            st.metric("📅 Calendar Events", calendar_count)
        
        with col3:
            slack_items = updates.get('slack', {})
            slack_count = len(slack_items.get('P0', [])) + len(slack_items.get('P1', []))
            st.metric("💬 Slack Messages", slack_count)

def main():
    # Main header with border
    st.markdown('<div class="header-container"><div class="main-header">OOO Summariser Agent</div><div class="main-subtitle">Automated Out-of-Office Communication Analysis and Action Item Prioritization</div></div>', unsafe_allow_html=True)
    
    # Test case selection section
    st.markdown('<div class="test-cases-header"><h2>Test Cases</h2><p>Select a test case to run the OOO Summariser Agent:</p></div>', unsafe_allow_html=True)
    
    # Test case selection dropdown
    test_case_options = [
        "Select a test case...",
        "Test Case 1 (3-day OOO)",
        "Test Case 2 (7-day OOO)", 
        "Test Case 3 (14-day OOO)",
        "Run All Test Cases"
    ]
    
    selected_test_case = st.selectbox(
        "Select Test Case:",
        options=test_case_options,
        help="Choose a test case to run the OOO Summariser Agent"
    )
    
    # Run button and debug mode checkbox in same row, centered with gap
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col1:
        st.empty()  # Empty space for centering
    
    with col2:
        # Run button and debug checkbox in center column
        button_col, gap_col, checkbox_col = st.columns([2, 0.5, 2])
        
        with checkbox_col:
            # Debug mode checkbox (define first for scope)
            debug_mode = st.checkbox("🐛 Debug Mode", help="Show raw output for troubleshooting")
        
        with gap_col:
            st.empty()  # Gap between button and checkbox
        
        with button_col:
            # Run button
            if st.button("🚀 Run Selected Test Case", disabled=(selected_test_case == "Select a test case...")):
                if selected_test_case == "Test Case 1 (3-day OOO)":
                    with st.spinner("Running Test Case 1..."):
                        report = run_test_case("test_case_1", debug=debug_mode)
                        if report:
                            st.session_state.current_report = report
                            st.session_state.current_test_case = "Test Case 1"
                
                elif selected_test_case == "Test Case 2 (7-day OOO)":
                    with st.spinner("Running Test Case 2..."):
                        report = run_test_case("test_case_2", debug=debug_mode)
                        if report:
                            st.session_state.current_report = report
                            st.session_state.current_test_case = "Test Case 2"
                
                elif selected_test_case == "Test Case 3 (14-day OOO)":
                    with st.spinner("Running Test Case 3..."):
                        report = run_test_case("test_case_3", debug=debug_mode)
                        if report:
                            st.session_state.current_report = report
                            st.session_state.current_test_case = "Test Case 3"
                
                elif selected_test_case == "Run All Test Cases":
                    with st.spinner("Running all test cases..."):
                        reports = run_all_test_cases(debug=debug_mode)
                        if reports:
                            st.session_state.all_reports = reports
                            st.session_state.current_test_case = "All Test Cases"
    
    with col3:
        st.empty()  # Empty space for centering
    
    # Main content area
    
    # Display current report
    if hasattr(st.session_state, 'current_report') and st.session_state.current_report:
        display_report(st.session_state.current_report, st.session_state.current_test_case)
    
    # Display all reports
    elif hasattr(st.session_state, 'all_reports') and st.session_state.all_reports:
        st.markdown("## 📊 All Test Cases Results")
        
        for test_case, report in st.session_state.all_reports.items():
            if report:
                display_report(report, test_case)
                st.markdown("---")
    
    # Default state
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Available Test Cases:**")
            st.markdown("- **Test Case 1**: 3-day OOO period")
            st.markdown("- **Test Case 2**: 7-day OOO period")  
            st.markdown("- **Test Case 3**: 14-day OOO period")
            st.markdown("- **Run All**: Execute all test cases sequentially")
        
        with col2:
            st.markdown("**How to use:**")
            st.markdown("1. 🎯 Select a test case from the dropdown above")
            st.markdown("2. 🚀 Click 'Run Selected Test Case' button")
            st.markdown("3. 📊 View the generated report below")
        
        st.markdown("**Each test case will:**")
        st.markdown("1. 🗄️ Seed the database with relevant data")
        st.markdown("2. 🤖 Run the OOO Summariser Agent")
        st.markdown("3. 📊 Generate a structured JSON report")
        st.markdown("4. 🎨 Render the results")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show sample data structure
        with st.expander("📋 Expected Report Structure"):
            st.json({
                "summary": "Critical production system outage requires immediate attention, along with security vulnerability patches and Q1 planning sessions.",
                "action_items": {
                    "P0": [
                        {
                            "id": "email_001",
                            "title": "CRITICAL: Production System Outage",
                            "due_date": "2024-01-02",
                            "source": "email",
                            "context": "Production API is down and customers are affected. Immediate attention required."
                        }
                    ],
                    "P1": [
                        {
                            "id": "email_005",
                            "title": "Q1 Strategic Planning Session",
                            "due_date": "2024-01-03",
                            "source": "email",
                            "context": "Q1 strategic planning session scheduled. Your input required for roadmap decisions."
                        }
                    ],
                    "P2": []
                },
                "updates": {
                    "email": {
                        "P0": [{"id": "email_001", "title": "Production System Outage Alert", "due_date": "2024-01-02", "source": "email", "context": "Urgent system outage affecting multiple clients."}],
                        "P1": [{"id": "email_005", "title": "Q1 Planning Meeting Invite", "due_date": "2024-01-03", "source": "email", "context": "Strategic planning session for Q1 roadmap."}]
                    },
                    "calendar": {
                        "P0": [{"id": "event_001", "title": "Emergency Incident Response", "due_date": "2024-01-02", "source": "calendar", "context": "Emergency response meeting for production system outage."}],
                        "P1": [{"id": "event_003", "title": "Infrastructure Migration Planning", "due_date": "2024-01-05", "source": "calendar", "context": "Planning session for upcoming infrastructure migration project."}]
                    },
                    "slack": {
                        "P0": [{"id": "slack_001", "title": "Security Vulnerability Alert", "due_date": "2024-01-02", "source": "slack", "context": "Critical security vulnerability detected. Immediate patch deployment required."}],
                        "P1": [{"id": "slack_007", "title": "Client Escalation Discussion", "due_date": "2024-01-04", "source": "slack", "context": "Major client escalation requires technical review and response strategy."}]
                    }
                }
            })

if __name__ == "__main__":
    main()
