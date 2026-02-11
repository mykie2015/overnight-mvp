#!/usr/bin/env python3
"""
Intent-to-Agent Compiler (Simplified)

Reads Context Capsule intent files and generates LangChain agents.
"""

import re
import sys
from pathlib import Path


def parse_intent(filepath):
    """Parse intent file into dict."""
    content = Path(filepath).read_text()
    sections = re.split(r'\n## ', content)
    
    intent = {}
    
    for section in sections:
        if section.startswith("Objective"):
            intent["objective"] = section.split('\n', 1)[1].strip() if '\n' in section else ""
        elif section.startswith("Desired Outcomes"):
            intent["outcomes"] = extract_list(section)
        elif section.startswith("Health Metrics"):
            intent["health_metrics"] = extract_list(section)
        elif section.startswith("Constraints"):
            intent["constraints"] = extract_constraints(section)
        elif section.startswith("Decision Types"):
            intent["decisions"] = extract_decisions(section)
        elif section.startswith("Stop Rules"):
            intent["stop_rules"] = extract_stop_rules(section)
    
    # Extract name
    name_match = re.search(r'# Intent:\s*(.+)', content)
    intent["name"] = name_match.group(1).strip() if name_match else "Unnamed"
    
    return intent


def extract_list(section):
    """Extract bullet list."""
    items = []
    for line in section.split('\n'):
        if line.strip().startswith('-'):
            item = re.sub(r'^-\s*\[.\]\s*', '', line.strip())
            item = re.sub(r'^-\s*', '', item)
            if item:
                items.append(item)
    return items


def extract_constraints(section):
    """Extract steering and hard constraints."""
    constraints = {"steering": [], "hard": []}
    current_type = None
    
    for line in section.split('\n'):
        if 'Steering' in line:
            current_type = "steering"
        elif 'Hard' in line:
            current_type = "hard"
        elif line.strip().startswith('-') and current_type:
            item = re.sub(r'^-\s*', '', line.strip())
            if item:
                constraints[current_type].append(item)
    
    return constraints


def extract_decisions(section):
    """Extract autonomous vs escalation decisions."""
    decisions = {"autonomous": [], "escalate": []}
    current_type = None
    
    for line in section.split('\n'):
        if 'Autonomous' in line:
            current_type = "autonomous"
        elif 'Escalate' in line:
            current_type = "escalate"
        elif line.strip().startswith('-') and current_type:
            item = re.sub(r'^-\s*', '', line.strip())
            if item:
                decisions[current_type].append(item)
    
    return decisions


def extract_stop_rules(section):
    """Extract stop rules."""
    rules = {"complete": [], "escalate": [], "halt": []}
    
    for line in section.split('\n'):
        if 'Complete' in line and ':' in line:
            rules["complete"].append(line.split(':', 1)[1].strip())
        elif 'Escalate' in line and ':' in line:
            rules["escalate"].append(line.split(':', 1)[1].strip())
        elif 'Halt' in line and ':' in line:
            rules["halt"].append(line.split(':', 1)[1].strip())
    
    return rules


def sanitize_name(name):
    """Convert to PascalCase class name."""
    name = re.sub(r'[^\w\s]', '', name)
    words = name.split()
    return ''.join(word.capitalize() for word in words)


def format_list_for_python(items):
    """Format list for Python code."""
    if not items:
        return "[]"
    formatted_items = [f'        "{item}"' for item in items]
    return "[\n" + ",\n".join(formatted_items) + "\n    ]"


def generate_agent(intent):
    """Generate LangChain agent code."""
    class_name = sanitize_name(intent["name"])
    objective = intent.get("objective", "")[:200]
    
    steering = format_list_for_python(intent.get("constraints", {}).get("steering", []))
    hard = format_list_for_python(intent.get("constraints", {}).get("hard", []))
    autonomous = format_list_for_python(intent.get("decisions", {}).get("autonomous", []))
    escalate = format_list_for_python(intent.get("decisions", {}).get("escalate", []))
    
    code = f'''"""
{intent["name"]} Agent

Auto-generated from Context Capsule intent.

Objective: {objective}...
"""

from typing import Dict
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate


class {class_name}Agent:
    """Agent with embedded intent guardrails."""
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0
        )
        
        # Intent-based constraints
        self.steering_constraints = {steering}
        self.hard_constraints = {hard}
        self.autonomous_decisions = {autonomous}
        self.escalation_triggers = {escalate}
        
        # Build agent
        self.agent = self._build_agent()
    
    def _build_agent(self) -> AgentExecutor:
        """Build ReAct agent with intent-aware prompt."""
        
        # Format constraints for prompt
        steering_text = "\\n".join(f"- {{c}}" for c in self.steering_constraints)
        autonomous_text = "\\n".join(f"- {{c}}" for c in self.autonomous_decisions)
        escalate_text = "\\n".join(f"- {{c}}" for c in self.escalation_triggers)
        
        prompt_template = f"""
Objective: {objective}

Steering Constraints:
{{steering_text}}

Autonomous Decisions:
{{autonomous_text}}

Escalation Triggers:
{{escalate_text}}

You have access to the following tools:
{{{{tools}}}}

Tool Names: {{{{tool_names}}}}

Question: {{{{input}}}}

Thought: {{{{agent_scratchpad}}}}
"""
        
        prompt = PromptTemplate.from_template(prompt_template)
        
        # Placeholder tools
        tools = [
            Tool(
                name="PlaceholderTool",
                func=lambda x: f"Processed: {{x}}",
                description="Placeholder - replace with actual tools"
            )
        ]
        
        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=5
        )
    
    def run(self, input_text: str) -> Dict:
        """Run agent with guardrail checks."""
        
        # Check escalation triggers
        for trigger in self.escalation_triggers:
            if trigger.lower() in input_text.lower():
                return {{
                    "output": None,
                    "status": "escalate",
                    "reason": f"Escalation trigger: {{trigger}}"
                }}
        
        # Run agent
        try:
            result = self.agent.invoke({{"input": input_text}})
            return {{
                "output": result["output"],
                "status": "complete",
                "reason": "Task completed"
            }}
        except Exception as e:
            return {{
                "output": None,
                "status": "error",
                "reason": str(e)
            }}


if __name__ == "__main__":
    agent = {class_name}Agent()
    
    # Example usage
    result = agent.run("Test input")
    print(f"Status: {{result['status']}}")
    print(f"Output: {{result.get('output', 'N/A')}}")
'''
    
    return code


def compile_intent(intent_file, output_file):
    """Compile intent to agent."""
    intent = parse_intent(intent_file)
    code = generate_agent(intent)
    
    Path(output_file).write_text(code)
    print(f"✅ Generated: {output_file}")
    print(f"   Intent: {intent['name']}")
    print(f"   Outcomes: {len(intent.get('outcomes', []))}")
    print(f"   Constraints: {len(intent.get('constraints', {}).get('steering', []))} steering, {len(intent.get('constraints', {}).get('hard', []))} hard")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: intent_to_agent_simple.py <intent.md> <output.py>")
        sys.exit(1)
    
    compile_intent(sys.argv[1], sys.argv[2])
