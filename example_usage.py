#!/usr/bin/env python3
"""
Advanced Strands Agent Examples

This script demonstrates various capabilities of Strands agents including:
- Multiple tool usage (calculator, time, Python REPL)
- Custom tool creation with @tool decorator
- Handling complex multi-step queries
- Performance metrics tracking

Supports both OpenAI and Azure OpenAI configurations.
"""

import os
import sys
from typing import Dict, Any

from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time, python_repl


# Custom Tools
@tool
def weather_info(location: str) -> str:
    """
    Get weather information for a location (mock implementation).

    In a real application, this would call a weather API service.

    Args:
        location: City or location name

    Returns:
        Weather information string
    """
    # Mock weather data
    weather_data = {
        "San Francisco": "Foggy, 58°F (14°C)",
        "New York": "Sunny, 75°F (24°C)",
        "London": "Rainy, 55°F (13°C)",
        "Tokyo": "Clear, 72°F (22°C)",
        "default": "Sunny, 72°F (22°C)",
    }

    return (
        f"Weather in {location}: {weather_data.get(location, weather_data['default'])}"
    )


@tool
def word_analyzer(text: str) -> Dict[str, Any]:
    """
    Analyze text and return statistics.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with word count, character count, and most common word
    """
    words = text.lower().split()
    word_freq = {}

    for word in words:
        word = word.strip('.,!?;:"')
        word_freq[word] = word_freq.get(word, 0) + 1

    most_common = max(word_freq.items(), key=lambda x: x[1]) if word_freq else ("", 0)

    return {
        "word_count": len(words),
        "character_count": len(text),
        "most_common_word": most_common[0],
        "most_common_count": most_common[1],
    }


def create_demo_agent() -> Agent:
    """
    Create a demonstration agent with multiple tools.

    Returns:
        Configured Agent instance
    """
    # Determine configuration based on environment
    if os.getenv("AZURE_API_KEY"):
        model_id = "azure/gpt-4"  # Update with your deployment
        print("Using Azure OpenAI configuration")
    else:
        model_id = "gpt-4o-mini"
        print("Using standard OpenAI configuration")

    # Create model
    model = LiteLLMModel(
        model_id=model_id,
        params={
            "temperature": 0.7,
            "max_tokens": 2000,
        },
    )

    # Create agent with all tools
    agent = Agent(
        model=model,
        tools=[calculator, current_time, python_repl, weather_info, word_analyzer],
        system_prompt=(
            "You are a helpful AI assistant with access to various tools. "
            "Use them to provide accurate and detailed responses. "
            "When using the Python REPL, always show both the code and results."
        ),
    )

    return agent


def run_example(agent: Agent, description: str, query: str) -> None:
    """
    Run an example query and display results with metrics.

    Args:
        agent: The Strands agent
        description: Description of the example
        query: The query to send to the agent
    """
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print("\nResponse:")

    # Execute query
    response = agent(query)
    print(response.message)

    # Display metrics
    metrics = response.metrics.accumulated_usage
    print(f"\nMetrics:")
    print(f"  • Input tokens: {metrics['inputTokens']}")
    print(f"  • Output tokens: {metrics['outputTokens']}")
    print(f"  • Total tokens: {metrics['inputTokens'] + metrics['outputTokens']}")
    print(f"  • Execution time: {sum(response.metrics.cycle_durations):.2f}s")

    # Show tool usage if any
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"  • Tools used: {len(response.tool_calls)}")


def main():
    """
    Main function to run all examples.
    """
    # Check for API configuration
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("AZURE_API_KEY"):
        print("Error: No API key found in environment variables")
        print("\nPlease set one of the following:")
        print("  • OPENAI_API_KEY for standard OpenAI")
        print("  • AZURE_API_KEY (with AZURE_API_BASE and AZURE_API_VERSION) for Azure")
        sys.exit(1)

    print("Strands Agent Examples")
    print("=" * 60)

    # Create agent
    agent = create_demo_agent()

    # Example 1: Simple calculation
    run_example(agent, "Simple Calculation", "What is 1234 * 5678?")

    # Example 2: Multiple tools
    run_example(
        agent,
        "Multiple Tools Usage",
        """Please help me with these tasks:
1. What's the current time?
2. Calculate the compound interest on $10,000 at 5% annual rate for 3 years
3. What's the weather in San Francisco?""",
    )

    # Example 3: Python code execution
    run_example(
        agent,
        "Python Code Execution",
        """Write a Python function to generate the first n prime numbers.
Then use it to find the first 15 prime numbers.
Show me both the code and the results.""",
    )

    # Example 4: Text analysis
    run_example(
        agent,
        "Text Analysis with Custom Tool",
        """Analyze this text: 'The quick brown fox jumps over the lazy dog. 
The dog was really lazy but the fox was extremely quick.'
Give me the word statistics.""",
    )

    # Example 5: Complex multi-step task
    run_example(
        agent,
        "Complex Multi-Step Task",
        """I'm planning a trip. Can you:
1. Tell me the current time
2. Check the weather in Tokyo
3. Calculate how much $1000 USD is worth in Japanese Yen (use 150 JPY per USD)
4. Write a Python function to calculate travel expenses and use it to find the total cost if:
   - Hotel: 15000 JPY per night for 5 nights
   - Food: 5000 JPY per day for 5 days
   - Transportation: 3000 JPY total""",
    )

    print("\n" + "=" * 60)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
