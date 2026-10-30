"""Exercise 4.2 — Working with a dictionary

WHAT THE PROGRAM MUST DO
    Describe one real object from your field using a dictionary of at least five fields,
    then read it, change it, remove one field, and display every field with its value.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What object did you describe, which five fields did you choose, and why those?
       A field you would never actually use does not count.

WHAT THE AI CANNOT KNOW
    Your object and your fields. A campaign, a customer, a product, a store, a supplier.
    Choose something you would genuinely have to describe in your job.

CHECK IT YOURSELF
    Ask your program for a field that does not exist. Note what happens in a comment,
    then make it survive that case.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: a dictionary with information about an ETF investment with 6 fields.
# 2. Process: the program reads the information, updates the price, removes one field, 
#    and calculates the investment value.
# 3. Out: value read, changed and removed. The program displays the ETF information
#   (with 5 fields because "Broker" was removed) and the updated investment value.
# 4. My object, my six fields, and why those: 
#    I chose an ETF investment because I am interested in asset management.
#    My six fields are the ETF name, number of shares, price, currency, asset class, 
#    and broker. I use them to identify my investment, calculate its value, 
#    and know where it is held.
#    I remove the broker when preparing a simple investment summary 
#    because I only need the financial information.


# Your code below

# I create a dictionary with six details about my ETF.
etf = {
    "name": "Global Equity ETF",
    "shares": 8,
    "price": 125,
    "currency": "EUR",
    "asset_class": "Equity",
    "broker": "Demo Broker"
}

# I check how many shares I own.
print("Number of shares:", etf["shares"])

# I update the ETF price and remove the broker.
etf["price"] = 130
etf.pop("broker")

# I display all the remaining information.
for key, value in etf.items():
    print(f"{key}: {value}")

# I calculate the updated value of my investment.
print("Position value:", etf["shares"] * etf["price"], "EUR")

# I safely check a field that does not exist.
print("Dividend yield:", etf.get("dividend_yield", "Not available"))

# CHECK IT YOURSELF

# I tried to access "dividend_yield", which does not exist.
# Python displayed a KeyError because the field was missing: KeyError: 'Dividend yield'
# I used get() to avoid the error and display "Not available".

# I also checked that the ETF price changed from 125 to 130.
# The broker field was removed from the dictionary.
# The remaining five fields were displayed correctly.

# Calculated the investment value.
# 8 shares x 130 euros = 1040 euros.
# Python returned this result, as expected.