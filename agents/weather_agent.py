"""
This module defines the weather_agent, which can get weather information for locations.
"""

import json
import sys
from pathlib import Path
import flyte

# Add project root to path for imports
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))

# Import tools to register them
import tools.weather_tools

from utils.decorators import agent, agent_tools
from utils.plan_executor import execute_plan
from dataclasses import dataclass
from config import base_env

# ----------------------------------
# Data Models
# ----------------------------------

@dataclass
class WeatherAgentResult:
    """Result from weather agent execution"""
    final_result: str
    steps: str  # JSON string of steps taken
    error: str = ""  # Empty if no error


# ----------------------------------
# Weather Agent Task Environment
# ----------------------------------
env = base_env
# Future: If we need weather-specific dependencies, we can extend:
# env = flyte.TaskEnvironment(
#     name="weather_agent_env",
#     image=base_env.image.with_pip_packages(["httpx"]),
#     secrets=base_env.secrets,
#     resources=flyte.Resources(cpu=1, mem="2Gi")
# )


@env.task
@agent("weather")
async def weather_agent(task: str) -> WeatherAgentResult:
    """
    Weather agent that can get current weather information for locations.

    Args:
        task (str): The weather task to perform.

    Returns:
        WeatherAgentResult: The result of the weather query and the steps taken.
    """
    print(f"[Weather Agent] Processing: {task}")

    toolset = agent_tools["weather"]
    tool_list = "\n".join([f"{name}: {fn.__doc__.strip()}" for name, fn in toolset.items()])
    system_msg = f"""
You are a weather information agent. You can get current weather information for any location.

Tools:
{tool_list}

CRITICAL: You must respond with ONLY a valid JSON array, nothing else. No markdown, no explanations.
Return a JSON array of tool calls in this exact format:
[
  {{"tool": "get_weather", "args": ["London"], "reasoning": "Getting current weather for London"}}
]

RULES:
1. Start your response with [ and end with ]
2. No markdown code blocks (no ```)
3. No extra text before or after the JSON
4. Always include a "reasoning" field for each step
5. Use the location name as the argument (e.g., "London", "New York", "Tokyo")
"""

    memory_log = []  # No memory persistence for now
    result = await execute_plan(task, agent="weather", system_msg=system_msg)

    print(f"[Weather Agent] Result: {result}")

    return WeatherAgentResult(
        final_result=str(result.get("final_result", "")),
        steps=json.dumps(result.get("steps", [])),
        error=result.get("error", "")
    )
