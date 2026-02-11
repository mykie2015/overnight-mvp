"""
Test suite for skill-to-langchain converter

Tests the conversion of OpenClaw skills to LangChain agents.
"""

import unittest
import os
from pathlib import Path


class TestSkillParser(unittest.TestCase):
    """Test SKILL.md parsing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_skill_content = '''---
name: github
description: "Interact with GitHub using the `gh` CLI."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] }
      }
  }
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub.

## Pull Requests

Check CI status on a PR:

```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:

```bash
gh run list --repo owner/repo --limit 10
```
'''
        self.test_skill_path = '/tmp/test_skill.md'
        Path(self.test_skill_path).write_text(self.test_skill_content)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_skill_path):
            os.remove(self.test_skill_path)
    
    def test_parse_skill_extracts_name(self):
        """Test that parser extracts skill name from frontmatter."""
        from skill_to_langchain import parse_skill_md
        result = parse_skill_md(self.test_skill_path)
        self.assertEqual(result['metadata']['name'], 'github')
    
    def test_parse_skill_extracts_description(self):
        """Test that parser extracts description."""
        from skill_to_langchain import parse_skill_md
        result = parse_skill_md(self.test_skill_path)
        self.assertIn('GitHub', result['metadata']['description'])
    
    def test_parse_skill_extracts_commands(self):
        """Test that parser extracts bash commands."""
        from skill_to_langchain import parse_skill_md
        result = parse_skill_md(self.test_skill_path)
        self.assertGreater(len(result['tools']), 0)
        # Should find at least the gh pr checks command
        commands = [t['command'] for t in result['tools']]
        self.assertTrue(any('gh pr checks' in cmd for cmd in commands))


class TestAgentGeneration(unittest.TestCase):
    """Test LangChain agent code generation."""
    
    def test_generate_agent_creates_valid_python(self):
        """Test that generated agent code is valid Python."""
        from skill_to_langchain import generate_langchain_agent
        
        skill_data = {
            'metadata': {'name': 'test', 'description': 'Test skill'},
            'tools': [
                {'command': 'echo "hello"', 'description': 'Print hello'}
            ]
        }
        
        output_path = '/tmp/test_agent.py'
        code = generate_langchain_agent(skill_data, output_path)
        
        # Should be valid Python (no syntax errors)
        try:
            compile(code, output_path, 'exec')
            valid = True
        except SyntaxError:
            valid = False
        
        self.assertTrue(valid, "Generated code should be valid Python")
        
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)
    
    def test_generate_agent_includes_tools(self):
        """Test that generated agent includes tool definitions."""
        from skill_to_langchain import generate_langchain_agent
        
        skill_data = {
            'metadata': {'name': 'test', 'description': 'Test skill'},
            'tools': [
                {'command': 'echo "hello"', 'description': 'Print hello'}
            ]
        }
        
        output_path = '/tmp/test_agent.py'
        code = generate_langchain_agent(skill_data, output_path)
        
        self.assertIn('Tool(', code)
        self.assertIn('echo', code)
        self.assertIn('hello', code)
        
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)


if __name__ == '__main__':
    unittest.main()
