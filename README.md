# Dynamic Flight Scraper - 149+ Real Data Sources

A comprehensive flight scraper application that searches **149+ real flight data sources** including airline websites and travel booking platforms. This application explicitly prevents the use of fake, generated, or fallback data.

## 🚫 NO FAKE DATA POLICY

This application is specifically designed to:
- ✅ Search 149+ real flight data sources (airlines + travel sites)
- ✅ Only fetch real flight data from legitimate sources
- ✅ Validate all data to ensure it's authentic
- ✅ Fail gracefully when real data is unavailable
- ❌ **NEVER** generate fake or fallback data

## 🌐 Data Sources (149+ Total)

### ✈️ Airline Websites (70+ sources)
- **US Airlines**: American, Delta, United, Southwest, JetBlue, Alaska, Spirit, Frontier, and more
- **European Airlines**: British Airways, Lufthansa, Air France, KLM, Iberia, Swiss, Austrian, Ryanair, easyJet, and more
- **Middle East Airlines**: Emirates, Qatar Airways, Etihad, Turkish Airlines, Saudia, EgyptAir, and more
- **Asian Airlines**: Singapore Airlines, Cathay Pacific, JAL, ANA, Thai Airways, Malaysia Airlines, AirAsia, and more
- **Other Regional**: LATAM, Aerolíneas Argentinas, Qantas, South African Airways, Ethiopian Airlines, and more

### 🛫 Travel Booking Sites (35+ sources)
- **Major International**: Expedia, Booking.com, Kayak, Priceline, Orbitz, Skyscanner, Momondo, and more
- **Regional Variants**: Expedia UK/CA/DE/FR/ES/IT/AU, Skyscanner regional sites, and more
- **Specialized Sites**: Google Flights, Hopper, Kiwi.com, eDreams, Opodo, CheapOair, and more

### 🔌 Flight Data APIs (2 sources)
- **Amadeus API**: Official airline industry data
- **Skyscanner API**: Via RapidAPI platform

## Features

- **Comprehensive Coverage**: 149+ real flight data sources worldwide
- **Real Data Sources**: Direct integration with airline websites and travel platforms
- **Strict Validation**: Every flight validated against real airline and airport codes
- **No Fallbacks**: Application fails rather than providing fake data
- **Data Integrity**: Comprehensive validation prevents fake data from being processed
- **Global Coverage**: Airlines and airports from all continents
- **Deduplication**: Intelligent removal of duplicate flights from multiple sources

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Prithiraz/dynamic-scraper.git
cd dynamic-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your real API keys
```

## Configuration

You need real API keys to use this application:

### Amadeus API
1. Sign up at [Amadeus for Developers](https://developers.amadeus.com/)
2. Create a new application
3. Get your API Key and API Secret
4. Add them to your `.env` file

### RapidAPI (for Skyscanner)
1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Subscribe to flight data APIs
3. Get your RapidAPI key
4. Add it to your `.env` file

## Usage

### Interactive Mode
```bash
python main.py
```

### Demonstration Mode (shows all 149+ sources)
```bash
python demo_all_sources.py
```

### Test Mode (without API keys)
```bash
python main.py --test
```

## Example

```python
from main import DynamicFlightScraperApp
import asyncio

app = DynamicFlightScraperApp()

# Search across all 149+ sources for real flights
flights = await app.search_flights('JFK', 'LAX', '2024-12-25')
print(app.format_flight_results(flights))
```

## Data Validation

The application includes comprehensive validation for all 149+ sources:

- **Airline Codes**: Validated against 100+ real IATA airline codes globally
- **Airport Codes**: Validated against 300+ real IATA airport codes worldwide  
- **Flight Numbers**: Must follow airline-specific formatting
- **Prices**: Must be realistic (no obvious fake prices like $999.99)
- **Dates**: Must be valid future dates
- **Fake Pattern Detection**: Rejects data containing test/fake indicators
- **Deduplication**: Removes duplicate flights found across multiple sources

## Testing

Run the comprehensive test suite to verify all sources work correctly:

```bash
python test_all_sources.py
```

Run the original no-fake-data tests:

```bash
python test_no_fake_data.py
```

Or using unittest:

```bash
python -m unittest test_all_sources.py -v
python -m unittest test_no_fake_data.py -v
```

## Error Handling

When real data is unavailable:
- ❌ No fake data is generated
- ✅ Clear error messages explain the issue
- ✅ Application suggests trying different parameters
- ✅ Logs detail which data sources failed

## Supported Airlines (70+ total)

Currently validates and scrapes from major airlines including:
- **US carriers**: AA, DL, UA, WN, B6, AS, NK, F9, G4, SY, YX, QX, OH, MQ, EV
- **European carriers**: BA, VS, LH, AF, KL, IB, AZ, LX, OS, SN, FR, U2, VY, W6, PC, A3, JU, OU, DY, WF, SK, AY, TP
- **Middle East carriers**: EK, QR, EY, TK, SV, MS, RJ, GF, WY, FZ, XY, G9
- **Asian carriers**: SQ, CX, JL, NH, TG, MH, PR, CI, BR, OZ, KE, AI, 6E, SG, TR, FD, AK, JQ, TT
- **Other regional**: LA, AR, CM, AV, G3, AD, QF, VA, NZ, FJ, SA, ET, KQ, RW, AT

## Supported Airports (300+ total)

Validates against major international airports from all continents including major hubs, regional airports, and international destinations.

## File Structure

```
dynamic-scraper/
├── main.py                 # Main application entry point
├── flight_scraper.py       # Enhanced flight data scraper (149+ sources)
├── airline_scrapers.py     # Multi-airline website scrapers
├── data_validator.py       # Data validation (expanded for global coverage)
├── config.py              # Configuration management
├── test_no_fake_data.py   # Original tests ensuring no fake data
├── test_all_sources.py    # Comprehensive tests for all 149+ sources
├── demo_all_sources.py    # Demonstration script showing all sources
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## Important Notes

1. **API Limits**: Real APIs have rate limits and usage costs
2. **Data Availability**: Not all routes may have real-time data from all sources
3. **Rate Limiting**: Application includes delays to avoid being blocked by websites
4. **No Caching**: Application doesn't cache data to ensure freshness
5. **Fail-Safe**: Better to fail than provide fake data
6. **Source Coverage**: 149+ sources provide comprehensive global coverage
7. **Performance**: Searches multiple sources simultaneously with intelligent timeouts

## Contributing

When contributing, ensure:
- No fake data generation is ever added
- All new sources maintain the real-data-only policy
- Tests verify data authenticity for all sources
- Documentation clearly states real data requirements
- New airline/airport codes are added to validation lists

## License

MIT License - See LICENSE file for details.

---

**Remember: This application searches 149+ real flight data sources and will NEVER provide fake flight data. If you need guaranteed results regardless of data availability, this is not the right tool for you. The comprehensive source coverage ensures maximum chance of finding real flight data when it exists.**