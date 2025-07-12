"""
Real flight data scrapers - NO FAKE DATA GENERATION.
This module only fetches real flight data from legitimate sources.
"""

import asyncio
import aiohttp
import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import time
from config import Config
from data_validator import FlightDataValidator

class RealFlightDataScraper:
    """
    Scraper that only returns real flight data.
    NO fallback data generation - fails gracefully if real data unavailable.
    """
    
    def __init__(self):
        self.config = Config()
        self.validator = FlightDataValidator()
        # Validate configuration to ensure no fake data is allowed
        self.config.validate_config()
    
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for real flights between origin and destination.
        Returns empty list if no real data is available - NO FAKE DATA.
        """
        all_flights = []
        
        # Try multiple real data sources
        try:
            # Try Amadeus API first
            amadeus_flights = await self._get_amadeus_flights(origin, destination, departure_date, return_date)
            if amadeus_flights:
                all_flights.extend(amadeus_flights)
        except Exception as e:
            print(f"Amadeus API failed: {e}")
        
        try:
            # Try RapidAPI/Skyscanner as backup
            skyscanner_flights = await self._get_skyscanner_flights(origin, destination, departure_date, return_date)
            if skyscanner_flights:
                all_flights.extend(skyscanner_flights)
        except Exception as e:
            print(f"Skyscanner API failed: {e}")
        
        # Validate all flights to ensure they are real
        validated_flights = self.validator.validate_flight_list(all_flights)
        
        if not validated_flights:
            raise ValueError(f"No real flight data available for {origin} to {destination} on {departure_date}. "
                           "Cannot provide fake data as per configuration.")
        
        return validated_flights
    
    async def _get_amadeus_flights(self, origin: str, destination: str, 
                                  departure_date: str, return_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get real flight data from Amadeus API."""
        if not self.config.AMADEUS_API_KEY or not self.config.AMADEUS_API_SECRET:
            raise ValueError("Amadeus API credentials not configured")
        
        # Get access token
        token = await self._get_amadeus_token()
        if not token:
            raise ValueError("Failed to authenticate with Amadeus API")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'originLocationCode': origin.upper(),
            'destinationLocationCode': destination.upper(),
            'departureDate': departure_date,
            'adults': 1,
            'max': 20
        }
        
        if return_date:
            params['returnDate'] = return_date
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.config.AMADEUS_BASE_URL}/v2/shopping/flight-offers"
            async with session.get(url, headers=headers, params=params, 
                                 timeout=self.config.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_amadeus_response(data)
                else:
                    raise ValueError(f"Amadeus API error: {response.status}")
    
    async def _get_amadeus_token(self) -> Optional[str]:
        """Get access token from Amadeus API."""
        auth_url = f"{self.config.AMADEUS_BASE_URL}/v1/security/oauth2/token"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.config.AMADEUS_API_KEY,
            'client_secret': self.config.AMADEUS_API_SECRET
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(auth_url, headers=headers, data=data) as response:
                if response.status == 200:
                    auth_data = await response.json()
                    return auth_data.get('access_token')
                return None
    
    def _parse_amadeus_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Amadeus API response into standardized flight data."""
        flights = []
        
        for offer in data.get('data', []):
            for itinerary in offer.get('itineraries', []):
                for segment in itinerary.get('segments', []):
                    flight_data = {
                        'airline': segment.get('carrierCode'),
                        'flight_number': f"{segment.get('carrierCode')}{segment.get('number')}",
                        'origin': segment.get('departure', {}).get('iataCode'),
                        'destination': segment.get('arrival', {}).get('iataCode'),
                        'departure_time': segment.get('departure', {}).get('at'),
                        'arrival_time': segment.get('arrival', {}).get('at'),
                        'price': float(offer.get('price', {}).get('total', 0)),
                        'currency': offer.get('price', {}).get('currency'),
                        'duration': segment.get('duration'),
                        'aircraft': segment.get('aircraft', {}).get('code'),
                        'source': 'amadeus'
                    }
                    
                    # Only add if it passes validation (is real data)
                    if self.validator.validate_flight_data(flight_data):
                        flights.append(flight_data)
        
        return flights
    
    async def _get_skyscanner_flights(self, origin: str, destination: str, 
                                    departure_date: str, return_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get real flight data from Skyscanner via RapidAPI."""
        if not self.config.RAPIDAPI_KEY:
            raise ValueError("RapidAPI key not configured")
        
        headers = {
            'X-RapidAPI-Host': 'skyscanner-api.p.rapidapi.com',
            'X-RapidAPI-Key': self.config.RAPIDAPI_KEY
        }
        
        params = {
            'origin': origin.upper(),
            'destination': destination.upper(),
            'departureDate': departure_date,
            'currency': 'USD',
            'adults': 1
        }
        
        if return_date:
            params['returnDate'] = return_date
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.config.SKYSCANNER_API_URL}/flights/search"
            async with session.get(url, headers=headers, params=params,
                                 timeout=self.config.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_skyscanner_response(data)
                else:
                    raise ValueError(f"Skyscanner API error: {response.status}")
    
    def _parse_skyscanner_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Skyscanner API response into standardized flight data."""
        flights = []
        
        # Parse based on Skyscanner API structure
        for flight in data.get('flights', []):
            flight_data = {
                'airline': flight.get('airline_code'),
                'flight_number': flight.get('flight_number'),
                'origin': flight.get('origin'),
                'destination': flight.get('destination'),
                'departure_time': flight.get('departure_time'),
                'arrival_time': flight.get('arrival_time'),
                'price': float(flight.get('price', 0)),
                'currency': flight.get('currency', 'USD'),
                'duration': flight.get('duration'),
                'source': 'skyscanner'
            }
            
            # Only add if it passes validation (is real data)
            if self.validator.validate_flight_data(flight_data):
                flights.append(flight_data)
        
        return flights
    
    def get_flight_details(self, flight_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific flight.
        Returns None if flight not found or data is not real.
        """
        # This would implement detailed flight lookup
        # For now, raises exception as we don't generate fake data
        raise NotImplementedError("Flight details lookup requires specific flight ID from real data source")
    
    def get_price_history(self, origin: str, destination: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get historical price data for a route.
        Returns empty list if no real historical data available.
        """
        # This would implement historical price lookup from real sources
        # For now, raises exception as we don't generate fake historical data
        raise NotImplementedError("Price history requires access to historical flight data APIs")

class NoFakeDataError(Exception):
    """Exception raised when no real flight data is available and fake data is not allowed."""
    pass