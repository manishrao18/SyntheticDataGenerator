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
        # Work type correlated with age and education
        work_type = self._get_work_type(age, education)

        # Income group and locale-specific financials
        income_group = self._get_world_bank_income_group(country_name)
        # make financials depend on work_type and age to improve correlations
        annual_income, net_worth = self._get_locale_financials(income_group, work_type, age)
        # Income sources and credit score (locale-specific)
        income_sources = self._get_income_sources(income_group, work_type, age)
        credit_score, credit_scale = self._get_credit_score(country_name, income_group, annual_income, net_worth, age)

        # Family metrics
        number_of_kids = self._get_number_of_kids(age, marital_status)
        family_members = 1 + (1 if marital_status == 'Married' else 0) + number_of_kids + self._additional_household_dependents(age)

        # Earnings roles
        is_main_earner, is_co_earner = self._get_earner_roles(marital_status, work_type, annual_income)

        # Vehicles and hobbies
        personal_vehicle_count = self._get_vehicle_count(income_group, annual_income, family_members)
        hobbies = self._get_hobbies()

        # Elderly and dependent flags
        is_elderly = age >= 65
        is_dependent = self._get_is_dependent(age, work_type, number_of_kids)

        # Marriage count (first/second) for relevant statuses
        marriage_count = None
        if marital_status in ['Married', 'Divorced', 'Widowed']:
            marriage_count = random.choices(['First', 'Second'], weights=[85,15])[0]
        
        return {
            'Country': country_name
            , 'Full Name': full_name
            , 'Gender': gender
            , 'Marital Status': marital_status
            , 'Age': age
            , 'Birthdate_dt': birthdate
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
            , 'Work Type': work_type
            , 'Annual Income (USD)': annual_income
            , 'Net Worth (USD)': net_worth
            , 'Income Group': income_group
                , 'Personal Vehicle Count': personal_vehicle_count
                , 'Hobbies': "; ".join(hobbies)
                , 'Income Sources': "; ".join(income_sources)
                , 'Credit Score': credit_score
                , 'Credit Score Scale': credit_scale
            , 'Is Elderly': is_elderly
            , 'Is Dependent': is_dependent
            , 'Is Main Earner': is_main_earner
            , 'Is Co-Earner': is_co_earner
            , 'Marriage Count': marriage_count
            , 'Number of Kids': number_of_kids
            , 'Family Members Count': family_members
        }

    # --- Helper methods for new fields ---
    def _get_work_type(self, age, education):
        if age < 22:
            return random.choices(['Unemployed', 'Salaried', 'Business'], weights=[50,40,10])[0]
        if education in ['PhD', "Master's Degree"]:
            return random.choices(['Salaried', 'Business', 'Unemployed'], weights=[70,25,5])[0]
        return random.choices(['Salaried', 'Business', 'Unemployed'], weights=[60,25,15])[0]

    def _get_world_bank_income_group(self, country_name):
        mapping = {
            'USA': 'High income', 'UK': 'High income', 'Canada': 'High income', 'Australia': 'High income',
            'France': 'High income', 'Germany': 'High income', 'Italy': 'High income', 'New Zealand': 'High income',
            'Ireland': 'High income', 'Spain': 'High income', 'Portugal': 'High income', 'Singapore': 'High income',
            'Israel': 'High income', 'UAE': 'High income', 'Saudi Arabia': 'High income',
            'China': 'Upper middle income', 'Malaysia': 'Upper middle income', 'Turkey': 'Upper middle income',
            'Albania': 'Upper middle income', 'India': 'Lower middle income', 'Nigeria': 'Lower middle income',
            'Bangladesh': 'Lower middle income', 'Pakistan': 'Lower middle income', 'Indonesia': 'Lower middle income'
        }
        return mapping.get(country_name, 'Upper middle income')

    def _get_locale_financials(self, income_group, work_type, age):
        """Returns (annual_income_usd, net_worth_usd) sampled from distributions per income group.
        Make distributions dependent on work_type and age to improve correlations."""
        # base means by income_group
        if income_group == 'High income':
            base_mean = 60000
            base_net = 250000
        elif income_group == 'Upper middle income':
            base_mean = 22000
            base_net = 80000
        elif income_group == 'Lower middle income':
            base_mean = 6000
            base_net = 15000
        else:  # Low income
            base_mean = 1200
            base_net = 3000

        # adjust for work type
        if work_type == 'Business':
            mean = base_mean * random.uniform(1.0, 2.5)
            sigma = base_mean * 1.2
        elif work_type == 'Salaried':
            mean = base_mean * random.uniform(0.8, 1.5)
            sigma = base_mean * 0.6
        else:  # Unemployed / student
            mean = base_mean * random.uniform(0.2, 0.6)
            sigma = base_mean * 0.5

        # age effect: peak earnings between 30-55
        if 30 <= age <= 55:
            mean *= 1.15
        elif age > 55:
            mean *= 0.9

        annual = int(max(0, random.gauss(mean, max(1000, sigma))))

        # net worth correlated with income, but more variance for business owners
        if work_type == 'Business':
            net_mean = base_net * random.uniform(0.8, 3.0) + annual * random.uniform(1, 4)
            net_sigma = base_net * 1.2
        else:
            net_mean = base_net * random.uniform(0.5, 1.5) + annual * random.uniform(0.5, 1.5)
            net_sigma = base_net * 0.6

        # older people often have higher net worth due to savings/estate
        if age >= 60:
            net_mean *= 1.2

        net = int(max(0, random.gauss(net_mean, max(500, net_sigma))))

        return annual, net

    def _get_number_of_kids(self, age, marital_status):
        if marital_status == 'Single' or age < 22:
            mean = 0.2
        elif age < 30:
            mean = 0.5
        elif age < 40:
            mean = 1.2
        elif age < 55:
            mean = 2.0
        else:
            mean = 2.5
        val = max(0, int(random.gauss(mean, max(0.5, mean*0.5))))
        return val

    def _additional_household_dependents(self, age):
        # Additional family members such as elderly parents or other dependents
        if age > 60:
            return random.choice([0,1,2])
        return random.choice([0,0,0,1])

    def _get_earner_roles(self, marital_status, work_type, annual_income):
        # Main earner: likely if employed; co-earner depends on marital status and income group proxy (annual_income)
        is_main = work_type != 'Unemployed' and random.random() < 0.9
        is_co = False
        if marital_status == 'Married':
            # higher household income increases chance of co-earner (dual-income households)
            if annual_income > 40000:
                is_co = random.random() < 0.6
            elif annual_income > 15000:
                is_co = random.random() < 0.4
            else:
                is_co = random.random() < 0.2

        return bool(is_main), bool(is_co)

    def _get_vehicle_count(self, income_group, annual_income, family_members=1):
        base = 0
        if income_group == 'High income':
            base = random.choices([0,1,2,3,4], weights=[5,40,35,15,5])[0]
        elif income_group == 'Upper middle income':
            base = random.choices([0,1,2,3], weights=[15,55,25,5])[0]
        elif income_group == 'Lower middle income':
            base = random.choices([0,1,2], weights=[50,40,10])[0]
        else:
            base = random.choices([0,1], weights=[80,20])[0]

        # more family members increases vehicle need
        if family_members >= 4:
            base = max(base, 1 + (family_members // 3))

        # extra chance of vehicles for very high income
        if annual_income > 150000 and random.random() < 0.3:
            base += 1

        return base

    def _get_hobbies(self):
        hobby_pool = ['Reading', 'Gardening', 'Cooking', 'Traveling', 'Photography', 'Cycling', 'Running', 'Gaming', 'Fishing', 'Hiking', 'Music', 'Dancing', 'Painting', 'Knitting']
        count = random.choices([1,2,3], weights=[60,30,10])[0]
        return random.sample(hobby_pool, count)

    def _get_is_dependent(self, age, work_type, number_of_kids):
        if number_of_kids > 0 and age < 30:
            return random.random() < 0.25
        if age < 22:
            return True
        if age >= 65:
            return random.random() < 0.35
        if work_type == 'Unemployed':
            return random.random() < 0.2
        return False

    def _get_income_sources(self, income_group, work_type, age):
        pool = ['Salary/Wages', 'Business Revenue', 'Investment Income', 'Rental Income', 'Pension', 'Government Benefits', 'Remittances', 'Freelance/Gig']
        sources = []
        # Primary source based on work_type
        if work_type == 'Salaried':
            sources.append('Salary/Wages')
        elif work_type == 'Business':
            sources.append('Business Revenue')
        else:
            # unemployed or other
            if age >= 65:
                sources.append('Pension')
            else:
                sources.append(random.choice(['Freelance/Gig', 'Government Benefits', 'Remittances']))

        # Add 0-2 secondary sources based on income group
        secondary_count = random.choices([0,1,2], weights=[60,30,10])[0]
        remaining = [s for s in pool if s not in sources]
        for _ in range(secondary_count):
            if not remaining:
                break
            pick = random.choice(remaining)
            sources.append(pick)
            remaining.remove(pick)

        return sources

    def _get_credit_score(self, country_name, income_group, annual_income, net_worth, age):
        # Define per-country scales (min, max, label)
        scales = {
            'USA': (300, 850, 'FICO'), 'NANP': (300,850,'FICO'), 'Canada': (300,900,'Canadian'),
            'UK': (0,999,'UK'),
            'Germany': (0,100,'Percent'), 'France': (0,100,'Percent'), 'Italy': (0,100,'Percent'), 'Spain': (0,100,'Percent'), 'Portugal': (0,100,'Percent'),
            'India': (300,900,'Local'), 'Nigeria': (300,900,'Local'), 'Bangladesh': (300,900,'Local'), 'Pakistan': (300,900,'Local')
        }
        min_v, max_v, label = scales.get(country_name, (300,850,'FICO-like'))

        # Base mean depends on income group and annual income; also consider net worth and age
        if isinstance(min_v, int) and min_v == 0:
            # percentage-like scale
            if income_group == 'High income':
                mean = 70
            elif income_group == 'Upper middle income':
                mean = 60
            elif income_group == 'Lower middle income':
                mean = 50
            else:
                mean = 40
            # shift by net_worth and age
            wealth_shift = min(15, int((net_worth / (net_worth + 50000)) * 20))
            age_shift = 5 if age >= 35 and age <= 65 else 0
            score = int(max(min_v, min(max_v, random.gauss(mean + wealth_shift + age_shift, 12))))
        else:
            # numeric credit score scale (e.g., 300-850)
            if income_group == 'High income':
                mean = min_v + (max_v - min_v) * 0.78
            elif income_group == 'Upper middle income':
                mean = min_v + (max_v - min_v) * 0.68
            elif income_group == 'Lower middle income':
                mean = min_v + (max_v - min_v) * 0.55
            else:
                mean = min_v + (max_v - min_v) * 0.45
            # shift mean slightly by annual income and net worth
            shift_income = (annual_income / (annual_income + 50000)) * (max_v - min_v) * 0.03
            shift_net = min(0.2, net_worth / (net_worth + 100000)) * (max_v - min_v) * 0.05
            age_bonus = 0.02 * (age - 30) if age > 30 else 0
            total_shift = shift_income + shift_net + age_bonus * (max_v - min_v)
            score = int(max(min_v, min(max_v, random.gauss(mean + total_shift, (max_v - min_v) * 0.06))))

        return score, label

    def _format_birthdate_from_date(self, date_obj, country_name):
        """Format a date object into a country-specific string."""
        if date_obj is None:
            return ''
        # Countries that prefer month-day-year
        mdy_countries = {'USA', 'Australia', 'NANP'}
        # Countries that prefer year-month-day
        ymd_countries = {'Canada', 'France', 'Germany', 'New Zealand'}
        if country_name in mdy_countries:
            return date_obj.strftime("%m-%d-%Y")
        if country_name in ymd_countries:
            return date_obj.strftime("%Y-%m-%d")
        # Default to day-month-year
        return date_obj.strftime("%d-%m-%Y")

# --- Concrete Country Factories ---
class AlbanianFactory(PIIFactory):
    def __init__(self): super().__init__('sq_AL')
    def generate_record(self):
        data = self.common_fields('Albania')
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Albania'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Ireland'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Nigeria'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Portugal'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Spain'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'NANP'),
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'USA')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Australia')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'UK')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'India')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Pakistan')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Canada')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'France')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Italy')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Germany')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'New Zealand')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Israel')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Bangladesh')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Saudi Arabia')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'UAE')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Indonesia')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Malaysia')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Singapore')
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
        data.update({
            'Birthdate': self._format_birthdate_from_date(data.pop('Birthdate_dt'), 'Hong Kong')
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
        'Work Type', 'Annual Income (USD)', 'Net Worth (USD)', 'Income Group',
        'Income Sources', 'Credit Score', 'Credit Score Scale',
        'Vehicle Registration', 'Personal Vehicle Count', 'Hobbies', 'Is Elderly', 'Is Dependent', 'Is Main Earner', 'Is Co-Earner',
        'Marriage Count', 'Number of Kids', 'Family Members Count', 'Biometric Data', 'Social Media Profiles']

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