import asyncio
import json
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch

from financial_tools import (
    search_finance_news,
    get_account_balance,
    recommend_financial_products,
    detect_fraud,
    analyze_portfolio,
)
from sentiment_analysis import (
    analyze_sentiment,
)  # Sentiment analysis for better customer experience

# AI Model Setup
llm_easy = ChatOpenAI(
    base_url="http://localhost:8889/v1", api_key="token-abc123", model="Llama-3.1-8B"
)
llm_hard = ChatOpenAI(
    base_url="http://localhost:8888/v1", api_key="token-abc456", model="DeepSeek-R1-8B"
)

# Define prompts for financial queries
direct_prompt = PromptTemplate.from_template(
    "Provide a direct financial answer:\n\n{input}"
)
market_prompt = PromptTemplate.from_template("Analyze today's stock market:\n\n{input}")
security_prompt = PromptTemplate.from_template(
    "Offer financial security tips:\n\n{input}"
)
recommend_prompt = PromptTemplate.from_template(
    "Suggest the best financial product based on the user's profile:\n\n{input}"
)

# Create LLM Chains
direct_chain = direct_prompt | llm_easy
market_chain = market_prompt | llm_hard
security_chain = security_prompt | llm_easy
recommend_chain = recommend_prompt | llm_hard

# Routing Setup for Financial Queries
router_prompt = PromptTemplate.from_template(
    """
You are a financial AI assistant deciding how to respond to a customer inquiry.
Return JSON:
{{
    "destination": "<one of: direct answer, market analysis, security tips, product recommendation>",
    "next_inputs": "{input}",
}}
Question: {input}
"""
)


def parse_response(response: AIMessage):

    try:
        parsed = json.loads(response.content)
        print("parsed result:", parsed)
        return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse response: {response}") from e


router_chain = router_prompt | llm_easy | RunnableLambda(lambda x: parse_response(x))


strategy_chains = {
    "direct answer": direct_chain,
    "market analysis": market_chain,
    "security tips": security_chain,
    "product recommendation": recommend_chain,
}


multi_chain = router_chain | RunnableBranch(
    (
        lambda x: x["destination"] == "direct answer",
        RunnableLambda(lambda x: {"input": x["next_inputs"]}) | direct_chain,
    ),
    (
        lambda x: x["destination"] == "market analysis",
        RunnableLambda(lambda x: {"input": x["next_inputs"]}) | market_chain,
    ),
    (
        lambda x: x["destination"] == "security tips",
        RunnableLambda(lambda x: {"input": x["next_inputs"]}) | security_chain,
    ),
    (
        lambda x: x["destination"] == "product recommendation",
        RunnableLambda(lambda x: {"input": x["next_inputs"]}) | recommend_chain,
    ),
    RunnableLambda(lambda x: {"input": x["next_inputs"]})
    | direct_chain,  # default fallback
)


class FinanceChatbot:
    def __init__(self):
        self.history_file = "chat_history.json"
        self.history = self.load_chat_history()

    def load_chat_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    async def get_response(self, question: str, user_id: str) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, multi_chain.invoke, {"input": question}
        )
        response_text = response.content

        # Additional financial functions
        if "balance" in question.lower():
            response_text += (
                f"\n👉 Your current account balance: {get_account_balance(user_id)}"
            )
        elif "stock market" in question.lower():
            response_text += f"\n📰 See the latest financial news: {search_finance_news(question)}"
        elif "recommendation" in question.lower():
            response_text += f"\n💡 Recommended financial product: {recommend_financial_products(user_id)}"
        elif "fraud" in question.lower():
            response_text += f"\n🔍 Fraud Detection Result: {detect_fraud(question)}"
        elif "portfolio analysis" in question.lower():
            response_text += f"\n📊 Investment Insights: {analyze_portfolio(user_id)}"

        # Sentiment analysis for enhanced customer experience
        sentiment = analyze_sentiment(question)
        if sentiment == "negative":
            response_text = (
                f"😢 It seems like you're frustrated. "
                f"Here's my response with additional support:\n\n{response_text}"
            )

        # Save chat history
        self.history.setdefault(user_id, []).append(
            {"question": question, "response": response_text}
        )
        self.save_chat_history()

        return response_text

    def save_chat_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
