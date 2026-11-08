"""Exercise 10.0 — Checking the shape of text (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Validate three pieces of information typed by the user, and only save them when all
    three are acceptable.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What are your three fields, and what makes a value acceptable for each? Write the
       rule in plain English before writing any pattern.

WHAT THE AI CANNOT KNOW
    Your three rules. "A valid email" is not a rule, it is a wish. Say what you accept
    and what you reject, and be ready to defend a borderline case.

WHAT TO WATCH
    An assistant will hand you a pattern that looks like line noise. Do not accept it
    until it has explained it to you piece by piece, and you have written that
    explanation in your own words above it.

CHECK IT YOURSELF
    For each field, prepare one value that must pass and two that must fail. Run all
    nine. Any surprise goes in a comment.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. What goes in?
# My program asks for a registration code, a finance sector and a seat number.

# 2. What happens to it?
# I check the three values using regular expressions.
# If they are all valid, I save them in a CSV file.

# 3. What comes out?
# My program displays True or False for each value.
# Valid registrations are saved in finance_registrations.csv.

# 4. What are my three rules?
# Code: FIN- followed by exactly four digits.
# Sector: only AM, ECM or DCM in capital letters.
# Seat: a letter from A to C, followed by a number from 01 to 30.
# I chose these fields to organise participants at a finance event.

import re
import csv
from pathlib import Path

# REGULAR EXPRESSIONS

# [0-9]{4} means exactly four digits after FIN-.
code_pattern = r"FIN-[0-9]{4}"

# | means OR, so I accept one of these three sectors.
sector_pattern = r"(AM|ECM|DCM)"

# [A-C] selects the section and the rest selects seats 01 to 30.
seat_pattern = r"[A-C](0[1-9]|[12][0-9]|30)"


# USER INPUT

# I ask for the three values and remove extra spaces.
code = input("Registration code: ").strip()
sector = input("Finance sector (AM/ECM/DCM): ").strip()
seat = input("Seat number (A01 to C30): ").strip()


# VALIDATION

# fullmatch checks the entire value against my pattern.
# bool converts the result into True or False.
code_ok = bool(re.fullmatch(code_pattern, code))
sector_ok = bool(re.fullmatch(sector_pattern, sector))
seat_ok = bool(re.fullmatch(seat_pattern, seat))


# DISPLAY RESULTS

print("\nREGISTRATION VERIFICATION")
print("-----------------------------")
print("Registration code:", code, "valid:", code_ok)
print("Finance sector:", sector, "valid:", sector_ok)
print("Seat number:", seat, "valid:", seat_ok)


# SAVE VALID REGISTRATIONS

# I save the information only if all three conditions are True.
if code_ok and sector_ok and seat_ok:

    path = Path(__file__).with_name("finance_registrations.csv")
    new_file = not path.exists() or path.stat().st_size == 0

    # Append mode keeps the previous registrations.
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # I write the header only when the file is new or empty.
        if new_file:
            writer.writerow(["registration_code", "finance_sector", "seat_number"])

        writer.writerow([code, sector, seat])

    print("\nRegistration saved successfully!")

else:
    # Invalid information is not saved.
    print("\nRegistration not saved.")

    if not code_ok:
        print("Invalid registration code.")
    if not sector_ok:
        print("Invalid finance sector.")
    if not seat_ok:
        print("Invalid seat number.")


# CHECK IT YOURSELF

# I prepared one valid and two invalid examples for each field.
# I want to understand which values Python accepts or rejects.

# Registration code:
# FIN-4821 should pass.
# FIN-482 and fin-4821 should fail.

# Finance sector:
# DCM should pass.
# dcm and FX should fail.

# Seat number:
# B12 should pass.
# B00 and D12 should fail.

# I will test the nine values and compare them with my predictions.
# I also want to verify that incorrect registrations are not saved.
# I will record any unexpected results after running the tests.