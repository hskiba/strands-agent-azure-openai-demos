# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a demonstration repository for the Strands Agents SDK, showcasing how to integrate AI agents with OpenAI and Azure OpenAI. The project provides example implementations of various agent patterns and tool usage.

## Commands

### Setup and Installation
```bash
# Using Poetry (preferred)
poetry install

# Using pip
pip install -r requirements.txt
```

### Running Examples
```bash
# Basic OpenAI agent
python openai_agent.py

# Advanced usage examples  
python example_usage.py

# Azure OpenAI examples
python azure_example.py

# File system specialist agent
python file_system.py
```

### Environment Setup
Required environment variables:
- For OpenAI: `OPENAI_API_KEY`
- For Azure: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_DEPLOYMENT_NAME`

## Architecture

### Agent Structure
All agents follow this pattern:
1. Create model wrapper using LiteLLM
2. Define or import tools
3. Create agent with model + tools + system prompt
4. Execute queries through agent.run()

### Key Components

**Model Integration**
- Uses LiteLLM for provider abstraction
- Supports both OpenAI and Azure OpenAI through unified interface
- Configuration through environment variables or explicit parameters

**Tool System**
- Built-in tools from `strands_tools`: calculator, current_time, python_repl, shell, file_read, file_write, editor
- Custom tools created with `@tool` decorator accepting description and parameters
- Tools enable agents to perform specific actions

**Agent Examples**
- `openai_agent.py`: Basic agent with calculator and time tools
- `example_usage.py`: Advanced patterns including multi-tool orchestration, metrics tracking
- `azure_example.py`: Azure-specific configuration with AzureOpenAIConfig
- `file_system.py`: Specialized agent for file operations

### Important Patterns

1. **Custom Tool Creation**
```python
from strands_agents.tools import tool

@tool(
    description="Tool description",
    parameters={
        "param_name": {"type": "string", "description": "Parameter description"}
    }
)
def custom_tool(param_name: str) -> str:
    # Implementation
```

2. **Agent Factory Pattern**
```python
def create_agent(api_key: str) -> Agent:
    model = LiteLLMModel(model="provider/model-name", api_key=api_key)
    return Agent(model=model, tools=[...], system_prompt="...")
```

3. **Callback Handlers**
For streaming responses, use callbacks to format output and track metrics.

## Development Notes

- Python 3.11+ required
- No formal test infrastructure - these are example/demo files
- When modifying examples, ensure they remain self-contained and runnable
- Each example file should demonstrate specific capabilities clearly
- Environment variables should be validated before use