import asyncio
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStdio


async def main():
    # MCP server command - assuming a shopping list MCP server
    # You may need to modify this to point to your actual MCP server command
    
    # List of queries to run
    queries = [
        "Show me the whole list",
        "Add 2 bananas",
        "Mark milk as purchased",
        "Show me only unpurchased items",
        "Remove bread from the list",
        "Show me the whole list"
    ]

    # Create MCP server using stdio - replace with your actual MCP server command
    mcp_server = MCPServerStdio(
        command="python",
        args=["-m", "your_shopping_list_server"]
    )

    # Create an agent with conversation-aware instructions.
    agent = Agent(
        name="Shopping Assistant",
        instructions=(
            "You are an assistant that uses shopping list tools to help manage a shopping list."
        ),
        toolsets=[mcp_server],
        model="openai:gpt-4o"  # Use proper model name
    )

    # Initialize conversation history as a list of messages
    message_history = []

    # Iterate over the queries
    async with agent:
        for query in queries:
            # Print the query
            print(f"Query: {query}")

            # Run the agent with the current query and message history
            result = await agent.run(
                user_prompt=query,
                message_history=message_history
            )

            # Print the agent's response
            print(f"Assistant: {result.output}\n")

            # Update the message history with the new messages
            message_history = result.all_messages()

if __name__ == "__main__":
    asyncio.run(main())
