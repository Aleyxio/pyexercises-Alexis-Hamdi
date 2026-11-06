"""Exercise 8.0 — Operators (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Take two values of your choice and display, as a readable table, the result of every
    comparison between them and of the logical combinations of those results.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two values did you pick, and which comparison result surprised you?

WHAT THE AI CANNOT KNOW
    Your two values. Pick a pair where the answer is not obvious: two strings with
    different capitalisation, a number and the same number written as text, or zero and
    an empty string.

CHECK IT YOURSELF
    Predict each result before running. Count how many you got right.

DELIVERABLE
    This file, with your comments and your code.
"""

# Your code below

# 1. What goes in?
#    My program uses two strings: "ETF" and "etf".
#    They have the same meaning but different capital letters.

# 2. What happens to it?
#    First, I compare both values using the six comparison operators.
#    Then, I use logical operators like and, or and not.
#    I want to understand which conditions are True or False.

# 3. What comes out?
#    My program displays a table with the different comparisons.
#    Each result is a Boolean value: True or False.

# 4. Which values did I choose and what surprised me?
#    I chose "ETF" and "etf" because I study finance.
#    I find it interesting that Python treats uppercase and lowercase
#    letters differently, even when the words have the same meaning.
#    I also want to check how this changes the comparison results.


# MY TWO VALUES

# I create two variables containing the same word with different cases.
first_value = "ETF"
second_value = "etf"


# COMPARISON OPERATORS

# I use == to check if both values are exactly equal.
equal = first_value == second_value

# I use != to check if the two values are different.
not_equal = first_value != second_value

# I use > to check if the first value is greater than the second.
greater = first_value > second_value

# I use < to check if the first value is smaller than the second.
smaller = first_value < second_value

# I use >= to check if the first value is greater than or equal.
greater_equal = first_value >= second_value

# I use <= to check if the first value is smaller than or equal.
smaller_equal = first_value <= second_value

# DISPLAY THE COMPARISON TABLE

# I display each comparison to see if the result is True or False.
print("COMPARISON OPERATORS")
print("------------------------------")

print(f"ETF == etf : {equal}")
print(f"ETF != etf : {not_equal}")
print(f"ETF > etf  : {greater}")
print(f"ETF < etf  : {smaller}")
print(f"ETF >= etf : {greater_equal}")
print(f"ETF <= etf : {smaller_equal}")

# LOGICAL OPERATORS

# I use and to check if two conditions are both True.
and_result = equal and smaller

# I use or to check if at least one condition is True.
or_result = equal or smaller

# I use not to reverse the result of a condition.
not_result = not equal

# I also combine two conditions to check if both are True.
combined_result = smaller and not_equal

# DISPLAY THE LOGICAL OPERATORS

# I display the logical results in another table.
print()
print("LOGICAL OPERATORS")
print("------------------------------")

print(f"Equal AND Smaller       : {and_result}")
print(f"Equal OR Smaller        : {or_result}")
print(f"NOT Equal               : {not_result}")
print(f"Smaller AND Not Equal   : {combined_result}")

# FINAL MESSAGE

# I use this exercise to understand how Python compares strings.
# I can see that capital letters change the comparison results.
# I also understand that logical operators combine True and False values.

print()
print("My comparison exercise is complete!")

# CHECK IT YOURSELF

# I decided to compare my original file with my cleaned file.
# My original names.txt contains 10 lines, including 2 empty lines.
# After cleaning, my new file contains 8 names.

# The difference comes from the 2 empty lines that I removed.
# I also corrected the capital letters and removed extra spaces.
# I kept the original file unchanged.

# I checked the first and last names of my sorted list manually.
# The first name is Margaret Hamilton because H comes before the other last names.
# The last name is Guido van Rossum because V comes after the other last names.

# I think my program works correctly because the number of lines is correct.
# The names are also sorted alphabetically by last name.
# This test helped me verify my results and understand my code better.