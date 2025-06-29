#!/usr/bin/env python
# coding: utf-8
import time
from openai import OpenAI
import json
import subprocess
import random

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
            "npu:0",
        ]
    )
    return server

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


if __name__ == "__main__":


    server = start_furiosa_llm_servers()
    time.sleep(50)

    client = OpenAI(base_url = f"http://localhost:8000/v1", 
                    api_key="EMPTY")

    try:
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
    finally:
        server.terminate()
        server.wait()
