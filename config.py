"""
Configuration file for the dynamic flight scraper.
Only real data sources are configured - NO fallback/fake data allowed.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys for real flight data sources
    AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
    AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    
    # Flight data API endpoints
    AMADEUS_BASE_URL = "https://api.amadeus.com"
    SKYSCANNER_API_URL = "https://skyscanner-api.p.rapidapi.com"
    
    # Scraping settings
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    # Data validation settings
    ALLOW_FAKE_DATA = False  # CRITICAL: This must always be False
    REQUIRE_REAL_PRICES = True
    VALIDATE_AIRLINE_CODES = True
    
    # User agents for web scraping
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    @classmethod
    def validate_config(cls):
        """Validate that we have proper API keys for real data sources."""
        if not cls.AMADEUS_API_KEY and not cls.RAPIDAPI_KEY:
            raise ValueError("No real flight data API keys configured. Cannot proceed without real data sources.")
        
        if cls.ALLOW_FAKE_DATA:
            raise ValueError("ALLOW_FAKE_DATA is set to True. This violates the requirement for real data only.")
        
        return True