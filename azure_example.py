import os
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator

# Azure OpenAI configuration
openai_model = "gpt-4o-mini"  # Your deployment name
os.environ["AZURE_API_KEY"] = "your-azure-api-key"
os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

# Create model
model = LiteLLMModel(
    model_id=f"azure/{openai_model}",
    params={
        "max_tokens": 16384,
        "temperature": 0.1,
    }
)

# Create agent
agent = Agent(
    model=model, 
    tools=[calculator],
    system_prompt="You are a helpful assistant"
)

# Test the agent
response = agent("Hi, my name is John Doe. Can you calculate 25 * 48 for me?")

# Print response and metrics
print(response.message)
print(f"\nInput tokens: {response.metrics.accumulated_usage['inputTokens']}")
print(f"Output tokens: {response.metrics.accumulated_usage['outputTokens']}")
print(f"Execution time: {sum(response.metrics.cycle_durations):.2f} seconds")