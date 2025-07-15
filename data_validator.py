"""
Data validator to ensure only real flight data is processed.
This module prevents any fake/fallback data from being used.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class FlightDataValidator:
    """Validates that flight data is real and not generated/fake."""
    
    # Real airline IATA codes (expanded for 149+ sources)
    VALID_AIRLINE_CODES = {
        # US Major Airlines
        'AA', 'DL', 'UA', 'WN', 'B6', 'AS', 'NK', 'F9', 'G4', 'SY',
        # US Regional/Other
        'YX', 'QX', 'OH', 'MQ', 'EV', 'YV', 'CP', '9E', '5Y', 'C5',
        # European Major Airlines
        'BA', 'VS', 'LH', 'AF', 'KL', 'IB', 'AZ', 'LX', 'OS', 'SN',
        # European LCC and Regional
        'FR', 'U2', 'VY', 'W6', 'PC', 'A3', 'JU', 'OU', 'JP', 'YM',
        'DY', 'WF', 'V7', 'VF', 'SK', 'AY', 'TP', 'UX', 'I2', 'HV',
        'EI', 'BE', 'LS', 'BY', 'MT', 'TO',
        # Middle East Airlines
        'EK', 'QR', 'EY', 'TK', 'SV', 'MS', 'RJ', 'GF', 'WY', 'FZ',
        'XY', 'G9', 'NP', 'IF', 'J9', 'AI', 'KC', 'IX', 'SM', 'Y9', 'W5', 'EP', 'IR',
        # Asian Airlines
        'SQ', 'CX', 'JL', 'NH', 'TG', 'MH', 'PR', 'CI', 'BR', 'OZ',
        'KE', 'AI', '6E', 'SG', 'IT', 'G8', 'TR', 'FD', 'AK', 'JQ',
        'TT', 'MI', 'CA', 'MU', 'CZ', 'HU', 'FM', 'SC', 'KN', 'JD',
        # African Airlines
        'SA', 'ET', 'KQ', 'RW', 'AT', 'UG', 'AH', 'HC', 'TU', 'FB',
        # Latin American Airlines
        'LA', 'AR', 'CM', 'AV', 'G3', 'JJ', 'AD', 'P5', 'VN', 'LP',
        'VL', 'Y4', 'AM', 'VB', 'VW', 'JM',
        # North American Airlines
        'AC', 'WS', 'PD', 'TS', 'WG', 'F8',
        # Oceania Airlines
        'QF', 'VA', 'NZ', 'FJ', 'PX', 'DJ', 'TL', 'IE',
        # Cargo and Charter Airlines (that also carry passengers)
        'FX', 'UPS', '5X', 'CV', 'CX', 'LH', 'KL', 'AF', 'QR', 'EK'
    }
    
    # Valid airport IATA codes (expanded for global coverage)
    VALID_AIRPORT_CODES = {
        # US Major Airports
        'JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'LAS', 'PHX',
        'MIA', 'EWR', 'LGA', 'BWI', 'DCA', 'IAD', 'BOS', 'MSP', 'DTW', 'CLT',
        'MCO', 'IAH', 'SAN', 'TPA', 'PDX', 'STL', 'HNL', 'ANC', 'SLC', 'RDU',
        'BNA', 'AUS', 'MCI', 'IND', 'CLE', 'CMH', 'MKE', 'BUF', 'PIT', 'CVG',
        # European Major Airports
        'LHR', 'CDG', 'AMS', 'FRA', 'MAD', 'FCO', 'ZUR', 'VIE', 'BRU', 'MUC',
        'LGW', 'STN', 'LTN', 'ORY', 'NCE', 'LYS', 'TLS', 'BOD', 'NTE', 'MPL',
        'BCN', 'PMI', 'AGP', 'LPA', 'TFS', 'IBZ', 'SVQ', 'BIO', 'VLC', 'OVD',
        'MXP', 'LIN', 'BGY', 'VCE', 'NAP', 'CIA', 'BLQ', 'CTA', 'PMO', 'BRI',
        'DUS', 'HAM', 'STR', 'CGN', 'TXL', 'SXF', 'NUE', 'FMM', 'DTM', 'LEJ',
        'CPH', 'OSL', 'ARN', 'GOT', 'BGO', 'TRD', 'HEL', 'TMP', 'KTT', 'OUL',
        'WAW', 'KRK', 'GDN', 'WRO', 'KTW', 'POZ', 'RZE', 'SZZ', 'BZG', 'LUZ',
        'PRG', 'BUD', 'SOF', 'OTP', 'BEG', 'ZAG', 'LJU', 'SKP', 'TGD', 'SJJ',
        'ATH', 'THR', 'SKG', 'HER', 'RHO', 'CFU', 'ZTH', 'PVK', 'KGS', 'JTR',
        'LIS', 'OPO', 'FAO', 'FNC', 'TER', 'PDL', 'HOR', 'PIX', 'BGZ', 'VRL',
        # Middle East Airports
        'DXB', 'DOH', 'AUH', 'IST', 'RUH', 'CAI', 'AMM', 'BAH', 'MCT', 'SHJ',
        'SAW', 'ADB', 'AYT', 'ESB', 'TZX', 'KYA', 'BJV', 'VAN', 'GZT', 'MLX',
        'JED', 'DMM', 'MED', 'TUU', 'AHB', 'GIZ', 'ELQ', 'HOF', 'URY', 'TIF',
        'KWI', 'IKA', 'MHD', 'SYZ', 'AWZ', 'KIH', 'ABD', 'BND', 'HDM', 'IFN',
        'BEY', 'DAM', 'ALP', 'LTK', 'KAC', 'PMS', 'DEI', 'QAM', 'OSM', 'RPN',
        # Asian Major Airports
        'SIN', 'HKG', 'NRT', 'ICN', 'BKK', 'KUL', 'MNL', 'TPE', 'PVG', 'PEK',
        'CGK', 'DPS', 'SUB', 'MDN', 'PLM', 'PKU', 'JOG', 'SRG', 'PDG', 'BPN',
        'CAN', 'CTU', 'KMG', 'XIY', 'WUH', 'CSX', 'TAO', 'SHE', 'DLC', 'CGO',
        'NKG', 'HGH', 'FOC', 'XMN', 'CKG', 'SYX', 'URC', 'LHW', 'INC', 'YNT',
        'DEL', 'BOM', 'BLR', 'HYD', 'MAA', 'CCU', 'AMD', 'GOI', 'COK', 'TRV',
        'PNQ', 'JAI', 'LKO', 'VNS', 'GAU', 'IXA', 'IXB', 'IXC', 'IXD', 'IXE',
        'KHI', 'LHE', 'ISB', 'KHI', 'MUX', 'PEW', 'SKT', 'UET', 'RYK', 'JIW',
        'DAC', 'CGP', 'JSR', 'SPD', 'CXB', 'ZYL', 'BZL', 'RJH', 'BAU', 'IXS',
        # Oceania Airports
        'SYD', 'MEL', 'BNE', 'PER', 'ADL', 'DRW', 'CNS', 'GC', 'HBA', 'LST',
        'AKL', 'WLG', 'CHC', 'ZQN', 'ROT', 'NPL', 'PMR', 'NPE', 'DUD', 'TRG',
        'NAN', 'SUV', 'LAB', 'BKI', 'KCH', 'MYY', 'TWU', 'LGK', 'PEN', 'AOR',
        # African Airports
        'JNB', 'CPT', 'DUR', 'PLZ', 'BFN', 'ELS', 'GRJ', 'KIM', 'UTN', 'WVB',
        'ADD', 'BJM', 'DIR', 'MQX', 'GOB', 'JIM', 'LLI', 'SHC', 'AWA', 'GMB',
        'NBO', 'MBA', 'KIS', 'ELD', 'LOK', 'MYD', 'NYE', 'UAS', 'WIL', 'LAU',
        'CMN', 'RAK', 'CAS', 'FEZ', 'TNG', 'AGA', 'OUD', 'AHU', 'MLN', 'ERH',
        'TUN', 'TOE', 'DJE', 'GAF', 'SFA', 'NBE', 'GAB', 'EBM', 'SID', 'TOZ',
        'CAI', 'LXR', 'HRG', 'SSH', 'ASW', 'RMF', 'UVL', 'ABS', 'EMY', 'SPX',
        # Latin American Airports
        'GRU', 'GIG', 'BSB', 'CGH', 'SDU', 'CNF', 'POA', 'REC', 'FOR', 'SSA',
        'EZE', 'AEP', 'COR', 'MDZ', 'USH', 'IGR', 'BRC', 'NQN', 'CTC', 'TUC',
        'SCL', 'LSC', 'CCP', 'IQQ', 'ANF', 'PMC', 'ZCO', 'WCH', 'ZAL', 'PUQ',
        'BOG', 'MDE', 'CLO', 'BAQ', 'SMR', 'CTG', 'BGA', 'MTR', 'AXM', 'ADZ',
        'LIM', 'CUZ', 'AQP', 'TRU', 'PIU', 'IQT', 'CJA', 'TCQ', 'AYP', 'JUL',
        'UIO', 'GYE', 'CUE', 'LTX', 'ESM', 'XMS', 'GPS', 'SCY', 'OCC', 'TUA',
        'PTY', 'DAV', 'CHX', 'LAC', 'ONX', 'PAC', 'OTD', 'COL', 'CTD', 'MPP',
        'SJO', 'LIR', 'PBP', 'SYQ', 'NCT', 'TMU', 'BCL', 'CSC', 'GLF', 'RIK',
        'GUA', 'FRS', 'AAZ', 'CMM', 'MCR', 'PCG', 'POP', 'UAX', 'CBL', 'LCE',
        'SAL', 'SAP', 'RTB', 'LCE', 'UAX', 'ACU', 'MVD', 'ASU', 'CYR', 'PDP'
    }
    
    @staticmethod
    def validate_flight_data(flight_data: Dict[str, Any]) -> bool:
        """
        Validate that flight data is real and not fake/generated.
        Returns True only if data passes all validation checks.
        """
        if not flight_data:
            return False
        
        # Check required fields exist
        required_fields = ['airline', 'flight_number', 'origin', 'destination', 'price', 'departure_time']
        for field in required_fields:
            if field not in flight_data or not flight_data[field]:
                return False
        
        # Validate airline code
        airline = flight_data.get('airline', '').upper()
        if not FlightDataValidator._is_valid_airline_code(airline):
            return False
        
        # Validate airport codes
        origin = flight_data.get('origin', '').upper()
        destination = flight_data.get('destination', '').upper()
        if not FlightDataValidator._is_valid_airport_code(origin) or not FlightDataValidator._is_valid_airport_code(destination):
            return False
        
        # Validate flight number format
        flight_number = str(flight_data.get('flight_number', ''))
        if not FlightDataValidator._is_valid_flight_number(flight_number, airline):
            return False
        
        # Validate price (must be reasonable and not obviously fake)
        price = flight_data.get('price')
        if not FlightDataValidator._is_valid_price(price):
            return False
        
        # Validate departure time is realistic
        departure_time = flight_data.get('departure_time')
        if not FlightDataValidator._is_valid_departure_time(departure_time):
            return False
        
        # Check for obvious fake data patterns
        if FlightDataValidator._contains_fake_patterns(flight_data):
            return False
        
        return True
    
    @staticmethod
    def _is_valid_airline_code(airline_code: str) -> bool:
        """Check if airline code is a real IATA code."""
        if not airline_code or len(airline_code) != 2:
            return False
        return airline_code in FlightDataValidator.VALID_AIRLINE_CODES
    
    @staticmethod
    def _is_valid_airport_code(airport_code: str) -> bool:
        """Check if airport code is a real IATA code."""
        if not airport_code or len(airport_code) != 3:
            return False
        return airport_code in FlightDataValidator.VALID_AIRPORT_CODES
    
    @staticmethod
    def _is_valid_flight_number(flight_number: str, airline_code: str) -> bool:
        """Validate flight number format and consistency with airline."""
        if not flight_number or not airline_code:
            return False
        
        # Flight number should start with airline code and have 1-4 digits
        pattern = rf'^{airline_code}\d{{1,4}}$'
        return bool(re.match(pattern, flight_number.upper()))
    
    @staticmethod
    def _is_valid_price(price) -> bool:
        """Validate that price is realistic and not fake."""
        try:
            price_float = float(price)
            # Price should be between $50 and $10,000 (reasonable range)
            if price_float < 50 or price_float > 10000:
                return False
            # Price should not be an obvious fake value (like exactly $999.99)
            if price_float in [999.99, 1000.00, 123.45, 100.00]:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def _is_valid_departure_time(departure_time) -> bool:
        """Validate departure time is realistic."""
        try:
            if isinstance(departure_time, str):
                # Try to parse common datetime formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M']:
                    try:
                        dt = datetime.strptime(departure_time, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False
            elif isinstance(departure_time, datetime):
                dt = departure_time
            else:
                return False
            
            # Departure time should be in the future but not more than 1 year ahead
            now = datetime.now()
            if dt < now or dt > now + timedelta(days=365):
                return False
            
            return True
        except:
            return False
    
    @staticmethod
    def _contains_fake_patterns(flight_data: Dict[str, Any]) -> bool:
        """Check for common patterns in fake/generated data."""
        # Check for common fake data indicators
        fake_patterns = [
            'test', 'fake', 'dummy', 'example', 'sample', 'mock',
            'generated', 'placeholder', 'demo', 'xxx', 'yyy'
        ]
        
        # Convert all string values to lowercase for checking
        data_str = str(flight_data).lower()
        for pattern in fake_patterns:
            if pattern in data_str:
                return True
        
        # Check for obviously sequential or patterned data
        price = flight_data.get('price', 0)
        try:
            price_str = str(float(price))
            # Check for patterns like 111.11, 222.22, etc.
            if re.match(r'^\d{3}\.\d{2}$', price_str):
                digit = price_str[0]
                if digit * 3 + '.' + digit * 2 == price_str:
                    return True
        except:
            pass
        
        return False
    
    @staticmethod
    def validate_flight_list(flights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate a list of flights and return only those with real data.
        If no real flights are found, raises an exception.
        """
        valid_flights = []
        for flight in flights:
            if FlightDataValidator.validate_flight_data(flight):
                valid_flights.append(flight)
        
        if not valid_flights:
            raise ValueError("No valid real flight data found. All data appears to be fake or invalid.")
        
        return valid_flights