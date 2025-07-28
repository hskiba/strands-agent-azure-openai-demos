# Strands Agents with Azure OpenAI Integration

This repository provides examples of using [Strands Agents SDK](https://strandsagents.com) with Azure OpenAI models. Strands Agents is a Python SDK for building AI agents with tool-use capabilities.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Azure OpenAI deployment
- Poetry package manager

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd strands-agent-azure-openai-demos
```

2. Install Poetry (if not already installed):
   - **macOS/Linux/WSL**: `curl -sSL https://install.python-poetry.org | python3 -`
   - **Windows PowerShell**: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
   - For more installation options, see [Poetry's official documentation](https://python-poetry.org/docs/#installation)

3. Install dependencies:
```bash
poetry install
```

4. Set up environment variables for Azure OpenAI:
```bash
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_DEPLOYMENT_NAME="your-deployment-name"
```

## 📁 Repository Structure

```
strands-agent-azure-openai-demos/
├── openai_agent.py      # Basic agent with calculator and time tools
├── example_usage.py     # Advanced examples with multiple tools
├── azure_example.py     # Azure OpenAI specific configuration
├── file_system.py      # File system operations specialist
├── pyproject.toml      # Poetry configuration and dependencies
├── requirements.txt     # Alternative pip dependencies
└── README.md           # This file
```

## 🎯 Examples

### Basic Agent (openai_agent.py)

A simple agent with calculator and time tools:

```bash
poetry run python openai_agent.py
```

Features:
- Basic mathematical calculations
- Current time queries
- Performance metrics display

### Advanced Examples (example_usage.py)

Demonstrates multiple capabilities:

```bash
poetry run python example_usage.py
```

Includes:
- Custom tool creation with `@tool` decorator
- Multiple tool orchestration
- Python code execution via REPL
- Text analysis capabilities
- Complex multi-step tasks

### Azure OpenAI (azure_example.py)

Specific configuration for Azure OpenAI:

```bash
poetry run python azure_example.py
```

Features:
- Configuration validation
- Interactive mode
- Error handling and troubleshooting tips
- Multiple demonstration scenarios

### File System Specialist (file_system.py)

A specialized agent focused on file operations:

```bash
poetry run python file_system.py
```

Features:
- Read and write files
- File manipulation using built-in editor
- Safe file operations with proper error handling

## 🛠️ Tools

For information on available tools and how to create custom tools, see the [Strands Agents Documentation](https://strandsagents.com).

## 🔧 Configuration Options

### Azure OpenAI Model Selection

The model is configured through environment variables:
- `AZURE_DEPLOYMENT_NAME`: Your Azure OpenAI deployment name
- The deployment should be configured in Azure portal with your chosen model (e.g., gpt-4, gpt-4-turbo)

### Parameters

```python
model = LiteLLMModel(
    model_id=f"azure/{deployment_name}",
    params={
        "temperature": 0.7,      # Response creativity (0.0-1.0)
        "max_tokens": 2000,      # Maximum response length
    }
)
```

## 📊 Metrics and Monitoring

All examples include performance metrics:
- Input/Output token counts
- Total token usage
- Execution time
- Tool usage tracking

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure environment variables are set
   - Check variable names match exactly

2. **Azure OpenAI Errors**
   - Verify deployment name matches Azure portal
   - Check API base URL format (no trailing slash)
   - Confirm API version is supported

3. **Tool Execution Failures**
   - Some tools require specific permissions
   - Python REPL requires proper Python environment
   - Shell commands depend on system configuration

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
```

## 📚 Learn More

- [Strands Agents Documentation](https://strandsagents.com)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [LiteLLM Documentation](https://docs.litellm.ai/)

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is provided as example code for using Strands Agents SDK. Please refer to the Strands Agents license for SDK usage terms.