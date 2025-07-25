import os
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time, python_repl

# Define a custom tool
@tool
def weather_info(location: str) -> str:
    """
    Get weather information for a location (mock implementation).

    Args:
        location (str): The location to get weather for

    Returns:
        str: Weather information
    """
    # This is a mock implementation - in real use, you'd call a weather API
    return f"The weather in {location} is sunny with a temperature of 72°F (22°C)"

# For standard OpenAI
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# For Azure OpenAI (uncomment and set these)
# os.environ["AZURE_API_KEY"] = "your-azure-api-key"
# os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
# os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"

# Model configuration
model_id = "gpt-4o-mini"  # For Azure: "azure/your-deployment-name"

# Create model using LiteLLM
model = LiteLLMModel(
    model_id=model_id,
    params={
        "temperature": 0.7,
        "max_tokens": 1000,
    }
)

# Create agent with multiple tools
agent = Agent(
    model=model,
    tools=[calculator, current_time, python_repl, weather_info],
    system_prompt="You are a helpful assistant with access to various tools"
)

# Example queries
if __name__ == "__main__":
    print("=== Simple Calculation ===")
    response = agent("What is 1234 * 5678?")
    print(response.message)

    print("\n=== Multiple Tools ===")
    response = agent("""
    Please help me with these tasks:
    1. What's the current time?
    2. Calculate the compound interest on $10,000 at 5% annual rate for 3 years
    3. What's the weather in San Francisco?
    """)
    print(response.message)

    print("\n=== Python Code Execution ===")
    response = agent("""
    Write a Python function to calculate the Fibonacci sequence up to n terms.
    Then execute it to find the first 10 Fibonacci numbers.
    Show me the code and the results.
    """)
    print(response.message)

    # Print metrics
    print("\n=== Metrics ===")
    print(f"Input tokens: {response.metrics.accumulated_usage['inputTokens']}")
    print(f"Output tokens: {response.metrics.accumulated_usage['outputTokens']}")
    print(f"Execution time: {sum(response.metrics.cycle_durations):.2f} seconds")
