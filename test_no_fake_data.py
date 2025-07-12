"""
Tests to ensure the dynamic flight scraper NEVER generates fake data.
These tests verify that the application fails gracefully when real data is unavailable.
"""

import unittest
import asyncio
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import our modules
from data_validator import FlightDataValidator
from flight_scraper import RealFlightDataScraper, NoFakeDataError
from config import Config
from main import DynamicFlightScraperApp

class TestNoFakeDataPolicy(unittest.TestCase):
    """Test that the application never generates fake data."""
    
    def setUp(self):
        self.validator = FlightDataValidator()
        # Mock API keys for testing
        with patch.object(Config, 'AMADEUS_API_KEY', 'test_key'):
            with patch.object(Config, 'AMADEUS_API_SECRET', 'test_secret'):
                self.app = DynamicFlightScraperApp()
    
    def test_config_prevents_fake_data(self):
        """Test that configuration prevents fake data generation."""
        # Config should not allow fake data
        self.assertFalse(Config.ALLOW_FAKE_DATA)
        self.assertTrue(Config.REQUIRE_REAL_PRICES)
        
        # Validation should fail if fake data is enabled
        # Need to patch both the API keys and the fake data flag
        with patch.object(Config, 'ALLOW_FAKE_DATA', True):
            with patch.object(Config, 'AMADEUS_API_KEY', 'test_key'):
                with patch.object(Config, 'AMADEUS_API_SECRET', 'test_secret'):
                    with self.assertRaises(ValueError) as context:
                        Config.validate_config()
                    self.assertIn("ALLOW_FAKE_DATA is set to True", str(context.exception))
    
    def test_validator_rejects_fake_data(self):
        """Test that the validator correctly identifies and rejects fake data."""
        # Test obviously fake flight data
        fake_flight_data = [
            {
                'airline': 'XX',  # Invalid airline code
                'flight_number': 'XX123',
                'origin': 'JFK',
                'destination': 'LAX',
                'price': 999.99,  # Suspicious price
                'departure_time': '2024-12-25 10:00:00'
            },
            {
                'airline': 'AA',
                'flight_number': 'AA123',
                'origin': 'XXX',  # Invalid airport code
                'destination': 'LAX',
                'price': 500.00,
                'departure_time': '2024-12-25 10:00:00'
            },
            {
                'airline': 'AA',
                'flight_number': 'AA123',
                'origin': 'JFK',
                'destination': 'LAX',
                'price': 'fake_price',  # Invalid price format
                'departure_time': '2024-12-25 10:00:00'
            },
            {
                'airline': 'TEST',  # Contains 'test' - fake data indicator
                'flight_number': 'TEST123',
                'origin': 'JFK',
                'destination': 'LAX',
                'price': 500.00,
                'departure_time': '2024-12-25 10:00:00'
            }
        ]
        
        for fake_data in fake_flight_data:
            with self.subTest(fake_data=fake_data):
                self.assertFalse(self.validator.validate_flight_data(fake_data))
    
    def test_validator_accepts_real_data(self):
        """Test that validator accepts realistic flight data."""
        # Use a future date for testing
        from datetime import datetime, timedelta
        future_date = datetime.now() + timedelta(days=30)
        future_date_str = future_date.strftime('%Y-%m-%d %H:%M:%S')
        
        real_flight_data = {
            'airline': 'AA',
            'flight_number': 'AA123',
            'origin': 'JFK',
            'destination': 'LAX',
            'price': 456.78,
            'departure_time': future_date_str,
            'arrival_time': future_date_str,
            'currency': 'USD',
            'duration': 'PT5H15M'
        }
        
        self.assertTrue(self.validator.validate_flight_data(real_flight_data))
    
    def test_airline_code_validation(self):
        """Test airline code validation against real IATA codes."""
        # Valid codes
        valid_codes = ['AA', 'DL', 'UA', 'BA', 'LH', 'AF']
        for code in valid_codes:
            self.assertTrue(self.validator._is_valid_airline_code(code))
        
        # Invalid codes
        invalid_codes = ['XX', 'ZZ', 'TEST', '', 'A', 'AAA']
        for code in invalid_codes:
            self.assertFalse(self.validator._is_valid_airline_code(code))
    
    def test_airport_code_validation(self):
        """Test airport code validation against real IATA codes."""
        # Valid codes
        valid_codes = ['JFK', 'LAX', 'LHR', 'CDG', 'DXB', 'SIN']
        for code in valid_codes:
            self.assertTrue(self.validator._is_valid_airport_code(code))
        
        # Invalid codes
        invalid_codes = ['XXX', 'ZZZ', 'TEST', '', 'JF', 'JFKK']
        for code in invalid_codes:
            self.assertFalse(self.validator._is_valid_airport_code(code))
    
    def test_price_validation(self):
        """Test price validation rejects fake prices."""
        # Valid prices
        valid_prices = [89.50, 234.67, 1456.78, 50.00]
        for price in valid_prices:
            self.assertTrue(self.validator._is_valid_price(price))
        
        # Invalid/fake prices
        invalid_prices = [999.99, 1000.00, 123.45, 100.00, -50, 15000, 'fake']
        for price in invalid_prices:
            self.assertFalse(self.validator._is_valid_price(price))
    
    def test_flight_number_format(self):
        """Test flight number format validation."""
        # Valid flight numbers
        valid_flights = [('AA123', 'AA'), ('DL1234', 'DL'), ('UA1', 'UA')]
        for flight_num, airline in valid_flights:
            self.assertTrue(self.validator._is_valid_flight_number(flight_num, airline))
        
        # Invalid flight numbers
        invalid_flights = [('XX123', 'AA'), ('AA', 'AA'), ('AA12345', 'AA'), ('123', 'AA')]
        for flight_num, airline in invalid_flights:
            self.assertFalse(self.validator._is_valid_flight_number(flight_num, airline))
    
    def test_fake_pattern_detection(self):
        """Test detection of fake data patterns."""
        fake_data_examples = [
            {'airline': 'AA', 'flight_number': 'AA123', 'note': 'This is test data'},
            {'airline': 'AA', 'flight_number': 'AA123', 'price': 111.11},  # Pattern price
            {'airline': 'FAKE', 'flight_number': 'FAKE123'},
            {'airline': 'AA', 'flight_number': 'AA123', 'origin': 'demo_airport'}
        ]
        
        for fake_data in fake_data_examples:
            self.assertTrue(self.validator._contains_fake_patterns(fake_data))
    
    def test_empty_flight_list_validation(self):
        """Test that empty flight lists raise appropriate errors."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate_flight_list([])
        self.assertIn("No valid real flight data found", str(context.exception))
    
    @patch('flight_scraper.RealFlightDataScraper._get_amadeus_flights')
    @patch('flight_scraper.RealFlightDataScraper._get_skyscanner_flights')
    async def test_scraper_fails_without_real_data(self, mock_skyscanner, mock_amadeus):
        """Test that scraper fails when no real data sources are available."""
        # Mock API calls to return empty results
        mock_amadeus.return_value = []
        mock_skyscanner.return_value = []
        
        scraper = RealFlightDataScraper()
        
        with self.assertRaises(ValueError) as context:
            await scraper.search_flights('JFK', 'LAX', '2024-12-25')
        
        self.assertIn("No real flight data available", str(context.exception))
    
    @patch('flight_scraper.RealFlightDataScraper._get_amadeus_flights')
    async def test_scraper_validates_returned_data(self, mock_amadeus):
        """Test that scraper validates all returned data."""
        # Mock API to return mix of valid and invalid data
        mock_amadeus.return_value = [
            {  # Valid data
                'airline': 'AA',
                'flight_number': 'AA123',
                'origin': 'JFK',
                'destination': 'LAX',
                'price': 456.78,
                'departure_time': '2024-12-25 14:30:00'
            },
            {  # Invalid data (fake airline)
                'airline': 'XX',
                'flight_number': 'XX999',
                'origin': 'JFK',
                'destination': 'LAX',
                'price': 999.99,
                'departure_time': '2024-12-25 14:30:00'
            }
        ]
        
        scraper = RealFlightDataScraper()
        flights = await scraper.search_flights('JFK', 'LAX', '2024-12-25')
        
        # Should only return the valid flight
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]['airline'], 'AA')

class TestAPIIntegration(unittest.TestCase):
    """Test API integration without making real API calls."""
    
    def test_config_validation_requires_api_keys(self):
        """Test that configuration validation requires API keys."""
        # Mock missing API keys
        with patch.object(Config, 'AMADEUS_API_KEY', None):
            with patch.object(Config, 'RAPIDAPI_KEY', None):
                with self.assertRaises(ValueError) as context:
                    Config.validate_config()
                self.assertIn("No real flight data API keys configured", str(context.exception))

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)