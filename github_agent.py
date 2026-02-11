"""
LangChain Agent: github

Auto-generated from OpenClaw skill.
Description: Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.
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
            return f"Error (exit {result.returncode}): {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


# Define tools based on skill commands
tools = [
    Tool(
        name="github_tool_1",
        func=lambda x, cmd="gh pr checks 55 --repo owner/repo": run_shell_command(cmd),
        description="Execute: gh pr checks 55 --repo owner/repo..."
    ),
    Tool(
        name="github_tool_2",
        func=lambda x, cmd="gh run list --repo owner/repo --limit 10": run_shell_command(cmd),
        description="Execute: gh run list --repo owner/repo --limit 10..."
    ),
    Tool(
        name="github_tool_3",
        func=lambda x, cmd="gh run view <run-id> --repo owner/repo": run_shell_command(cmd),
        description="Execute: gh run view <run-id> --repo owner/repo..."
    ),
    Tool(
        name="github_tool_4",
        func=lambda x, cmd="gh run view <run-id> --repo owner/repo --log-failed": run_shell_command(cmd),
        description="Execute: gh run view <run-id> --repo owner/repo --log-faile..."
    ),
    Tool(
        name="github_tool_5",
        func=lambda x, cmd="gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'": run_shell_command(cmd),
        description="Execute: gh api repos/owner/repo/pulls/55 --jq '.title, .st..."
    ),
]

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
    print(f"\nResponse: {response}")
