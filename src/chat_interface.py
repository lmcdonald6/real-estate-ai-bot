"""
Real Estate Chat Interface
Handles natural language processing and response formatting for property queries.
"""

from typing import Dict, List
import json
import logging
from datetime import datetime

from .data.manager import DataManager
from .utils.formatter import ResponseFormatter
from .real_estate_agent import RealEstateAgent

class RealEstateChatInterface:
    def __init__(self):
        self.data_manager = DataManager()
        self.formatter = ResponseFormatter()
        self.agent = RealEstateAgent()
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def process_query(self, query: str) -> Dict:
        """Process a natural language property query."""
        try:
            # Analyze query intent
            query_type = self.agent.analyze_query_type(query)
            
            # Fetch relevant data
            property_data = await self.data_manager.fetch_property_data(query)
            
            # Format response based on query type
            if query_type == "value_analysis":
                response = self.formatter.format_value_analysis(property_data)
            elif query_type == "property_details":
                response = self.formatter.format_property_details(property_data)
            elif query_type == "owner_info":
                response = self.formatter.format_owner_analysis(property_data)
            elif query_type == "occupancy":
                response = self.formatter.format_occupancy_status(property_data)
            elif query_type == "distressed":
                response = self.formatter.format_distressed_analysis(property_data)
            elif query_type == "market":
                response = self.formatter.format_market_analysis(property_data)
            elif query_type == "investment":
                response = self.formatter.format_investment_analysis(property_data)
            else:
                response = self.formatter.format_comprehensive_view(property_data)

            return {
                "status": "success",
                "response": response,
                "query_type": query_type,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to process query: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
