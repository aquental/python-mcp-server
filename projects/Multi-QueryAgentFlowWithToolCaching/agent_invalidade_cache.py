import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerSse


async def main():
    # Configure the MCP server parameters
    server_params = {"url": "http://localhost:3000/sse"}

    # List of queries to run
    queries = [
        "Show me the whole list",
        "Add 2 bananas",
        "Mark milk as purchased",
        "Show me only unpurchased items"
    ]

    # Connect to the MCP server with tool caching enabled
    async with MCPServerSse(
        params=server_params,
        cache_tools_list=True  # Cache the tools list to avoid re-fetching it
    ) as mcp_server:

        # Create an agent with conversation-aware instructions.
        agent = Agent(
            name="Shopping Assistant",
            instructions=(
                "You are an assistant that uses shopping list tools to help manage a shopping list."
            ),
            mcp_servers=[mcp_server],
            model="gpt-4.1"
        )

        # Initialize conversation history as a list of message dictionaries.
        conversation_history = []
        query_counter = 0  # Counter to track queries for cache invalidation

        for idx, query in enumerate(queries):
            print(f"Query {idx+1}: {query}")
            conversation_history.append({"role": "user", "content": query})

            result = await Runner.run(
                starting_agent=agent,
                input=conversation_history
            )

            print(f"Assistant: {result.final_output}\n")
            conversation_history = result.to_input_list()

            # Increment counter and invalidate cache after every two queries
            query_counter += 1
            if query_counter % 2 == 0:
                mcp_server.invalidate_tool_cache()

if __name__ == "__main__":
    asyncio.run(main())
