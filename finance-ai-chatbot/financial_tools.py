import requests
import random

# Dummy API replacement version


def search_finance_news(query: str):
    """
    Simulates searching for financial news.
    """
    print(f"Simulating news search for: {query}")
    dummy_news = [
        {
            "title": "Stock futures slip as U.S. and China agree to framework for future trade talks: Live updates",
            "url": "https://www.cnbc.com/2025/06/10/stock-market-today-live-updates-.html",
        },
        {
            "title": "China, U.S. officials reach agreement for allowing rare-earth, tech trade. Now it’s up to Trump and X",
            "url": "https://www.cnbc.com/2025/06/11/us-china-agree-on-framework-to-implement-geneva-trade-consensus-.html",
        },
        {
            "title": "When it comes to saving, Gen Z asks: ‘What’s the point?’ That’s dangerous, expert says",
            "url": "https://www.cnbc.com/2025/06/07/gen-z-asks-whats-the-point-of-saving-money.html",
        },
    ]
    return [f"{item['title']} - {item['url']}" for item in dummy_news[:3]]


def detect_fraud(transaction_info: str):
    """
    Simulates fraud detection logic.
    """
    print(f"Simulating fraud detection for transaction: {transaction_info}")
    if "suspicious" in transaction_info.lower():
        fraud_risk = "High"
    else:
        fraud_risk = "Low"
    return f"🔍 Fraud Risk Assessment: {fraud_risk}"


def analyze_portfolio(user_id: str):
    """
    Simulates portfolio analysis for a user.
    """
    print(f"Simulating portfolio analysis for user: {user_id}")
    dummy_recommendations = [
        "Increase holdings in renewable energy",
        "Reduce exposure to volatile tech stocks",
        "Consider international diversification",
    ]
    return f"Investment Analysis: {' | '.join(dummy_recommendations)}"


def get_account_balance(user_id: str):
    """
    Retrieves a mock account balance for demonstration.
    """
    balances = {"user123": "$5,000 USD", "user456": "$1,200 USD"}
    return balances.get(user_id, "Account not found.")


def recommend_financial_products(user_id: str):
    """
    Provides personalized investment recommendations.
    """
    recommendations = {
        "user123": "Recommended: Short-term investment fund.",
        "user456": "Recommended: Long-term stable savings account.",
    }
    return recommendations.get(user_id, "No personalized recommendation available.")
