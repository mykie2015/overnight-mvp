"""
Skill to LangChain Agent Converter

Converts OpenClaw skills (SKILL.md format) into LangChain agent Python code.
Uses real GitHub skill as example.
"""

import re
from pathlib import Path
from typing import Dict, List


def parse_skill_md(skill_path: str) -> Dict:
    """
    Parse SKILL.md and extract metadata, description, and code blocks.
    
    Args:
        skill_path: Path to SKILL.md file
        
    Returns:
        Dict with 'metadata', 'tools', and 'raw_content' keys
    """
    content = Path(skill_path).read_text()
    
    # Extract YAML frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    metadata = {}
    
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # Extract name
        name_match = re.search(r'name:\s*(\S+)', frontmatter)
        if name_match:
            metadata['name'] = name_match.group(1)
        
        # Extract description (handle quoted strings)
        desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip('"\'')
    
    # Extract code blocks (bash commands)
    code_blocks = re.findall(r'```bash\n(.*?)\n```', content, re.DOTALL)
    
    # Extract commands and context
    tools = []
    for block in code_blocks:
        lines = block.strip().split('\n')
        
        for line in lines:
            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue
            
            # Extract command
            command = line.strip()
            if command:
                # Look for description in preceding comments
                description = f"Execute: {command[:50]}..."
                tools.append({
                    'command': command,
                    'description': description
                })
    
    return {
        'metadata': metadata,
        'tools': tools,
        'raw_content': content
    }


def generate_langchain_agent(skill_data: Dict, output_path: str) -> str:
    """
    Generate LangChain agent Python code from parsed skill data.
    
    Args:
        skill_data: Parsed skill data from parse_skill_md
        output_path: Where to write the generated agent code
        
    Returns:
        Generated Python code as string
    """
    name = skill_data['metadata'].get('name', 'unknown')
    description = skill_data['metadata'].get('description', 'No description')
    tools = skill_data['tools']
    
    # Generate Python code
    code = f'''"""
LangChain Agent: {name}

Auto-generated from OpenClaw skill.
Description: {description}
"""

import subprocess
from typing import Optional
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic


def run_shell_command(command: str) -> str:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip() or "Command executed successfully"
        else:
            return f"Error (exit {{result.returncode}}): {{result.stderr}}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {{str(e)}}"


# Define tools based on skill commands
tools = [
'''
    
    # Add each tool (limit to first 5 for MVP)
    for i, tool in enumerate(tools[:5]):
        tool_name = f"{name}_tool_{i+1}"
        cmd = tool['command'].replace('"', '\\"')  # Escape quotes
        desc = tool['description'].replace('"', '\\"')
        
        code += f'''    Tool(
        name="{tool_name}",
        func=lambda x, cmd="{cmd}": run_shell_command(cmd),
        description="{desc}"
    ),
'''
    
    code += ''']

# Create agent prompt
prompt = PromptTemplate.from_template("""
You are a helpful assistant with access to {skill_name} tools.

Available tools:
{{tools}}

Tool names: {{tool_names}}

Question: {{input}}

Thought: {{agent_scratchpad}}
""".replace('{skill_name}', name))

# Initialize LLM (using Claude)
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0)

# Create agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


def query(question: str) -> str:
    """Query the agent with a question."""
    try:
        result = agent_executor.invoke({"input": question})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Test the agent
    print(f"Testing {name} agent...")
    response = query("What can you help me with?")
    print(f"\\nResponse: {response}")
'''
    
    # Write to file
    Path(output_path).write_text(code)
    return code


def main():
    """Main conversion workflow."""
    print("🔄 Skill to LangChain Converter\\n")
    
    # Parse GitHub skill
    skill_path = "/app/skills/github/SKILL.md"
    print(f"📖 Parsing skill: {skill_path}")
    skill_data = parse_skill_md(skill_path)
    
    print(f"✅ Found skill: {skill_data['metadata'].get('name', 'unknown')}")
    print(f"📝 Description: {skill_data['metadata'].get('description', 'N/A')}")
    print(f"🔧 Extracted {len(skill_data['tools'])} tools\\n")
    
    # Generate LangChain agent
    output_path = "/home/node/.openclaw/workspace/repos/skill-to-langchain-converter/github_agent.py"
    print(f"🏗️  Generating LangChain agent: {output_path}")
    generate_langchain_agent(skill_data, output_path)
    
    print(f"✅ Agent generated successfully!")
    print(f"\\n📦 Output: {output_path}")


if __name__ == "__main__":
    main()
