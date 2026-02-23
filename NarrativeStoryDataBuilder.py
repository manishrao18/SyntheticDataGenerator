# ===================  *****  ===================
# Description: Utility code to generate PII Data in narrative story format for further usage
# important libraries required to install are:
# !pip install pandas
# In this example, the input data file is CSV and output is a text file
# ----------------------------------------------
# Developed By: Manish Patil
# ===================  *****  ===================

import re
import random
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

    # Choose narrative point-of-view per record (weighted): mostly third, some first, few second
    pov = None
    # Allow CSV override if a POV column exists
    if "Narrative POV" in row and pd.notna(row["Narrative POV"]) and str(row["Narrative POV"]).strip():
        pov = str(row["Narrative POV"]).strip().lower()
    else:
        pov = random.choices(["third", "first", "second"], weights=[70, 20, 10], k=1)[0]

    use_name = True
    if pov != "third":
        use_name = False
        if pov == "first":
            sub, obj, pos, refl = ("i", "me", "my", "myself")
        else:
            sub, obj, pos, refl = ("you", "you", "your", "yourself")

    # Intro (Name + role)
    lead_bits = []
    # Prefer honorific if present and not already in the name
    display_name = f"{hon} {clean_name}".strip() if hon else (clean_name or (full or "This person"))

    # Subject and verb forms per POV to keep grammar correct
    if pov == "first":
        subject = "I"
        birth_verb = "was born"
        identify_verb = "identify as"
        stand_verb = "stand"
        weigh_verb = "weigh"
        have_verb = "have"
        maintain_verb = "maintain"
    elif pov == "second":
        subject = "You"
        birth_verb = "were born"
        identify_verb = "identify as"
        stand_verb = "stand"
        weigh_verb = "weigh"
        have_verb = "have"
        maintain_verb = "maintain"
    else:
        subject = sub.capitalize() if sub else display_name
        birth_verb = "was born"
        identify_verb = "identifies as"
        stand_verb = "stands"
        weigh_verb = "weighs"
        have_verb = "has"
        maintain_verb = "maintains"

    if pov == "first":
        # Self-introduction for first-person POV (include honorific when available)
        if hon and clean_name:
            lead_bits.append(f"Hi, I'm {hon} {clean_name}.")
        elif clean_name:
            lead_bits.append(f"Hi, I'm {clean_name}.")
        elif display_name:
            lead_bits.append(f"Hi, I'm {display_name}.")
        else:
            lead_bits.append("Hi, I'm someone.")

        if title and workplace and country:
            lead_bits.append(f"I work as {a_or_an(title)} {fmt(title)} at {fmt(workplace)} in {fmt(country)}.")
        elif title and workplace:
            lead_bits.append(f"I work as {a_or_an(title)} {fmt(title)} at {fmt(workplace)}.")
        elif title and country:
            lead_bits.append(f"I am {a_or_an(title)} {fmt(title)} based in {fmt(country)}.")
        else:
            base_loc = f" in {fmt(country)}" if country else ""
            lead_bits.append(f"I{base_loc} lead a life shaped by many details.")

    elif pov == "second":
        # Second-person uses honorifics/name mention when available
        if hon and clean_name:
            person_ref = f"{hon} {clean_name}"
        elif clean_name:
            person_ref = clean_name
        else:
            person_ref = display_name

        if title and workplace and country:
            lead_bits.append(f"You, {person_ref}, work as {a_or_an(title)} {fmt(title)} at {fmt(workplace)} in {fmt(country)}.")
        elif title and workplace:
            lead_bits.append(f"You, {person_ref}, work as {a_or_an(title)} {fmt(title)} at {fmt(workplace)}.")
        elif title and country:
            lead_bits.append(f"You, {person_ref}, are {a_or_an(title)} {fmt(title)} based in {fmt(country)}.")
        else:
            base_loc = f" in {fmt(country)}" if country else ""
            lead_bits.append(f"You, {person_ref}{base_loc}, lead a life shaped by many details.")

    else:
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
    id_parts = []
    if birth:
        id_parts.append(f"{subject} {birth_verb} on {fmt(birth)}")
    if age:
        id_parts.append(f"aged {fmt(age)}")
    if gender or raceeth or marital:
        demo = []
        if gender:  demo.append(fmt(gender))
        if raceeth: demo.append(fmt(raceeth))
        if marital: demo.append(fmt(marital))
        if demo:
            id_parts.append(f"{identify_verb} {' and '.join(demo)}")
    if id_parts:
        # Use coordinating conjunctions and varied punctuation
        if len(id_parts) == 1:
            lead_bits.append(f"{id_parts[0]}.")
        elif len(id_parts) == 2:
            lead_bits.append(f"{id_parts[0]}, and {id_parts[1]}.")
        else:
            lead_bits.append(f"{id_parts[0]}; {' while '.join(id_parts[1:])}.")

    # Physique & health
    phys = []
    phys_main = []
    if h_cm: phys_main.append(f"{stand_verb} {fmt(h_cm)} cm tall")
    if w_kg: phys_main.append(f"{weigh_verb} {fmt(w_kg)} kg")
    if phys_main:
        phys.append(" and ".join(phys_main))

    visage = []
    if eye:  visage.append(f"{fmt(eye)} eyes")
    if skin: visage.append(f"{fmt(skin)} skin")
    if hair: visage.append(f"{fmt(hair)} hair")
    if visage:
        phys.append(f"{have_verb} " + ", ".join(visage))

    if blood: phys.append(f"blood group {fmt(blood)}")
    if cond:  phys.append(f"medical condition: {fmt(cond)}")
    if disab: phys.append(f"disability: {fmt(disab)}")

    if phys:
        # Use subordinating conjunctions and varied punctuation
        subj = subject
        if len(phys) == 1:
            lead_bits.append(f"{subj} {phys[0]}.")
        elif len(phys) == 2:
            lead_bits.append(f"{subj} {phys[0]}, and {phys[1]}.")
        else:
            lead_bits.append(f"{subj} {phys[0]}. Additionally, {phys[1]}. " + 
                           ("Furthermore, " + phys[2] + "." if len(phys) > 2 else ""))

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
        ids_bits.append("Financial accounts: " + " and ".join(fin))
    if ids_bits:
        # Prefix varies with POV: use possessive for first/second, neutral for third
        if pov == "first":
            prefix = "My key documents include"
        elif pov == "second":
            prefix = "Your key documents include"
        else:
            prefix = "Key documents include"

        if len(ids_bits) == 1:
            lead_bits.append(f"{prefix} {ids_bits[0]}.")
        else:
            lead_bits.append(prefix + ": " + "; ".join(ids_bits[:-1]) + (f"; and {ids_bits[-1]}." if len(ids_bits) > 1 else f"{ids_bits[0]}."))

    # Contact, addresses, tech, social
    addr_bits = []
    if addr:     addr_bits.append(f"home address {fmt(addr)}")
    if workaddr: addr_bits.append(f"work address {fmt(workaddr)}")
    if addr_bits:
        conjunction = " and " if len(addr_bits) > 1 else ""
        other_addr = f"{conjunction}".join(addr_bits) if len(addr_bits) > 1 else addr_bits[0]
        lead_bits.append(f"{pos.capitalize()} addresses are {other_addr}.")

    phones = []
    if mobile:   phones.append(f"mobile {fmt(mobile)}")
    if landline: phones.append(f"landline {fmt(landline)}")
    if phones or email:
        contact_parts = []
        if phones: contact_parts.append(" or ".join(phones))
        if email:  contact_parts.append(f"email {fmt(email)}")
        # Use coordinating conjunction "or" for contact channels
        reach_method = " or ".join(contact_parts)
        lead_bits.append(f"{sub.capitalize()} can be reached via {reach_method}.")

    if ip or mac:
        tech_parts = []
        if ip:  tech_parts.append(f"IP {fmt(ip)}")
        if mac: tech_parts.append(f"MAC {fmt(mac)}")
        lead_bits.append(f"Technical identifiers include {' and '.join(tech_parts)}.")
    if bio:
        lead_bits.append(f"Additionally, biometric data on file: {fmt(bio)}.")

    if social:
        lead_bits.append(f"On social platforms, {sub.lower()} maintains presence as {fmt(social)}.")

    # Financial profile and credit
    fin_parts = []
    if work_type:
        fin_parts.append(f"works in {fmt(work_type)}")
    
    income_str = ""
    if annual_income:
        try:
            ai = int(float(str(annual_income).replace(',', '').strip()))
            income_str = f"earns approximately {ai:,} annually"
        except Exception:
            income_str = f"earns {fmt(annual_income)} annually"
    
    if net_worth:
        net_str = f"maintains a net worth of {fmt(net_worth)}"
        if income_str:
            fin_parts.append(f"{income_str}, and {net_str}")
        else:
            fin_parts.append(net_str)
    elif income_str:
        fin_parts.append(income_str)
    
    if income_sources:
        # Use subordinating conjunction "with" to show additional revenue
        fin_parts.append(f"derives income from {fmt(income_sources)}")
    
    credit_str = ""
    if credit or credit_scale:
        scr = fmt(credit) if credit else "an available score"
        scs = (" (" + fmt(credit_scale) + ")") if credit_scale else ""
        credit_str = f"credit score {scr}{scs}"
    
    if personal_vehicle_count:
        veh_str = f"owns {fmt(personal_vehicle_count)} personal vehicle(s)"
        if credit_str:
            fin_parts.append(f"{veh_str}, yet maintains {credit_str}")
        else:
            fin_parts.append(veh_str)
    elif credit_str:
        fin_parts.append(f"has {credit_str}")
    
    if hobbies:
        # Use coordinating conjunction "and" to add lifestyle detail
        fin_parts.append(f"enjoys {fmt(hobbies)}")
    
    if fin_parts:
        lead_bits.append("Financially, " + "; ".join(fin_parts) + ".")

    # Household / family / roles
    hh_parts = []
    
    # Household roles - use correlative conjunction "both...and"
    roles = []
    is_main = is_main_earner and str(is_main_earner).strip().lower() in ("true","yes","1","y")
    is_co = is_co_earner and str(is_co_earner).strip().lower() in ("true","yes","1","y")
    
    if is_main and is_co:
        hh_parts.append("serves both as main earner and co-earner")
    elif is_main:
        hh_parts.append("serves as the main earner")
    elif is_co:
        hh_parts.append("serves as a co-earner")
    
    # Family structure - use subordinating conjunction "with"
    family_desc = []
    if num_kids:
        family_desc.append(f"{fmt(num_kids)} child(ren)")
    if family_members:
        family_desc.append(f"household size {fmt(family_members)}")
    
    if family_desc:
        hh_parts.append("supports " + " and ".join(family_desc))
    
    # Marriage history - use "having been" subordinating form
    if marriage_count:
        hh_parts.append(f"has been married {fmt(marriage_count)} time(s)")
    
    # Status flags - use "yet" and "furthermore" to show contrasts/additions
    status_flags = []
    if is_elderly and str(is_elderly).strip().lower() in ("true","yes","1","y"):
        status_flags.append("considered elderly")
    if is_dependent and str(is_dependent).strip().lower() in ("true","yes","1","y"):
        status_flags.append("marked as dependent")
    
    if status_flags:
        hh_parts.append(" and ".join(status_flags))
    
    if hh_parts:
        if len(hh_parts) == 1:
            lead_bits.append(f"Within the household, {sub.lower()} {hh_parts[0]}.")
        elif len(hh_parts) == 2:
            lead_bits.append(f"Within the household, {sub.lower()} {hh_parts[0]}, and {hh_parts[1]}.")
        else:
            lead_bits.append(f"Within the household: {sub.lower()} {hh_parts[0]}. " +
                           "Furthermore, " + ", yet ".join(hh_parts[1:]) + ".")

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