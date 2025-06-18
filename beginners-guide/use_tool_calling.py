#!/usr/bin/env python
# coding: utf-8

# # How-to-Use FuriosaAI SDK Tool Calling to build AI Agents
# 
# Llama 3.1 models, which are now equipped with native support for tool calling.
# In this notebook, we'll explore what tool calling means in the context of large language models (LLMs), and demonstrate how to use the Llama-3.1-8B model with tool calling capabilities on the FuriosaAI SDK to build AI Agents.
# 
# ## This notebook covers,
# - Introduction to Tool Calling
# - Using Llama 3.1 model with FuriosaAI SDK for tool calling
# - Building a simple search agent using LangChain tools and agents
# 
# 
# ## Tool calling
# Tool calling is a method that extends an LLM's capabilities by allowing it to interact with external tool or functions. The available tools and their required input parameters are defined in the system prompt, and provided to the model along with the user's input. When the model receives a user query and determines that a tool is needed, it generates a tool call request in JSON format. For example, if asked for current weather, the model may issue a structure request to a weather API tool.
# 
# 
# When an LLM attempts to call a tool in response to a user query, it must extract the necessary parameters from the input and generate a structured output that conforms to the expected function call input format. This is a non-trivial task, as the model not only accurately identify and format the required parameters according to the specific schema defined for the tool, but also generate structured data for tool calling requests.  
# 
# To enable this capability, some approaches use few-shot prompting, where examples of tool usage and the required output format are provided as demonstrations. More recently, advanced models like Llama-3.1-8B have been trained with built-in tool calling capabilities, allowing them to perform this process more reliably without extensive prompt engineering.
# 
# #### 1. Define Tool
# ```
# tools = [{
#     "type": "function",
#     "function": {
#         "name": "get_weather",
#         "description": "Get the current weather in a given location",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {"type": "string", "description": "City and state, e.g., 'San Francisco, CA'"},
#                 "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
#             },
#             "required": ["location", "unit"]
#         }
#     }
# }]
# ```
# 
# #### 2. Get user question
# - "What's the weather like in San Francisco?"
# 
# 
# #### 3. Get tool call request
# - Function called: `get_weather`
# - Arguments: {"location": "San Francisco, CA", "unit": "fahrenheit"}
# 
# 
# #### 4. Get tool call outputs by executing to python backend
# - Tool call outputs (by tool execution): Getting the weather for San Francisco, CA in fahrenheit...
# 
# 
# #### 5. Append tool calling outputs and generate final LLM responses. 
# - By appending the tool calling outputs to previous chat history and giving to LLM, the model can generate final outputs.
# - Final LLM responses: The weather for San Francisco, CA is ... 
# 
# 
# ## How FuriosaAI SDK supports tool calling?
# 
# For more extensive AI/ML inference workflows, the FuriosaAI SDK offers support for tool calling via an OpenAI-compatible chat API. This means that AI agents can use the SDK to invoke external or custom tools while reasoning and generating responses. Let’s dive into how you can leverage tool calling with the FuriosaAI SDK to build an AI agent.
# 
# 
# 
# ## Prerequisites
# - RNGD servers
# - FuriosaSDK 2025.02 release
# - AI application framework to use, in this case we'll adopt Langchain.
# 
# 

# #### 1. Load RNGD servers
# 
# - Load RNGD servers with `furiosa-llm serve` command.
# - We'll use tool calling supported server with `--enable-auto-tool-choice` and `--tool-call-parser`.
# 
# 
# ```
# furiosa-llm serve furiosa-ai/Llama-3.1-8B-Instruct-FP8 \
#     --enable-auto-tool-choice \
#     --tool-call-parser llama3_json \
#     --port 8000 \
#     --devices "npu:2"
# ```
import subprocess
def start_furiosa_llm_servers():
    server = subprocess.Popen(
        [
            "furiosa-llm",
            "serve",
            "furiosa-ai/Llama-3.1-8B-Instruct",
            "--host",
            "localhost",
            "--port",
            "8000",
            "--enable-auto-tool-choice",
            "--tool-call-parser",
            "llama3_json",
            "--devices",
            "npu:2",
        ]
    )
    return server




server = start_furiosa_llm_servers()
import time
time.sleep(50)
# In[4]:


from openai import OpenAI
import json


port= 8000
api_key="EMPTY"
client = OpenAI(base_url = f"http://localhost:{port}/v1", 
                api_key=api_key)

# ## Chat with Tool calling 
# Here are four-step that simplifies the process of LLM chat with tool calling. 
# 1. The model generates inputs for the tools.
# 2. The specified tools are executed using these inputs, returning the corresponding outputs.
# 3. The outputs from the tool calls are incorporated into the ongoing chat history.
# 4. The model uses the tool outputs along with the prior context to generate the final response.
# 
# 
# 
# 
# #### 1. Tool Definition
# First, we need to specify the following arguments.
# - name of tool
# - description of tool
# - json schema describing the inputs to the tool
# 
# 
# #### 2. Tool binding
# Once a tool is defined, the related information—such as tools and tool_choice—is passed into the chat API. By linking these tools with the language model, the model receives both the tools and the surrounding context. Based on the provided tool definitions and the selected tool_choice strategy, the model can generate a function call by deciding which tool to use and what input parameters to provide.
# 
# 

# ## Tool Usage -- Custom Tool Use

# In[1]:


import json
import random

def get_stock_price(ticker: str, currency: str) -> str:
    price = round(random.uniform(100, 1500), 2)
    return f"The current price of {ticker.upper()} is {price} {currency.upper()}."

def get_exchange_rate(base_currency: str, target_currency: str) -> str:
    rate = round(random.uniform(0.5, 1.5), 4)
    return f"Current exchange rate from {base_currency.upper()} to {target_currency.upper()} is {rate}."

def get_financial_news(company: str) -> str:
    sample_news = [
        f"{company} reported better-than-expected quarterly earnings.",
        f"{company} announced a strategic partnership to expand into new markets.",
        f"Analysts are optimistic about {company}'s growth prospects for the upcoming year."
    ]
    return random.choice(sample_news)

tool_functions = {
    "get_stock_price": get_stock_price,
    "get_exchange_rate": get_exchange_rate,
    "get_financial_news": get_financial_news
}

custom_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Retrieve the latest stock price for a given ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol, e.g., 'AAPL', 'TSLA'"},
                    "currency": {"type": "string", "enum": ["USD", "EUR", "KRW"], "description": "Currency code for the price."}
                },
                "required": ["ticker", "currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get the current exchange rate between two currencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_currency": {"type": "string", "description": "Base currency code, e.g., 'USD'"},
                    "target_currency": {"type": "string", "description": "Target currency code, e.g., 'EUR'"}
                },
                "required": ["base_currency", "target_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_financial_news",
            "description": "Get recent financial news headlines related to a company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Company name, e.g., 'Apple', 'Tesla'"}
                },
                "required": ["company"]
            }
        }
    }
]


user_inputs = ["What's Tesla's stock price in USD?",
              "What's the current USD to EUR exchange rate?",
              " Also, any recent news about Tesla?"]


tool_functions = {"get_stock_price": get_stock_price,
                  "get_exchange_rate": get_exchange_rate,
                  "get_financial_news": get_financial_news} 

# In[5]:


for user_input in user_inputs:
    messages = [{"role": "user", "content": user_input}]
 
    response = client.chat.completions.create(
        model="furiosa-ai/Llama-3.1-8B-Instruct",
        messages=messages,
        tools=custom_tools,
        tool_choice="auto"
    )

    print("===================")
    print(response.choices[0])
    tool_call = response.choices[0].message.tool_calls[0].function
    print(f"Function called: {tool_call.name}")
    print(f"Arguments: {tool_call.arguments}")
    print(f"Result: {tool_functions[tool_call.name](**json.loads(tool_call.arguments))}")

