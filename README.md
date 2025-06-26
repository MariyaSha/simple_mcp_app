# 🌐 AI GUI App with Full Web Access

What if your own language model could search the web and answer real-time questions? Just like ChatGPT, but running locally on your system, inside your app, where you have full control? 

In this project, we’ll build exactly that using:

- 🧠 **Ollama** – to run powerful language models like `gemma3` on your local machine.
- 🔗 **LangChain** – to interface with LLMs from Python.
- 🌐 **Bright Data MCP** – to fetch live web content using real-world scraping tools. [Bright Data MCP GitHub Repo](https://github.com/brightdata/brightdata-mcp)
- 🎨 **Streamlit** – to wrap everything in a clean, interactive user interface.

---

## 🛠️ Prerequisites

Before running the app, make sure you have the following:

- ✅ WSL 2 + Miniforge (or any other Conda type software)
- ✅ [Ollama](https://ollama.com) installed and a model (e.g., `gemma3`) pulled and serving.
- ✅ An API key from [Bright Data](https://brdta.com/pythonsimplified_mcp), make sure that at least one **Web Unlocker** zone is configured. 
- ✅ Add the following line of code to the end of your .bashrc file in WSL. Replace <your-key> with the Brigth Data API Key you copied.
    <br>
    ```
    export BRD_API_KEY=<your-key>
    ```
---

## 📺 Video Tutorial

If you're not sure how to install the requirements, or what .bashrc is, or if you'd like to build this entire application step by step alongside me, please checkout my video tutorial on YouTube:

<a href="https://youtu.be/CBVVMhvvbHM"><img src="https://github.com/user-attachments/assets/04bfeed3-c77d-4a11-98dc-dec1aa9449ee" width=600px></a>

### Watch the full tutorial to learn how to:

- Connect a local LLM to real-time web data
- Use MCP tools for scraping websites, X posts, and LinkedIn profiles
- Build a Streamlit GUI with optional context fields and memory
- Understand how MCP gives models access to live external resources

---
## 💸 Coupon
Get 10$ of **Bright Data** credits using the promo link (goes a long way!):
<br>
https://brdta.com/pythonsimplified_mcp

Just for perspective. I've featured Bright Data tools in a few tutorials already, and so far it cost me $6 bucks.

---
## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/MariyaSha/simple_mcp_app.git
cd simple_mcp_app

# create working environment 
conda create -n mcp_env python=3.12
conda activate mcp_env

conda install nodejs
# Make sure you've updated your .bashrc file (check Prerequisites)
npx @brightdata/mcp API_TOKEN=$BRD_API_KEY

# Install Python dependencies
pip install -r requirements.txt

cd simple_mcp_app
# OR cd advanced_mcp_app

# run application
streamlit run mcp_app.py
```
