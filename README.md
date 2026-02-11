# Skill to LangChain Converter

Reusable converter that transforms OpenClaw skills (SKILL.md) into LangChain agents.

## The Converter

`skill_to_langchain.py` - The main converter script (reusable for any skill)

## Usage

```bash
# Convert the example skill
python3 skill_to_langchain.py example-skill/SKILL.md

# Convert any skill
python3 skill_to_langchain.py path/to/your/SKILL.md
```

Output will be generated in `output/{skill_name}_agent.py`

## Example

**Input**: `example-skill/SKILL.md` (GitHub skill)
- YAML frontmatter with metadata
- Bash commands for `gh` CLI operations

**Output**: `output/github_agent.py`
- LangChain ReAct agent
- Tools wrapping each command
- Claude Sonnet as reasoning engine

## How It Works

1. **Parse SKILL.md**: Extract YAML frontmatter (name, description) and bash code blocks
2. **Generate Tools**: Convert each bash command into a LangChain Tool
3. **Create Agent**: Wrap tools in ReAct agent with Claude Sonnet
4. **Output Python**: Standalone runnable agent file

## Test

```bash
python3 test_converter.py
```

## Key Features

✅ **Reusable**: Works with any OpenClaw skill
✅ **TDD**: 5 passing unit tests
✅ **Preserves Logic**: Exact commands from SKILL.md → LangChain tools
✅ **Error Handling**: Timeouts, exit codes, exceptions
✅ **Standalone Output**: Generated agents run independently

## Files

- `skill_to_langchain.py` - **The converter (main deliverable)**
- `test_converter.py` - Test suite
- `example-skill/SKILL.md` - Example input (GitHub skill)
- `output/github_agent.py` - Example output (generated)

## Feasibility: PROVEN

Successfully converts GitHub skill (6 bash commands) to runnable LangChain agent.
