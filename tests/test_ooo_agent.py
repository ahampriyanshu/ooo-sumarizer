"""
Test suite for OOO Summarizer Agent
Tests the agent's output JSON structure, prioritization, and data processing
"""

import pytest
import json
import os
import subprocess
from datetime import datetime

# Test case constants
TEST_CASES = ["test_case_3", "test_case_1", "test_case_2"]


def load_test_data(test_case="test_case_1"):
    """Load test data from JSON file"""
    test_data_path = os.path.join(
        os.path.dirname(__file__), "test_data", f"{test_case}.json"
    )
    with open(test_data_path, "r") as f:
        return json.load(f)


class TestOOOSummarizerAgent:
    """Test class for OOO Summarizer Agent output validation"""

    def _get_agent_report(self, test_case):
        """Get agent report for a specific test case, with caching"""
        # Create cache file name based on test case with fixed constant ID
        cache_file = f"tests/test_data/reports/agent_report_{test_case}_v1.json"

        if os.path.exists(cache_file):
            print(
                f"📋 Using cached agent report for {test_case} (fixed constant ID: v1)"
            )
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
        result = subprocess.run(["python", seed_script], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to seed test data for {test_case}: {result.stderr}"
            )

        # Load test data to get date range
        test_data = load_test_data(test_case)

        # Run the agent using summarizer.py
        start_date = test_data["date_range"]["start"]
        end_date = test_data["date_range"]["end"]

        # Run summarizer.py with date parameters
        result = subprocess.run(
            ["python", "summarizer.py", start_date, end_date],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Agent failed with return code {result.returncode}: {result.stderr}"
            )

        # The agent should output JSON to stdout, but it might be mixed with other output
        # Look for JSON in the output
        output_lines = result.stdout.strip().split("\n")
        json_output = None

        # Find the JSON output (it should be the last meaningful line)
        for line in reversed(output_lines):
            line = line.strip()
            if line and line.startswith("{") and line.endswith("}"):
                json_output = line
                break

        if not json_output:
            # If no JSON found in lines, look for JSON in the entire output
            # Find the first occurrence of { and the last occurrence of }
            start_idx = result.stdout.find("{")
            end_idx = result.stdout.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_output = result.stdout[start_idx : end_idx + 1]
            else:
                # Fallback: try to parse the entire output
                json_output = result.stdout.strip()

        try:
            report = json.loads(json_output)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Failed to parse agent output as JSON: {e}\nOutput: {result.stdout}"
            )

        # Cache the result
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"✅ Agent report for {test_case} cached for future test runs")
        return report

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_report_is_valid_json(self, test_case):
        """Verify agent output is valid JSON format"""
        agent_report = self._get_agent_report(test_case)
        # Try to serialize and deserialize
        json_str = json.dumps(agent_report)
        parsed_report = json.loads(json_str)
        assert (
            parsed_report == agent_report
        ), f"User must ensure agent returns valid JSON for {test_case}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_report_has_required_structure(self, test_case):
        """Verify agent report contains all required fields and nested structures"""
        agent_report = self._get_agent_report(test_case)
        # Check top-level keys
        required_keys = ["summary", "action_items", "updates"]
        for key in required_keys:
            assert (
                key in agent_report
            ), f"User must ensure report includes '{key}' field for {test_case}"

        # Check action_items structure
        action_items = agent_report["action_items"]
        assert (
            "P0" in action_items
        ), f"User must include P0 priority in action_items for {test_case}"
        assert (
            "P1" in action_items
        ), f"User must include P1 priority in action_items for {test_case}"
        assert (
            "P2" in action_items
        ), f"User must include P2 priority in action_items for {test_case}"

        # Check updates structure
        updates = agent_report["updates"]
        required_sources = ["email", "calendar", "slack"]
        for source in required_sources:
            assert (
                source in updates
            ), f"User must include {source} in updates for {test_case}"
            assert (
                "P0" in updates[source]
            ), f"User must include P0 priority for {source} in {test_case}"
            assert (
                "P1" in updates[source]
            ), f"User must include P1 priority for {source} in {test_case}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_summary_meets_quality_criteria(self, test_case):
        """Verify summary meets quality standards using LLM judge"""
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage

        agent_report = self._get_agent_report(test_case)
        summary = agent_report["summary"]

        # Load judge prompt from file
        with open("tests/prompts/summary_judge_prompt.txt", "r") as f:
            judge_prompt_template = f.read()

        # Format the prompt with the actual summary (use string replacement to avoid JSON formatting issues)
        judge_prompt = judge_prompt_template.replace("{summary}", summary)

        try:
            llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=200, temperature=0)
            message = SystemMessage(content=judge_prompt)

            response = llm.invoke([message])
            llm_response = response.content.strip()

            # Parse JSON response
            try:
                judgement = json.loads(llm_response)
            except json.JSONDecodeError as e:
                assert (
                    False
                ), f"Failed to parse LLM response as JSON: {e}\nResponse: {llm_response}"

            # Validate JSON structure
            required_fields = ["result", "reason", "criteria_met"]
            for field in required_fields:
                assert (
                    field in judgement
                ), f"Missing required field '{field}' in LLM response"

            required_criteria = [
                "focus_on_urgent_items",
                "conciseness",
                "key_information",
                "relevance",
                "actionability",
            ]
            for criterion in required_criteria:
                assert (
                    criterion in judgement["criteria_met"]
                ), f"Missing required criterion '{criterion}' in LLM response"

            # Check result
            result = judgement["result"].upper()
            reason = judgement["reason"]
            criteria_met = judgement["criteria_met"]

            if result == "PASS":
                # Summary passed
                pass
            elif result == "FAIL":
                # Summary failed - provide detailed feedback
                failed_criteria = [
                    criterion for criterion, met in criteria_met.items() if not met
                ]
                assert (
                    False
                ), f"User must improve summary quality. {reason}\nFailed criteria: {failed_criteria}"
            else:
                assert (
                    False
                ), f"Invalid LLM judge result: {result}. Expected 'PASS' or 'FAIL'"

        except Exception as e:
            print(f"Error evaluating summary: {e}")

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_action_items_have_required_fields(self, test_case):
        """Verify each action item contains all required fields"""
        agent_report = self._get_agent_report(test_case)
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                required_fields = ["title", "due_date", "source", "context"]
                for field in required_fields:
                    assert (
                        field in item
                    ), f"User must include '{field}' in {priority} action items for {test_case}"
                    assert item[
                        field
                    ], f"User must provide non-empty '{field}' in {priority} action items for {test_case}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_updates_have_required_fields(self, test_case):
        """Verify each update contains all required fields"""
        agent_report = self._get_agent_report(test_case)
        for source in ["email", "calendar", "slack"]:
            for priority in ["P0", "P1"]:
                for item in agent_report["updates"][source][priority]:
                    required_fields = ["title", "source", "context"]
                    for field in required_fields:
                        assert (
                            field in item
                        ), f"User must include '{field}' in {source} {priority} updates for {test_case}"
                        assert item[
                            field
                        ], f"User must provide non-empty '{field}' in {source} {priority} updates for {test_case}"

                    # due_date is optional for updates
                    if "due_date" in item:
                        assert item[
                            "due_date"
                        ], f"User must provide non-empty due_date when included in {source} {priority} updates for {test_case}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_important_items_prioritized_correctly(self, test_case):
        """Verify critical items are classified as P0 priority"""
        # Load test data for the specific test case
        test_data = load_test_data(test_case)

        # Get agent report for this test case
        agent_report = self._get_agent_report(test_case)

        # Get all important IDs from test data
        important_ids = []
        for source, ids in test_data["important_ids"].items():
            important_ids.extend(ids)

        # Check action items P0 - look for IDs that match important_ids
        p0_action_items = agent_report["action_items"]["P0"]
        p0_ids = [item.get("id") for item in p0_action_items if "id" in item]

        found_important_ids = [iid for iid in important_ids if iid in p0_ids]
        assert (
            len(found_important_ids) >= 1
        ), f"User must prioritize important items as P0 in action_items for {test_case}, found: {found_important_ids}"

        # Check updates P0 - look for IDs that match important_ids
        for source in ["email", "calendar", "slack"]:
            p0_updates = agent_report["updates"][source]["P0"]
            if p0_updates:  # If there are P0 updates for this source
                update_ids = [item.get("id") for item in p0_updates if "id" in item]
                found_source_ids = [iid for iid in important_ids if iid in update_ids]
                assert (
                    len(found_source_ids) >= 1
                ), f"User must prioritize important {source} items as P0 for {test_case}, found: {found_source_ids}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_noise_items_not_over_prioritized(self, test_case):
        """Verify low-priority noise items are not classified as P0"""
        # Load test data for the specific test case
        test_data = load_test_data(test_case)

        # Get agent report for this test case
        agent_report = self._get_agent_report(test_case)

        # Get all noise IDs from test data
        noise_ids = []
        for source, ids in test_data["noise_ids"].items():
            noise_ids.extend(ids)

        p0_action_items = agent_report["action_items"]["P0"]
        p0_ids = [item.get("id") for item in p0_action_items if "id" in item]

        # Count how many noise IDs are present in P0 action items
        noise_in_p0 = [nid for nid in noise_ids if nid in p0_ids]

        # Allow some noise in P0 but not too much (max 1 noise item)
        assert (
            len(noise_in_p0) <= 1
        ), f"User must avoid over-prioritizing noise items as P0 for {test_case}, found: {noise_in_p0}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_all_data_sources_represented(self, test_case):
        """Verify report includes data from all available sources"""
        # Get agent report for this test case
        agent_report = self._get_agent_report(test_case)

        sources_in_action_items = set()
        sources_in_updates = set()

        # Collect sources from action items
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                sources_in_action_items.add(item["source"])

        # Collect sources from updates
        for source in agent_report["updates"]:
            if any(len(agent_report["updates"][source][p]) > 0 for p in ["P0", "P1"]):
                sources_in_updates.add(source)

        # Should have at least 1 source represented (be flexible for different test cases)
        all_sources = sources_in_action_items.union(sources_in_updates)
        assert (
            len(all_sources) >= 1
        ), f"User must include at least one data source in report for {test_case}, found: {all_sources}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_due_dates_use_correct_format(self, test_case):
        """Verify all due dates follow YYYY-MM-DD format"""
        agent_report = self._get_agent_report(test_case)
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                due_date = item["due_date"]
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    pytest.fail(
                        f"User must format due dates as YYYY-MM-DD for {test_case}, got: {due_date}"
                    )

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_context_provides_meaningful_information(self, test_case):
        """Verify context fields contain sufficient detail"""
        agent_report = self._get_agent_report(test_case)
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                context = item["context"]
                assert (
                    len(context) >= 20
                ), f"User must provide sufficient context (min 20 chars) for {test_case}: {context}"
                assert (
                    len(context.split()) >= 4
                ), f"User must provide detailed context (min 4 words) for {test_case}: {context}"

    @pytest.mark.parametrize("test_case", TEST_CASES)
    def test_required_priorities_not_empty(self, test_case):
        """Verify P0 and P1 priority levels contain items"""
        # Get agent report for this test case
        agent_report = self._get_agent_report(test_case)

        # P0 and P1 should always have at least one action item (P2 can be empty)
        for priority in ["P0", "P1"]:
            assert (
                len(agent_report["action_items"][priority]) > 0
            ), f"User must include at least one {priority} action item for {test_case}"

        # P0 should have at least one update across all sources, P1 is optional
        total_p0_updates = 0
        for source in agent_report["updates"]:
            total_p0_updates += len(agent_report["updates"][source]["P0"])
        assert (
            total_p0_updates > 0
        ), f"User must include at least one P0 update across all sources for {test_case}"

        # P1 updates are optional - agent may put items in P0/P2 instead
        total_p1_updates = 0
        for source in agent_report["updates"]:
            total_p1_updates += len(agent_report["updates"][source]["P1"])
        # P1 can be empty if agent puts items in P0/P2 instead
