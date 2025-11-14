"""
This module defines the writer_agent, which can create written content based on research.
"""

import sys
from pathlib import Path
import flyte
from openai import AsyncOpenAI

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.decorators import agent
from dataclasses import dataclass
from config import base_env, OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# ----------------------------------
# Data Models
# ----------------------------------

@dataclass
class WriterAgentResult:
    """Result from writer agent execution"""
    final_result: str
    error: str = ""  # Empty if no error


# ----------------------------------
# Writer Agent Task Environment
# ----------------------------------
env = base_env


@env.task
@agent("writer")
async def writer_agent(task: str) -> WriterAgentResult:
    """
    Writer agent that creates written content based on research and requirements.
    Uses LLM directly to generate content without intermediate tools.

    Args:
        task (str): The writing task to perform (should include research context).

    Returns:
        WriterAgentResult: The written content.
    """
    print(f"[Writer Agent] Processing: {task}")

    system_msg = """
You are a professional content writer. Your job is to create well-structured, engaging content based on the research provided.

Write clear, informative content that:
- Has a compelling title (using # for markdown)
- Is well-organized with sections (using ## for subheadings)
- Synthesizes the research into coherent paragraphs
- Is approximately 200-400 words
- Uses proper markdown formatting

Return ONLY the written content, no preamble or explanation.
"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": task}
            ]
        )

        content = response.choices[0].message.content
        print(f"[Writer Agent] Generated {len(content)} characters of content")

        return WriterAgentResult(
            final_result=content,
            error=""
        )
    except Exception as e:
        print(f"[Writer Agent] Error: {str(e)}")
        return WriterAgentResult(
            final_result="",
            error=str(e)
        )
