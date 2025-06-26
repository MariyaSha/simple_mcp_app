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

# fetch environment variables from ~/.bashrc file
BRD_API_KEY = os.environ.get('BRD_API_KEY')

# setup Brigth Data MCP client
mcp = MultiServerMCPClient({
    "brd_mcp": {
        "command": "node",
        "args": ["../../node_modules/@brightdata/mcp/server.js"],
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
    
async def handle_prompt(tools, is_url, url, user_prompt):
    """
    generate response from url and user prompt
    """ 
    # if URL is provided
    if is_url:
        # if URL hasn't changed from previous prompt
        if url == st.session_state.last_url:
            # fetch the already scraped data
            result = st.session_state.last_result
        # if new URL was provided by user
        else:
            # choose the right tool for the URL kind
            if url.startswith("https://x.com/"):
                scraper = tools[16]
            elif url.startswith("https://www.linkedin.com/in/"):
                scraper = tools[6]
            else:
                scraper = tools[1]
            
            # call tool on new URL
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
        # store results in app sessions
        st.session_state.last_url = url
        st.session_state.last_result = result
    # if URL is not provided
    else:
        full_prompt = user_prompt
    
    # obtain model response
    response = llm.invoke(full_prompt)
    return response

######################################
# run application
######################################

tools = asyncio.run(mcp_tools()) #fetch mcp tools

# initialize interface elements
st.title("🌐 LLM Web Search")

# initialize state to track if URL changes
if "last_url" not in st.session_state:
    st.session_state.last_url = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

url = None
is_url = st.checkbox("Use context from URL?", value=True)

# display url input field only if is_url checkbox is checked
if is_url:
    url = st.text_input(
        "Enter URL:", 
        placeholder="https://example.com",
    )

user_prompt = st.text_area("Enter Question:")
submit = st.button("Submit")

# handle submit button press
if submit:
    if not user_prompt:
        st.warning("Please enter a prompt.")
    elif is_url and not url:
        st.warning("Please enter a URL to scrape or uncheck box.")
    else:
        with st.spinner("Processing..."):
            response = asyncio.run(
                handle_prompt(tools, is_url, url, user_prompt)
            )
            st.write(response)
