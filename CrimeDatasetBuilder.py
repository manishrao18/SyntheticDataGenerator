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

# --- Base Factory Interface ---
class CrimeFactory(ABC):
    def __init__(self, country, states_cities):
        self.country = country
        self.fake = Faker()
        self.states_cities = states_cities  # dict: {state: [cities]}
        self._rules = []
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
                'Night': ['Armed Robbery', 'Aggravated Assault', 'Burglary', 'Theft']
            },
            'Residential Area': {
                'Morning': ['Burglary', 'Theft', 'Assault', 'Drug Violation'],
                'Afternoon': ['Burglary', 'Theft', 'Vandalism', 'Minor Assault'],
                'Evening': ['Burglary', 'Assault', 'Drug Violation', 'Theft'],
                'Night': ['Burglary', 'Breaking and Entering', 'Drug Violation', 'Assault']
            },
            'Street': {
                'Morning': ['Theft', 'Robbery', 'Assault', 'Vandalism'],
                'Afternoon': ['Theft', 'Robbery', 'Assault', 'Vandalism'],
                'Evening': ['Armed Robbery', 'Assault', 'Drug Violation', 'Gang Activity'],
                'Night': ['Armed Robbery', 'Aggravated Assault', 'Gang Activity', 'Drug Violation']
            },
            'Hospital/School': {
                'Morning': ['Assault', 'Theft', 'Drug Violation', 'Trespassing'],
                'Afternoon': ['Assault', 'Theft', 'Drug Violation', 'Vandalism'],
                'Evening': ['Assault', 'Drug Violation', 'Trespassing', 'Theft'],
                'Night': ['Trespassing', 'Drug Violation', 'Assault', 'Theft']
            },
            'Industrial Zone': {
                'Morning': ['Burglary', 'Theft', 'Fraud', 'Vehicle Theft'],
                'Afternoon': ['Burglary', 'Theft', 'Assault', 'Drug Violation'],
                'Evening': ['Burglary', 'Vehicle Theft', 'Drug Violation', 'Theft'],
                'Night': ['Burglary', 'Armed Robbery', 'Vehicle Theft', 'Drug Violation']
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

    def _get_weapon_by_crime(self, crime_type):
        """Determine weapon type based on crime."""
        weapon_map = {
            'Armed Robbery': ['Gun', 'Knife', 'Handgun'],
            'Aggravated Assault': ['Knife', 'Gun', 'Blunt Object'],
            'Murder': ['Gun', 'Knife', 'Blunt Object'],
            'Robbery': ['Gun', 'Knife', 'Threat'],
            'Burglary': ['None', 'Knife', 'Crowbar'],
            'Assault': ['None', 'Fist', 'Blunt Object'],
            'Theft': ['None', 'None'],
            'Fraud': ['None', 'None'],
            'Drug Violation': ['None', 'Knife'],
            'Vehicle Theft': ['None', 'None'],
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
        suspect_race = random.choice(['White', 'Black', 'Hispanic', 'Asian', 'Other'])
        
        victim_age, victim_gender, victim_relationship = self._get_victim_by_crime(crime_type, suspect_age)
        
        evidence = self._get_evidence_by_crime(crime_type, weapon)
        charges = self._get_charges_by_crime_severity(crime_type, severity)
        arrest_status = self._get_arrest_status(severity, evidence)
        
        time_since_crime = (datetime.now().date() - crime_date).days
        case_status = self._get_case_status(arrest_status, evidence, time_since_crime)
        
        criminal_history = self._get_criminal_history(suspect_age)
        num_witnesses = random.randint(0, 5)
        
        # Random time within the day
        crime_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        
        return {
            'Country': self.country,
            'State_Province': state,
            'City': city,
            'Locality': locality,
            'Crime Type': crime_type,
            'Severity Level': severity,
            'Date': crime_date.strftime('%Y-%m-%d'),
            'Time': crime_time,
            'Location Type': location_type,
            'Suspect Age': suspect_age,
            'Suspect Gender': suspect_gender,
            'Suspect Race': suspect_race,
            'Victim Age': victim_age,
            'Victim Gender': victim_gender,
            'Victim Race': random.choice(['White', 'Black', 'Hispanic', 'Asian', 'Other']),
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
        }

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


# --- Crime Dataset Generator ---
class CrimeDatasetGenerator:
    def __init__(self):
        self.factories = {
            'USA': USACrimeFactory(),
            'UK': UKCrimeFactory(),
            'India': IndiaCrimeFactory(),
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
