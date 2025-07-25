# Strands Agent with OpenAI Demo

This repository demonstrates how to create a simple AI agent using Strands Agents SDK with OpenAI models via LiteLLM (which supports OpenAI, Azure OpenAI, and other providers).

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:

For standard OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

For Azure OpenAI:
```bash
export AZURE_API_KEY="your-azure-api-key"
export AZURE_API_BASE="https://your-resource.openai.azure.com"
export AZURE_API_VERSION="2024-02-15-preview"
```

## Files

- `openai_agent.py` - Basic agent setup with OpenAI model
- `example_usage.py` - Extended examples showing various agent capabilities
- `requirements.txt` - Python dependencies

## Usage

### Basic Agent
```python
python openai_agent.py
```

### Extended Examples
```python
python example_usage.py
```

## Features Demonstrated

1. **OpenAI Integration** - Using GPT-4 models through Strands via LiteLLM
2. **Azure OpenAI Support** - Works with Azure OpenAI endpoints
3. **Built-in Tools** - Calculator, current time, Python REPL
4. **Custom Tools** - Creating custom tools with the `@tool` decorator
5. **Multi-tool Usage** - Agent intelligently uses multiple tools to answer complex queries

## Azure OpenAI Configuration

For Azure OpenAI, update the model_id and environment variables:
```python
# Set environment variables
os.environ["AZURE_API_KEY"] = "your-azure-api-key"
os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

# Configure model
model = LiteLLMModel(
    model_id="azure/your-deployment-name",
    params={
        "temperature": 0.7,
        "max_tokens": 1000,
    }
)
```

## Example Queries

The agent can handle various types of requests:
- Mathematical calculations
- Time-based queries
- Code generation and execution
- Custom tool invocations

## Learn More

- [Strands Agents Documentation](https://strandsagents.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)