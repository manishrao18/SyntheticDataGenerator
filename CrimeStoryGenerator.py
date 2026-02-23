# ===================  *****  ===================
# Description: Crime Case Narrative Story Generator
# Generates detailed narrative stories from crime dataset records
# Important libraries required: pandas
# !pip install pandas
# Input: crime_dataset.csv
# Output: crime_narratives.txt
# ----------------------------------------------
# Developed By: AI Assistant
# ===================  *****  ===================

import re
import random
import pandas as pd
from datetime import datetime

INPUT_PATH = "crime_dataset.csv"
OUTPUT_PATH = "crime_narratives.txt"
STORY_COL_NAME = "Case Narrative"

def load_sheet(path):
    try:
        try:
            return pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding='utf-16')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise

def gender_pronouns(gender: str):
    g = str(gender).strip().lower() if pd.notna(gender) else ""
    if g == "male":
        return ("he", "him", "his")
    if g == "female":
        return ("she", "her", "her")
    return ("they", "them", "their")

def fmt(val):
    """Format value safely."""
    if pd.isna(val):
        return "Unknown"
    return str(val).strip()

def build_crime_narrative(row: pd.Series) -> str:
    """Build detailed crime case narrative from record."""
    
    get = lambda k: row[k] if (k in row and pd.notna(row[k]) and str(row[k]).strip()) else None
    
    # Extract all fields
    country = fmt(get("Country") or "Unknown Country")
    state = fmt(get("State_Province") or "Unknown State")
    city = fmt(get("City") or "Unknown City")
    locality = fmt(get("Locality") or "Local Area")
    crime_type = fmt(get("Crime Type") or "Crime")
    severity = fmt(get("Severity Level") or "Unknown")
    date = fmt(get("Date") or "2023-01-01")
    time = fmt(get("Time") or "Unknown Time")
    location_type = fmt(get("Location Type") or "Unknown Location")
    
    suspect_age = get("Suspect Age")
    suspect_gender = fmt(get("Suspect Gender") or "Unknown Gender")
    suspect_race = fmt(get("Suspect Race") or "Unknown Ethnicity")
    suspect_pronouns = gender_pronouns(suspect_gender)
    
    victim_age = get("Victim Age")
    victim_gender = fmt(get("Victim Gender") or "Unknown Gender")
    victim_race = fmt(get("Victim Race") or "Unknown Ethnicity")
    victim_occ = fmt(get("Victim Occupation") or "Resident")
    victim_pronouns = gender_pronouns(victim_gender)
    
    motive = fmt(get("Suspect Motive") or "Unknown Motive")
    weapon = fmt(get("Weapon Type") or "No Weapon")
    evidence = fmt(get("Evidence Found") or "Minimal Evidence")
    charges = fmt(get("Charges") or "Charges Pending")
    arrest_status = fmt(get("Arrest Status") or "Unresolved")
    case_status = fmt(get("Case Status") or "Under Investigation")
    criminal_history = fmt(get("Criminal History") or "Unknown Background")
    victim_relationship = fmt(get("Victim-Suspect Relationship") or "Unknown")
    witnesses = get("Number of Witnesses")
    
    # Format numbers
    try:
        suspect_age = int(suspect_age) if suspect_age else random.randint(20, 50)
        victim_age = int(victim_age) if victim_age else random.randint(20, 70)
        witnesses = int(witnesses) if witnesses else random.randint(0, 3)
    except:
        suspect_age = 35
        victim_age = 45
        witnesses = 1
    
    # Build detailed narrative
    narrative_parts = []
    
    # Case Header
    narrative_parts.append(f"CASE REPORT - {crime_type.upper()}")
    narrative_parts.append(f"Case ID: CR-{date.replace('-', '')}-{random.randint(1000, 9999)}")
    narrative_parts.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
    narrative_parts.append(f"Jurisdiction: {city}, {state}, {country}")
    narrative_parts.append("")
    
    # Incident Details
    narrative_parts.append("INCIDENT DETAILS:")
    narrative_parts.append(f"Date of Incident: {date}")
    narrative_parts.append(f"Time of Incident: {time}")
    narrative_parts.append(f"Location: {locality} ({location_type})")
    narrative_parts.append(f"Crime Classification: {crime_type}")
    narrative_parts.append(f"Severity Level: {severity}")
    narrative_parts.append("")
    
    # Suspect Profile
    narrative_parts.append("SUSPECT PROFILE:")
    narrative_parts.append(f"Age: {suspect_age} years old")
    narrative_parts.append(f"Gender: {suspect_gender}")
    narrative_parts.append(f"Race/Ethnicity: {suspect_race}")
    narrative_parts.append(f"Criminal History: {criminal_history}")
    narrative_parts.append(f"Suspected Motive: {motive}")
    narrative_parts.append("")
    
    # Victim Profile
    narrative_parts.append("VICTIM PROFILE:")
    narrative_parts.append(f"Age: {victim_age} years old")
    narrative_parts.append(f"Gender: {victim_gender}")
    narrative_parts.append(f"Race/Ethnicity: {victim_race}")
    narrative_parts.append(f"Occupation: {victim_occ}")
    narrative_parts.append(f"Relationship to Suspect: {victim_relationship}")
    narrative_parts.append("")
    
    # Detailed Narrative
    narrative_parts.append("NARRATIVE:")
    
    # Build crime-specific narrative
    if crime_type == "Robbery":
        narrative = f"On {date} at approximately {time}, a {crime_type.lower()} occurred at {locality}. "
        narrative += f"The victim, a {victim_age}-year-old {victim_gender.lower()}, was approached by the suspect. "
        narrative += f"The suspect, identified as a {suspect_age}-year-old {suspect_gender.lower()} of {suspect_race} descent, "
        narrative += f"demanded property. "
        if weapon != "No Weapon":
            narrative += f"The suspect was armed with {article(weapon).lower()}. "
        narrative += f"The victim complied with demands. "
        if arrest_status == "Arrested":
            narrative += f"The suspect was apprehended at the scene."
        else:
            narrative += f"The suspect fled the scene and remains at large."
    
    elif crime_type in ["Assault", "Aggravated Assault"]:
        narrative = f"On {date} around {time}, an assault incident was reported at {locality}. "
        narrative += f"The victim, aged {victim_age}, was attacked by the suspect. "
        narrative += f"The suspect, a {suspect_age}-year-old {suspect_gender.lower()}, "
        narrative += f"allegedly acted out of {motive.lower()}. "
        narrative += f"{suspect_pronouns[0].capitalize()} {suspect_pronouns[1]} {weapon.lower()} during the altercation. "
        narrative += f"The victim sustained injuries and sought medical attention."
    
    elif crime_type == "Burglary":
        narrative = f"A burglary was reported on {date} at {locality}. "
        narrative += f"The suspect, a {suspect_age}-year-old {suspect_gender.lower()}, allegedly broke into the property. "
        narrative += f"The victim, a {victim_age}-year-old {victim_gender.lower()}, discovered the intrusion upon returning home. "
        narrative += f"The suspect's motive was {motive.lower()}. "
        narrative += f"Several items were reported missing from the property."
    
    elif crime_type in ["Theft", "Shoplifting"]:
        narrative = f"On {date}, a {crime_type.lower()} occurred at {locality}. "
        narrative += f"The suspect, aged {suspect_age}, allegedly took merchandise without payment. "
        narrative += f"Store personnel observed the incident and {arrest_status.lower()}. "
        narrative += f"The value of stolen items was approximately estimated."
    
    elif crime_type == "Murder":
        narrative = f"A homicide investigation was initiated on {date} at {locality}. "
        narrative += f"The victim, a {victim_age}-year-old {victim_gender.lower()} {victim_occ}, "
        narrative += f"was found deceased. The primary suspect, a {suspect_age}-year-old {suspect_gender.lower()}, "
        narrative += f"had {victim_relationship.lower()} relationship with the victim. "
        narrative += f"The motive is believed to be {motive.lower()}. "
        if weapon != "No Weapon":
            narrative += f"{article(weapon)} was recovered at the scene. "
        narrative += f"The case status is currently {case_status.lower()}."
    
    elif crime_type == "Fraud":
        narrative = f"A fraud complaint was filed on {date} involving {locality}. "
        narrative += f"The suspect, a {suspect_age}-year-old individual, is alleged to have committed financial fraud. "
        narrative += f"The victim, a {victim_age}-year-old {victim_occ}, reported suspicious transactions. "
        narrative += f"The financial loss is being assessed. Digital evidence has been collected for investigation."
    
    elif crime_type == "Drug Violation":
        narrative = f"On {date}, law enforcement responded to a drug-related incident at {locality}. "
        narrative += f"A {suspect_age}-year-old suspect was found in possession of controlled substances. "
        narrative += f"{suspect_pronouns[0].capitalize()} was {arrest_status.lower()} at the scene. "
        narrative += f"Evidence collected includes {evidence.lower()}."
    
    else:
        narrative = f"On {date} at {time}, an incident classified as {crime_type} occurred at {locality}. "
        narrative += f"The suspect, a {suspect_age}-year-old {suspect_gender.lower()}, is the primary person of interest. "
        narrative += f"The victim, aged {victim_age}, reported {motive.lower()} as the suspected motive. "
        narrative += f"The case is {case_status.lower()}."
    
    narrative_parts.append(narrative)
    narrative_parts.append("")
    
    # Evidence
    narrative_parts.append("EVIDENCE:")
    narrative_parts.append(f"Evidence Collected: {evidence}")
    if weapon != "No Weapon":
        narrative_parts.append(f"Weapon: {weapon}")
    narrative_parts.append("")
    
    # Investigation Status
    narrative_parts.append("INVESTIGATION STATUS:")
    narrative_parts.append(f"Charges: {charges}")
    narrative_parts.append(f"Arrest Status: {arrest_status}")
    narrative_parts.append(f"Case Status: {case_status}")
    narrative_parts.append(f"Witnesses: {witnesses} witness(es) identified")
    narrative_parts.append("")
    
    # Case Notes
    narrative_parts.append("CASE NOTES:")
    if arrest_status == "Arrested":
        narrative_parts.append(f"Suspect has been taken into custody. {criminal_history}.")
    else:
        narrative_parts.append(f"Suspect remains fugitive. Active manhunt underway.")
    
    narrative_parts.append(f"Investigating Officer: Officer [ID: {random.randint(1000, 9999)}]")
    narrative_parts.append(f"Department: {city} Police Department")
    narrative_parts.append("-" * 80)
    narrative_parts.append("")
    
    return "\n".join(narrative_parts)


def article(word):
    """Return appropriate article (a/an) for a word."""
    if not word or str(word).strip().lower() == "unknown":
        return "an object"
    return ("an" if str(word).lower()[0] in "aeiou" else "a") + " " + str(word).lower()


def generate_narratives():
    """Main function to generate crime narratives."""
    print("Loading crime dataset...")
    df = load_sheet(INPUT_PATH)
    print(f"Loaded {len(df)} crime records")
    
    print("Generating narratives...")
    narratives = []
    for idx, row in df.iterrows():
        narrative = build_crime_narrative(row)
        narratives.append(narrative)
        
        if (idx + 1) % 500 == 0:
            print(f"  Generated {idx + 1}/{len(df)} narratives...")
    
    print(f"Writing {len(narratives)} narratives to file...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(narratives))
    
    print(f"✓ Successfully generated {len(narratives)} crime narratives")
    print(f"✓ Saved to: {OUTPUT_PATH}")
    return len(narratives)


if __name__ == "__main__":
    try:
        count = generate_narratives()
        print(f"\nCompleted! Generated {count} crime case narratives.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
