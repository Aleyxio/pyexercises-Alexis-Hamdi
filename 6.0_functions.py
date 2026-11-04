"""Exercise 6.0 - Naming a piece of work

Data (from exercise 4.0): a list of how many minutes I studied each day.
Example: [45, 60, 0, 30, 90, 120, 15]
"""

# 1. What goes in?
#    - daily_minutes: a list of integers, one per day, = minutes studied.
#    - goal_minutes:  an integer, the daily target I want to reach.
#
# 2. What happens to it?
#    The function walks through the days in order and counts how many days
#    IN A ROW reached the goal. Each time a day misses the goal, the current
#    streak resets to 0. It keeps the best streak seen so far.
#    (An average tells me "how much"; a streak tells me "how regular" -
#    and regularity is what actually builds a study habit.)
#
# 3. What comes out?
#    One integer: the length of the longest streak of consecutive days
#    where minutes studied >= goal_minutes.
#
# 4. What is it called?
#    longest_goal_streak(daily_minutes, goal_minutes)
#    Yes: reading the name alone you know it returns the "longest streak"
#    of days that met a "goal". No need to open the code.
#
# ---------------------------------------------------------------------------
# WHY RETURN AND NOT PRINT?
# ---------------------------------------------------------------------------
# print() only SHOWS a value on the screen, then the value is gone: the
# function itself gives back None. Nothing else in the program can use it.
# return HANDS the value back to the caller, so the result can be:
#   - stored in a variable,
#   - compared (e.g. "is this week's streak better than last week's?"),
#   - passed to another function, tested with assert, saved to a file...
# A function that prints decides FOR the caller what to do with the result.
# A function that returns lets the caller decide. That makes it reusable.
# Proof: see the "return vs print" demo at the bottom of this file.
# ---------------------------------------------------------------------------


# ---- The function ---------------------------------------------------------
def longest_goal_streak(daily_minutes, goal_minutes):
    """Return the longest number of consecutive days with minutes >= goal."""
    best_streak = 0      # best streak found so far
    current_streak = 0   # streak we are currently counting

    for minutes in daily_minutes:
        if minutes >= goal_minutes:
            # Goal reached: the streak continues
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            # Goal missed: the streak is broken, start again from zero
            current_streak = 0

    return best_streak   # RETURN the result, never print it here


# ---- My data from exercise 4.0 --------------------------------------------
study_minutes = [45, 60, 0, 30, 90, 120, 15, 60, 75, 80, 50, 10, 0, 95]


# ---- Three calls with different inputs ------------------------------------
# Call 1: same data, an easy goal (30 min/day)
easy_streak = longest_goal_streak(study_minutes, 30)

# Call 2: same data, an ambitious goal (60 min/day)
hard_streak = longest_goal_streak(study_minutes, 60)

# Call 3: a different list (an exam week) with a 60 min/day goal
exam_week = [120, 90, 60, 75, 100, 30, 150]
exam_streak = longest_goal_streak(exam_week, 60)


# ---- Display the three results --------------------------------------------
# Printing happens HERE, outside the function: the caller decides how to show it.
print(f"Longest streak at >= 30 min/day : {easy_streak} days")
print(f"Longest streak at >= 60 min/day : {hard_streak} days")
print(f"Exam week streak at >= 60 min   : {exam_streak} days")


# ---- Bonus: using the returned values (impossible with print) -------------
# Because the function RETURNS numbers, I can compare and compute with them.
if exam_streak > hard_streak:
    gain = exam_streak - hard_streak
    print(f"Exam week beat my usual record by {gain} day(s)!")


# ---- Demo: return vs print ------------------------------------------------
def longest_goal_streak_printing(daily_minutes, goal_minutes):
    """Bad version on purpose: prints instead of returning."""
    print(longest_goal_streak(daily_minutes, goal_minutes))

value = longest_goal_streak_printing(study_minutes, 30)   # shows 4 on screen...
print("Value received from the printing version:", value)  # ...but value is None
# -> 'value' is None: the number was shown but lost. I could not compare it,
#    add it, or test it. That is exactly why the function must RETURN.


# ---------------------------------------------------------------------------
# CHECK IT YOURSELF: empty list
# ---------------------------------------------------------------------------
empty_result = longest_goal_streak([], 60)
print(f"Empty list -> {empty_result}")
# What happens: no crash. The loop never runs, so the function returns 0.
# Is it acceptable? YES. With no days recorded, there is no streak at all,
# so 0 is the honest answer. (An average function would crash here with
# ZeroDivisionError - one more reason I chose a streak over an average.)
assert empty_result == 0