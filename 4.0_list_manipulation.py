"""Exercise 4.0 — Working with a list

WHAT THE PROGRAM MUST DO
    Build a list of at least eight items, then display: the whole list, one item of your
    choice, the list sorted, and something computed from it.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What is your list about, and what did you compute from it? Why is that number
       interesting?

WHAT THE AI CANNOT KNOW
    The content of your list. It must come from your own field: marketing channels,
    campaign names, product references, cities you operate in, monthly budgets. Not
    fruit, not "item1, item2, item3".

    Keep this file. Exercise 5.1 and exercise 6.0 both reuse the list you build here.

CHECK IT YOURSELF
    If you computed an average, a total or a maximum, work it out by hand on three of
    your items first, then check your program agrees on those three.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: a list of eight monthly investment amounts in euros.
# 2. Process: the program selects one amount, sorts the list, 
#    and calculates the total investment.
# 3. Out: the complete list, one monthly investment, the sorted list,
#    and the total amount invested.
# 4. What my list is about, and what I computed from it: 
#    I chose monthly ETF investments because I am interested in asset management. 
#    I calculate the total to see how much money I invested over eight months.

# Your code below
# I create a list of my monthly ETF investments.
investments = [120, 180, 150, 200, 220, 170, 250, 210]

# I display the complete list.
print("Monthly investments:", investments)

# I select the fourth month using [3] because Python starts counting from 0.
print("April investment:", investments[3])

# I sort the amounts from smallest to largest.
print("Sorted investments:", sorted(investments))

# I calculate the total amount invested.
print("Total invested:", sum(investments), "euros")

# First three months: 120 + 180 + 150 = 450 euros.
print("Test first 3 months:", sum(investments[:3]))

# CHECK IT YOURSELF
# My list contains eight monthly investments:
# [120, 180, 150, 200, 220, 170, 250, 210]

# After sorting from smallest to largest, I get:
# [120, 150, 170, 180, 200, 210, 220, 250]

# Calculated the total of the first three months.
# 120 + 180 + 150 = 450 euros.
# Python returned the results, as expected.

# Then, calculated the total of all eight investments.
# 120 + 180 + 150 + 200 + 220 + 170 + 250 + 210 = 1500 euros.

# Finally, I calculated the average monthly investment by hand.
# 1500 / 8 = 187.5 euros.

# These results show that the total and average calculations
# and the investments are sorted in ascending order.