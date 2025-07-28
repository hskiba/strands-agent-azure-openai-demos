#!/usr/bin/env python3
"""
Azure OpenAI Integration with Strands Agents

This example demonstrates how to configure and use Strands agents with Azure OpenAI.
It includes proper error handling, configuration validation, and usage examples.

Prerequisites:
1. Azure OpenAI resource deployed
2. Model deployment created in Azure
3. API key and endpoint configured
"""

import os
import sys
from typing import Union

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, shell, file_read

# Keep terminal settings default to allow prompts


class AzureOpenAIConfig:
    """Configuration helper for Azure OpenAI."""

    def __init__(self):
        self.api_key = os.getenv("AZURE_API_KEY")
        self.api_base = os.getenv("AZURE_API_BASE")
        self.api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")

    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        if not self.api_key:
            print("Error: AZURE_API_KEY environment variable not set")
            return False

        if not self.api_base:
            print("Error: AZURE_API_BASE environment variable not set")
            return False

        return True

    def display(self):
        """Display current configuration (safely)."""
        print("Azure OpenAI Configuration:")
        print(f"  • API Base: {self.api_base}")
        print(f"  • API Version: {self.api_version}")
        print(f"  • Deployment: {self.deployment_name}")
        print(f"  • API Key: {'*' * 10 if self.api_key else 'Not set'}")


def create_azure_agent(
    deployment_name: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    system_prompt: Union[str, None] = None,
) -> Agent:
    """
    Create a Strands agent configured for Azure OpenAI.

    Args:
        deployment_name: Azure OpenAI deployment name
        temperature: Response variability (0.0-1.0)
        max_tokens: Maximum response tokens
        system_prompt: Custom system prompt

    Returns:
        Configured Agent instance
    """
    # Create model with Azure configuration
    model = LiteLLMModel(
        model_id=f"azure/{deployment_name}",
        params={
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    )

    # Default system prompt
    if system_prompt is None:
        system_prompt = (
            "You are an AI assistant powered by Azure OpenAI. "
            "You have access to various tools to help users effectively. "
            "Always strive to be helpful, accurate, and efficient."
        )

    # Create agent with tools
    agent = Agent(
        model=model, tools=[calculator, shell, file_read], system_prompt=system_prompt
    )

    return agent


def demonstrate_capabilities(agent: Agent):
    """Run various demonstrations of agent capabilities."""

    examples = [
        {
            "name": "Basic Interaction",
            "query": "Hello! Can you tell me about yourself and what tools you have access to?",
        },
        {
            "name": "Mathematical Calculation",
            "query": "Calculate the factorial of 12 and express it in scientific notation.",
        },
        {
            "name": "System Information",
            "query": "Can you check what operating system I'm using and the current directory?",
        },
        {
            "name": "File Operations",
            "query": "Read the README.md file if it exists and summarize its contents.",
        },
        {
            "name": "Complex Task",
            "query": """Help me with these tasks:
1. Calculate the area of a circle with radius 7.5 cm
2. Convert the result to square inches (1 inch = 2.54 cm)
3. Tell me the current working directory
4. List the Python files in the current directory""",
        },
    ]

    for example in examples:
        print(f"\n{'='*60}")
        print(f"Example: {example['name']}")
        print(f"{'='*60}")
        print(f"Query: {example['query']}\n")

        try:
            # Execute query
            response = agent(example["query"])

            print("Response:")
            print(response.message)

            # Show metrics
            if hasattr(response, "metrics"):
                metrics = response.metrics.accumulated_usage
                print(f"\nMetrics:")
                print(f"  • Input tokens: {metrics['inputTokens']}")
                print(f"  • Output tokens: {metrics['outputTokens']}")
                print(
                    f"  • Execution time: {sum(response.metrics.cycle_durations):.2f}s"
                )

        except Exception as e:
            print(f"\nError: {str(e)}")


def main():
    """Main function to run Azure OpenAI demonstration."""
    print("Azure OpenAI with Strands Agents")
    print("=" * 60)

    # Load and validate configuration
    config = AzureOpenAIConfig()

    if not config.validate():
        print("\nPlease set the following environment variables:")
        print("  export AZURE_API_KEY='your-api-key'")
        print("  export AZURE_API_BASE='https://your-resource.openai.azure.com'")
        print("  export AZURE_API_VERSION='2024-02-15-preview'  # optional")
        print("  export AZURE_DEPLOYMENT_NAME='your-deployment'  # optional")
        sys.exit(1)

    # Display configuration
    config.display()

    try:
        # Create agent
        print("\nCreating Azure OpenAI agent...")
        agent = create_azure_agent(
            deployment_name=config.deployment_name, temperature=0.7, max_tokens=2000
        )
        print("Agent created successfully!")

        # Run demonstrations
        demonstrate_capabilities(agent)

        # Interactive mode option
        print("\n" + "=" * 60)
        print("Demonstrations complete!")

        while True:
            user_input = input("\nEnter your own query (or 'quit' to exit): ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                break

            if user_input:
                try:
                    response = agent(user_input)
                    print("\nResponse:")
                    print(response.message)
                except Exception as e:
                    print(f"\nError: {str(e)}")

        print("\nThank you for using Azure OpenAI with Strands!")

    except Exception as e:
        print(f"\nError creating agent: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify your Azure OpenAI resource is deployed")
        print("2. Check that your deployment name matches your Azure configuration")
        print("3. Ensure your API key has proper permissions")
        print(
            "4. Confirm your API base URL is correct (should not include deployment name)"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
