# ===================  *****  ===================
# Description: Utility code to generate PII Data in narrative story format for further usage
# important libraries required to install are:
# !pip install pandas
# In this example, the input data file is CSV and output is a text file
# ----------------------------------------------
# Developed By: Manish Patil
# ===================  *****  ===================

import re
import pandas as pd
from datetime import datetime

INPUT_PATH = "synthetic_pii_data.csv"           # your CSV file
OUTPUT_PATH = "narrative_stories.txt"
STORY_COL_NAME = "Story Narrative"       # will appear as a new column

def load_sheet(path):
    try:
        # Try UTF-8 first, fallback to UTF-16 if needed
        try:
            return pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding='utf-16')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise

def honorific_and_name(full_name: str):
    if pd.isna(full_name):
        return ("", "")
    name = str(full_name).strip()
    # Common honorifics + a few locale variants you have in your data
    m = re.match(r"^(Mr\\.?|Mrs\\.?|Ms\\.?|Miss|Dr\\.?|Prof\\.?|Sir|Madam|Sig\\.?|Sig\\.ra|Sig\\.na|Mme|M\\.)\\s+(.*)$",
                 name, flags=re.IGNORECASE)
    if m:
        return (m.group(1), m.group(2))
    return ("", name)

def pronouns(gender: str):
    g = str(gender).strip().lower() if pd.notna(gender) else ""
    if g == "male":
        return ("he", "him", "his", "himself")
    if g == "female":
        return ("she", "her", "her", "herself")
    return ("they", "them", "their", "themself")

def a_or_an(word: str):
    if not word or not str(word).strip():
        return "a"
    return "an" if str(word).strip().lower()[0] in "aeiou" else "a"

def fmt(val):
    return str(val).strip()

def build_story(row: pd.Series) -> str:
    # Pull fields defensively (only if present & non-null)
    get = lambda k: row[k] if (k in row and pd.notna(row[k]) and str(row[k]).strip()) else None

    country  = get("Country")
    full     = get("Full Name")
    birth    = get("Birthdate")
    gender   = get("Gender")
    marital  = get("Marital Status")
    raceeth  = get("Race_Ethnicity") or get("Race") or get("Ethnicity")
    natid    = get("National ID")
    dln      = get("Driving License")
    passport = get("Passport")
    taxid    = get("Tax ID")
    bank     = get("Bank Account")
    card     = get("Credit Card")
    blood    = get("Blood Group")
    h_cm     = get("Height (cm)")
    eye      = get("Eye Color")
    skin     = get("Skin Tone")
    hair     = get("Hair Color")
    w_kg     = get("Weight (kg)")
    cond     = get("Medical Condition")
    disab    = get("Disability")
    addr     = get("Address")
    workaddr = get("Work Address")
    mobile   = get("Mobile")
    landline = get("Landline")
    email    = get("Email")
    ip       = get("IP Address")
    mac      = get("MAC Address")
    title    = get("Job Title")
    workplace= get("Workplace")
    edu      = get("Education Level")
    vehicle  = get("Vehicle Registration")
    bio      = get("Biometric Data")
    social   = get("Social Media Profiles")
    # New/extended fields from synthetic_pii_data.csv
    age = get("Age")
    work_type = get("Work Type")
    annual_income = get("Annual Income")
    net_worth = get("Net Worth")
    income_sources = get("Income Sources")
    credit = get("Credit Score")
    credit_scale = get("Credit Score Scale")
    personal_vehicle_count = get("Personal Vehicle Count")
    hobbies = get("Hobbies")
    is_elderly = get("Is Elderly")
    is_dependent = get("Is Dependent")
    is_main_earner = get("Is Main Earner")
    is_co_earner = get("Is Co-Earner")
    marriage_count = get("Marriage Count")
    num_kids = get("Number of Kids")
    family_members = get("Family Members Count")

    hon, clean_name = honorific_and_name(full or "")
    sub, obj, pos, refl = pronouns(gender)

    # Intro (Name + role)
    lead_bits = []
    # Prefer honorific if present and not already in the name
    display_name = f"{hon} {clean_name}".strip() if hon else (clean_name or (full or "This person"))
    if title and workplace and country:
        lead_bits.append(f"{display_name} works as {a_or_an(title)} {fmt(title)} at {fmt(workplace)} in {fmt(country)}.")
    elif title and workplace:
        lead_bits.append(f"{display_name} works as {a_or_an(title)} {fmt(title)} at {fmt(workplace)}.")
    elif title and country:
        lead_bits.append(f"{display_name} is {a_or_an(title)} {fmt(title)} based in {fmt(country)}.")
    else:
        # Fallback
        base_loc = f" in {fmt(country)}" if country else ""
        lead_bits.append(f"{display_name}{base_loc} leads a life shaped by many details.")

    # Identity & demographics
    id_bits = []
    if birth:
        id_bits.append(f"{sub.capitalize()} was born on {fmt(birth)}")
    if age:
        id_bits.append(f"aged {fmt(age)}")
    if gender or raceeth or marital:
        parts = []
        if gender:  parts.append(fmt(gender))
        if raceeth: parts.append(fmt(raceeth))
        if marital: parts.append(fmt(marital))
        if parts:
            id_bits.append(f"identifies as {', '.join(parts)}")
    if id_bits:
        lead_bits.append((", ".join(id_bits) + "."))

    # Physique & health
    phys = []
    if h_cm: phys.append(f"stands {fmt(h_cm)} cm tall")
    if w_kg: phys.append(f"weighs {fmt(w_kg)} kg")
    visage = []
    if eye:  visage.append(f"{fmt(eye)} eyes")
    if skin: visage.append(f"{fmt(skin)} skin")
    if hair: visage.append(f"{fmt(hair)} hair")
    if visage:
        phys.append("has " + ", ".join(visage))
    if blood: phys.append(f"blood group {fmt(blood)}")
    if cond:  phys.append(f"medical condition: {fmt(cond)}")
    if disab: phys.append(f"disability: {fmt(disab)}")
    if phys:
        lead_bits.append(f"{sub.capitalize()} " + "; ".join(phys) + ".")

    # IDs & financials
    ids_bits = []
    if natid:    ids_bits.append(f"National ID {fmt(natid)}")
    if dln:      ids_bits.append(f"Driving License {fmt(dln)}")
    if passport: ids_bits.append(f"Passport {fmt(passport)}")
    if taxid:    ids_bits.append(f"Tax ID {fmt(taxid)}")
    if vehicle:  ids_bits.append(f"Vehicle Registration {fmt(vehicle)}")
    if bank or card:
        fin = []
        if bank: fin.append(f"Bank Account {fmt(bank)}")
        if card: fin.append(f"Credit Card {fmt(card)}")
        ids_bits.append("; ".join(fin))
    if ids_bits:
        lead_bits.append(f"Key documents include " + "; ".join(ids_bits) + ".")

    # Contact, addresses, tech, social
    contact_bits = []
    addr_bits = []
    tech_bits = []
    social_bits = []

    if addr:     addr_bits.append(f"home address {fmt(addr)}")
    if workaddr: addr_bits.append(f"work address {fmt(workaddr)}")
    if addr_bits:
        lead_bits.append(f"{pos.capitalize()} addresses are " + " and ".join(addr_bits) + ".")

    phones = []
    if mobile:   phones.append(f"mobile {fmt(mobile)}")
    if landline: phones.append(f"landline {fmt(landline)}")
    if phones or email:
        contact_sentence = f"{sub.capitalize()} can be reached via "
        joined = []
        if phones: joined.append(" and ".join(phones))
        if email:  joined.append(f"email {fmt(email)}")
        contact_bits.append(contact_sentence + " or ".join(joined) + ".")
    if contact_bits:
        lead_bits.extend(contact_bits)

    if ip or mac:
        tmps = []
        if ip:  tmps.append(f"IP {fmt(ip)}")
        if mac: tmps.append(f"MAC {fmt(mac)}")
        tech_bits.append(f"Technical identifiers include " + " and ".join(tmps) + ".")
    if bio:
        tech_bits.append(f"Biometric data: {fmt(bio)}.")
    if tech_bits:
        lead_bits.extend(tech_bits)

    if social:
        social_bits.append(f"On social platforms, {sub.lower()} is listed as {fmt(social)}.")
        lead_bits.extend(social_bits)

    # Financial profile and credit
    fin_bits = []
    if work_type:
        fin_bits.append(f"works in {fmt(work_type)}")
    if annual_income:
        try:
            ai = int(float(str(annual_income).replace(',', '').strip()))
            fin_bits.append(f"earns about {ai:,} annually")
        except Exception:
            fin_bits.append(f"earns {fmt(annual_income)} annually")
    if net_worth:
        fin_bits.append(f"has an estimated net worth of {fmt(net_worth)}")
    if income_sources:
        fin_bits.append(f"income sources include {fmt(income_sources)}")
    if credit or credit_scale:
        scr = fmt(credit) if credit else "an available score"
        scs = (" (" + fmt(credit_scale) + ")") if credit_scale else ""
        fin_bits.append(f"has a credit score of {scr}{scs}")
    if personal_vehicle_count:
        fin_bits.append(f"owns {fmt(personal_vehicle_count)} personal vehicle(s)")
    if hobbies:
        fin_bits.append(f"enjoys {fmt(hobbies)}")
    if fin_bits:
        lead_bits.append("Financial profile: " + "; ".join(fin_bits) + ".")

    # Household / family / roles
    hh_bits = []
    roles = []
    if is_main_earner and str(is_main_earner).strip().lower() in ("true","yes","1","y"):
        roles.append("main earner")
    if is_co_earner and str(is_co_earner).strip().lower() in ("true","yes","1","y"):
        roles.append("co-earner")
    if roles:
        hh_bits.append(" and ".join(roles))
    if marriage_count:
        hh_bits.append(f"been married {fmt(marriage_count)} time(s)")
    if num_kids:
        hh_bits.append(f"has {fmt(num_kids)} child(ren)")
    if family_members:
        hh_bits.append(f"family size {fmt(family_members)}")
    if is_elderly and str(is_elderly).strip().lower() in ("true","yes","1","y"):
        hh_bits.append("is considered elderly")
    if is_dependent and str(is_dependent).strip().lower() in ("true","yes","1","y"):
        hh_bits.append("is marked as dependent")
    if hh_bits:
        lead_bits.append("Household: " + "; ".join(hh_bits) + ".")

    return " ".join(lead_bits)

# --- run ---
df = load_sheet(INPUT_PATH)
stories = df.apply(build_story, axis=1)
df[STORY_COL_NAME] = stories

# Save stories to text file
try:
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("NARRATIVE STORIES FROM SYNTHETIC PII DATA\n")
        f.write("=" * 50 + "\n\n")
        
        for idx, story in enumerate(stories, 1):
            f.write(f"Record {idx}:\n")
            f.write("-" * 50 + "\n")
            f.write(story)
            f.write("\n\n")
    
    print(f"✓ Written {len(stories)} stories to: {OUTPUT_PATH}")
except IOError as e:
    print(f"✗ Error writing to file: {e}")