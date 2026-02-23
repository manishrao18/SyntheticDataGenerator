#===================  *****  ===================
# Description: Utility code to generate Synthetic PII data per country for any analysis or any usuage
# important libraries required to install are:
# !pip install faker
# csv and random are natively available, possibly not required to be installed
#----------------------------------------------
# Fields generated are:
# 'Country', 'Full Name', 'Birthdate', 'Gender', 'Marital Status', 'Race_Ethnicity','National ID',
# 'Driving License', 'Passport', 'Tax ID', 'Bank Account', 'Credit Card',
# 'Blood Group', 'Height (cm)', 'Eye Color', 'Skin Tone', 'Hair Color', 'Weight (kg)',
# 'Medical Condition', 'Disability', 'Address', 'Work Address', 'Mobile', 'Landline', #'Postal Code'
# 'Email', 'IP Address', 'MAC Address', 'Job Title', 'Workplace', 'Education Level',
# 'Vehicle Registration', 'Biometric Data', 'Social Media Profiles'
#----------------------------------------------
# Developed By: Manish Patil
#===================  *****  ===================

#### date format concate
#### print(fake.random_element(elements=(str(fake.date_of_birth(minimum_age=18).strftime("%m-%d-%Y")),
####                 str(fake.date_of_birth(minimum_age=18).strftime("%d-%m-%Y")),
####                 str(fake.date_of_birth(minimum_age=18).strftime("%Y-%m-%d")))))

import csv
import random
import logging
import sys
from abc import ABC, abstractmethod
from faker import Faker
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Base Factory Interface ---
class PIIFactory(ABC):
    def __init__(self, locale):
        self.fake = Faker(locale)

    @abstractmethod
    def generate_record(self):
        """Must be implemented by each country factory."""
        pass

    def _get_realistic_gender_name(self, full_name):
        """Extract or infer gender from name to ensure consistency."""
        # This is a simplified heuristic - Faker generates gender-appropriate names in most locales
        return 'Female' if any(name.endswith(('a', 'i', 'ie')) for name in full_name.split()) else 'Male'
    
    def _get_realistic_age_marital(self, age):
        """Generate realistic marital status based on age."""
        if age < 25:
            return random.choice(['Single', 'Single', 'Single', 'Married'])  # Mostly single when young
        elif age < 35:
            return random.choice(['Single', 'Married', 'Married', 'Married'])  # More married
        elif age < 50:
            return random.choice(['Married', 'Married', 'Married', 'Divorced', 'Divorced'])  # Often married, some divorced
        else:
            return random.choice(['Married', 'Divorced', 'Widowed', 'Widowed'])  # More diverse, more widowed

    def _get_realistic_height_weight(self, gender):
        """Generate realistic height and weight with proper correlation."""
        if gender.lower() == 'female':
            height = random.gauss(165, 6)  # Average female height ~165cm
            height = max(152, min(182, height))  # Realistic range: 152-182cm
            weight = height * 0.38 + random.gauss(0, 5)  # Weight correlates with height
        else:
            height = random.gauss(178, 7)  # Average male height ~178cm
            height = max(162, min(195, height))  # Realistic range: 162-195cm
            weight = height * 0.42 + random.gauss(0, 5)  # Weight correlates with height
        
        return int(height), int(weight)

    def _get_realistic_medical_disability(self):
        """Generate realistic medical condition and disability - most people have none."""
        if random.random() < 0.85:  # 85% have no conditions
            return 'None', 'None'
        
        # If they have something, usually one not both
        has_condition = random.random() < 0.6
        has_disability = random.random() < 0.3
        
        condition = random.choice(['None', 'Asthma', 'Diabetes', 'Hypertension', 'Thyroid Disorder']) if has_condition else 'None'
        disability = random.choice(['None', 'Visual Impairment', 'Hearing Impairment', 'Mobility Impairment']) if has_disability else 'None'
        
        return condition, disability

    def _get_education_job_match(self, education):
        """Generate a job title that matches the education level."""
        job_by_education = {
            'High School': ['Retail Worker', 'Cashier', 'Delivery Driver', 'Manufacturing Technician', 'Administrative Assistant', 'Sales Representative'],
            'Associate Degree': ['Medical Technician', 'Graphic Designer', 'Network Administrator', 'Electrician', 'Paralegal', 'Lab Technician'],
            'Bachelor\'s Degree': ['Software Engineer', 'Accountant', 'Marketing Manager', 'Project Manager', 'Nurse', 'Analyst', 'Teacher'],
            'Master\'s Degree': ['Senior Manager', 'Data Scientist', 'Systems Architect', 'Senior Consultant', 'Director', 'Senior Engineer'],
            'PhD': ['Research Scientist', 'University Professor', 'Lead Researcher', 'Chief Scientist', 'Principal Investigator', 'Academic Director'],
            'Professional Certificate': ['Security Officer', 'Real Estate Agent', 'Personal Trainer', 'Technical Specialist', 'Certified Technician']
        }
        return random.choice(job_by_education.get(education, self.fake.job()))

    def common_fields(self, country_name):
        """Generates standard fields applicable across all regions with realistic correlations."""
        full_name = self.fake.name()
        gender = self._get_realistic_gender_name(full_name)
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        age = (datetime.now().date() - birthdate).days // 365
        marital_status = self._get_realistic_age_marital(age)
        height, weight = self._get_realistic_height_weight(gender)
        medical_cond, disability = self._get_realistic_medical_disability()
        education = random.choice(['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Associate Degree', 'Professional Certificate'])
        job_title = self._get_education_job_match(education)
        
        return {
            'Country': country_name
            , 'Full Name': full_name
            , 'Gender': gender
            , 'Marital Status': marital_status
            , 'Blood Group': random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
            , 'Height (cm)': height
            , 'Eye Color': random.choice(['Blue', 'Green', 'Brown', 'Hazel', 'Gray', 'Amber'])
            , 'Skin Tone': random.choice(['Very Fair', 'Fair', 'Medium', 'Tan', 'Brown', 'Dark'])
            , 'Hair Color': random.choice(['Blonde', 'Brown', 'Black', 'Red', 'Gray', 'White', 'Bald'])
            , 'Weight (kg)': weight
            , 'Biometric Data': self.fake.sha256()
            , 'Medical Condition': medical_cond
            , 'Disability': disability
            , 'Email': self.fake.free_email()
            , 'Social Media Profiles': f"https://www.{random.choice(['facebook', 'twitter', 'linkedin', 'instagram'])}.com/{self.fake.user_name()}"
            , 'IP Address': self.fake.ipv4()
            , 'MAC Address': self.fake.mac_address()
            , 'Job Title': job_title
            , 'Workplace': self.fake.company()
            , 'Education Level': education
        }

# --- Concrete Country Factories ---
class AlbanianFactory(PIIFactory):
    def __init__(self): super().__init__('sq_AL')
    def generate_record(self):
        data = self.common_fields('Albania')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y"),
            'Race_Ethnicity': random.choice(['Albanian', 'Greek', 'Roma', 'Other']),
            'National ID': self.fake.bothify("#########"),
            'Tax ID': self.fake.bothify("#########"),
            'Bank Account': self.fake.iban(),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify("AL#########"),
            'Vehicle Registration': self.fake.bothify("AL-###-##").upper(),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}",
            'Mobile': self.fake.phone_number(),
            'Landline': self.fake.phone_number(),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class IrishFactory(PIIFactory):
    def __init__(self): super().__init__('en_IE')
    def generate_record(self):
        data = self.common_fields('Ireland')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y"),
            'Race_Ethnicity': random.choice(['Irish', 'Traveller', 'Other']),
            'National ID': self.fake.bothify("#########"),
            'Tax ID': self.fake.bothify("#########"),
            'Bank Account': self.fake.iban(),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify("IE#########"),
            'Vehicle Registration': self.fake.bothify("IE-###-##").upper(),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}",
            'Mobile': self.fake.phone_number(),
            'Landline': self.fake.phone_number(),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class NigerianFactory(PIIFactory):
    def __init__(self): super().__init__('en_NG')
    def generate_record(self):
        data = self.common_fields('Nigeria')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y"),
            'Race_Ethnicity': random.choice(['Yoruba', 'Igbo', 'Hausa', 'Fulani', 'Other']),
            'National ID': self.fake.bothify("#########"),
            'Tax ID': self.fake.bothify("#########"),
            'Bank Account': self.fake.iban(),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify("NG#########"),
            'Vehicle Registration': self.fake.bothify("NG-###-##").upper(),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}",
            'Mobile': self.fake.phone_number(),
            'Landline': self.fake.phone_number(),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class PortugueseFactory(PIIFactory):
    def __init__(self): super().__init__('pt_PT')
    def generate_record(self):
        data = self.common_fields('Portugal')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y"),
            'Race_Ethnicity': random.choice(['Portuguese', 'Brazilian', 'African', 'Other']),
            'National ID': self.fake.bothify("#########"),
            'Tax ID': self.fake.bothify("#########"),
            'Bank Account': self.fake.iban(),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify("PT#########"),
            'Vehicle Registration': self.fake.bothify("PT-###-##").upper(),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}",
            'Mobile': self.fake.phone_number(),
            'Landline': self.fake.phone_number(),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class SpanishFactory(PIIFactory):
    def __init__(self): super().__init__('es_ES')
    def generate_record(self):
        data = self.common_fields('Spain')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y"),
            'Race_Ethnicity': random.choice(['Spanish', 'Catalan', 'Basque', 'Galician', 'Other']),
            'National ID': self.fake.bothify("#########"),
            'Tax ID': self.fake.bothify("#########"),
            'Bank Account': self.fake.iban(),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify("ES#########"),
            'Vehicle Registration': self.fake.bothify("ES-###-##").upper(),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}",
            'Mobile': self.fake.phone_number(),
            'Landline': self.fake.phone_number(),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class NANPFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('NANP')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%m-%d-%Y"),
            'Race_Ethnicity': random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Native American', 'Other']),
            'National ID': self.fake.ssn().upper(),
            'Tax ID': self.fake.itin(),
            'Bank Account': self.fake.bothify(random.choice(["##########", "###########", "############"])),
            'Credit Card': self.fake.credit_card_number(),
            'Passport': self.fake.bothify("?########").upper(),
            'Driving License': self.fake.bothify(random.choice(["#########", "?########", "??########", "??#########"]).upper()),
            'Vehicle Registration': self.fake.bothify(random.choice(["??-####-##", "?#-####-##", "??-#####-#"]).upper()),
            'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}",
            'Mobile': self.fake.bothify(random.choice(["(###)###-####", "###-###-####", "+1-###-###-####","+1(###)###-####"])),
            'Landline': self.fake.bothify(random.choice(["(###)###-####", "###-###-####", "+1-###-###-####","+1(###)###-####"])),
            'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"
        })
        return data

class USAFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('USA')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%m-%d-%Y")
            , 'Race_Ethnicity': random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Native American', 'Mixed Race', 'Other'])
            , 'National ID': self.fake.ssn().upper()
            , 'Tax ID': self.fake.itin()
            , 'Bank Account': self.fake.bothify(random.choice(["##########", "###########", "############"]))
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify("?########").upper()
            , 'Driving License': self.fake.bothify(random.choice(["#########", "?########", "??########", "??#########"]).upper())
            , 'Vehicle Registration': self.fake.bothify(random.choice(["??-####-##", "?#-####-##", "??-#####-#"]).upper())
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"
        })
        return data

class AustraliaFactory(PIIFactory):
    def __init__(self): super().__init__('en_AU')
    def generate_record(self):
        data = self.common_fields('Australia')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%m-%d-%Y")
            , 'Race_Ethnicity': random.choice(['Indigenous', 'European', 'Chinese', 'Indian', 'Other'])
            , 'National ID': self.fake.bothify(random.choice(["####/#####", "##########", "###-###-###"]).upper())
            , 'Tax ID': self.fake.bothify(random.choice(["### ### ##", "### ### ###"]))
            , 'Bank Account': self.fake.bothify(random.choice(["###-###-####", "###-###-###"]))
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(random.choice(["?#######", "??#######"]).upper())
            , 'Driving License': self.fake.bothify(random.choice(["########", "#########", "###-###-###"]))
            , 'Vehicle Registration': self.fake.bothify(random.choice(["??-####-##", "?#-####-##"]).upper())
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.postcode()}"
        })
        return data

class UKFactory(PIIFactory):
    def __init__(self): super().__init__('en_GB')
    def generate_record(self):
        data = self.common_fields('UK')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'Race_Ethnicity': random.choice(['White', 'Black', 'Asian', 'Mixed', 'Asian British', 'Black British', 'Other'])
            , 'National ID': self.fake.bothify(random.choice(["?? ## ## ## A", "??-##-##-##-B"]).upper())
            , 'Tax ID': self.fake.bothify("###########")
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(random.choice(["?########", "#########"]).upper())
            , 'Driving License': self.fake.bothify("????###########").upper()
            , 'Vehicle Registration': self.fake.bothify("?? ## ???").upper()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class IndiaFactory(PIIFactory):
    def __init__(self): super().__init__('en_IN')
    def generate_record(self):
        data = self.common_fields('India')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'Race_Ethnicity': random.choice(['Marathi', 'Gujarati', 'Rajasthani', 'North Indian', 'Telugu', 'Tamil', 'Kannada', 'Malayali', 'Bengali', 'Punjabi', 'Other'])
            , 'National ID': self.fake.aadhaar_id()
            , 'Tax ID': self.fake.bothify(text='?????####?').upper()
            , 'Bank Account': self.fake.bban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify("?##############").upper()
            , 'Driving License': self.fake.bothify("??-#############").upper()
            , 'Vehicle Registration': self.fake.bothify("?? ## ?? ####").upper()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
        })
        return data

class PakistanFactory(PIIFactory):
    def __init__(self): super().__init__('en_PK')
    def generate_record(self):
        data = self.common_fields('Pakistan')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'Race_Ethnicity': random.choice(['Punjabi', 'Sindhi', 'Saraiki', 'Muhajir', 'Baloch', 'Pashtun', 'Other'])
            , 'National ID': self.fake.bothify(text='#####-#######-#')
            , 'Tax ID': self.fake.bothify(text='#####-#######-#').upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='?########').upper()
            , 'Driving License': self.fake.numerify('####-#######')
            , 'Vehicle Registration': self.fake.bothify("??? ## ####").upper()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
        })
        return data

class CanadaFactory(PIIFactory):
    def __init__(self): super().__init__('en_CA')
    def generate_record(self):
        data = self.common_fields('Canada')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%Y-%m-%d")
            , 'Race_Ethnicity': random.choice(['White', 'Black', 'Indigenous', 'Asian', 'Chinese', 'Indian', 'Other'])
            , 'National ID': self.fake.bothify(text='###-###-###')
            , 'Tax ID': self.fake.bothify(text='###-###-###')
            , 'Bank Account': self.fake.numerify(text='#######')
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='?########').upper()
            , 'Driving License': self.fake.numerify('#######')
            , 'Vehicle Registration': self.fake.license_plate()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.province()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.province()} {self.fake.postcode()}"
        })
        return data

class FranceFactory(PIIFactory):
    def __init__(self): super().__init__('fr_FR')
    def generate_record(self):
        data = self.common_fields('France')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%Y-%m-%d")
            , 'Race_Ethnicity': random.choice(['European', 'North African', 'Sub-Saharan African', 'Asian', 'Indian', 'Other'])
            , 'National ID': self.fake.numerify(text='############')
            , 'Tax ID': f"{self.fake.random_int(0,3)}{self.fake.numerify('############')}"
            , 'Bank Account': self.fake.bban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='??######').upper()
            , 'Driving License': self.fake.bothify(text='#### ## ## ## ##')
            , 'Vehicle Registration': self.fake.license_plate()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class ItalyFactory(PIIFactory):
    def __init__(self): super().__init__('it_IT')
    def generate_record(self):
        data = self.common_fields('Italy')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'Race_Ethnicity': random.choice(['Mediterranean', 'Celtic', 'Germanic', 'Slavic', 'Asian', 'Indian', 'Other'])
            , 'National ID': self.fake.ssn()
            , 'Tax ID': self.fake.ssn()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='??#######').upper()
            , 'Driving License': self.fake.bothify(text='######??##??')
            , 'Vehicle Registration': self.fake.license_plate()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
        })
        return data

class GermanyFactory(PIIFactory):
    def __init__(self): super().__init__('de_DE')
    def generate_record(self):
        data = self.common_fields('Germany')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%Y-%m-%d")
            , 'Race_Ethnicity': random.choice(['Germanic', 'Caucasian', 'Asian', 'Indian', 'African', 'Other'])
            , 'National ID': self.fake.ssn()
            , 'Tax ID': self.fake.bothify("## ### ### ### #")
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='#########').upper()
            , 'Driving License': self.fake.bothify(text='#########')
            , 'Vehicle Registration': self.fake.license_plate()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state()} {self.fake.postcode()}"
        })
        return data

class NewZealandFactory(PIIFactory):
    def __init__(self): super().__init__('en_NZ')
    def generate_record(self):
        data = self.common_fields('New Zealand')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%Y-%m-%d")
            , 'Race_Ethnicity': random.choice(['European', 'Māori', 'Pacific Islander', 'Asian', 'Indian', 'Other'])
            , 'National ID': self.fake.bothify(text='#########')
            , 'Tax ID': self.fake.numerify('#########')
            , 'Bank Account': self.fake.bothify(text='##-####-#######-###')
            , 'Credit Card': self.fake.credit_card_number()
            , 'Passport': self.fake.bothify(text='?########').upper()
            , 'Driving License': self.fake.bothify(text='??######').upper()
            , 'Vehicle Registration': self.fake.license_plate()
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
        })
        return data

class IsraelFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('Israel')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("#########")
            , 'Tax ID': self.fake.bothify("#########")
            , 'Passport': self.fake.bothify("#########")
            , 'Driving License': self.fake.bothify("#########")
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Vehicle Registration': self.fake.bothify("???-##-###").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
        })
        return data

class BangladeshFactory(PIIFactory):
    def __init__(self): super().__init__('en_IN')
    def generate_record(self):
        data = self.common_fields('Bangladesh')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("#### #### ####")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("?#######")
            , 'Driving License': self.fake.bothify("BD#########")
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Vehicle Registration': self.fake.bothify("?? ### ####").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Bengali', 'Chakma', 'Rohingya', 'Marma', 'Other'])
        })
        return data

class SaudiArabiaFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('Saudi Arabia')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("#### #### ####")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("#########")
            , 'Driving License': self.fake.bothify("SA#########")
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Vehicle Registration': self.fake.bothify("???-##-###").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Arab', 'Other'])
        })
        return data

class UAEFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('UAE')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("### #### ####")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("#########")
            , 'Driving License': self.fake.bothify("784-#######")
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}"
            , 'Vehicle Registration': self.fake.bothify("???-##-###").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Emirati', 'Arab', 'Other'])
        })
        return data

class IndonesiaFactory(PIIFactory):
    def __init__(self): super().__init__('en_US')
    def generate_record(self):
        data = self.common_fields('Indonesia')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("#### #### #### ####")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("?########")
            , 'Driving License': self.fake.bothify("####-##-###-####")
            , 'Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.postcode()}"
            , 'Vehicle Registration': self.fake.bothify("??? ## ####").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Javanese', 'Sundanese', 'Madurese', 'Minangkabau', 'Other'])
        })
        return data

class MalaysiaFactory(PIIFactory):
    def __init__(self): super().__init__('en_IN')
    def generate_record(self):
        data = self.common_fields('Malaysia')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("########-##-####")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("?########")
            , 'Driving License': self.fake.bothify("?-##-##-####")
            , 'Address': f"{self.fake.street_address()}, {self.fake.postcode()} {self.fake.city()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.postcode()} {self.fake.city()}"
            , 'Vehicle Registration': self.fake.bothify("?? ## ####").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Malay', 'Chinese', 'Indian', 'Other'])
        })
        return data

class SingaporeFactory(PIIFactory):
    def __init__(self): super().__init__('en_IN')
    def generate_record(self):
        data = self.common_fields('Singapore')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("S####@@@")
            , 'Tax ID': self.fake.bothify("##-###-###")
            , 'Passport': self.fake.bothify("?########")
            , 'Driving License': self.fake.bothify("S####-##-###")
            , 'Address': f"{self.fake.street_address()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.postcode()}"
            , 'Vehicle Registration': self.fake.bothify("?## ###").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Chinese', 'Malay', 'Indian', 'Eurasian', 'Other'])
        })
        return data

class HongKongFactory(PIIFactory):
    def __init__(self): super().__init__('en_IN')
    def generate_record(self):
        data = self.common_fields('Hong Kong')
        birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=85)
        data.update({
            'Birthdate': birthdate.strftime("%d-%m-%Y")
            , 'National ID': self.fake.bothify("?########")
            , 'Tax ID': self.fake.bothify("###########")
            , 'Passport': self.fake.bothify("?########")
            , 'Driving License': self.fake.bothify("####/###/##")
            , 'Address': f"{self.fake.street_address()}, {self.fake.postcode()}"
            , 'Mobile': self.fake.phone_number()
            , 'Landline': self.fake.phone_number()
            , 'Work Address': f"{self.fake.street_address()}, {self.fake.postcode()}"
            , 'Vehicle Registration': self.fake.bothify("?? ## ####").upper()
            , 'Bank Account': self.fake.iban()
            , 'Credit Card': self.fake.credit_card_number()
            , 'Race_Ethnicity': random.choice(['Hong Kong Chinese', 'Chinese', 'Western', 'Indian', 'Other'])
        })
        return data

# --- Factory Registry & Orchestrator ---
class PIIGenerator:
    def __init__(self):
        """Initialize PII Generator with country factories."""
        try:
            self.factories = {
               'USA': USAFactory()
               ,'UK': UKFactory()
               ,'India': IndiaFactory()
               ,'Australia': AustraliaFactory()
               ,'Canada': CanadaFactory()
               ,'France': FranceFactory()
               ,'Italy': ItalyFactory()
               ,'Germany': GermanyFactory()
               ,'New Zealand': NewZealandFactory()
               , 'Pakistan': PakistanFactory()
               , 'Israel': IsraelFactory()
               , 'Bangladesh': BangladeshFactory()
               , 'Saudi Arabia': SaudiArabiaFactory()
               , 'UAE': UAEFactory()
               , 'Indonesia': IndonesiaFactory()
               , 'Malaysia': MalaysiaFactory()
               , 'Singapore': SingaporeFactory()
               , 'Hong Kong': HongKongFactory()
               , 'Albania': AlbanianFactory()
               , 'Ireland': IrishFactory()
               , 'Nigeria': NigerianFactory()
               , 'Portugal': PortugueseFactory()
               , 'Spain': SpanishFactory()
               #, 'NANP': NANPFactory()
            }
            logger.info(f"Initialized PIIGenerator with {len(self.factories)} factories")
        except Exception as e:
            logger.error(f"Error initializing PIIGenerator: {str(e)}")
            raise

    def export_csv(self, records_per_country=100):
        """Export synthetic PII data to CSV file.

        Args:
            records_per_country (int): Number of records to generate per country (default: 100)

        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(records_per_country, int) or records_per_country <= 0:
            logger.error(f"Invalid records_per_country value: {records_per_country}. Must be positive integer.")
            return False

        headers = [
        'Country', 'Full Name', 'Birthdate', 'Gender', 'Marital Status', 'Race_Ethnicity','National ID',
        'Driving License', 'Passport', 'Tax ID', 'Bank Account', 'Credit Card',
        'Blood Group', 'Height (cm)', 'Eye Color', 'Skin Tone', 'Hair Color', 'Weight (kg)',
        'Medical Condition', 'Disability', 'Address', 'Work Address', 'Mobile', 'Landline', #'Postal Code'
        'Email', 'IP Address', 'MAC Address', 'Job Title', 'Workplace', 'Education Level',
        'Vehicle Registration', 'Biometric Data', 'Social Media Profiles']

        file_name = 'synthetic_pii_data.csv'

        try:
            with open(file_name, 'w', newline='', encoding='utf-16') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                total_records = 0

                for country, factory in self.factories.items():
                    try:
                        logger.info(f"Generating data for {country}...")
                        for i in range(records_per_country):
                            try:
                                record = factory.generate_record()
                                writer.writerow(record)
                                total_records += 1
                            except Exception as e:
                                logger.error(f"Error generating record {i+1} for {country}: {str(e)}")
                                continue
                    except Exception as e:
                        logger.error(f"Error processing {country}: {str(e)}")
                        continue

            logger.info(f"Successfully exported {total_records} records to {file_name}")
            print(f"[OK] Dataset generated successfully: {file_name} ({total_records} records)")
            return True

        except IOError as e:
            logger.error(f"File I/O error while writing to {file_name}: {str(e)}")
            print(f"[ERROR] Cannot write to file '{file_name}'. Check directory permissions.")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during CSV export: {str(e)}")
            print(f"[ERROR] {str(e)}")
            return False

if __name__ == "__main__":
    try:
        gen = PIIGenerator()
        success = gen.export_csv(100)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.critical(f"Fatal error in main execution: {str(e)}")
        print(f"[CRITICAL] {str(e)}")
        sys.exit(1)