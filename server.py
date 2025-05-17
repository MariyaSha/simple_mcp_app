from fastmcp import FastMCP
from langchain_ollama import OllamaLLM
from playwright.async_api import async_playwright

# Bright data unlocker credentials
proxy = {
    'server': 'http://{}:{}'.format(
        'brd.superproxy.io',
        33335,
    ),
    'username': "my_user",
    'password': "my_pass",
}

# set up server
mcp = FastMCP("Mariya's MCP")
# set up Ollama model
llm = OllamaLLM(model="gemma3")

@mcp.tool()
async def do_scrape(urls):
    """
    scrape text content from a list of user-provided URLS
    """
    results = []
    
    # initialize browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True, 
        proxy=proxy
    )
    # initialize context
    context = await browser.new_context(
        ignore_https_errors=True
    )

    for url in urls:
        # navigate to URLs in separate tabs
        page = await context.new_page()
        await page.goto(url, wait_until="load")
        
        # fetch title, and inner text
        title = await page.title()
        text = await page.evaluate("document.body.innerText")
        
        # store outside the loop along with url
        results.append({"url": url, "title": title, "text": text})
        await page.close()

    # close browser and terminate playwright
    await browser.close()
    await playwright.stop()
    
    return results

@mcp.tool()
async def ask_with_context(prompt, urls):
    """
    inquire Ollama LLM
    """
    if urls:
        # scrape URLs if URLs were provided
        scraped = await do_scrape(urls)
        # join all scraped URLs into one string
        full_prompt = "\n\n".join(scraped)
    else:
        # pass prompt as is if URLs were not provided
        full_prompt = prompt
    return llm.invoke(full_prompt)

if __name__ == "__main__":
    mcp.run()
