"""Exercise 7.0 — Collecting data and saving it

WHAT THE PROGRAM MUST DO
    Ask the user for the information needed to record one entry, then save it to a CSV
    file. Running the program twice must produce two entries, not overwrite the first.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?  (name your file, and list your columns)
    4. Which columns did you choose, and what would you actually do with this file once
       it has two hundred rows in it?

WHAT THE AI CANNOT KNOW
    Your columns. They must be the ones you would really need to collect for a purpose
    you can state. See 7.0_student_data.csv for the shape of a header line, not for
    the columns to use.

    Two behaviours are yours to decide, and an assistant will guess them wrong:
    what happens the very first time, when the file does not exist yet and needs its
    header line, and what happens when a value the user typed is not acceptable.

CHECK IT YOURSELF
    Run your program three times with different values. Then open the file and count
    the lines. You should have three entries and exactly one header line. If you have
    three header lines, or one entry, your program is wrong.

DELIVERABLE
    This file, plus the CSV your program produced.
"""

# 1. In:
#    My program asks for the month, the name of the ETF and the amount invested.
#    I type one investment each time I run the program.
# 2. Process:
#    First, I check that the month and ETF name are valid.
#    Then, I convert the amount into a number and check that it is positive.
#    Finally, I save the entry to a CSV file without deleting older entries.
# 3. Out, file name and columns:
#    The program creates or updates a file called 7.0_etf_investments.csv.
#    I chose three columns: month, etf_name and amount_eur.
# 4. Why these columns, and what this file is for:
#    I want to know when I invested, which ETF I chose and how much I invested.
#    With 200 rows, I could compare my monthly amounts and calculate totals
#    for each ETF. This would help me understand my investment habits.


# Your code below

import csv
import math
from pathlib import Path


# I save the CSV next to my Python file.
file_path = Path(__file__).with_name("7.0_etf_investments.csv")

# I ask the user for the month.
# If the format is incorrect, I ask again.
while True:
    month = input("Month (YYYY-MM): ").strip()

    correct_format = (
        len(month) == 7
        and month[4] == "-"
        and month[:4].isdigit()
        and month[5:].isdigit()
    )

    if correct_format and int(month[:4]) > 0 and 1 <= int(month[5:]) <= 12:
        break

    print("Please enter a valid month, for example 2026-11.")


# I ask for the ETF name.
# I do not accept an empty answer.
while True:
    etf_name = input("ETF name: ").strip()

    if etf_name:
        break

    print("Please enter an ETF name.")


# I ask how much money was invested.
# I use float because the amount can include decimals.
while True:
    amount_text = input("Amount invested in EUR: ").strip().replace(",", ".")

    try:
        amount = float(amount_text)

        # I only accept positive and finite numbers.
        if math.isfinite(amount) and amount > 0:
            break

        print("Please enter an amount greater than zero.")

    except ValueError:
        # If the user enters text instead of a number, I ask again.
        print("Please enter a number, for example 150 or 150,50.")


# I check if the file already exists.
# I only want one header, even if I run the program several times.
first_entry = not file_path.exists() or file_path.stat().st_size == 0


# I use append mode "a" to add data without deleting previous investments.
with file_path.open("a", newline="", encoding="utf-8") as file:

    writer = csv.writer(file, delimiter=";")

    # If the file is new or empty, I write the column names first.
    if first_entry:
        writer.writerow(["month", "etf_name", "amount_eur"])

    # I save the new investment with two decimals.
    writer.writerow([month, etf_name, f"{amount:.2f}"])


# I display a message to confirm that my investment was saved.
print("Investment saved successfully!")
print(f"CSV file: {file_path.name}")

# CHECK IT YOURSELF

# I decided to run my program three times with different ETF investments.
# First, I entered 1000 euros for Apple in November 2026.
# Second, I entered 20000.00 euros for Tesla in December 2000.
# Finally, I entered 2000000.00 euros for S&P 500 in February 2025.

# I expect my CSV file to contain 4 lines in total:
# 1 header with the column names and 3 different investment entries.

# After running my program, I need to open the CSV file and check the lines.
# I want to make sure that the header appears only once.
# I also want to verify that my previous investments were not deleted.

# I think this test is important because I want to keep
# a complete history of my ETF investments without losing data.

# If my CSV contains exactly 1 header and 3 entries,
# I can confirm that my program works correctly for these tests.