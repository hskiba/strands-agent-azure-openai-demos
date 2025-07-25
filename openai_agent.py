import os
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time

# For standard OpenAI
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# For Azure OpenAI (uncomment and set these)
# os.environ["AZURE_API_KEY"] = "your-azure-api-key"
# os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
# os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

# Model configuration
model_id = "gpt-4o"  # For Azure: "azure/your-deployment-name"

# Create model using LiteLLM
model = LiteLLMModel(
    model_id=model_id,
    params={
        "temperature": 0.7,
        "max_tokens": 1000,
    }
)

# Create the agent with OpenAI model and tools
agent = Agent(
    model=model, 
    tools=[calculator, current_time],
    system_prompt="You are a helpful assistant powered by OpenAI"
)

# Test the agent
if __name__ == "__main__":
    # Test with a calculation
    response = agent("What is 25 * 48? Also, what time is it?")
    print(response.message)