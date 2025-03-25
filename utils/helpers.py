"""
Helper functions for the financial assistant
"""
import re
import json

def validate_input(user_input):
    """
    Validate user input to ensure it's appropriate and related to finance
    
    Args:
        user_input (str): The user's message
        
    Returns:
        bool: True if input is valid, False otherwise
    """
    if not user_input or user_input.strip() == "":
        return False
    
    # Extremely simple check for now - could be expanded with more sophisticated validation
    if len(user_input) < 2:
        return False
    
    return True

def format_response(response_text):
    """
    Format the AI response to be more readable and user-friendly
    
    Args:
        response_text (str): The raw AI response
        
    Returns:
        str: The formatted response
    """
    # Replace multiple newlines with just two
    formatted = re.sub(r'\n{3,}', '\n\n', response_text)
    
    # Add markdown formatting for better rendering
    # Convert headers
    formatted = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', formatted, flags=re.MULTILINE)
    formatted = re.sub(r'^## (.*?)$', r'<h3>\1</h3>', formatted, flags=re.MULTILINE)
    
    # Convert lists
    formatted = re.sub(r'^\* (.*?)$', r'• \1', formatted, flags=re.MULTILINE)
    
    # Convert simple tables if present
    # This is basic - a more comprehensive approach would use a markdown parser
    
    return formatted

def extract_financial_entities(text):
    """
    Extract financial entities from text like stock symbols, amounts, etc.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Extracted entities
    """
    entities = {}
    
    # Extract stock symbols - simple implementation
    stock_pattern = r'\b[A-Z]{2,5}\b'
    entities['stocks'] = re.findall(stock_pattern, text)
    
    # Extract monetary amounts
    money_pattern = r'₹\s*\d+(?:,\d+)*(?:\.\d+)?|\d+(?:,\d+)*(?:\.\d+)?\s*(?:rupees|Rs\.?|INR)'
    entities['amounts'] = re.findall(money_pattern, text)
    
    # Extract percentages
    percentage_pattern = r'\d+(?:\.\d+)?\s*%'
    entities['percentages'] = re.findall(percentage_pattern, text)
    
    # Extract time periods
    time_pattern = r'\b(?:\d+\s+)?(?:year|month|day|week)s?\b'
    entities['time_periods'] = re.findall(time_pattern, text, re.IGNORECASE)
    
    return entities

def detect_user_intent(query):
    """
    Detect the user's intent from their query
    
    Args:
        query (str): The user's query
        
    Returns:
        str: The detected intent
    """
    query = query.lower()
    
    # Define intent patterns
    intents = {
        "learn_basics": ["what is", "how does", "explain", "understand", "basics", "beginner"],
        "market_info": ["market", "current", "today", "performance", "nifty", "sensex"],
        "product_search": ["recommend", "find", "suggest", "best", "investment", "options"],
        "risk_assessment": ["risk", "profile", "assessment", "tolerance", "conservative", "aggressive"],
        "calculate": ["calculate", "returns", "interest", "sip", "lumpsum", "maturity"],
        "tax": ["tax", "saving", "section", "80c", "deduction", "exempt"],
        "compare": ["compare", "difference", "better", "versus", "vs"]
    }
    
    # Check for matches
    for intent, keywords in intents.items():
        if any(keyword in query for keyword in keywords):
            return intent
    
    return "general"

def parse_investment_criteria(query):
    """
    Parse investment criteria from user query
    
    Args:
        query (str): The user's investment query
        
    Returns:
        dict: Extracted investment criteria
    """
    criteria = {}
    
    # Extract risk profile
    risk_patterns = {
        "conservative": ["conservative", "safe", "low risk", "no risk", "secure"],
        "moderate": ["moderate", "balanced", "medium risk"],
        "aggressive": ["aggressive", "high risk", "growth", "higher returns"],
        "very_aggressive": ["very aggressive", "maximum growth", "highest returns"]
    }
    
    for profile, keywords in risk_patterns.items():
        if any(keyword in query.lower() for keyword in keywords):
            criteria["risk_profile"] = profile
            break
    
    # Extract investment horizon
    if any(term in query.lower() for term in ["short term", "1 year", "one year", "few months"]):
        criteria["investment_horizon"] = "short"
    elif any(term in query.lower() for term in ["medium term", "3 year", "three year", "2-5 year"]):
        criteria["investment_horizon"] = "medium"
    elif any(term in query.lower() for term in ["long term", "5 year", "10 year", "retirement"]):
        criteria["investment_horizon"] = "long"
    
    # Extract amount patterns
    amount_pattern = r'(?:Rs\.?|₹|INR)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rupees|Rs\.?|INR|lakhs?|crores?)?'
    amount_matches = re.search(amount_pattern, query, re.IGNORECASE)
    
    if amount_matches:
        amount_str = amount_matches.group(1).replace(',', '')
        amount = float(amount_str)
        
        # Convert lakhs/crores to actual numbers
        if "lakh" in query.lower():
            amount *= 100000
        elif "crore" in query.lower():
            amount *= 10000000
            
        criteria["amount"] = amount
    
    # Extract goals
    goals = {
        "retirement": ["retirement", "retire", "old age"],
        "education": ["education", "college", "school", "university"],
        "home": ["home", "house", "property"],
        "emergency": ["emergency", "fund", "rainy day"],
        "wealth": ["wealth", "build wealth", "grow money"]
    }
    
    for goal, keywords in goals.items():
        if any(keyword in query.lower() for keyword in keywords):
            criteria["goal"] = goal
            break
    
    return criteria