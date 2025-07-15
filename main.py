"""
Main dynamic flight scraper application.
ONLY REAL FLIGHT DATA - NO FAKE/FALLBACK DATA GENERATION.
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from flight_scraper import RealFlightDataScraper, NoFakeDataError
from data_validator import FlightDataValidator
from config import Config

class DynamicFlightScraperApp:
    """
    Main application class for the dynamic flight scraper.
    Enforces strict real-data-only policy.
    """
    
    def __init__(self):
        self.scraper = RealFlightDataScraper()
        self.validator = FlightDataValidator()
        
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for flights with strict real-data validation.
        Fails if no real data is available - NO FAKE DATA FALLBACK.
        """
        try:
            print(f"Searching for real flight data: {origin} → {destination} on {departure_date}")
            
            # Validate input parameters
            if not self._validate_search_params(origin, destination, departure_date):
                raise ValueError("Invalid search parameters")
            
            # Search for real flights only
            flights = await self.scraper.search_flights(origin, destination, departure_date, return_date)
            
            if not flights:
                raise NoFakeDataError(f"No real flight data found for {origin} to {destination}")
            
            # Double-validate all returned flights
            validated_flights = []
            for flight in flights:
                if self.validator.validate_flight_data(flight):
                    validated_flights.append(flight)
                else:
                    print(f"Warning: Filtered out invalid flight data: {flight.get('flight_number', 'Unknown')}")
            
            if not validated_flights:
                raise NoFakeDataError("All flight data failed validation - appears to be fake or corrupted")
            
            print(f"Found {len(validated_flights)} validated real flights")
            return validated_flights
            
        except NoFakeDataError:
            raise
        except Exception as e:
            raise NoFakeDataError(f"Failed to retrieve real flight data: {str(e)}")
    
    def _validate_search_params(self, origin: str, destination: str, departure_date: str) -> bool:
        """Validate search parameters."""
        # Check airport codes
        if (not origin or len(origin) != 3 or 
            not destination or len(destination) != 3):
            return False
        
        # Check date format and validity
        try:
            dep_date = datetime.strptime(departure_date, '%Y-%m-%d')
            if dep_date < datetime.now().date():
                return False
        except ValueError:
            return False
        
        return True
    
    def format_flight_results(self, flights: List[Dict[str, Any]]) -> str:
        """Format flight results for display."""
        if not flights:
            return "No real flight data available."
        
        output = f"\n{'='*80}\n"
        output += f"REAL FLIGHT DATA RESULTS ({len(flights)} flights found)\n"
        output += f"{'='*80}\n"
        
        for i, flight in enumerate(flights, 1):
            output += f"\nFlight {i}:\n"
            output += f"  Airline: {flight.get('airline', 'N/A')}\n"
            output += f"  Flight: {flight.get('flight_number', 'N/A')}\n"
            output += f"  Route: {flight.get('origin', 'N/A')} → {flight.get('destination', 'N/A')}\n"
            output += f"  Departure: {flight.get('departure_time', 'N/A')}\n"
            output += f"  Arrival: {flight.get('arrival_time', 'N/A')}\n"
            output += f"  Price: {flight.get('currency', '$')}{flight.get('price', 'N/A')}\n"
            output += f"  Duration: {flight.get('duration', 'N/A')}\n"
            output += f"  Source: {flight.get('source', 'N/A')}\n"
            output += f"  Status: ✓ VALIDATED REAL DATA\n"
            output += f"  {'-'*40}\n"
        
        return output
    
    async def run_interactive_mode(self):
        """Run the scraper in interactive mode."""
        source_info = self.scraper.get_source_details()
        
        print("\n" + "="*80)
        print("DYNAMIC FLIGHT SCRAPER - 149+ REAL DATA SOURCES")
        print("="*80)
        print("This application searches real flight data from:")
        print(f"• {source_info['airlines']} airline websites")
        print(f"• {source_info['travel_sites']} travel booking sites") 
        print(f"• {len(source_info['api_sources'])} flight data APIs")
        print(f"• TOTAL: {source_info['total_with_apis']} real flight data sources")
        print("\nNo fake or fallback data will EVER be generated.")
        print("All flight data is validated for authenticity.")
        print("="*80 + "\n")
        
        while True:
            try:
                print("\nEnter flight search details:")
                origin = input("Origin airport code (e.g., JFK): ").strip().upper()
                if not origin:
                    break
                
                destination = input("Destination airport code (e.g., LAX): ").strip().upper()
                if not destination:
                    break
                
                departure_date = input("Departure date (YYYY-MM-DD): ").strip()
                if not departure_date:
                    break
                
                return_date = input("Return date (YYYY-MM-DD, optional): ").strip()
                if not return_date:
                    return_date = None
                
                print("\nSearching for real flight data...")
                flights = await self.search_flights(origin, destination, departure_date, return_date)
                
                result = self.format_flight_results(flights)
                print(result)
                
                # Ask if user wants to save results
                save = input("\nSave results to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"flights_{origin}_{destination}_{departure_date.replace('-', '')}.json"
                    with open(filename, 'w') as f:
                        json.dump(flights, f, indent=2, default=str)
                    print(f"Results saved to {filename}")
                
                continue_search = input("\nSearch for more flights? (y/n): ").strip().lower()
                if continue_search != 'y':
                    break
                    
            except NoFakeDataError as e:
                print(f"\nERROR: {e}")
                print("Cannot provide fake data as a fallback. Please try different search parameters.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                continue

async def main():
    """Main entry point."""
    try:
        # Validate configuration first
        Config.validate_config()
        
        app = DynamicFlightScraperApp()
        
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            # Test mode with sample data
            print("Testing with sample search...")
            try:
                flights = await app.search_flights('JFK', 'LAX', '2024-12-25')
                print(app.format_flight_results(flights))
            except NoFakeDataError as e:
                print(f"Test failed as expected (no API keys configured): {e}")
        else:
            # Interactive mode
            await app.run_interactive_mode()
            
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease ensure you have valid API keys configured.")
        print("This application requires real flight data sources and will not generate fake data.")
        sys.exit(1)
    except Exception as e:
        print(f"Application Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting Dynamic Flight Scraper (Real Data Only)...")
    asyncio.run(main())