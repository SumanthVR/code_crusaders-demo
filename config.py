"""
Configuration settings for the Financial Assistant application
"""
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API settings
GEMINI_MODEL = "gemini-1.5-pro-latest"
API_KEY = os.getenv("GOOGLE_API_KEY")

# Response settings
GREETING_RESPONSES = [
    "Hello! How can I help with your financial questions today?",
    "Hi there! What financial topics would you like to discuss?",
    "Hey! I'm ready to assist with your investment questions.",
    "Greetings! Ask me anything about personal finance."
]

MAX_RESPONSE_TOKENS = 500  # Normal responses
SHORT_RESPONSE_TOKENS = 50  # For simple non-greeting messages

# Financial data settings
DEFAULT_MARKET = "NSE"  # National Stock Exchange (India)
INDEX_SYMBOLS = ["NIFTY 50", "NIFTY BANK", "NIFTY IT"]
CURRENCY = "INR"

# Application settings
DEBUG = os.getenv("FLASK_ENV") == "development"
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# Financial literacy categories
FINANCIAL_CATEGORIES = [
    "Investing Basics",
    "Stock Market",
    "Mutual Funds",
    "Tax Planning",
    "Retirement Planning",
    "Insurance",
    "Fixed Income",
    "Risk Assessment",
    "Portfolio Management"
]

# Risk profiles
RISK_PROFILES = {
    "conservative": "Low-risk investments focusing on capital preservation",
    "moderate": "Balanced approach between growth and preservation",
    "aggressive": "Higher risk strategy focusing on growth potential",
    "very_aggressive": "Maximum growth potential with high volatility tolerance"
}

# Financial product types for recommendations
PRODUCT_TYPES = [
    "Mutual Funds",
    "Stocks",
    "ETFs",
    "Bonds",
    "Fixed Deposits",
    "Government Schemes",
    "PPF",
    "NPS"
]

# User experience levels
EXPERIENCE_LEVELS = ["beginner", "intermediate", "advanced"]

# Age brackets for investment recommendations
AGE_BRACKETS = ["18-30", "31-45", "46-60", "60+"]
