#===================  *****  ===================
# Description: Rule-based Crime Dataset Generator
# Generated realistic crime data with proper correlations across multiple jurisdictions
# Important libraries required: faker, pandas
# !pip install faker pandas numpy
#----------------------------------------------
# Fields generated:
# 'Country', 'State_Province', 'City', 'Locality', 'Crime Type', 'Severity Level',
# 'Date', 'Time', 'Location Type', 'Suspect Age', 'Suspect Gender', 'Suspect Race',
# 'Victim Age', 'Victim Gender', 'Victim Race', 'Victim Occupation', 'Suspect Motive',
# 'Weapon Type', 'Evidence Found', 'Charges', 'Arrest Status', 'Case Status',
# 'Criminal History', 'Victim-Suspect Relationship', 'Number Of Witnesses'
#----------------------------------------------
# Developed By: AI Assistant
#===================  *****  ===================

import csv
import random
import logging
import sys
from abc import ABC, abstractmethod
from faker import Faker
from datetime import datetime, timedelta
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crime_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Country and City Metadata for realism ---
COUNTRY_METADATA = {
    'USA': {
        'locale': 'en_US',
        'races': ['White', 'Black', 'Hispanic', 'Asian', 'Other'],
        'agencies': ['Local Police', 'Sheriff', 'State Police', 'FBI'],
        'date_format': '%Y-%m-%d',
        'case_prefix': 'US-CF-',
        'incident_prefix': 'US-IC-',
        'officer_title': 'Detective Assigned',
        'severity_label_name': 'Severity Level',
        'police_unit_label': 'Police Department'
    },
    'UK': {
        'locale': 'en_GB',
        'races': ['White', 'Black', 'Asian', 'Other'],
        'agencies': ['Local Police', 'Metropolitan Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'UK-CF-',
        'incident_prefix': 'UK-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Offence Classification',
        'police_unit_label': 'Police Station'
    },
    'India': {
        'locale': 'en_IN',
        'races': ['South Asian', 'Other'],
        'agencies': ['Local Police', 'State Police', 'Central Bureau of Investigation'],
        'date_format': '%d-%m-%Y',
        'case_prefix': 'IN-CF-',
        'incident_prefix': 'IN-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Offence Type',
        'police_unit_label': 'Police Station'
    },
    'Pakistan': {
        'locale': 'en_PK',
        'races': ['Punjabi', 'Sindhi', 'Pashtun', 'Balochi', 'Other'],
        'agencies': ['Local Police', 'Punjab Police', 'Federal Investigation Agency'],
        'date_format': '%d-%m-%Y',
        'case_prefix': 'PK-CF-',
        'incident_prefix': 'PK-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Offence Type',
        'police_unit_label': 'Police Station'
    },
    'Bangladesh': {
        'locale': 'en_BD',
        'races': ['Bengali', 'Other'],
        'agencies': ['Local Police', 'Bangladesh Police'],
        'date_format': '%d-%m-%Y',
        'case_prefix': 'BD-CF-',
        'incident_prefix': 'BD-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Offence Type',
        'police_unit_label': 'Police Station'
    },
    'Sri Lanka': {
        'locale': 'en_LK',
        'races': ['Sinhalese', 'Tamil', 'Other'],
        'agencies': ['Sri Lanka Police'],
        'date_format': '%d-%m-%Y',
        'case_prefix': 'LK-CF-',
        'incident_prefix': 'LK-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Offence Type',
        'police_unit_label': 'Police Station'
    },
    'Malaysia': {
        'locale': 'en_MY',
        'races': ['Malay', 'Chinese', 'Indian', 'Other'],
        'agencies': ['Royal Malaysia Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'MY-CF-',
        'incident_prefix': 'MY-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Severity Level',
        'police_unit_label': 'Police Station'
    },
    'Indonesia': {
        'locale': 'id_ID',
        'races': ['Javanese', 'Sundanese', 'Other'],
        'agencies': ['Indonesian National Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'ID-CF-',
        'incident_prefix': 'ID-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Severity Level',
        'police_unit_label': 'Polsek'
    },
    'Saudi Arabia': {
        'locale': 'ar_SA',
        'races': ['Arab', 'Other'],
        'agencies': ['Local Police', 'Public Security'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'SA-CF-',
        'incident_prefix': 'SA-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Severity Level',
        'police_unit_label': 'Police Station'
    },
    'United Arab Emirates': {
        'locale': 'en_US',
        'races': ['Emirati', 'Expats', 'Other'],
        'agencies': ['Local Police', 'Dubai Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'AE-CF-',
        'incident_prefix': 'AE-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Severity Level',
        'police_unit_label': 'Police Station'
    },
    'Mexico': {
        'locale': 'es_MX',
        'races': ['Mestizo', 'Other'],
        'agencies': ['Local Police', 'Federal Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'MX-CF-',
        'incident_prefix': 'MX-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Clasificación',
        'police_unit_label': 'Comisaría'
    },
    'Brazil': {
        'locale': 'pt_BR',
        'races': ['Pardo', 'White', 'Black', 'Other'],
        'agencies': ['Local Police', 'Federal Police'],
        'date_format': '%d/%m/%Y',
        'case_prefix': 'BR-CF-',
        'incident_prefix': 'BR-IC-',
        'officer_title': 'Officer In Charge',
        'severity_label_name': 'Classificação',
        'police_unit_label': 'Delegacia'
    },
    # default fallback for other countries
    'DEFAULT': {
        'police_unit_label': 'Police Station'
    }
}

# City center coordinates for realistic lat/long (sampled for major cities used)
CITY_CENTERS = {
    'Lahore': (31.5204, 74.3587),
    'Karachi': (24.8607, 67.0011),
    'Islamabad': (33.6844, 73.0479),
    'Gwadar': (25.1264, 62.3254),
    'Dhaka': (23.8103, 90.4125),
    'Colombo': (6.9271, 79.8612),
    'Kuala Lumpur': (3.1390, 101.6869),
    'Jakarta': (-6.2088, 106.8456),
    'Riyadh': (24.7136, 46.6753),
    'Jeddah': (21.4858, 39.1925),
    'Mexico City': (19.4326, -99.1332),
    'São Paulo': (-23.5505, -46.6333),
    'Bogotá': (4.7110, -74.0721),
    'Kinshasa': (-4.4419, 15.2663),
    'Libreville': (0.4162, 9.4673),
}

# Sample neighborhood names for some cities
NEIGHBORHOODS = {
    'Lahore': ['Gulberg', 'Model Town', 'DHA', 'Township'],
    'Karachi': ['Clifton', 'Gulistan-e-Johar', 'Saddar', 'PECHS'],
    'Dhaka': ['Dhanmondi', 'Gulshan', 'Banani', 'Mirpur'],
    'Colombo': ['Fort', 'Bambalapitiya', 'Dehiwala'],
    'Kuala Lumpur': ['Bukit Bintang', 'KLCC', 'Chow Kit'],
    'Jakarta': ['Menteng', 'Kuningan', 'Kelapa Gading'],
    'Riyadh': ['Olaya', 'King Fahd', 'Al Malaz'],
}

# Socioeconomic data by city (sampled estimates used to bias generation)
SOCIOECONOMIC_DATA = {
    # Pakistan
    'Lahore': {'poverty_rate': 0.25, 'crime_index': 1.2, 'unemployment': 0.06, 'median_income': 6000},
    'Karachi': {'poverty_rate': 0.30, 'crime_index': 1.4, 'unemployment': 0.08, 'median_income': 5000},
    'Islamabad': {'poverty_rate': 0.15, 'crime_index': 0.8, 'unemployment': 0.04, 'median_income': 12000},
    'Gwadar': {'poverty_rate': 0.35, 'crime_index': 1.1, 'unemployment': 0.12, 'median_income': 3000},
    # Bangladesh
    'Dhaka': {'poverty_rate': 0.28, 'crime_index': 1.3, 'unemployment': 0.07, 'median_income': 4500},
    # Sri Lanka
    'Colombo': {'poverty_rate': 0.18, 'crime_index': 1.0, 'unemployment': 0.05, 'median_income': 8000},
    # Malaysia/Indonesia
    'Kuala Lumpur': {'poverty_rate': 0.10, 'crime_index': 0.9, 'unemployment': 0.03, 'median_income': 15000},
    'Jakarta': {'poverty_rate': 0.22, 'crime_index': 1.1, 'unemployment': 0.06, 'median_income': 7000},
    # Gulf
    'Riyadh': {'poverty_rate': 0.06, 'crime_index': 0.7, 'unemployment': 0.05, 'median_income': 30000},
    'Jeddah': {'poverty_rate': 0.08, 'crime_index': 0.9, 'unemployment': 0.06, 'median_income': 18000},
    # Latin America
    'Mexico City': {'poverty_rate': 0.35, 'crime_index': 1.6, 'unemployment': 0.09, 'median_income': 9000},
    'São Paulo': {'poverty_rate': 0.28, 'crime_index': 1.5, 'unemployment': 0.10, 'median_income': 11000},
    'Bogotá': {'poverty_rate': 0.32, 'crime_index': 1.4, 'unemployment': 0.08, 'median_income': 7000},
    # Central Africa
    'Kinshasa': {'poverty_rate': 0.60, 'crime_index': 1.8, 'unemployment': 0.25, 'median_income': 1200},
    'Libreville': {'poverty_rate': 0.40, 'crime_index': 1.3, 'unemployment': 0.12, 'median_income': 4000},
}

# --- Base Factory Interface ---
class CrimeFactory(ABC):
    def __init__(self, country, states_cities):
        self.country = country
        # Use locale-specific Faker where possible for more realistic local data
        locale = COUNTRY_METADATA.get(country, {}).get('locale')
        try:
            self.fake = Faker(locale) if locale else Faker()
        except Exception:
            self.fake = Faker()
        self.states_cities = states_cities  # dict: {state: [cities]}
        self._rules = []
        # metadata for country (races, agencies, etc.)
        self.country_metadata = COUNTRY_METADATA.get(country, {})
        self._register_default_rules()
        
    @abstractmethod
    def generate_record(self):
        """Must be implemented by each country factory."""
        pass

    # === Crime Correlation Methods ===
    def _get_crime_by_location(self, location_type, time_of_day):
        """Generate realistic crime type based on location and time."""
        crime_by_location_time = {
            'Commercial District': {
                'Morning': ['Robbery', 'Fraud', 'Theft', 'Shoplifting'],
                'Afternoon': ['Robbery', 'Fraud', 'Assault', 'Theft'],
                'Evening': ['Robbery', 'Aggravated Assault', 'Burglary', 'Fraud'],
                'Night': ['Armed Robbery', 'Aggravated Assault', 'Burglary', 'Theft', 'Cybercrime']
            },
            'Residential Area': {
                'Morning': ['Burglary', 'Theft', 'Assault', 'Drug Violation'],
                'Afternoon': ['Burglary', 'Theft', 'Vandalism', 'Minor Assault'],
                'Evening': ['Burglary', 'Assault', 'Drug Violation', 'Domestic Violence'],
                'Night': ['Burglary', 'Breaking and Entering', 'Drug Violation', 'Assault', 'Domestic Violence']
            },
            'Street': {
                'Morning': ['Theft', 'Robbery', 'Assault', 'Vandalism'],
                'Afternoon': ['Theft', 'Robbery', 'Assault', 'Vandalism'],
                'Evening': ['Armed Robbery', 'Assault', 'Drug Violation', 'Gang Activity', 'Extortion'],
                'Night': ['Armed Robbery', 'Aggravated Assault', 'Gang Activity', 'Drug Violation', 'Kidnapping']
            },
            'Hospital/School': {
                'Morning': ['Assault', 'Theft', 'Drug Violation', 'Trespassing'],
                'Afternoon': ['Assault', 'Theft', 'Drug Violation', 'Vandalism'],
                'Evening': ['Assault', 'Drug Violation', 'Trespassing', 'Sexual Assault'],
                'Night': ['Trespassing', 'Drug Violation', 'Assault', 'Sexual Assault']
            },
            'Industrial Zone': {
                'Morning': ['Burglary', 'Theft', 'Fraud', 'Vehicle Theft'],
                'Afternoon': ['Burglary', 'Theft', 'Assault', 'Drug Violation'],
                'Evening': ['Burglary', 'Vehicle Theft', 'Drug Violation', 'Arson'],
                'Night': ['Burglary', 'Armed Robbery', 'Vehicle Theft', 'Arson']
            }
        }
        
        crimes = crime_by_location_time.get(location_type, {}).get(time_of_day, ['Theft', 'Assault'])
        return random.choice(crimes)

    def _get_severity_by_crime(self, crime_type):
        """Determine severity level based on crime type."""
        severity_map = {
            'Theft': ['Misdemeanor', 'Felony 3'],
            'Shoplifting': ['Misdemeanor', 'Misdemeanor'],
            'Assault': ['Misdemeanor', 'Felony 3'],
            'Aggravated Assault': ['Felony 2', 'Felony 1'],
            'Armed Robbery': ['Felony 1', 'Felony 1'],
            'Robbery': ['Felony 2', 'Felony 1'],
            'Burglary': ['Felony 2', 'Felony 1'],
            'Arson': ['Felony 2', 'Felony 1'],
            'Sexual Assault': ['Felony 1', 'Felony 1'],
            'Kidnapping': ['Felony 1', 'Felony 1'],
            'Human Trafficking': ['Felony 1', 'Felony 1'],
            'Cybercrime': ['Misdemeanor', 'Felony 2'],
            'Extortion': ['Felony 2', 'Felony 1'],
            'Identity Theft': ['Misdemeanor', 'Felony 2'],
            'Breaking and Entering': ['Felony 2', 'Felony 3'],
            'Murder': ['Felony 1', 'Felony 1'],
            'Fraud': ['Misdemeanor', 'Felony 2'],
            'Drug Violation': ['Misdemeanor', 'Felony 3'],
            'Gang Activity': ['Felony 3', 'Felony 2'],
            'Vandalism': ['Misdemeanor', 'Misdemeanor'],
            'Trespassing': ['Misdemeanor', 'Misdemeanor'],
            'Vehicle Theft': ['Felony 2', 'Felony 1'],
            'Minor Assault': ['Misdemeanor', 'Misdemeanor'],
        }
        severities = severity_map.get(crime_type, ['Misdemeanor', 'Felony 3'])
        return random.choice(severities)

    def _format_severity_for_country(self, severity):
        """Map generic severity labels to country-specific classification."""
        c = self.country
        if not severity:
            return severity

        # Default: return as-is
        # Country-specific mappings
        # UK: use court-friendly labels
        if c == 'UK':
            if 'Felony 1' in severity:
                return 'Indictable - Very Serious'
            if 'Felony 2' in severity:
                return 'Indictable - Serious'
            if 'Felony 3' in severity:
                return 'Either Way Offence'
            if 'Misdemeanor' in severity:
                return 'Summary Offence'

        # South Asia: cognizable vs non-cognizable distinction (generalized)
        if c in ('India', 'Pakistan', 'Bangladesh', 'Sri Lanka'):
            if any(tok in severity for tok in ('Felony', 'Murder', 'Aggravated', 'Armed', 'Kidnapping', 'Sexual')):
                return 'Cognizable (Serious Offence)'
            return 'Non-Cognizable (Minor Offence)'

        # Latin America: broad Spanish labels
        if c in ('Mexico', 'Brazil', 'Colombia', 'Peru', 'Chile', 'Argentina'):
            if any(tok in severity for tok in ('Felony', 'Murder', 'Aggravated', 'Armed', 'Kidnapping', 'Sexual')):
                return 'Delito Grave'
            return 'Delito Menor'

        # Eastern Europe: generalized criminal classification
        if c in ('Poland', 'Romania', 'Ukraine', 'Czechia', 'Hungary', 'Bulgaria', 'Slovakia'):
            if any(tok in severity for tok in ('Felony', 'Murder', 'Aggravated', 'Armed', 'Kidnapping', 'Sexual')):
                return 'Criminal Offence - Major'
            return 'Criminal Offence - Minor'

        # Gulf / MENA and Southeast Asia: serious vs minor wording
        if c in ('Saudi Arabia', 'United Arab Emirates', 'Qatar', 'Bahrain', 'Kuwait', 'Oman', 'Malaysia', 'Indonesia'):
            if any(tok in severity for tok in ('Felony', 'Murder', 'Aggravated', 'Armed', 'Kidnapping', 'Sexual')):
                return 'Serious Criminal Offence'
            return 'Minor Criminal Offence'

        # USA: map felonies/misdemeanors to commonly used class labels
        if c == 'USA':
            if 'Felony 1' in severity:
                return 'Felony I'
            if 'Felony 2' in severity:
                return 'Felony II'
            if 'Felony 3' in severity:
                return 'Felony III'
            if 'Misdemeanor' in severity:
                return 'Misdemeanor'

        # Default fallback: return original severity
        return severity

    def _get_weapon_by_crime(self, crime_type):
        """Determine weapon type based on crime."""
        weapon_map = {
            'Armed Robbery': ['Gun', 'Knife', 'Handgun'],
            'Aggravated Assault': ['Knife', 'Gun', 'Blunt Object'],
            'Murder': ['Gun', 'Knife', 'Blunt Object'],
            'Sexual Assault': ['None', 'Hands', 'Knife'],
            'Kidnapping': ['None', 'Threat', 'Weapon'],
            'Robbery': ['Gun', 'Knife', 'Threat'],
            'Burglary': ['None', 'Knife', 'Crowbar'],
            'Assault': ['None', 'Fist', 'Blunt Object'],
            'Theft': ['None', 'None'],
            'Fraud': ['None', 'None'],
            'Drug Violation': ['None', 'Knife'],
            'Vehicle Theft': ['None', 'None'],
            'Arson': ['Accelerant', 'None'],
            'Cybercrime': ['None'],
        }
        weapons = weapon_map.get(crime_type, ['None'])
        return random.choice(weapons)

    def _get_evidence_by_crime(self, crime_type, weapon):
        """Generate realistic evidence based on crime type."""
        evidence_options = {
            'Theft': ['Witness Statement', 'Security Footage', 'Fingerprints'],
            'Robbery': ['Security Footage', 'Eyewitness Account', 'Physical Evidence'],
            'Burglary': ['Fingerprints', 'Tool Marks', 'Witness Statement'],
            'Assault': ['Medical Records', 'Witness Statement', 'Physical Evidence'],
            'Murder': ['Forensic Evidence', 'Eyewitness', 'DNA Sample'],
            'Fraud': ['Digital Evidence', 'Financial Records', 'Document Evidence'],
            'Gang Activity': ['Witness Statement', 'Surveillance', 'Physical Evidence'],
            'Drug Violation': ['Drug Evidence', 'Digital Records', 'Witness Statement'],
            'Cybercrime': ['Digital Logs', 'IP Traces', 'Forensic Image'],
            'Arson': ['Accelerant Residue', 'Fire Patterns', 'Witness Statement'],
            'Sexual Assault': ['Medical Records', 'DNA Sample', 'Witness Statement'],
            'Human Trafficking': ['Victim Testimony', 'Financial Records', 'Travel Logs'],
            'Identity Theft': ['Financial Records', 'Digital Evidence'],
        }
        
        base_evidence = evidence_options.get(crime_type, ['Witness Statement'])
        num_evidence = random.randint(1, 3)
        selected = random.sample(base_evidence, min(num_evidence, len(base_evidence)))
        
        if weapon != 'None' and random.random() > 0.3:
            selected.append('Weapon Evidence')
        
        return '; '.join(selected) if selected else 'None'

    def _get_suspect_age_by_crime(self, crime_type):
        """Generate age appropriate for crime type."""
        age_distribution = {
            'Shoplifting': (16, 35),
            'Theft': (18, 50),
            'Burglary': (18, 45),
            'Drug Violation': (16, 40),
            'Gang Activity': (16, 35),
            'Vandalism': (14, 30),
            'Fraud': (25, 65),
            'Assault': (18, 50),
            'Robbery': (18, 45),
            'Armed Robbery': (20, 50),
            'Vehicle Theft': (16, 40),
        }
        
        if crime_type in age_distribution:
            min_age, max_age = age_distribution[crime_type]
            return random.gauss((min_age + max_age) / 2, (max_age - min_age) / 6)
        else:
            return random.gauss(35, 12)
        
        return max(14, min(70, int(age)))

    def _get_victim_by_crime(self, crime_type, suspect_age):
        """Generate victim info appropriate for crime."""
        victim_age = random.randint(18, 80)
        victim_gender = random.choice(['Male', 'Female'])
        
        # Victim-suspect relationship varies by crime
        if crime_type in ['Assault', 'Aggravated Assault', 'Murder']:
            relationship = random.choice(['Acquaintance', 'Stranger', 'Intimate Partner', 'Family Member'])
        elif crime_type in ['Robbery', 'Armed Robbery']:
            relationship = random.choice(['Stranger', 'Stranger', 'Acquaintance'])
        elif crime_type in ['Theft', 'Shoplifting', 'Burglary']:
            relationship = 'Stranger'
        else:
            relationship = random.choice(['Stranger', 'Acquaintance', 'Unknown'])
        
        return victim_age, victim_gender, relationship

    def _get_charges_by_crime_severity(self, crime_type, severity):
        """Determine charges based on crime and severity."""
        base_charges = {
            'Theft': 'Theft',
            'Robbery': 'Robbery',
            'Armed Robbery': 'Armed Robbery',
            'Burglary': 'Burglary',
            'Assault': 'Assault',
            'Aggravated Assault': 'Aggravated Assault',
            'Arson': 'Arson',
            'Sexual Assault': 'Sexual Assault',
            'Kidnapping': 'Kidnapping',
            'Human Trafficking': 'Human Trafficking',
            'Cybercrime': 'Cybercrime/Computer Fraud',
            'Identity Theft': 'Identity Theft',
            'Murder': 'Murder',
            'Fraud': 'Fraud',
            'Drug Violation': 'Drug Possession/Distribution',
        }
        
        base = base_charges.get(crime_type, crime_type)
        
        # Add severity modifiers
        if 'Felony 1' in severity:
            return f"{base} - Felony Class 1"
        elif 'Felony 2' in severity:
            return f"{base} - Felony Class 2"
        elif 'Felony 3' in severity:
            return f"{base} - Felony Class 3"
        else:
            return f"{base} - Misdemeanor"

    def _get_arrest_status(self, severity, evidence_quality):
        """Determine arrest status based on severity and evidence."""
        if severity == 'Felony 1':
            arrest_prob = 0.85  # High probability for serious crimes
        elif 'Felony' in severity:
            arrest_prob = 0.70
        else:
            arrest_prob = 0.50
        
        return 'Arrested' if random.random() < arrest_prob else 'At Large'

    def _get_case_status(self, arrest_status, evidence_quality, time_since_crime_days):
        """Determine case status."""
        if arrest_status == 'At Large':
            if time_since_crime_days > 365:
                return 'Cold Case'
            else:
                return 'Under Investigation'
        else:
            if random.random() > 0.7:
                return 'Solved'
            elif random.random() > 0.5:
                return 'Under Investigation'
            else:
                return random.choice(['Pending Trial', 'Convicted'])

    def _get_criminal_history(self, suspect_age):
        """Determine if suspect has criminal history."""
        if suspect_age < 18:
            return 'Juvenile Record'
        elif random.random() < 0.4:  # 40% have prior records
            num_priors = random.randint(1, 5)
            return f"{num_priors} Prior Convictions"
        else:
            return 'Clean Record'

    def _get_location_type(self):
        """Random location type."""
        return random.choice(['Street', 'Commercial District', 'Residential Area', 
                             'Industrial Zone', 'Hospital/School', 'Park'])

    def _get_time_of_day(self):
        """Random time of day."""
        return random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])

    def generate_common_fields(self, state, city, locality):
        """Generates standard fields applicable across all regions."""
        crime_date = self.fake.date_between(start_date='-3y')
        time_of_day = self._get_time_of_day()
        location_type = self._get_location_type()
        
        crime_type = self._get_crime_by_location(location_type, time_of_day)
        severity = self._get_severity_by_crime(crime_type)
        weapon = self._get_weapon_by_crime(crime_type)
        
        suspect_age = max(14, min(70, int(self._get_suspect_age_by_crime(crime_type))))
        suspect_gender = random.choice(['Male', 'Female'])
        # choose race from country metadata when available for locality realism
        suspect_race = random.choice(self.country_metadata.get('races', ['White', 'Black', 'Hispanic', 'Asian', 'Other']))
        
        victim_age, victim_gender, victim_relationship = self._get_victim_by_crime(crime_type, suspect_age)
        
        evidence = self._get_evidence_by_crime(crime_type, weapon)
        charges = self._get_charges_by_crime_severity(crime_type, severity)
        arrest_status = self._get_arrest_status(severity, evidence)

        # Socioeconomic modifiers
        city_metrics = SOCIOECONOMIC_DATA.get(city, None)
        if city_metrics:
            poverty = city_metrics.get('poverty_rate', 0.2)
            crime_index = city_metrics.get('crime_index', 1.0)
            unemployment = city_metrics.get('unemployment', 0.08)
            median_income = city_metrics.get('median_income', None)
        else:
            # fallback defaults based on country metadata where possible
            poverty = 0.2
            crime_index = 1.0
            unemployment = 0.08
            median_income = None

        # Increase severity / violent crime likelihood in higher crime_index areas
        if crime_index > 1.2 and random.random() < min(0.5, (crime_index - 1.0) / 1.5):
            severe_options = ['Armed Robbery', 'Aggravated Assault', 'Gang Activity', 'Kidnapping', 'Arson']
            crime_type = random.choice(severe_options + [crime_type])
            severity = self._get_severity_by_crime(crime_type)
            weapon = self._get_weapon_by_crime(crime_type)

        # (Deferred) gang/property scaling and output variables will be applied after
        # local variables like property_loss_value and gang_affiliation are created.
        
        
        time_since_crime = (datetime.now().date() - crime_date).days
        case_status = self._get_case_status(arrest_status, evidence, time_since_crime)
        
        criminal_history = self._get_criminal_history(suspect_age)
        num_witnesses = random.randint(0, 5)
        
        # Random time within the day
        crime_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        # Additional metadata
        # Case and incident identifiers formatted per-country when metadata available
        meta = self.country_metadata
        date_fmt = meta.get('date_format', '%Y-%m-%d')
        formatted_date = crime_date.strftime(date_fmt)

        case_prefix = meta.get('case_prefix', f"{self.country[:2].upper()}-CF-")
        case_file_number = f"{case_prefix}{formatted_date.replace('/', '').replace('-', '')}-{random.randint(1000,9999)}"

        reporting_agency = random.choice(meta.get('agencies', ['Local Police', 'National Police', 'Federal Agency', 'Special Investigations Unit']))
        officer_key = meta.get('officer_title', 'Detective Assigned')
        officer_name = self.fake.name()

        incident_prefix = meta.get('incident_prefix', f"{self.country[:2].upper()}-IC-")
        incident_code = f"{incident_prefix}{random.randint(10000,99999)}"

        # Police unit labeling
        police_unit_label = meta.get('police_unit_label', COUNTRY_METADATA.get('DEFAULT', {}).get('police_unit_label', 'Police Station'))
        police_unit_name = f"{city} {police_unit_label}"

        # Basic injury/fatality counts for violent incidents
        num_injuries = 0
        num_fatalities = 0
        if 'Assault' in crime_type or 'Murder' in crime_type or 'Armed Robbery' in crime_type or 'Sexual Assault' in crime_type:
            num_injuries = random.randint(0, 5)
            if 'Murder' in crime_type:
                num_fatalities = random.randint(1, 3)

        # Property loss estimate for theft/burglary/arson
        property_loss_value = 0.0
        if crime_type in ['Theft', 'Burglary', 'Arson', 'Vehicle Theft', 'Robbery']:
            property_loss_value = round(random.uniform(50.0, 50000.0), 2)

        # Gang affiliation (if gang activity or related crimes)
        gang_affiliation = 'None'
        if crime_type in ['Gang Activity', 'Armed Robbery', 'Robbery'] and random.random() > 0.6:
            gang_affiliation = random.choice(['Gang A', 'Gang B', 'Gang C'])

        # Now apply socioeconomic-influenced gang probability and property loss scaling
        gang_prob = min(0.8, 0.1 + poverty * 1.5 + max(0, (crime_index - 1.0)))
        if gang_affiliation == 'None' and random.random() < gang_prob:
            gang_affiliation = random.choice(['Local Gang', 'Organized Group', 'Youth Gang'])

        # Scale property loss expectations by median income and poverty
        if property_loss_value > 0 and median_income:
            multiplier = 1.0 + (median_income / 20000.0)
            property_loss_value = round(property_loss_value * multiplier * (1.0 + poverty * 0.5), 2)

        # Add socioeconomic outputs
        poverty_rate_out = round(poverty, 3)
        crime_index_out = round(crime_index, 3)
        unemployment_out = round(unemployment, 3)
        median_income_out = median_income if median_income is not None else ''

        # Drug type for drug violations
        drug_type = ''
        if 'Drug' in crime_type or 'Drug Violation' in crime_type:
            drug_type = random.choice(['Cannabis', 'Heroin', 'Cocaine', 'Methamphetamine', 'Prescription Drugs'])

        # Locality selection: use known neighborhoods when available for more local specificity
        if city in NEIGHBORHOODS:
            locality = random.choice(NEIGHBORHOODS[city])

        # Generate realistic lat/long near known city center if available
        if city in CITY_CENTERS:
            base_lat, base_lon = CITY_CENTERS[city]
            # small random offset ~ up to ~5 km (approx 0.05 degrees)
            latitude = round(base_lat + random.uniform(-0.05, 0.05), 6)
            longitude = round(base_lon + random.uniform(-0.05, 0.05), 6)
        else:
            latitude = round(random.uniform(-90.0, 90.0), 6)
            longitude = round(random.uniform(-180.0, 180.0), 6)
        
        # Prepare returned record with country-specific keys
        # Map severity to country-specific label and include label name
        severity_label = self._format_severity_for_country(severity)
        severity_label_name = meta.get('severity_label_name', 'Severity Level')

        record = {
            'Country': self.country,
            'State_Province': state,
            'City': city,
            'Locality': locality,
            'Crime Type': crime_type,
            'Severity Level': severity_label,
            'Severity Label Name': severity_label_name,
            'Date': formatted_date,
            'Time': crime_time,
            'Location Type': location_type,
            'Suspect Age': suspect_age,
            'Suspect Gender': suspect_gender,
            'Suspect Race/Ethnicity': suspect_race,
            'Victim Age': victim_age,
            'Victim Gender': victim_gender,
            'Victim Race/Ethnicity': random.choice(self.country_metadata.get('races', ['White', 'Black', 'Hispanic', 'Asian', 'Other'])),
            'Victim Occupation': self.fake.job(),
            'Suspect Motive': random.choice(['Financial Gain', 'Revenge', 'Drugs', 'Gang Activity', 
                                            'Personal Conflict', 'Unknown', 'Opportunity']),
            'Weapon Type': weapon,
            'Evidence Found': evidence,
            'Charges': charges,
            'Arrest Status': arrest_status,
            'Case Status': case_status,
            'Criminal History': criminal_history,
            'Victim-Suspect Relationship': victim_relationship,
            'Number of Witnesses': num_witnesses,
            'Case File Number': case_file_number,
            'Reporting Agency': reporting_agency,
            officer_key: officer_name,
            'Incident Code': incident_code,
            'Number of Injuries': num_injuries,
            'Number of Fatalities': num_fatalities,
            'Property Loss Value': property_loss_value,
            'Gang Affiliation': gang_affiliation,
            'Drug Type': drug_type,
            'Latitude': latitude,
            'Longitude': longitude,
            'Poverty Rate': poverty_rate_out,
            'Crime Rate Index': crime_index_out,
            'Unemployment Rate': unemployment_out,
            'Median Income': median_income_out,
            'Police Unit Label': police_unit_label,
            'Police Unit Name': police_unit_name,
        }

        # Ensure both keys exist for consistent CSV fieldnames (one may be empty)
        record['Detective Assigned'] = officer_name if officer_key == 'Detective Assigned' else ''
        record['Officer In Charge'] = officer_name if officer_key == 'Officer In Charge' else ''

        return record

    # --- Rules engine ---
    def register_rule(self, rule_callable):
        """Register custom rule for record validation."""
        if callable(rule_callable):
            self._rules.append(rule_callable)

    def _register_default_rules(self):
        """Register built-in consistency rules."""
        self.register_rule(self._rule_severity_weapon_consistency)
        self.register_rule(self._rule_crime_time_consistency)
        self.register_rule(self._rule_suspect_victim_consistency)

    def _rule_severity_weapon_consistency(self, record):
        """Ensure weapon presence aligns with severity."""
        if 'Felony 1' in record['Severity Level'] and record['Weapon Type'] == 'None':
            if random.random() > 0.7:
                record['Weapon Type'] = random.choice(['Gun', 'Knife', 'Blunt Object'])

    def _rule_crime_time_consistency(self, record):
        """Ensure crime time aligns with location patterns."""
        if 'Street' in record['Location Type']:
            if record['Time'].split(':')[0] in ['22', '23', '00', '01', '02', '03']:
                if record['Crime Type'] in ['Theft', 'Assault']:
                    if random.random() > 0.6:
                        record['Crime Type'] = random.choice(['Armed Robbery', 'Aggravated Assault'])

    def _rule_suspect_victim_consistency(self, record):
        """Ensure victim-suspect relationship is realistic."""
        if record['Crime Type'] in ['Robbery', 'Armed Robbery', 'Burglary']:
            if record['Victim-Suspect Relationship'] not in ['Stranger', 'Acquaintance']:
                record['Victim-Suspect Relationship'] = 'Stranger'

    def enforce_rules(self, record):
        """Apply all registered rules to a record."""
        for rule in self._rules:
            rule(record)
        return record


# --- USA Factory ---
class USACrimeFactory(CrimeFactory):
    def __init__(self):
        states_cities = {
            'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Oakland'],
            'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
            'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany'],
            'Illinois': ['Chicago', 'Springfield', 'Aurora', 'Peoria'],
            'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
            'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie'],
            'Ohio': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'],
            'Georgia': ['Atlanta', 'Augusta', 'Savannah', 'Athens'],
            'North Carolina': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'],
            'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor', 'Flint'],
        }
        super().__init__('USA', states_cities)

    def generate_record(self):
        """Generate a USA-specific crime record."""
        state = random.choice(list(self.states_cities.keys()))
        city = random.choice(self.states_cities[state])
        locality = self.fake.neighborhood() if hasattr(self.fake, 'neighborhood') else f"{city} District {random.randint(1, 10)}"
        
        record = self.generate_common_fields(state, city, locality)
        record = self.enforce_rules(record)
        return record


# --- UK Factory ---
class UKCrimeFactory(CrimeFactory):
    def __init__(self):
        states_cities = {
            'England': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool'],
            'Scotland': ['Edinburgh', 'Glasgow', 'Aberdeen', 'Inverness'],
            'Wales': ['Cardiff', 'Swansea', 'Newport', 'Wrexham'],
            'Northern Ireland': ['Belfast', 'Derry', 'Armagh', 'Newry'],
        }
        super().__init__('UK', states_cities)

    def generate_record(self):
        """Generate a UK-specific crime record."""
        region = random.choice(list(self.states_cities.keys()))
        city = random.choice(self.states_cities[region])
        locality = self.fake.postcode() if hasattr(self.fake, 'postcode') else f"{city} Area {random.randint(1, 20)}"
        
        record = self.generate_common_fields(region, city, locality)
        record = self.enforce_rules(record)
        return record


# --- India Factory ---
class IndiaCrimeFactory(CrimeFactory):
    def __init__(self):
        states_cities = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
            'Delhi': ['New Delhi', 'East Delhi', 'North Delhi', 'South Delhi'],
            'Karnataka': ['Bangalore', 'Mysore', 'Mangalore', 'Belgaum'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem'],
            'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot'],
            'West Bengal': ['Kolkata', 'Darjeeling', 'Asansol', 'Siliguri'],
            'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Ajmer'],
            'Punjab': ['Punjab', 'Amritsar', 'Ludhiana', 'Jaipur'],
            'Telangana': ['Hyderabad', 'Secunderabad', 'Warangal', 'Nizamabad'],
        }
        super().__init__('India', states_cities)

    def generate_record(self):
        """Generate an India-specific crime record."""
        state = random.choice(list(self.states_cities.keys()))
        city = random.choice(self.states_cities[state])
        locality = f"{city} - Police Station {random.randint(1, 15)}"
        
        record = self.generate_common_fields(state, city, locality)
        record = self.enforce_rules(record)
        return record


# --- Simple Generic Factory (for additional countries) ---
class SimpleCrimeFactory(CrimeFactory):
    def __init__(self, country, states_cities):
        super().__init__(country, states_cities)

    def generate_record(self):
        state = random.choice(list(self.states_cities.keys()))
        city = random.choice(self.states_cities[state])
        locality = f"{city} Area {random.randint(1, 20)}"

        record = self.generate_common_fields(state, city, locality)
        record = self.enforce_rules(record)
        return record


# --- Crime Dataset Generator ---
class CrimeDatasetGenerator:
    def __init__(self):
        self.factories = {
            'USA': USACrimeFactory(),
            'UK': UKCrimeFactory(),
            'India': IndiaCrimeFactory(),
            # South Asia
            'Pakistan': SimpleCrimeFactory('Pakistan', {
                'Punjab': ['Lahore', 'Faisalabad', 'Rawalpindi', 'Multan'],
                'Sindh': ['Karachi', 'Hyderabad', 'Sukkur', 'Nawabshah'],
                'Khyber Pakhtunkhwa': ['Peshawar', 'Mardan', 'Abbottabad', 'Swat'],
                'Balochistan': ['Quetta', 'Gwadar', 'Sibi'],
                'Islamabad Capital Territory': ['Islamabad'],
            }),
            'Afghanistan': SimpleCrimeFactory('Afghanistan', {
                'Kabul Province': ['Kabul'],
                'Kandahar Province': ['Kandahar'],
                'Herat Province': ['Herat'],
                'Balkh Province': ['Mazar-i-Sharif'],
                'Nangarhar Province': ['Jalalabad'],
            }),
            'Bangladesh': SimpleCrimeFactory('Bangladesh', {
                'Dhaka Division': ['Dhaka', 'Tangail', 'Manikganj'],
                'Chattogram Division': ['Chattogram', "Cox's Bazar", 'Comilla'],
                'Rajshahi Division': ['Rajshahi', 'Rangpur', 'Bogra'],
            }),
            'Sri Lanka': SimpleCrimeFactory('Sri Lanka', {
                'Western Province': ['Colombo', 'Gampaha', 'Kalutara'],
                'Central Province': ['Kandy', 'Matale'],
                'Southern Province': ['Galle', 'Matara'],
            }),
            # Southeast Asia
            'Malaysia': SimpleCrimeFactory('Malaysia', {
                'Selangor': ['Shah Alam', 'Petaling Jaya', 'Subang Jaya'],
                'Kuala Lumpur': ['Kuala Lumpur'],
                'Penang': ['George Town', 'Butterworth'],
                'Sabah': ['Kota Kinabalu', 'Tawau'],
            }),
            'Indonesia': SimpleCrimeFactory('Indonesia', {
                'Java': ['Jakarta', 'Surabaya', 'Bandung', 'Yogyakarta'],
                'Sumatra': ['Medan', 'Palembang', 'Padang'],
                'Kalimantan': ['Pontianak', 'Banjarmasin', 'Balikpapan'],
                'Sulawesi': ['Makassar', 'Manado'],
            }),
            # Gulf countries
            'Saudi Arabia': SimpleCrimeFactory('Saudi Arabia', {
                'Riyadh Province': ['Riyadh', 'Al-Kharj'],
                'Makkah Province': ['Jeddah', 'Mecca'],
                'Eastern Province': ['Dammam', 'Khobar', 'Dhahran'],
            }),
            'United Arab Emirates': SimpleCrimeFactory('United Arab Emirates', {
                'Abu Dhabi': ['Abu Dhabi'],
                'Dubai': ['Dubai'],
                'Sharjah': ['Sharjah'],
            }),
            'Qatar': SimpleCrimeFactory('Qatar', {
                'Doha': ['Doha'],
            }),
            'Bahrain': SimpleCrimeFactory('Bahrain', {
                'Manama Governorate': ['Manama'],
            }),
            'Kuwait': SimpleCrimeFactory('Kuwait', {
                'Kuwait Governorate': ['Kuwait City'],
            }),
            'Oman': SimpleCrimeFactory('Oman', {
                'Muscat Governorate': ['Muscat'],
            }),
            # Eastern Europe
            'Poland': SimpleCrimeFactory('Poland', {
                'Mazovian': ['Warsaw', 'Radom'],
                'Greater Poland': ['Poznan', 'Kalisz'],
                'Lesser Poland': ['Krakow', 'Tarnow'],
            }),
            'Romania': SimpleCrimeFactory('Romania', {
                'Bucharest': ['Bucharest'],
                'Cluj': ['Cluj-Napoca', 'Turda'],
                'Iași': ['Iași'],
            }),
            'Ukraine': SimpleCrimeFactory('Ukraine', {
                'Kyiv Oblast': ['Kyiv', 'Bila Tserkva'],
                'Lviv Oblast': ['Lviv', 'Drohobych'],
                'Kharkiv Oblast': ['Kharkiv', 'Poltava'],
            }),
            'Czechia': SimpleCrimeFactory('Czechia', {
                'Prague': ['Prague'],
                'South Moravian': ['Brno', 'Znojmo'],
            }),
            'Hungary': SimpleCrimeFactory('Hungary', {
                'Central Hungary': ['Budapest'],
                'Western Transdanubia': ['Győr', 'Sopron'],
            }),
            'Bulgaria': SimpleCrimeFactory('Bulgaria', {
                'Sofia Province': ['Sofia'],
                'Plovdiv Province': ['Plovdiv'],
            }),
            'Slovakia': SimpleCrimeFactory('Slovakia', {
                'Bratislava Region': ['Bratislava'],
                'Košice Region': ['Košice'],
            }),
            # Latin America
            'Mexico': SimpleCrimeFactory('Mexico', {
                'Mexico City': ['Mexico City'],
                'Jalisco': ['Guadalajara'],
                'Nuevo León': ['Monterrey'],
            }),
            'Brazil': SimpleCrimeFactory('Brazil', {
                'São Paulo': ['São Paulo', 'Campinas'],
                'Rio de Janeiro': ['Rio de Janeiro', 'Niterói'],
                'Bahia': ['Salvador'],
            }),
            'Argentina': SimpleCrimeFactory('Argentina', {
                'Buenos Aires Province': ['Buenos Aires', 'La Plata'],
                'Córdoba Province': ['Córdoba'],
            }),
            'Colombia': SimpleCrimeFactory('Colombia', {
                'Bogotá DC': ['Bogotá'],
                'Antioquia': ['Medellín', 'Bello'],
                'Valle del Cauca': ['Cali'],
            }),
            'Chile': SimpleCrimeFactory('Chile', {
                'Santiago Metropolitan': ['Santiago'],
                'Valparaíso Region': ['Valparaíso', 'Viña del Mar'],
            }),
            'Peru': SimpleCrimeFactory('Peru', {
                'Lima Province': ['Lima'],
                'Cusco Region': ['Cusco'],
            }),
            # Central Africa
            'DR Congo': SimpleCrimeFactory('DR Congo', {
                'Kinshasa Province': ['Kinshasa'],
                'Haut-Katanga': ['Lubumbashi'],
                'Kongo Central': ['Matadi'],
            }),
            'Central African Republic': SimpleCrimeFactory('Central African Republic', {
                'Bangui Prefecture': ['Bangui'],
            }),
            'Cameroon': SimpleCrimeFactory('Cameroon', {
                'Centre': ['Yaoundé'],
                'Littoral': ['Douala'],
            }),
            'Gabon': SimpleCrimeFactory('Gabon', {
                'Estuaire': ['Libreville'],
            }),
            'Republic of Congo': SimpleCrimeFactory('Republic of Congo', {
                'Brazzaville Department': ['Brazzaville'],
            }),
        }
        self.records = []

    def generate_records(self, records_per_country=1333):
        """Generate crime records across all countries."""
        logger.info(f"Generating {records_per_country} records per country...")
        
        for country_name, factory in self.factories.items():
            logger.info(f"Generating {records_per_country} records for {country_name}...")
            for i in range(records_per_country):
                record = factory.generate_record()
                self.records.append(record)
                if (i + 1) % 500 == 0:
                    logger.info(f"  Generated {i + 1}/{records_per_country} records for {country_name}")
        
        logger.info(f"Total records generated: {len(self.records)}")
        return self.records

    def export_csv(self, filename='crime_dataset.csv'):
        """Export records to CSV."""
        if not self.records:
            logger.error("No records to export. Generate records first.")
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = self.records[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.records)
            
            logger.info(f"Successfully exported {len(self.records)} records to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            return False


# --- Main Execution ---
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("CRIME DATASET GENERATOR - Starting")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    gen = CrimeDatasetGenerator()
    gen.generate_records(records_per_country=1333)  # ~4000 total records
    success = gen.export_csv('crime_dataset.csv')
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info("=" * 60)
    logger.info(f"Generation completed in {duration:.2f} seconds")
    logger.info(f"Records per second: {len(gen.records) / duration:.0f}")
    logger.info("=" * 60)
    
    print(f"\n✓ Generated {len(gen.records)} crime records in {duration:.2f} seconds")
    print(f"✓ Exported to: crime_dataset.csv")
    print(f"✓ Countries: USA, UK, India")
    print(f"✓ Cities: ~30 across all countries")
