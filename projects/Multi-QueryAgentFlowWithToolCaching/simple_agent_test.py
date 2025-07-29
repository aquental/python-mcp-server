import asyncio
from pydantic_ai import Agent

async def main():
    # Create a simple agent without MCP server
    agent = Agent(
        name="Test Assistant",
        instructions="You are a helpful assistant.",
        model="openai:gpt-4o"  # You need OPENAI_API_KEY environment variable
    )

    queries = [
        "Hello, how are you?",
        "What's 2 + 2?",
        "Tell me a joke"
    ]

    message_history = []

    for query in queries:
        print(f"Query: {query}")
        
        try:
            result = await agent.run(
                user_prompt=query,
                message_history=message_history
            )
            print(f"Assistant: {result.output}\n")
            message_history = result.all_messages()
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
