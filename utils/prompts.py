"""
Prompt templates for the Gemini AI model
"""

def get_financial_prompt(user_query, financial_data=None):
    """
    Generate a prompt for financial advice based on user query
    
    Args:
        user_query (str): The user's query
        financial_data (dict, optional): Financial data context
        
    Returns:
        str: The formatted prompt
    """
    base_prompt = """
You are a helpful and knowledgeable financial assistant for Indian investors. Your goal is to help users understand financial concepts, make informed investment decisions, and improve their financial literacy. Focus on providing accurate, educational information that is relevant to the Indian financial market.

Remember these important guidelines:
1. Always provide financial education rather than specific investment advice
2. Explain concepts in simple language suitable for beginners
3. Include relevant Indian context (taxes, regulations, etc.)
4. Cite numerical data with proper context and disclaimers
5. Emphasize long-term investing principles
6. Encourage diversification and risk management
7. Be accurate about tax implications but remind users to consult tax professionals
8. Include both pros and cons for investment products

USER QUERY: {user_query}
"""
    
    # Add financial data context if available
    if financial_data:
        data_context = "\n\nRELEVANT FINANCIAL DATA:\n"
        
        if "market_overview" in financial_data:
            overview = financial_data["market_overview"]
            data_context += "MARKET OVERVIEW:\n"
            
            for index_name, index_data in overview.items():
                if index_name != "market_breadth" and index_data:
                    data_context += f"- {index_name}: {index_data['last_price']} ({index_data['percent_change']}%)\n"
            
            if "market_breadth" in overview:
                breadth = overview["market_breadth"]
                data_context += f"- Market Breadth: Advances {breadth['advances']}, Declines {breadth['declines']}\n"
        
        if "stocks" in financial_data:
            stocks = financial_data["stocks"]
            data_context += "\nSTOCK DATA:\n"
            
            for symbol, data in stocks.items():
                if data is not None and not data.empty:
                    recent = data.iloc[-1]
                    start = data.iloc[0]
                    change_percent = ((recent['Close'] - start['Close']) / start['Close']) * 100
                    data_context += f"- {symbol}: Latest Close ₹{recent['Close']:.2f}, 1-Month Change: {change_percent:.2f}%\n"
        
        if "index" in financial_data:
            index_data = financial_data["index"]
            data_context += f"\nINDEX DATA - {index_data['name']}:\n"
            data_context += f"- Current Value: {index_data['last_price']}\n"
            data_context += f"- Change: {index_data['change']} ({index_data['percent_change']}%)\n"
            data_context += f"- As of: {index_data['timestamp']}\n"
        
        base_prompt += data_context
    
    # Add reply formatting instructions
    base_prompt += """

Now provide a helpful response that:
1. Directly addresses the user's query
2. Explains financial concepts in simple terms
3. Provides relevant information for the Indian context
4. Includes specific details from the financial data provided (if relevant)
5. Offers educational guidance rather than specific investment recommendations
6. Suggests questions the user might want to ask next to learn more

ASSISTANT RESPONSE:
"""
    
    # Format the prompt with the user query
    formatted_prompt = base_prompt.format(user_query=user_query)
    return formatted_prompt

def get_risk_assessment_prompt(user_answers):
    """
    Generate a prompt for risk assessment based on user answers
    
    Args:
        user_answers (dict): The user's answers to risk assessment questions
        
    Returns:
        str: The formatted prompt
    """
    prompt = """
You are a helpful financial assistant conducting a risk assessment for an Indian investor.

Based on the following user responses, analyze their risk profile and provide appropriate guidance:

"""
    
    for question, answer in user_answers.items():
        prompt += f"Question: {question}\nUser Answer: {answer}\n\n"
    
    prompt += """
Please provide:
1. An assessment of the user's risk profile (Conservative, Moderate, Aggressive, or Very Aggressive)
2. A brief explanation of what this risk profile means
3. General asset allocation guidance appropriate for this risk profile
4. Examples of investment products suited to this profile in the Indian market
5. Important considerations the user should keep in mind

Keep your response educational rather than prescriptive. Emphasize that this is a general assessment and not personalized financial advice.
"""
    
    return prompt

def get_investment_recommendation_prompt(criteria):
    """
    Generate a prompt for investment recommendations based on criteria
    
    Args:
        criteria (dict): The user's investment criteria
        
    Returns:
        str: The formatted prompt
    """
    prompt = """
You are a helpful financial assistant providing educational information about investment options for an Indian investor.

Based on the following criteria, suggest suitable investment categories and educational information:

"""
    
    for key, value in criteria.items():
        prompt += f"{key.replace('_', ' ').title()}: {value}\n"
    
    prompt += """
Please provide:
1. An overview of 3-5 investment categories that might be suitable given these criteria
2. For each category:
   - A brief explanation of how it works
   - Typical returns that might be expected (historical range)
   - Associated risks
   - Minimum investment typically required
   - Tax implications in India
3. General educational considerations for the investor based on their criteria
4. Questions they should ask themselves before investing

Remember to provide educational information only, not specific investment advice. Make it clear that past performance is not indicative of future results and that all investments carry risk.
"""
    
    return prompt

def get_financial_literacy_prompt(topic, experience_level="beginner"):
    """
    Generate a prompt for financial literacy education
    
    Args:
        topic (str): The financial topic
        experience_level (str): The user's experience level
        
    Returns:
        str: The formatted prompt
    """
    prompt = f"""
You are a helpful financial educator providing information about "{topic}" for an Indian investor with {experience_level} level experience.

Please provide:
1. A simple explanation of {topic} in plain language
2. Why this topic is important for investors in India
3. Key concepts that someone should understand about this topic
4. How this relates to the Indian financial/tax system specifically
5. Common misconceptions about this topic
6. Next steps for someone who wants to learn more

For a {experience_level}, focus on:
"""
    
    if experience_level == "beginner":
        prompt += """
- Very basic explanations with analogies
- Avoiding jargon and technical terms when possible
- Covering fundamental concepts only
- Simple examples that relate to everyday life
"""
    elif experience_level == "intermediate":
        prompt += """
- More detailed explanations with some technical terms
- Connections between different financial concepts
- More specific examples with numbers
- Some discussion of strategies and approaches
"""
    else:  # advanced
        prompt += """
- In-depth analysis including technical considerations
- Detailed discussion of strategies, risks, and optimization
- Specific numerical examples with calculations
- Reference to relevant regulations and recent changes
"""
    
    prompt += """
Make your response educational and informative, focusing on Indian context where relevant. Avoid giving specific investment advice.
"""
    
    return prompt