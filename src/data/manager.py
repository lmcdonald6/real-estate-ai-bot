"""
Data Manager
Handles property data caching and retrieval with in-memory storage.
"""

from typing import Dict, Optional
import logging
import json
from datetime import datetime, timedelta
import aiohttp
import os
from dotenv import load_dotenv

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cache = {}
        self._cache_ttl = timedelta(hours=24)
        
        # Load environment variables
        load_dotenv()
        self.attom_api_key = os.getenv('ATTOM_API_KEY')
        
        if not self.attom_api_key:
            self.logger.warning("ATTOM API key not found in environment variables")

    async def fetch_property_data(self, query: str) -> Dict:
        """Fetch property data from cache or API."""
        # Parse address from query
        address = self._parse_address(query)
        cache_key = self._generate_cache_key(address)
        
        # Check cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            self.logger.info(f"Cache hit for {address}")
            return cached_data
            
        # Fetch from API if not in cache
        try:
            property_data = await self._fetch_from_api(address)
            self._add_to_cache(cache_key, property_data)
            return property_data
        except Exception as e:
            self.logger.error(f"Error fetching property data: {str(e)}")
            raise

    def _parse_address(self, query: str) -> Dict:
        """Extract address components from query string."""
        # Basic address parsing
        parts = query.lower().split()
        address = {
            'street_number': '',
            'street_name': '',
            'city': '',
            'state': '',
            'zip': ''
        }
        
        # Extract components (simplified)
        for i, part in enumerate(parts):
            if part.isdigit() and not address['street_number']:
                address['street_number'] = part
            elif part in ['st', 'street', 'ave', 'avenue', 'rd', 'road']:
                address['street_name'] = ' '.join(parts[1:i+1])
                remaining = parts[i+1:]
                if len(remaining) >= 2:
                    address['city'] = remaining[0]
                    address['state'] = remaining[1]
                    if len(remaining) > 2 and remaining[2].isdigit():
                        address['zip'] = remaining[2]
                break
                
        return address

    def _generate_cache_key(self, address: Dict) -> str:
        """Generate a unique cache key for an address."""
        components = [
            address['street_number'],
            address['street_name'],
            address['city'],
            address['state'],
            address['zip']
        ]
        return '_'.join(filter(None, components)).lower()

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Retrieve data from cache if not expired."""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_ttl:
                return data
            else:
                del self._cache[key]
        return None

    def _add_to_cache(self, key: str, data: Dict) -> None:
        """Add data to cache with current timestamp."""
        self._cache[key] = (data, datetime.now())

    async def _fetch_from_api(self, address: Dict) -> Dict:
        """Fetch property data from ATTOM API."""
        # Construct API URL
        base_url = "https://api.attomdata.com/property/detail"
        address_str = f"{address['street_number']} {address['street_name']}"
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'apikey': self.attom_api_key,
                'accept': 'application/json'
            }
            params = {
                'address': address_str,
                'city': address['city'],
                'state': address['state'],
                'zip': address['zip']
            }
            
            try:
                async with session.get(base_url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_api_response(data)
                    else:
                        error_msg = f"API request failed with status {response.status}"
                        self.logger.error(error_msg)
                        raise Exception(error_msg)
            except Exception as e:
                self.logger.error(f"API request error: {str(e)}")
                raise

    def _process_api_response(self, api_data: Dict) -> Dict:
        """Process and structure API response data."""
        # Extract relevant data (example structure)
        property_data = {
            'address': '',
            'price': 0,
            'property_details': {
                'beds': 0,
                'baths': 0,
                'sqft': 0,
                'lot_size': 0,
                'year_built': 0,
                'condition': '',
                'repairs_needed': {
                    'major': [],
                    'moderate': [],
                    'minor': []
                }
            },
            'owner_info': {
                'type': '',
                'time_owned': 0,
                'estimated_equity': 0,
                'tax_status': '',
                'contact_info': {
                    'response_rate': 0,
                    'best_contact_time': ''
                }
            },
            'financial_metrics': {
                'arv': 0,
                'repair_estimate': 0,
                'max_offer': 0,
                'potential_roi': 0,
                'cap_rate': 0,
                'rental_estimate': 0
            },
            'market_data': {
                'price_trends': {},
                'sales_metrics': {},
                'rental_metrics': {},
                'development': {}
            },
            'distress_indicators': [],
            'lead_status': {
                'category': '',
                'priority': 0,
                'next_action': '',
                'follow_up_date': ''
            }
        }
        
        # Populate with mock data for testing
        self._populate_mock_data(property_data)
        
        return property_data

    def _populate_mock_data(self, data: Dict) -> None:
        """Populate mock data for testing."""
        data.update({
            'address': '123 Main St, Bessemer, AL 35020',
            'price': 150000,
            'property_details': {
                'beds': 3,
                'baths': 2,
                'sqft': 1800,
                'lot_size': 0.25,
                'year_built': 1985,
                'condition': 'Fair',
                'repairs_needed': {
                    'major': ['Roof replacement', 'HVAC system upgrade'],
                    'moderate': ['Kitchen renovation', 'Bathroom updates'],
                    'minor': ['Interior paint', 'Carpet replacement', 'Landscaping']
                }
            },
            'owner_info': {
                'type': 'Absentee',
                'time_owned': '2010',
                'estimated_equity': '45%',
                'tax_status': 'Delinquent',
                'contact_info': {
                    'response_rate': '60%',
                    'best_contact_time': 'Evening'
                }
            },
            'financial_metrics': {
                'arv': 225000,
                'repair_estimate': 45000,
                'max_offer': 135000,
                'potential_roi': 28,
                'cap_rate': 8.2,
                'rental_estimate': 1500
            },
            'market_data': {
                'price_trends': {
                    '1_month': '+1.2%',
                    '3_month': '+3.5%',
                    '12_month': '+8.7%'
                },
                'sales_metrics': {
                    'velocity': '14 days',
                    'absorption_rate': '2.8 months',
                    'sale_to_list_ratio': '98%'
                },
                'rental_metrics': {
                    'average_rent': '$1,450',
                    'vacancy_rate': '3.2%',
                    'rent_growth': '+5.2%'
                },
                'development': {
                    'zoning_changes': 'None',
                    'new_construction': 'Low',
                    'infrastructure': 'Stable'
                }
            },
            'distress_indicators': ['tax_delinquent', 'vacant'],
            'lead_status': {
                'category': 'Hot',
                'priority': 1,
                'next_action': 'Direct Mail + Phone Call',
                'follow_up_date': '2025-03-21'
            }
        })
