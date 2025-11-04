"""
Dynamic workflow example using the planner agent for intelligent task routing.
This workflow demonstrates how the planner can dynamically choose which agent to use for different tasks.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import flyte

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import tools to register them
import tools.math_tools
import tools.string_tools

from agents.planner_agent import planner_agent
from agents.math_agent import math_agent
from agents.string_agent import string_agent

# ----------------------------------
# Data Models
# ----------------------------------

@dataclass
class TaskResult:
    """Result from agent execution"""
    planner_decision: Dict[str, str]
    agent_result: Dict[str, str]
    chosen_agent: str


# ----------------------------------
# Flyte Task Environment(s)
# ----------------------------------

env = flyte.TaskEnvironment(
    name="ai_agent_env",
    image=flyte.Image.from_debian_base().with_requirements("requirements.txt"),
    secrets=[
        flyte.Secret(key="OPENAI_API_KEY", as_env_var="OPENAI_API_KEY"),

    ]
)


# ----------------------------------
# Task Definition
# ----------------------------------

@env.task
async def execute_dynamic_task(user_request: str) -> TaskResult:
    """
    Execute a task dynamically by first asking the planner which agent to use.

    Args:
        user_request (str): The user's request

    Returns:
        TaskResult: Combined result from planner decision and agent execution
    """
    print(f"User request: {user_request}")

    # Initialize empty memory log (for now, not persisting between calls)
    memory_log = []

    # Step 1: Ask planner which agent to use
    print("Step 1: Consulting planner agent...")
    planner_result = await planner_agent(user_request, memory_log)

    print(f"Planner result type: {type(planner_result)}, value: {planner_result}")

    # Handle if planner_result is a list (shouldn't be, but let's be defensive)
    if isinstance(planner_result, list):
        print(f"WARNING: planner_result is a list, taking first element")
        planner_result = planner_result[0] if planner_result else {"agent": "math", "task": user_request}

    agent_choice = planner_result["agent"]
    task = planner_result["task"]
    
    print(f"Planner decision: Use '{agent_choice}' agent for task: '{task}'")
    
    # Step 2: Execute the task with the chosen agent
    print(f"Step 2: Executing with {agent_choice} agent...")
    
    if agent_choice == "math":
        result = await math_agent(task, memory_log)
    elif agent_choice == "string":
        result = await string_agent(task, memory_log)
    else:
        result = {"error": f"Unknown agent: {agent_choice}"}
    
    print(f"Agent result: {result}")

    return TaskResult(
        planner_decision=planner_result,
        agent_result=result,
        chosen_agent=agent_choice
    )

# Optional: Local execution helper (only runs when executed directly, not when imported)
if __name__ == "__main__":
    # This allows local testing but won't break remote execution
    flyte.init_from_config(".flyte/config.yaml")
    execution = flyte.run(
        execute_dynamic_task,
        user_request="Calculate the factorial of 5 and then analyze the string 'Hello World!'"
    )

    print(f"Execution: {execution.name}")
    print(f"URL: {execution.url}")
    print("Click the link above to view execution details in the Flyte UI 👆")
