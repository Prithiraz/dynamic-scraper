# Dynamic Flight Scraper - Real Data Only

A dynamic flight scraper application that **ONLY** uses real flight data from legitimate APIs. This application explicitly prevents the use of fake, generated, or fallback data.

## 🚫 NO FAKE DATA POLICY

This application is specifically designed to:
- ✅ Only fetch real flight data from legitimate sources
- ✅ Validate all data to ensure it's authentic
- ✅ Fail gracefully when real data is unavailable
- ❌ **NEVER** generate fake or fallback data

## Features

- **Real Data Sources**: Integrates with Amadeus API and Skyscanner (via RapidAPI)
- **Strict Validation**: Every flight is validated against real airline and airport codes
- **No Fallbacks**: Application fails rather than providing fake data
- **Data Integrity**: Comprehensive validation prevents fake data from being processed

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

### Test Mode (without API keys)
```bash
python main.py --test
```

## Example

```python
from main import DynamicFlightScraperApp
import asyncio

app = DynamicFlightScraperApp()

# Search for real flights only
flights = await app.search_flights('JFK', 'LAX', '2024-12-25')
print(app.format_flight_results(flights))
```

## Data Validation

The application includes comprehensive validation:

- **Airline Codes**: Validated against real IATA airline codes
- **Airport Codes**: Validated against real IATA airport codes  
- **Flight Numbers**: Must follow airline-specific formatting
- **Prices**: Must be realistic (no obvious fake prices like $999.99)
- **Dates**: Must be valid future dates
- **Fake Pattern Detection**: Rejects data containing test/fake indicators

## Testing

Run the test suite to verify no fake data is generated:

```bash
python -m pytest test_no_fake_data.py -v
```

Or using unittest:

```bash
python test_no_fake_data.py
```

## Error Handling

When real data is unavailable:
- ❌ No fake data is generated
- ✅ Clear error messages explain the issue
- ✅ Application suggests trying different parameters
- ✅ Logs detail which data sources failed

## Supported Airlines

Currently validates against major airlines including:
- US carriers: AA, DL, UA, WN, B6, AS, NK, F9, G4, SY
- European carriers: BA, VS, LH, AF, KL, IB, AZ, LX, OS, SN  
- Middle East carriers: EK, QR, EY, TK, SV, MS, RJ, GF, WY, FZ
- Asian carriers: SQ, CX, JL, NH, TG, MH, PR, CI, BR, OZ

## Supported Airports

Validates against major international airports. The list can be expanded as needed.

## File Structure

```
dynamic-scraper/
├── main.py                 # Main application entry point
├── flight_scraper.py       # Real flight data scraper
├── data_validator.py       # Data validation (no fake data)
├── config.py              # Configuration management
├── test_no_fake_data.py   # Tests ensuring no fake data
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## Important Notes

1. **API Limits**: Real APIs have rate limits and usage costs
2. **Data Availability**: Not all routes may have real-time data
3. **No Caching**: Application doesn't cache data to ensure freshness
4. **Fail-Safe**: Better to fail than provide fake data

## Contributing

When contributing, ensure:
- No fake data generation is ever added
- All new features maintain the real-data-only policy
- Tests verify data authenticity
- Documentation clearly states real data requirements

## License

MIT License - See LICENSE file for details.

---

**Remember: This application will NEVER provide fake flight data. If you need guaranteed results regardless of data availability, this is not the right tool for you.**