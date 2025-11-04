"""
Dynamic workflow example using the planner agent for intelligent task routing.
This workflow demonstrates how the planner can dynamically choose which agent to use for different tasks.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import tools to register them
import tools.math_tools
import tools.string_tools

from agents.planner_agent import planner_agent
from agents.math_agent import math_agent
from agents.string_agent import string_agent


async def execute_dynamic_task(user_request, memory_log):
    """
    Execute a task dynamically by first asking the planner which agent to use.
    
    Args:
        user_request (str): The user's request
        memory_log (list): Memory of previous interactions
    
    Returns:
        dict: Combined result from planner decision and agent execution
    """
    print(f"User request: {user_request}")
    
    # Step 1: Ask planner which agent to use
    print("Step 1: Consulting planner agent...")
    planner_result = await planner_agent(user_request, memory_log)
    
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
    
    # Update memory log
    memory_log.append((user_request, result))
    
    return {
        "planner_decision": planner_result,
        "agent_result": result,
        "chosen_agent": agent_choice
    }


async def dynamic_workflow_demo():
    """
    Demonstrate the dynamic workflow with various types of requests.
    """
    print("=== Dynamic Workflow Demo ===")
    
    memory_log = []
    
    # Test cases that should route to different agents
    test_requests = [
        "Calculate the square of 7",
        "Count the words in this sentence: 'Hello beautiful world'",
        "What is 15 multiplied by 8?",
        "How many letters are in the word 'programming'?",
        "Find the result of 20 divided by 4, then add 10",
        "Analyze this text: 'The quick brown fox jumps'"
    ]
    
    results = []
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n--- Test {i} ---")
        result = await execute_dynamic_task(request, memory_log)
        results.append(result)
        
        # Small delay for readability
        await asyncio.sleep(0.5)
    
    return results


async def adaptive_conversation():
    """
    Demonstrate an adaptive conversation where the planner learns from context.
    """
    print("\n=== Adaptive Conversation ===")
    
    memory_log = []
    
    conversation_flow = [
        "What's 5 plus 3?",
        "Now count the letters in the word 'eight'",
        "Multiply the previous math result by 2",
        "Count words in: 'We calculated sixteen total'"
    ]
    
    for i, message in enumerate(conversation_flow, 1):
        print(f"\n--- Conversation Step {i} ---")
        result = await execute_dynamic_task(message, memory_log)
        
        # Show how memory builds up
        print(f"Memory log now has {len(memory_log)} entries")
    
    return memory_log


async def main():
    """
    Main function to run dynamic workflow examples.
    """
    # Run the demo with different request types
    demo_results = await dynamic_workflow_demo()
    
    # Run adaptive conversation
    conversation_memory = await adaptive_conversation()
    
    print("\n=== Summary ===")
    print(f"Completed {len(demo_results)} dynamic task routings")
    print(f"Final conversation memory has {len(conversation_memory)} entries")
    
    # Show agent usage statistics
    agent_usage = {}
    for result in demo_results:
        agent = result["chosen_agent"]
        agent_usage[agent] = agent_usage.get(agent, 0) + 1
    
    print("Agent usage statistics:")
    for agent, count in agent_usage.items():
        print(f"  {agent}: {count} times")


if __name__ == "__main__":
    asyncio.run(main())