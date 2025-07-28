#!/usr/bin/env python3
"""
Simple Strands Agent with OpenAI Integration

This example demonstrates how to create a basic AI agent using the Strands SDK
with OpenAI models via LiteLLM. The agent has access to calculator and time tools.

Supports both standard OpenAI and Azure OpenAI endpoints.
"""

import os
import sys
from typing import Optional

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time


def create_openai_agent(
    model_id: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None,
) -> Agent:
    """
    Create a Strands agent with OpenAI model.

    Args:
        model_id: OpenAI model ID or Azure deployment (e.g., "azure/deployment-name")
        temperature: Model temperature for response variability (0.0-1.0)
        max_tokens: Maximum tokens in response
        system_prompt: Custom system prompt for the agent

    Returns:
        Configured Strands Agent instance
    """
    # Create model with configuration
    model = LiteLLMModel(
        model_id=model_id,
        params={
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
    )

    # Default system prompt if none provided
    if system_prompt is None:
        system_prompt = (
            "You are a helpful AI assistant with access to calculation and time tools."
        )

    # Create agent with tools
    agent = Agent(
        model=model, tools=[calculator, current_time], system_prompt=system_prompt
    )

    return agent


def main():
    """
    Main function to demonstrate agent usage.
    """
    # Check for API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("AZURE_API_KEY"):
        print("Error: Please set OPENAI_API_KEY or AZURE_API_KEY environment variable")
        print("\nFor OpenAI:")
        print("  export OPENAI_API_KEY='your-api-key'")
        print("\nFor Azure OpenAI:")
        print("  export AZURE_API_KEY='your-api-key'")
        print("  export AZURE_API_BASE='https://your-resource.openai.azure.com'")
        print("  export AZURE_API_VERSION='2024-02-15-preview'")
        sys.exit(1)

    # Determine model ID based on environment
    if os.getenv("AZURE_API_KEY"):
        # For Azure, you need to specify the deployment name
        model_id = "azure/gpt-4"  # Update with your deployment name
    else:
        model_id = "gpt-4o"

    # Create agent
    agent = create_openai_agent(model_id=model_id)

    # Example query
    print("=== Strands Agent with OpenAI ===")
    print(f"Model: {model_id}")
    print("\nQuery: What is 25 * 48? Also, what time is it?")
    print("\nResponse:")

    response = agent("What is 25 * 48? Also, what time is it?")
    print(response.message)

    # Display metrics
    print("\n=== Performance Metrics ===")
    print(f"Input tokens: {response.metrics.accumulated_usage['inputTokens']}")
    print(f"Output tokens: {response.metrics.accumulated_usage['outputTokens']}")
    print(
        f"Total tokens: {response.metrics.accumulated_usage['inputTokens'] + response.metrics.accumulated_usage['outputTokens']}"
    )
    print(f"Execution time: {sum(response.metrics.cycle_durations):.2f} seconds")


if __name__ == "__main__":
    main()
