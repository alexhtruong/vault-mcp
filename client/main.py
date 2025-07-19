import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient
import os

async def main():
    # Load environment variables
    load_dotenv()
    print("✅ Environment loaded")

    # Create configuration dictionary
    config = {
      "mcpServers": {
        "playwright": {
          "command": "npx",
          "args": ["@playwright/mcp@latest"],
          "env": {
              "DISPLAY": ":1"
          }
        }
      }
    }
    print("✅ Config created")

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)
    print("✅ MCP Client created")

    # Create LLM with Gemini free tier (much faster than local)
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("❌ Please set GOOGLE_API_KEY in your .env file")
        print("Get your free API key from: https://aistudio.google.com/")
        return
    
    # Try the most common working model names for current API
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.3,
        google_api_key=google_api_key,
        max_output_tokens=512,
    )
    
    print("✅ LLM created")
    
    # Create agent with reduced steps for faster testing
    agent = MCPAgent(llm=llm, client=client, max_steps=5)
    print("✅ Agent created with Gemini (cloud-powered)...")

    # Run the query - should be much faster now!
    result = await agent.run(
        "Hello, can you tell me what tools you have available?",
    )
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())