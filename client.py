import asyncio
import streamlit as st
from fastmcp import Client
import json

# initialize server
client = Client("server.py")

async def run_scrape_tool(url_list):
    async with client:
        return await client.call_tool(
            "do_scrape", {"urls": url_list}
        )

async def run_ask_tool(prompt: str, urls: list[str] = []):
    async with client:
        return await client.call_tool(
            "ask_with_context", {"prompt": prompt, "urls": urls}
        )

# Streamlit UI
st.title("MARIYA'S URL SCRAPER")
is_url = st.checkbox("Include scraped data", value=True)

if is_url:
    url_string = st.text_area(
        "Enter URLs", 
        placeholder="http://google.com, http://bing.com")
else:
    url_string = ""

question = st.text_input(
    "Ask Ollama anything", 
    placeholder="E.g., Summarize text"
)

if st.button("Submit"):
    if not question:
        # user prompt was not provided
        st.warning("Enter a question!")
        
    elif is_url and not url_string:
        # URL box is checked but URLs were not provided
        st.warning("Enter URL or uncheck box!")
        
    elif not is_url and question:
        # URL box is unchecked and user prompt provided
        full_prompt = question 
        
    elif is_url and url_string and question:
        # prompt with URLs
        with st.spinner("Processing..."):
            scraped_data = None
            
            # convert URLs string to a list
            current_urls = [i.strip() for i in url_string.split(",") if i.strip()]
            
            if current_urls != st.session_state.get("last_urls"):
                # new URLS were provided by user
                # scrape content from server
                response = asyncio.run(
                    run_scrape_tool(current_urls)
                )
                # load JSON response from server
                scraped_data = json.loads(response[0].text)
                # cache data for future prompts
                st.session_state.scraped_data = scraped_data
                st.session_state.last_urls = current_urls
            else:
                # URLS were not changed from previous prompt
                # use cached data
                scraped_data = st.session_state.get("scraped_data")
            
            # format model prompt
            full_prompt = "\n\n".join(
                ["Context (scraped data):"] + 
                ["URL: {}\nTitle: {}\nText: {}".format(
                    i['url'], 
                    i['title'], 
                    i['text']
                ) for i in scraped_data] + 
                ["\nQuestion: {}".format(
                    question
                )])    

    # ask LLM 
    llm_response = asyncio.run(run_ask_tool(full_prompt))
    st.subheader("Ollama Response")
    st.write(llm_response[0].text)
        
        
