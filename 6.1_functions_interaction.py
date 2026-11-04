"""Exercise 6.1 — Small functions working together

WHAT THE PROGRAM MUST DO
    Write three small functions, each doing one thing, and a fourth that uses the other
    three to answer one question about your data.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?  (say which function does what, in order)
    3. What comes out?
    4. What question does your fourth function answer, and why does splitting it into
       three make it easier to check?

WHAT THE AI CANNOT KNOW
    Your question and your split. Ask an assistant for "three functions" and it will
    invent three; they will not be the three your question needs. Decide the split first,
    on paper, then ask.

    One function, one job. If you cannot describe what one of yours does in a single
    sentence without using the word "and", it is doing two things.

CHECK IT YOURSELF
    Test each of the three small functions on its own before combining them. Write in a
    comment the input and expected output you used for each. That is three test cases,
    and they are part of the deliverable.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In:
#    My program uses my list of monthly ETF investments from exercise 4.0.
#    I also choose a monthly investment goal, which is 200 euros.
# 2. Process, function by function:
#    I decided to divide my calculation into three small functions.
#    First, total_invested calculates how much I invested so far.
#    Second, target_total calculates how much I need in total.
#    Third, amount_missing calculates the difference between both amounts.
#    My fourth function uses these results to calculate my next investment.
# 3. Out:
#     My program returns the amount I need to invest next month.
#    The result is a number that I can also use in another calculation.
# 4. The question my fourth function answers:
#    My question is: How much should I invest next month to reach my goal?
#    I think splitting the calculation into three functions is useful.
#    Each function has only one job, so I can check mistakes more easily.
#    It also makes my code easier to understand and reuse.

# Your code below

# MY DATA FROM EXERCISE 4.0

# I use my original list of monthly ETF investments.
investments = [120, 180, 150, 200, 220, 170, 250, 210]

# I decided to set my average monthly goal at 200 euros.
monthly_goal = 200


# FUNCTION 1 - TOTAL INVESTED

# This function calculates how much I invested in total.
def total_invested(investments):
    return sum(investments)


# FUNCTION 2 - TARGET TOTAL

# This function calculates the total amount needed for my goal.
def target_total(goal_per_month, number_of_months):
    return goal_per_month * number_of_months


# FUNCTION 3 - AMOUNT MISSING

# This function calculates how much money I still need.
# I use max to avoid getting a negative result.
def amount_missing(goal, invested):
    return max(goal - invested, 0)


# FUNCTION 4 - MY MAIN FUNCTION

# This function uses my three previous functions.
# I want to calculate how much I should invest next month.
def next_month_needed(investments, monthly_goal):

    # First, I calculate the total amount already invested.
    current_total = total_invested(investments)

    # I add one month because I want to include the next month.
    number_of_months = len(investments) + 1

    # Then, I calculate the total amount needed for my goal.
    goal = target_total(monthly_goal, number_of_months)

    # Finally, I calculate how much money is still missing.
    result = amount_missing(goal, current_total)

    # I return the result so I can use it outside my function.
    return result


# TEST MY THREE SMALL FUNCTIONS

# Test 1: I use [120, 180, 150].
# I expect 450 because 120 + 180 + 150 = 450.
test_total = total_invested([120, 180, 150])
assert test_total == 450

# Test 2: I use a goal of 200 euros for 3 months.
# I expect 600 because 200 * 3 = 600.
test_goal = target_total(200, 3)
assert test_goal == 600

# Test 3: I use a goal of 600 and an investment of 450.
# I expect 150 because 600 - 450 = 150.
test_missing = amount_missing(600, 450)
assert test_missing == 150

# These tests help me check each function separately.
# If a result is incorrect, Python will show an error.
print("All three tests passed!")


# FINAL RESULT

# Now I use my fourth function with my original investment list.
next_investment = next_month_needed(investments, monthly_goal)

# I display the results to understand my investment goal.
print(f"Total invested: {total_invested(investments)} euros")
print(f"Monthly average goal: {monthly_goal} euros")
print(f"Amount needed next month: {next_investment} euros")


# CHECK IT YOURSELF

# I decided to test my three small functions separately.
# I use simple numbers so I can verify the results manually.

# TEST 1 - TOTAL INVESTED
# Input: [120, 180, 150]
# Expected output: 450, because 120 + 180 + 150 = 450.

# TEST 2 - TARGET TOTAL
# Input: 200 euros per month for 3 months.
# Expected output: 600, because 200 * 3 = 600.

# TEST 3 - AMOUNT MISSING
# Input: my target is 600 and I already have 450.
# Expected output: 150, because 600 - 450 = 150.

# I used assert to verify my three calculations.
# If a result is different, Python will show an error.
# If all tests pass, my small functions work for these examples.

# FINAL RESULT
# Now I use my fourth function with my original ETF list.
# I can also verify the fourth function with my full list.
# I expect 300 euros because 200 * 9 - 1500 = 300.