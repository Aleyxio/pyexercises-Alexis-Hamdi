"""Exercise 5.1 — Doing the same thing to every item

WHAT THE PROGRAM MUST DO
    Take the list you built in exercise 4.0 and, for every item, display a line that
    combines the item, its position, and something computed about it.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What did you compute for each item, and what does the reader learn from that line?

WHAT THE AI CANNOT KNOW
    Your list from 4.0, and what is worth computing about its items. Length of the name,
    share of a total, position in a ranking, whether the item passes a threshold you set.
    Open your 4.0 file, copy the list across, and say in a comment what you decided.

CHECK IT YOURSELF
    Count the lines your program printed. There must be exactly as many as items in your
    list. If there is one more or one less, you have an off-by-one, and it is worth
    understanding now rather than in the exam.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: A list of eight monthly ETF investments in euros, from Exercise 4.0
# 2. Process: The program goes through each month and adds 
#   the investment to a running total.
# 3. Out: Eight lines showing the month (from 1 to 8), the investment amount, 
#   and the total invested so far.
# 4. What I compute for each item, and why it is worth showing:
# I calculate the total invested after each month 
# because I want to see how my investments grow over time. 
# This helps me track how much money I have invested.

# Your code below

# I use the same ETF investments from Exercise 4.0.
investments = [120, 180, 150, 200, 220, 170, 250, 210]

# I start with zero euros invested.
total = 0

# I go through each month and calculate the total invested.
# I use start=1 to make the months start from 1 instead of 0.
# This avoids an off-by-one error and keeps the month numbers correct.
for month, amount in enumerate(investments, start=1):
    total = total + amount
    print(f"Month {month}: {amount} euros, Total invested: {total} euros")

# CHECK IT YOURSELF

# My original list contains 8 monthly investments.
# The program displayed exactly 8 lines, as expected.

# I checked the first three months by hand:
# Month 1: 120 euros.
# Month 2: 120 + 180 = 300 euros.
# Month 3: 300 + 150 = 450 euros.

# The results match my calculations.
# The final total is 1500 euros after 8 months.
# No month was skipped or repeated.