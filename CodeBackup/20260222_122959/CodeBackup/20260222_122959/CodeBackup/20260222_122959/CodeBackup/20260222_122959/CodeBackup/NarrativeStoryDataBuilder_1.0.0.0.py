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