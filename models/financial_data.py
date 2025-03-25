"""
Service for fetching and processing financial data
"""
import pandas as pd
import yfinance as yf
from nsepython import nse_get_index_list, nse_get_index_quote, nse_get_advances_declines
import re
from config import DEFAULT_MARKET, INDEX_SYMBOLS, PRODUCT_TYPES, RISK_PROFILES

class FinancialDataService:
    """Service for handling financial data operations"""
    
    def __init__(self):
        """Initialize the financial data service"""
        self.market = DEFAULT_MARKET
        self.data_cache = {}
        self.cache_timestamp = None
        
    def needs_market_data(self, query):
        """Determine if a query needs real-time market data"""
        market_keywords = [
            "price", "stock", "market", "index", "nifty", "sensex", 
            "current", "today", "performance", "return", "moving average",
            "PE ratio", "dividend", "yield", "mutual fund", "NAV"
        ]
        
        return any(keyword.lower() in query.lower() for keyword in market_keywords)
    
    def get_index_data(self, index_name="NIFTY 50"):
        """Get current index data from NSE"""
        try:
            index_data = nse_get_index_quote(index_name)
            return {
                "name": index_data["name"],
                "last_price": index_data["lastPrice"],
                "change": index_data["change"],
                "percent_change": index_data["pChange"],
                "timestamp": index_data["timestamp"]
            }
        except Exception as e:
            print(f"Error fetching index data: {str(e)}")
            return None
    
    def get_stock_data(self, symbol, period="1mo"):
        """Get historical stock data"""
        try:
            # For Indian stocks, format the symbol correctly
            if self.market == "NSE":
                symbol = f"{symbol}.NS"
                
            data = yf.Ticker(symbol).history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")
            return None
    
    def get_market_overview(self):
        """Get a general market overview with major indices"""
        overview = {}
        
        for index in INDEX_SYMBOLS:
            overview[index] = self.get_index_data(index)
            
        # Get advances/declines data
        try:
            adv_dec = nse_get_advances_declines()
            overview["market_breadth"] = {
                "advances": adv_dec["advances"],
                "declines": adv_dec["declines"],
                "unchanged": adv_dec["unchanged"]
            }
        except Exception as e:
            print(f"Error fetching advances/declines: {str(e)}")
        
        return overview
    
    def extract_stock_symbols(self, query):
        """Extract potential stock symbols from a query"""
        # Basic regex pattern for stock symbols
        pattern = r'\b[A-Z]{2,5}\b'
        matches = re.findall(pattern, query)
        return matches
    
    def get_relevant_data(self, query):
        """Get relevant financial data based on user query"""
        context = {}
        
        # First check for specific stock mentions
        potential_symbols = self.extract_stock_symbols(query)
        if potential_symbols:
            stocks_data = {}
            for symbol in potential_symbols[:3]:  # Limit to 3 stocks for performance
                stocks_data[symbol] = self.get_stock_data(symbol, period="1mo")
            context["stocks"] = stocks_data
        
        # Check for index mentions
        for index in INDEX_SYMBOLS:
            if index.lower() in query.lower():
                context["index"] = self.get_index_data(index)
                break
        
        # If no specific stocks or indices mentioned, provide market overview
        if not context:
            context["market_overview"] = self.get_market_overview()
        
        return context
    
    def search_investments(self, criteria):
        """
        Search for investment products based on criteria
        
        Args:
            criteria (dict): Dict containing search criteria like:
                - risk_profile (str): User's risk profile
                - investment_horizon (str): Short/medium/long term
                - amount (float): Investment amount
                - goal (str): Financial goal
                - product_type (str, optional): Specific product type
        
        Returns:
            list: List of recommended investment products
        """
        # In a real implementation, this would query a database or API
        # For demo purposes, we'll generate some example recommendations
        
        recommendations = []
        risk_profile = criteria.get("risk_profile", "moderate")
        investment_horizon = criteria.get("investment_horizon", "medium")
        product_type = criteria.get("product_type", None)
        
        # Filter products by type if specified
        if product_type and product_type in PRODUCT_TYPES:
            product_types = [product_type]
        else:
            product_types = PRODUCT_TYPES
        
        # Example data - in production, this would come from a database
        if "Mutual Funds" in product_types:
            if risk_profile == "conservative":
                recommendations.append({
                    "name": "HDFC Corporate Bond Fund",
                    "type": "Mutual Fund - Debt",
                    "risk_level": "Low",
                    "returns": "7-8% average annual",
                    "min_investment": 5000,
                    "description": "A debt fund investing in high-quality corporate bonds"
                })
            elif risk_profile == "moderate":
                recommendations.append({
                    "name": "ICICI Prudential Balanced Advantage Fund",
                    "type": "Mutual Fund - Hybrid",
                    "risk_level": "Medium",
                    "returns": "10-12% average annual",
                    "min_investment": 1000,
                    "description": "A balanced fund with dynamic asset allocation"
                })
            elif risk_profile in ["aggressive", "very_aggressive"]:
                recommendations.append({
                    "name": "Axis Small Cap Fund",
                    "type": "Mutual Fund - Equity",
                    "risk_level": "High",
                    "returns": "15-18% average annual",
                    "min_investment": 500,
                    "description": "A small-cap fund focusing on high-growth companies"
                })
        
        if "Fixed Deposits" in product_types and risk_profile in ["conservative", "moderate"]:
            recommendations.append({
                "name": "SBI Fixed Deposit",
                "type": "Fixed Deposit",
                "risk_level": "Very Low",
                "returns": "5.5-6.5% annual",
                "min_investment": 10000,
                "description": "A secure fixed deposit option from State Bank of India"
            })
        
        if "Government Schemes" in product_types:
            recommendations.append({
                "name": "Public Provident Fund (PPF)",
                "type": "Government Scheme",
                "risk_level": "Very Low",
                "returns": "7.1% annual (tax-free)",
                "min_investment": 500,
                "description": "A government-backed long-term savings scheme with tax benefits"
            })
        
        # Add more dynamic recommendations based on criteria
        
        return recommendations