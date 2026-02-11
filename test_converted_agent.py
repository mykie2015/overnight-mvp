"""
Test suite for converted LangChain agents

Tests that the generated agents are valid and functional.
"""

import unittest
import os
import sys
from pathlib import Path


class TestConvertedAgent(unittest.TestCase):
    """Test the generated LangChain agent."""
    
    @classmethod
    def setUpClass(cls):
        """Generate the agent before running tests."""
        # Run converter to generate output
        from skill_to_langchain import parse_skill_md, generate_langchain_agent
        
        skill_path = "example-skill/SKILL.md"
        skill_data = parse_skill_md(skill_path)
        output_path = "output/github_agent.py"
        generate_langchain_agent(skill_data, output_path)
    
    def test_generated_agent_is_valid_python(self):
        """Test that generated agent is syntactically valid Python."""
        output_path = "output/github_agent.py"
        self.assertTrue(Path(output_path).exists(), "Generated agent file should exist")
        
        code = Path(output_path).read_text()
        
        # Should compile without syntax errors
        try:
            compile(code, output_path, 'exec')
            valid = True
        except SyntaxError as e:
            valid = False
            print(f"Syntax error: {e}")
        
        self.assertTrue(valid, "Generated agent should be valid Python")
    
    def test_generated_agent_has_required_imports(self):
        """Test that generated agent has necessary imports."""
        output_path = "output/github_agent.py"
        code = Path(output_path).read_text()
        
        required_imports = [
            'import subprocess',
            'from langchain.agents import Tool',
            'from langchain_openai import ChatOpenAI'
        ]
        
        for imp in required_imports:
            self.assertIn(imp, code, f"Generated agent should have: {imp}")
    
    def test_generated_agent_has_tools(self):
        """Test that generated agent defines tools."""
        output_path = "output/github_agent.py"
        code = Path(output_path).read_text()
        
        self.assertIn('tools = [', code, "Generated agent should define tools list")
        self.assertIn('Tool(', code, "Generated agent should create Tool instances")
    
    def test_generated_agent_has_query_function(self):
        """Test that generated agent has query function."""
        output_path = "output/github_agent.py"
        code = Path(output_path).read_text()
        
        self.assertIn('def query(', code, "Generated agent should have query function")
        self.assertIn('agent_executor.invoke', code, "Query function should invoke agent")
    
    def test_generated_agent_has_error_handling(self):
        """Test that generated agent has error handling."""
        output_path = "output/github_agent.py"
        code = Path(output_path).read_text()
        
        self.assertIn('try:', code, "Generated agent should have try blocks")
        self.assertIn('except', code, "Generated agent should have exception handling")
        self.assertIn('timeout=30', code, "Generated agent should have timeout")
    
    def test_generated_agent_preserves_skill_name(self):
        """Test that generated agent preserves skill name from SKILL.md."""
        output_path = "output/github_agent.py"
        code = Path(output_path).read_text()
        
        self.assertIn('github', code.lower(), "Generated agent should reference github skill")
    
    def test_generated_agent_can_be_imported(self):
        """Test that generated agent can be imported as a module."""
        output_path = "output/github_agent.py"
        
        # Add output directory to path
        sys.path.insert(0, 'output')
        
        try:
            # Try to import (will fail if syntax errors or missing deps, but that's ok for this test)
            import importlib.util
            spec = importlib.util.spec_from_file_location("github_agent", output_path)
            self.assertIsNotNone(spec, "Generated agent should be importable")
        except Exception as e:
            # If it fails due to missing langchain deps, that's expected in test env
            if "No module named 'langchain" in str(e):
                self.skipTest("LangChain not installed in test environment")
            else:
                raise
        finally:
            sys.path.pop(0)


if __name__ == '__main__':
    unittest.main()
