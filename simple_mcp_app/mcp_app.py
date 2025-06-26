from langchain_mcp_adapters.client import MultiServerMCPClient
import os
import asyncio
from langchain_ollama import OllamaLLM
import streamlit as st

######################################
# settings
######################################

# load model
llm = OllamaLLM(model="gemma3")

# fetch environment variable from ~/.bashrc file
BRD_API_KEY = os.environ.get('BRD_API_KEY')

# setup Brigth Data MCP client
mcp = MultiServerMCPClient({
    "brd_mcp": {
        "command": "node",
        "args": ["node_modules/@brightdata/mcp/server.js"],
        "transport": "stdio",
        "env": {
            "API_TOKEN": BRD_API_KEY,
        }
    }
}) 

######################################
# functions
######################################

async def mcp_tools():
    """
    fetch and display available tools from MCP
    """
    tools = await mcp.get_tools() 
    for idx, tool in enumerate(tools):
        print(idx, tool.name, "\n", tool.args)
    return tools
    
async def handle_prompt(tools, url, user_prompt):
    """
    generate response from url and user prompt
    """
    if url.startswith("https://x.com/"):
        # load tool for scraping x posts
        scraper = tools[16]
    elif url.startswith("https://www.linkedin.com/in/"):
        # load tool for scraping linkedin profiles
        scraper = tools[6]
    else:
        # load tool for scraping other URLs
        scraper = tools[1]
    
    # call tool on user provided url
    result = await scraper.ainvoke({
        "url": url
    })
    
    # combine scraped content with user prompt
    full_prompt = (
        "Context (scraped data):\n\n"
        + result.strip()
        + "\n\nQuestion:\n\n"
        + user_prompt
    )
    
    # obttain model response
    response = llm.invoke(full_prompt)
    return response

######################################
# run application
######################################

tools = asyncio.run(mcp_tools()) #fetch mcp tools

# initialize interface elements
st.title("🌐 LLM Web Search")
url = st.text_input("Enter URL:")
user_prompt = st.text_area("Enter Question:")
submit = st.button("Submit")

# handle submit button press
if submit:
    with st.spinner("Processing..."):
        response = asyncio.run(
            handle_prompt(tools, url, user_prompt)
        )
        st.write(response)
