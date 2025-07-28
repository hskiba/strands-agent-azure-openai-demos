from strands import Agent
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

# Create a file-focused agent with selected tools
file_agent = Agent(
    system_prompt=FILE_SYSTEM_PROMPT,
    tools=[file_read, file_write, editor, shell],
)
response = file_agent(
    "Can you check what operating system I'm using and the current directory?"
)
