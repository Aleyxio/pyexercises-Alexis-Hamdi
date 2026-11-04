"""Exercise 6.0 — Naming a piece of work

WHAT THE PROGRAM MUST DO
    Write a function that computes something useful about the list you built in exercise
    4.0, then call it three times with different inputs and display the three results.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?  (what your function receives)
    2. What happens to it?
    3. What comes out?  (what your function returns)
    4. What is your function called, and does its name say what it does without reading
       the code?

WHAT THE AI CANNOT KNOW
    What is worth computing about your data, and what to call it. A function named
    "process" or "do_stuff" fails this exercise even if it works.

    Your function must RETURN its result, not print it. Find out why that difference
    matters and write the reason in a comment. It is the whole point of the exercise.

CHECK IT YOURSELF
    Call your function with an empty list. Note what happens. Then decide whether that
    behaviour is acceptable, and say so in a comment.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. What goes in?
# My function receives two inputs:
# - investments: my list of monthly ETF investment amounts.
# - goal_amount: the minimum amount I want to invest each month.

# 2. What happens to it?
# I use a for loop to check each monthly investment.
# If I reach my goal, my streak increases by 1.
# If I invest less than my goal, my streak goes back to 0.
# I keep the longest streak found during the loop.

# 3. What comes out?
# The function returns one integer showing the longest
# number of consecutive months when I reached my goal.

# 4. What is it called?
# I called my function longest_investment_streak.
# I chose this name because it clearly explains
# what my function calculates.

# WHY RETURN AND NOT PRINT?
# I use return because I want to reuse my result later.
# For example, I can save it or compare different investment goals.
# print only displays a value, while return gives it back to my code.



# Your code below

# MY FUNCTION

# This function calculates my longest monthly investment streak.
def longest_investment_streak(investments, goal_amount):

    # I start both values at 0 before checking my investments.
    best_streak = 0
    current_streak = 0

    # I check each monthly investment using a for loop.
    for amount in investments:

        # If I reach my goal, I add 1 to my current streak.
        if amount >= goal_amount:
            current_streak += 1

            # I keep the highest streak found so far.
            best_streak = max(best_streak, current_streak)

        else:
            # If I miss my goal, my current streak goes back to 0.
            current_streak = 0

    # I return the result so I can use it outside the function.
    return best_streak

# MY DATA FROM EXERCISE 4.0

# This is my list of monthly ETF investments.
investments = [120, 180, 150, 200, 220, 170, 250, 210]

# THREE CALLS WITH DIFFERENT INPUTS

# Test 1: I check my streak with a monthly goal of 150.
streak_150 = longest_investment_streak(investments, 150)

# Test 2: I increase my monthly goal to 200.
streak_200 = longest_investment_streak(investments, 200)

# Test 3: I use another list with a monthly goal of 200.
other_investments = [250, 220, 180, 240, 260, 300]
other_streak = longest_investment_streak(other_investments, 200)

# DISPLAY MY RESULTS

# I display my three results to compare my investment streaks.
print(f"Longest streak with a goal of 150: {streak_150} months")
print(f"Longest streak with a goal of 200: {streak_200} months")
print(f"Other investment streak: {other_streak} months")

# CHECK WITH AN EMPTY LIST

# I want to check what happens if my investment list is empty.
empty_result = longest_investment_streak([], 200)

print(f"Empty list result: {empty_result}")

# The function returns 0 because there are no investments to check.
# I think this is correct because no streak can exist without data.
# My program also works without crashing.
assert empty_result == 0

# CHECK IT YOURSELF

# I decided to verify my calculation using my first three investments.
# My first three monthly amounts are 120, 180 and 150.
# I use a monthly goal of 150.

# I calculated the result manually:
# Month 1: 120 is below my goal, so my streak is 0.
# Month 2: 180 reaches my goal, so my streak becomes 1.
# Month 3: 150 reaches my goal, so my streak becomes 2.