import random
import string
import re

# Simple template generator compatible with Faker's bothify-style patterns
# '#' -> digit, '?' -> uppercase letter, '@' -> lowercase letter
def from_template(template: str) -> str:
    out = []
    for ch in template:
        if ch == '#':
            out.append(random.choice(string.digits))
        elif ch == '?':
            out.append(random.choice(string.ascii_uppercase))
        elif ch == '@':
            out.append(random.choice(string.ascii_lowercase))
        else:
            out.append(ch)
    return ''.join(out)


# Luhn algorithm (commonly used for SIN/credit-card-like checks)
def luhn_checksum(number: str) -> int:
    def digits_of(n):
        return [int(d) for d in n]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(str(d * 2)))
    return total % 10


def luhn_create(number_without_check: str) -> str:
    check = luhn_checksum(number_without_check + '0')
    digit = (10 - check) % 10
    return number_without_check + str(digit)


def luhn_validate(number: str) -> bool:
    return luhn_checksum(number) == 0


# Verhoeff algorithm implementation for Aadhaar
# Tables for Verhoeff checksum
_d_table = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0]
]

_p_table = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,9,8,4,2,7,0,6,3],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,7,1,3,2,6,0,8],
    [4,2,7,0,3,6,9,8,1,5],
    [2,7,3,9,6,8,0,4,5,1],
    [7,0,4,1,9,1,8,2,3,6],
    [0,6,8,2,5,7,1,3,9,4],
    [6,3,6,4,2,0,5,9,7,0]
]

_inv_table = [0,4,3,2,1,5,6,7,8,9]


def verhoeff_validate(num_str: str) -> bool:
    c = 0
    for i, ch in enumerate(reversed(num_str)):
        c = _d_table[c][_p_table[(i % 8)][int(ch)]]
    return c == 0


def verhoeff_generate(base_digits: str) -> str:
    # compute check digit for base_digits and append
    c = 0
    for i, ch in enumerate(reversed(base_digits)):
        c = _d_table[c][_p_table[((i+1) % 8)][int(ch)]]
    return base_digits + str(_inv_table[c])


# Aadhaar: 12 digits, Verhoeff checksum on full number
def generate_aadhaar(formatted: bool = False) -> str:
    base = ''.join(random.choice(string.digits) for _ in range(11))
    full = verhoeff_generate(base)
    if formatted:
        return f"{full[0:4]} {full[4:8]} {full[8:12]}"
    return full


# Canadian SIN: 9 digits with Luhn checksum
def generate_sin(formatted: bool = False) -> str:
    base = ''.join(random.choice(string.digits) for _ in range(8))
    full = luhn_create(base)
    if formatted:
        return f"{full[0:3]}-{full[3:6]}-{full[6:9]}"
    return full


def validate_sin(sin: str) -> bool:
    digits = re.sub(r"\D", "", sin)
    return len(digits) == 9 and luhn_validate(digits)


# UK NINO (National Insurance Number) generator/validator
# Format: two letters, six digits, one optional letter (A-D)
def generate_nino() -> str:
    # Exclude certain first letters per gov guidance (D,F,I,Q,U,V) - keep simple
    letters = [c for c in string.ascii_uppercase if c not in 'DFIQUV']
    first = random.choice(letters)
    second = random.choice(letters)
    nums = ''.join(random.choice(string.digits) for _ in range(6))
    suffix = random.choice(['A','B','C','D',''])
    return f"{first}{second}{nums}{suffix}"


# Basic IBAN validator (checksum only)
def validate_iban(iban: str) -> bool:
    s = re.sub(r"\s+", '', iban).upper()
    if not re.match(r'^[A-Z0-9]+$', s):
        return False
    # move first 4 chars to end
    rearr = s[4:] + s[:4]
    # convert letters to numbers A=10 .. Z=35
    conv = []
    for ch in rearr:
        if ch.isdigit():
            conv.append(ch)
        else:
            conv.append(str(ord(ch) - 55))
    num = ''.join(conv)
    # perform mod-97 on large number in chunks
    remainder = 0
    for i in range(0, len(num), 9):
        part = num[i:i+9]
        remainder = (remainder * (10 ** len(part)) + int(part)) % 97
    return remainder == 1


# Passport generator for a handful of countries
def generate_passport(country: str = 'USA') -> str:
    c = country.lower()
    if 'india' in c:
        # 1 letter + 7 digits
        return random.choice(string.ascii_uppercase) + ''.join(random.choice(string.digits) for _ in range(7))
    if 'usa' in c or 'nanp' in c:
        return ''.join(random.choice(string.digits) for _ in range(9))
    if 'uk' in c or 'united kingdom' in c:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
    # default: 1 letter + 8 digits (common-ish)
    return random.choice(string.ascii_uppercase) + ''.join(random.choice(string.digits) for _ in range(8))


# Exported API
__all__ = [
    'from_template', 'generate_aadhaar', 'generate_sin', 'validate_sin', 'generate_nino',
    'validate_iban', 'generate_passport', 'luhn_validate', 'luhn_create'
    'generate_german_tin', 'validate_german_tin', 'generate_pak_cnic', 'validate_pak_cnic',
    'generate_nigeria_nin', 'validate_nigeria_nin', 'generate_codice_fiscale', 'generate_dni', 'validate_dni'
    'generate_german_tin', 'validate_german_tin', 'generate_pak_cnic', 'validate_pak_cnic',
    'generate_nigeria_nin', 'validate_nigeria_nin', 'generate_codice_fiscale', 'generate_dni', 'validate_dni'
]

# ---- Additional country-specific helpers ----
def generate_german_tin() -> str:
    # Germany tax identification number: 11 digits (for synthetic data we ensure 11 digits)
    return ''.join(random.choice(string.digits) for _ in range(11))


def validate_german_tin(tin: str) -> bool:
    s = re.sub(r"\D", '', tin)
    return len(s) == 11


def generate_pak_cnic(formatted: bool = True) -> str:
    # CNIC: 5-7-1 digits (#####-#######-#)
    part1 = ''.join(random.choice(string.digits) for _ in range(5))
    part2 = ''.join(random.choice(string.digits) for _ in range(7))
    part3 = random.choice(string.digits)
    if formatted:
        return f"{part1}-{part2}-{part3}"
    return part1 + part2 + part3


def validate_pak_cnic(cnic: str) -> bool:
    return bool(re.match(r'^\d{5}-\d{7}-\d$', cnic))


def generate_nigeria_nin(formatted: bool = False) -> str:
    # NIN is 11 digits
    nin = ''.join(random.choice(string.digits) for _ in range(11))
    if formatted:
        return f"{nin[0:3]} {nin[3:7]} {nin[7:11]}"
    return nin


def validate_nigeria_nin(nin: str) -> bool:
    s = re.sub(r"\D", '', nin)
    return len(s) == 11


def _cf_extract_consonants(s: str) -> str:
    s = re.sub(r'[^A-Za-z]', '', s).upper()
    consonants = ''.join([c for c in s if c not in 'AEIOU'])
    return consonants


def generate_codice_fiscale(full_name: str, birthdate, gender: str, place_code: str = 'Z000') -> str:
    # Simplified Codice Fiscale generator: uses surname & name consonants, encoded DOB, gender, and place code.
    # birthdate: datetime.date or str in YYYY-MM-DD
    from datetime import datetime
    if isinstance(birthdate, str):
        dob = datetime.strptime(birthdate, '%Y-%m-%d').date()
    else:
        dob = birthdate

    parts = full_name.split()
    surname = parts[-1] if len(parts) > 0 else 'RUSSO'
    name = parts[0] if len(parts) > 0 else 'MARIA'

    s_cons = _cf_extract_consonants(surname)
    n_cons = _cf_extract_consonants(name)

    # Surname code: first 3 consonants, pad with vowels or X
    s_code = (s_cons + ''.join([c for c in surname.upper() if c in 'AEIOU']) + 'XXX')[:3]
    # Name code: special rule - if more than 3 consonants, take 1st,3rd,4th; else take first 3
    if len(n_cons) > 3:
        n_code = n_cons[0] + n_cons[2] + n_cons[3]
    else:
        n_code = (n_cons + ''.join([c for c in name.upper() if c in 'AEIOU']) + 'XXX')[:3]

    year = f"{dob.year % 100:02d}"
    month_codes = 'ABCDEHLMPRST'  # Jan..Dec mapping used in CF
    month = month_codes[dob.month - 1]
    day = dob.day + (40 if gender and gender.lower().startswith('f') else 0)
    day_code = f"{day:02d}"

    partial = s_code + n_code + year + month + day_code + (place_code or 'Z000')

    # checksum: simple mod-26 mapping of digits/letters (lightweight, not exact official algorithm)
    total = 0
    for ch in partial:
        if ch.isdigit():
            total += int(ch)
        else:
            total += ord(ch) - 65
    check = chr((total % 26) + 65)
    return (partial + check).upper()


def generate_dni() -> str:
    letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    number = ''.join(random.choice(string.digits) for _ in range(8))
    idx = int(number) % 23
    return number + letters[idx]


def validate_dni(dni: str) -> bool:
    s = dni.strip().upper()
    m = re.match(r'^(?:[XYZ]?)(\d{7,8})([A-Z])$', s)
    if not m:
        return False
    num_part, check = m.group(1), m.group(2)
    # handle NIE starting letters
    prefix = s[0]
    if prefix == 'X':
        num_full = '0' + num_part
    elif prefix == 'Y':
        num_full = '1' + num_part
    elif prefix == 'Z':
        num_full = '2' + num_part
    else:
        num_full = num_part
    letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    return letters[int(num_full) % 23] == check
