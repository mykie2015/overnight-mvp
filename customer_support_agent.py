"""
Customer Support Agent (Example) Agent

Auto-generated from Context Capsule intent.

Objective: Help customers resolve Tier-1 technical issues without frustration so they can get back to work quickly and maintain trust in our product....
"""

from typing import Dict
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate


class CustomerSupportAgentExampleAgent:
    """Agent with embedded intent guardrails."""
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0
        )
        
        # Intent-based constraints
        self.steering_constraints = [
        "Prioritize clarity over technical accuracy when explaining solutions",
        "Use simple language, avoid jargon unless customer demonstrates technical knowledge",
        "Acknowledge frustration empathetically before diving into solutions",
        "Provide step-by-step instructions, not just links"
    ]
        self.hard_constraints = [
        "Never access customer payment information",
        "Maximum 3 knowledge base API calls per ticket",
        "Response time must be <2 seconds",
        "Cannot modify customer account settings",
        "Must log all interactions for audit"
    ]
        self.autonomous_decisions = [
        "Standard troubleshooting steps (restart, clear cache, check settings)",
        "Providing documentation links and tutorials",
        "Creating follow-up reminders",
        "Tagging tickets by category"
    ]
        self.escalation_triggers = [
        "Refund requests >$50",
        "Account security issues or suspected breaches",
        "Bug reports requiring code changes",
        "Customer explicitly requests human agent",
        "Unable to resolve after 3 troubleshooting attempts"
    ]
        
        # Build agent
        self.agent = self._build_agent()
    
    def _build_agent(self) -> AgentExecutor:
        """Build ReAct agent with intent-aware prompt."""
        
        # Format constraints for prompt
        steering_text = "\n".join(f"- {c}" for c in self.steering_constraints)
        autonomous_text = "\n".join(f"- {c}" for c in self.autonomous_decisions)
        escalate_text = "\n".join(f"- {c}" for c in self.escalation_triggers)
        
        prompt_template = f"""
Objective: Help customers resolve Tier-1 technical issues without frustration so they can get back to work quickly and maintain trust in our product.

Steering Constraints:
{steering_text}

Autonomous Decisions:
{autonomous_text}

Escalation Triggers:
{escalate_text}

You have access to the following tools:
{{tools}}

Tool Names: {{tool_names}}

Question: {{input}}

Thought: {{agent_scratchpad}}
"""
        
        prompt = PromptTemplate.from_template(prompt_template)
        
        # Placeholder tools
        tools = [
            Tool(
                name="PlaceholderTool",
                func=lambda x: f"Processed: {x}",
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
                return {
                    "output": None,
                    "status": "escalate",
                    "reason": f"Escalation trigger: {trigger}"
                }
        
        # Run agent
        try:
            result = self.agent.invoke({"input": input_text})
            return {
                "output": result["output"],
                "status": "complete",
                "reason": "Task completed"
            }
        except Exception as e:
            return {
                "output": None,
                "status": "error",
                "reason": str(e)
            }


if __name__ == "__main__":
    agent = CustomerSupportAgentExampleAgent()
    
    # Example usage
    result = agent.run("Test input")
    print(f"Status: {result['status']}")
    print(f"Output: {result.get('output', 'N/A')}")
