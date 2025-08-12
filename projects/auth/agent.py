import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerSse


async def main():
    # Setup the SSE server parameters with the API key
    server_params = {
        "url": "http://localhost:3000/mcp/sse",
        "headers": {
            "X-API-Key": "super_secret_value"
        }
    }

    # Connect to the MCP server over SSE
    async with MCPServerSse(params=server_params) as mcp_server:

        # Create an agent
        agent = Agent(
            name="OpenAI Shopping Agent",
            instructions="You are an assistant that uses shopping list tools to assist with a shopping list",
            mcp_servers=[mcp_server],
            model="gpt-4.1"
        )

        # Run the agent
        result = await Runner.run(
            starting_agent=agent,
            input="Give me my shopping list"
        )

        # Print the final output
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
