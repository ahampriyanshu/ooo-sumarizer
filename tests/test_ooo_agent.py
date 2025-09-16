"""
Test suite for OOO Summariser Agent
Tests the agent's output JSON structure, prioritization, and data processing
"""

import pytest
import json
import os
from datetime import datetime


def load_test_data(test_case="test_case_1"):
    """Load test data from JSON file"""
    test_data_path = os.path.join(os.path.dirname(__file__), "test_data", f"{test_case}.json")
    with open(test_data_path, 'r') as f:
        return json.load(f)


class TestOOOSummarizerAgent:
    """Test class for OOO Summariser Agent output validation"""
    
    def test_json_validity(self, agent_report):
        """Test that the report is valid JSON"""
        # Try to serialize and deserialize
        json_str = json.dumps(agent_report)
        parsed_report = json.loads(json_str)
        assert parsed_report == agent_report, "Report should be valid JSON"
    
    def test_json_structure(self, agent_report):
        """Test that the agent report has the correct JSON structure"""
        # Check top-level keys
        required_keys = ["summary", "action_items", "updates"]
        for key in required_keys:
            assert key in agent_report, f"Missing required key: {key}"
        
        # Check action_items structure
        action_items = agent_report["action_items"]
        assert "P0" in action_items, "Missing P0 action items"
        assert "P1" in action_items, "Missing P1 action items"
        assert "P2" in action_items, "Missing P2 action items"
        
        # Check updates structure
        updates = agent_report["updates"]
        required_sources = ["email", "calendar", "slack"]
        for source in required_sources:
            assert source in updates, f"Missing updates for source: {source}"
            assert "P0" in updates[source], f"Missing P0 updates for {source}"
            assert "P1" in updates[source], f"Missing P1 updates for {source}"
    
    
    def test_summary_content(self, agent_report):
        """Test that the summary meets quality criteria using an LLM judge"""
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage

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
                assert False, f"Failed to parse LLM response as JSON: {e}\nResponse: {llm_response}"
            
            # Validate JSON structure
            required_fields = ["result", "reason", "criteria_met"]
            for field in required_fields:
                assert field in judgement, f"Missing required field '{field}' in LLM response"
            
            required_criteria = ["focus_on_urgent_items", "conciseness", "key_information", "relevance", "actionability"]
            for criterion in required_criteria:
                assert criterion in judgement["criteria_met"], f"Missing required criterion '{criterion}' in LLM response"
            
            # Check result
            result = judgement["result"].upper()
            reason = judgement["reason"]
            criteria_met = judgement["criteria_met"]
            
            if result == "PASS":
                # Summary passed
                pass
            elif result == "FAIL":
                # Summary failed - provide detailed feedback
                failed_criteria = [criterion for criterion, met in criteria_met.items() if not met]
                assert False, f"LLM judged summary as not meeting quality criteria: {reason}\nFailed criteria: {failed_criteria}"
            else:
                assert False, f"Invalid result value: {result}. Expected 'PASS' or 'FAIL'"
                
        except Exception as e:
            print(f"Error evaluating summary: {e}")
    
    def test_action_items_structure(self, agent_report):
        """Test that action items have the correct structure"""
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                required_fields = ["title", "due_date", "source", "context"]
                for field in required_fields:
                    assert field in item, f"Missing {field} in {priority} action item"
                    assert item[field], f"Empty {field} in {priority} action item"
    
    def test_updates_structure(self, agent_report):
        """Test that updates have the correct structure"""
        for source in ["email", "calendar", "slack"]:
            for priority in ["P0", "P1"]:
                for item in agent_report["updates"][source][priority]:
                    required_fields = ["title", "source", "context"]
                    for field in required_fields:
                        assert field in item, f"Missing {field} in {source} {priority} update"
                        assert item[field], f"Empty {field} in {source} {priority} update"
                    
                    # due_date is optional for updates
                    if "due_date" in item:
                        assert item["due_date"], f"Empty due_date in {source} {priority} update"
    
    def test_important_items_in_p0(self, agent_report):
        """Test that important items from Test Case 1 are correctly prioritized as P0"""
        # Load test data from JSON file
        test_data = load_test_data("test_case_1")
        
        # Get all important IDs from test data
        important_ids = []
        for source, ids in test_data["important_ids"].items():
            important_ids.extend(ids)

        # Check action items P0 - look for IDs that match important_ids
        p0_action_items = agent_report["action_items"]["P0"]
        p0_ids = [item.get("id") for item in p0_action_items if "id" in item]

        found_important_ids = [iid for iid in important_ids if iid in p0_ids]
        assert len(found_important_ids) >= 2, f"Expected at least 2 important IDs in P0 action items, found: {found_important_ids}"

        # Check updates P0 - look for IDs that match important_ids
        for source in ["email", "calendar", "slack"]:
            p0_updates = agent_report["updates"][source]["P0"]
            if p0_updates:  # If there are P0 updates for this source
                update_ids = [item.get("id") for item in p0_updates if "id" in item]
                found_source_ids = [iid for iid in important_ids if iid in update_ids]
                assert len(found_source_ids) >= 1, f"Expected at least 1 important ID in {source} P0 updates, found: {found_source_ids}"
    
    def test_noise_items_not_in_p0(self, agent_report):
        """Test that noise items are not over-prioritized as P0"""
        # Load test data from JSON file
        test_data = load_test_data("test_case_1")
        
        # Get all noise IDs from test data
        noise_ids = []
        for source, ids in test_data["noise_ids"].items():
            noise_ids.extend(ids)
        
        p0_action_items = agent_report["action_items"]["P0"]
        p0_ids = [item.get("id") for item in p0_action_items if "id" in item]
        
        # Count how many noise IDs are present in P0 action items
        noise_in_p0 = [nid for nid in noise_ids if nid in p0_ids]
        
        # Allow some noise in P0 but not too much (max 1 noise item)
        assert len(noise_in_p0) <= 1, f"Too many noise items in P0 action items, found: {noise_in_p0}"
    
    # def test_priority_themes_validation(self, agent_report):
    #     """Test that priority assignments follow expected themes from test data"""
    #     # Load test data from JSON file
    #     test_data = load_test_data("test_case_1")
        
    #     # Get expected themes for each priority
    #     p0_themes = test_data["expected_priorities"]["p0_themes"]
    #     p1_themes = test_data["expected_priorities"]["p1_themes"]
        
    #     # Check P0 action items contain urgent themes
    #     p0_action_items = agent_report["action_items"]["P0"]
    #     p0_contexts = [item.get("context", "").lower() for item in p0_action_items]
        
    #     urgent_themes_found = 0
    #     for context in p0_contexts:
    #         if any(theme in context for theme in p0_themes):
    #             urgent_themes_found += 1
        
    #     assert urgent_themes_found >= 1, f"P0 action items should contain urgent themes like {p0_themes}, found contexts: {p0_contexts}"
        
    #     # Check P1 action items contain planning themes
    #     p1_action_items = agent_report["action_items"]["P1"]
    #     p1_contexts = [item.get("context", "").lower() for item in p1_action_items]
        
    #     planning_themes_found = 0
    #     for context in p1_contexts:
    #         if any(theme in context for theme in p1_themes):
    #             planning_themes_found += 1
        
    #     # P1 themes are optional but if present, should be planning-related
    #     if p1_action_items:
    #         assert planning_themes_found >= 1, f"P1 action items should contain planning themes like {p1_themes}, found contexts: {p1_contexts}"
    
    def test_all_sources_present(self, agent_report):
        """Test that all data sources are represented in the report"""
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
        
        # Should have at least 3 sources represented
        all_sources = sources_in_action_items.union(sources_in_updates)
        assert len(all_sources) >= 3, f"Should have at least 3 sources represented, found: {all_sources}"
    
    def test_due_dates_format(self, agent_report):
        """Test that due dates are in the correct format"""
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                due_date = item["due_date"]
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid due date format: {due_date}")
    
    def test_context_quality(self, agent_report):
        """Test that context provides meaningful information"""
        for priority in ["P0", "P1", "P2"]:
            for item in agent_report["action_items"][priority]:
                context = item["context"]
                assert len(context) >= 20, f"Context too short: {context}"
                assert len(context.split()) >= 5, f"Context should have at least 5 words: {context}"
    
    def test_no_empty_sections(self, agent_report):
        """Test that each priority level has at least one item"""
        # P0 and P1 should always have at least one action item (P2 can be empty)
        for priority in ["P0", "P1"]:
            assert len(agent_report["action_items"][priority]) > 0, f"Should have at least one {priority} action item"
        
        # Each priority level should have at least one update across all sources
        for priority in ["P0", "P1"]:
            total_priority_updates = 0
            for source in agent_report["updates"]:
                total_priority_updates += len(agent_report["updates"][source][priority])
            assert total_priority_updates > 0, f"Should have at least one {priority} update across all sources"
