from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import file_read, file_write, editor, shell

# Define a focused system prompt for file operations
FILE_SYSTEM_PROMPT = """You are a file operations specialist. You help users read,
write, search, and modify files. Focus on providing clear information about file
operations and always confirm when files have been modified.

Key Capabilities:
1. Read files with various options (full content, line ranges, search)
2. Create and write to files
3. Edit existing files with precision
4. Report file information and statistics

Always specify the full file path in your responses for clarity.
"""

ANTHROPIC_SONNET = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
ANTHROPIC_HAIKU = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

model = BedrockModel(
    model_id=ANTHROPIC_SONNET,
    include_tool_result_status=True,
    region_name="us-east-2",
)

# Create a file-focused agent with selected tools
file_agent = Agent(
    model=model,
    system_prompt=FILE_SYSTEM_PROMPT,
    tools=[file_read, file_write, editor, shell],
)
response = file_agent(
    "Can you check what operating system I'm using and the current directory?"
)
