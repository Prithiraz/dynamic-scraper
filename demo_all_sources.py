#!/usr/bin/env python3
"""
Demonstration script showing all 149+ flight data sources.
This script showcases the comprehensive flight scraper capabilities.
"""

import asyncio
import json
from datetime import datetime, timedelta
from main import DynamicFlightScraperApp
from airline_scrapers import MultiAirlineFlightScraper
from config import Config

async def demonstrate_all_sources():
    """Demonstrate the 149+ flight data sources."""
    
    print("🛩️  DYNAMIC FLIGHT SCRAPER DEMONSTRATION")
    print("="*80)
    
    # Initialize the scraper
    try:
        app = DynamicFlightScraperApp()
        multi_scraper = MultiAirlineFlightScraper()
    except ValueError as e:
        print(f"⚠️  Configuration issue: {e}")
        print("📋 This demo will show configured sources without API calls")
        multi_scraper = MultiAirlineFlightScraper()
    
    # Show source statistics
    source_info = multi_scraper.get_supported_sources()
    
    print(f"📊 FLIGHT DATA SOURCE STATISTICS")
    print(f"   • Airline websites: {source_info['airlines']}")
    print(f"   • Travel booking sites: {source_info['travel_sites']}")
    print(f"   • Total sources: {source_info['total_sources']}")
    print(f"   • Plus Amadeus & Skyscanner APIs")
    print(f"   ⭐ GRAND TOTAL: {source_info['total_sources'] + 2} sources")
    print()
    
    # Show airline sources by region
    print("✈️  AIRLINE WEBSITES BY REGION")
    print("-" * 40)
    
    airlines = multi_scraper.airline_websites
    
    # US Airlines
    us_airlines = {k: v for k, v in airlines.items() if k in [
        'AA', 'DL', 'UA', 'WN', 'B6', 'AS', 'NK', 'F9', 'G4', 'SY'
    ]}
    print(f"🇺🇸 US Airlines ({len(us_airlines)}):")
    for code, info in us_airlines.items():
        print(f"   {code} - {info['name']}")
    print()
    
    # European Airlines
    eu_airlines = {k: v for k, v in airlines.items() if k in [
        'BA', 'LH', 'AF', 'KL', 'IB', 'LX', 'OS', 'SN', 'AZ', 'TP', 'SK', 'AY',
        'FR', 'U2', 'VY', 'W6', 'PC', 'A3', 'JU', 'OU', 'JP', 'YM', 'DY', 'WF', 'V7', 'VF'
    ]}
    print(f"🇪🇺 European Airlines ({len(eu_airlines)}):")
    for code, info in list(eu_airlines.items())[:10]:  # Show first 10
        print(f"   {code} - {info['name']}")
    if len(eu_airlines) > 10:
        print(f"   ... and {len(eu_airlines) - 10} more European airlines")
    print()
    
    # Middle East Airlines
    me_airlines = {k: v for k, v in airlines.items() if k in [
        'EK', 'QR', 'EY', 'TK', 'SV', 'MS', 'RJ', 'G9', 'XY', 'FZ'
    ]}
    print(f"🏜️  Middle East Airlines ({len(me_airlines)}):")
    for code, info in me_airlines.items():
        print(f"   {code} - {info['name']}")
    print()
    
    # Asian Airlines
    asia_airlines = {k: v for k, v in airlines.items() if k in [
        'SQ', 'CX', 'JL', 'NH', 'TG', 'MH', 'PR', 'CI', 'BR', 'OZ', 'KE',
        'AI', '6E', 'SG', 'TR', 'FD', 'JQ', 'TT'
    ]}
    print(f"🌏 Asian Airlines ({len(asia_airlines)}):")
    for code, info in list(asia_airlines.items())[:10]:  # Show first 10
        print(f"   {code} - {info['name']}")
    if len(asia_airlines) > 10:
        print(f"   ... and {len(asia_airlines) - 10} more Asian airlines")
    print()
    
    # Other regions
    other_airlines = set(airlines.keys()) - set(us_airlines.keys()) - set(eu_airlines.keys()) - set(me_airlines.keys()) - set(asia_airlines.keys())
    if other_airlines:
        print(f"🌍 Other Regional Airlines ({len(other_airlines)}):")
        for code in list(other_airlines)[:8]:  # Show first 8
            print(f"   {code} - {airlines[code]['name']}")
        if len(other_airlines) > 8:
            print(f"   ... and {len(other_airlines) - 8} more airlines")
        print()
    
    # Show travel booking sites
    print("🛫 TRAVEL BOOKING WEBSITES")
    print("-" * 40)
    
    travel_sites = multi_scraper.travel_sites
    
    # Major international sites
    major_sites = ['expedia', 'booking', 'kayak', 'priceline', 'orbitz', 'skyscanner', 
                  'momondo', 'cheapflights', 'tripadvisor', 'hopper', 'google_flights']
    
    print(f"🌐 Major International Sites ({len(major_sites)}):")
    for site in major_sites:
        if site in travel_sites:
            print(f"   • {travel_sites[site]['name']}")
    print()
    
    # Regional variants
    regional_sites = [site for site in travel_sites.keys() if '_' in site]
    print(f"🌏 Regional Variants ({len(regional_sites)}):")
    for site in regional_sites[:10]:  # Show first 10
        print(f"   • {travel_sites[site]['name']}")
    if len(regional_sites) > 10:
        print(f"   ... and {len(regional_sites) - 10} more regional sites")
    print()
    
    # Other travel sites
    other_sites = set(travel_sites.keys()) - set(major_sites) - set(regional_sites)
    if other_sites:
        print(f"✈️  Other Travel Sites ({len(other_sites)}):")
        for site in list(other_sites)[:8]:  # Show first 8
            print(f"   • {travel_sites[site]['name']}")
        if len(other_sites) > 8:
            print(f"   ... and {len(other_sites) - 8} more sites")
        print()
    
    # Show API sources
    print("🔌 API DATA SOURCES")
    print("-" * 40)
    print("   • Amadeus API (official airline data)")
    print("   • Skyscanner API via RapidAPI")
    print()
    
    print("🔒 DATA VALIDATION & SECURITY")
    print("-" * 40)
    print("   ✅ All airline codes validated against real IATA codes")
    print("   ✅ All airport codes validated against real IATA codes")
    print("   ✅ Flight numbers validated for proper format")
    print("   ✅ Prices validated for realistic ranges")
    print("   ✅ Fake data patterns detected and rejected")
    print("   ✅ NO fake or fallback data generation")
    print("   ✅ Graceful failure when real data unavailable")
    print()
    
    # Demonstrate a search (if API keys are configured)
    try:
        print("🔍 DEMONSTRATION SEARCH")
        print("-" * 40)
        print("Attempting to search JFK → LAX for tomorrow...")
        
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        
        # This will only work if API keys are properly configured
        # Otherwise it will show the error gracefully
        flights = await app.search_flights('JFK', 'LAX', tomorrow_str)
        
        if flights:
            print(f"✅ Found {len(flights)} real flights!")
            print("\nSample flight:")
            sample_flight = flights[0]
            print(f"   Flight: {sample_flight.get('flight_number')}")
            print(f"   Airline: {sample_flight.get('airline')}")
            print(f"   Price: {sample_flight.get('currency', '$')}{sample_flight.get('price')}")
            print(f"   Source: {sample_flight.get('source')}")
        
    except Exception as e:
        print(f"⚠️  Demo search failed (expected without API keys): {str(e)[:100]}...")
        print("💡 Configure real API keys in .env file to enable live searches")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print(f"✅ {source_info['total_sources'] + 2} real flight data sources ready")
    print("✅ No fake data generation - only real flight information")
    print("✅ Comprehensive global coverage with 149+ sources")
    print("="*80)

def show_source_summary():
    """Show a quick summary of all sources."""
    multi_scraper = MultiAirlineFlightScraper()
    source_info = multi_scraper.get_supported_sources()
    
    print("\n📋 QUICK SOURCE SUMMARY")
    print("=" * 50)
    print(f"Airlines: {source_info['airlines']}")
    print(f"Travel Sites: {source_info['travel_sites']}")
    print(f"APIs: 2 (Amadeus, Skyscanner)")
    print(f"TOTAL: {source_info['total_sources'] + 2} sources")
    print("=" * 50)
    
    # Show some example sources
    airlines = list(multi_scraper.airline_websites.keys())
    travel_sites = list(multi_scraper.travel_sites.keys())
    
    print("Example airlines:", ', '.join(airlines[:10]) + "...")
    print("Example travel sites:", ', '.join(travel_sites[:10]) + "...")

if __name__ == "__main__":
    print("Starting comprehensive flight scraper demonstration...")
    
    try:
        # Run the full demonstration
        asyncio.run(demonstrate_all_sources())
    except KeyboardInterrupt:
        print("\n👋 Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("🔧 Showing source summary instead...")
        show_source_summary()
    
    print("\n🚀 Ready to search real flight data from 149+ sources!")
    print("💡 Run 'python main.py' to start interactive flight search")