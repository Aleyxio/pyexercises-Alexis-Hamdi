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
# 2. Process, function by function:
# 3. Out:
# 4. The question my fourth function answers:


# Your code below

"""Exercise 6.1 - Small functions working together

Data (from exercise 4.0): a list of how many minutes I studied each day,
starting on a Monday. 21 days = 3 weeks.
"""

# ---------------------------------------------------------------------------
# ANSWERS TO THE QUESTIONS (decided on paper before writing any code)
# ---------------------------------------------------------------------------
# 1. What goes in?
#    A list of integers: minutes studied per day, in date order,
#    the first value being a Monday.
#
# 2. What happens to it? (which function does what, in order)
#    a) split_into_weeks   -> cuts the daily list into chunks of 7 days.
#    b) total_minutes      -> adds up the minutes of ONE week.
#    c) position_of_largest -> finds where the biggest number is in a list.
#    d) best_study_week    -> uses a), then b) on every week, then c) on the
#                             weekly totals, and turns the position into a
#                             human week number (1, 2, 3... not 0, 1, 2).
#
# 3. What comes out?
#    An integer: the number of the week in which I studied the most
#    (week 1 = first week). None if there is no data at all.
#
# 4. What question does the fourth function answer, and why split it?
#    Question: "Which week did I study the most?"
#    Splitting helps because each small piece can be checked alone with a
#    tiny input I can compute in my head. If the final answer is wrong, I
#    test the three pieces and the broken one shows itself immediately,
#    instead of hunting through one long function. The pieces are also
#    reusable: total_minutes and position_of_largest work on ANY list.
#
# ONE FUNCTION, ONE JOB - each described in one sentence, without "and":
#    split_into_weeks     : "Cuts a list of days into 7-day weeks."
#    total_minutes        : "Adds up the minutes of one week."
#    position_of_largest  : "Gives the position of the biggest value."
#    best_study_week      : "Tells which week had the most study time."
# ---------------------------------------------------------------------------


# ---- Small function 1: one job = cut the list into weeks ------------------
def split_into_weeks(daily_minutes):
    """Return a list of weeks, each week being a list of up to 7 days."""
    weeks = []
    # Jump 7 days at a time; each slice [start : start + 7] is one week.
    # The last week may be shorter if the data stops mid-week.
    for start in range(0, len(daily_minutes), 7):
        weeks.append(daily_minutes[start:start + 7])
    return weeks


# ---- Small function 2: one job = total of one week ------------------------
def total_minutes(week):
    """Return the sum of the minutes in one week."""
    total = 0
    for minutes in week:
        total += minutes
    return total


# ---- Small function 3: one job = where is the biggest value? --------------
def position_of_largest(values):
    """Return the index of the largest value, or None if the list is empty."""
    if not values:          # nothing to compare -> no answer
        return None
    best_index = 0
    for index in range(1, len(values)):
        if values[index] > values[best_index]:
            best_index = index
    return best_index       # on a tie, the FIRST (earliest) one wins


# ---- Fourth function: the three pieces working together -------------------
def best_study_week(daily_minutes):
    """Return the week number (starting at 1) with the most study time."""
    weeks = split_into_weeks(daily_minutes)                  # step a
    weekly_totals = [total_minutes(week) for week in weeks]  # step b
    index = position_of_largest(weekly_totals)               # step c
    if index is None:                                        # no data
        return None
    return index + 1        # humans count weeks from 1, Python from 0


# ---------------------------------------------------------------------------
# CHECK IT YOURSELF: test each small function ON ITS OWN first
# (inputs small enough to compute the expected output by hand)
# ---------------------------------------------------------------------------
# Test 1 - split_into_weeks
#   input    : [1, 2, 3, 4, 5, 6, 7, 8, 9]
#   expected : [[1, 2, 3, 4, 5, 6, 7], [8, 9]]   (9 days = 1 full week + 2 days)
assert split_into_weeks([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [[1, 2, 3, 4, 5, 6, 7], [8, 9]]

# Test 2 - total_minutes
#   input    : [10, 20, 30]
#   expected : 60
assert total_minutes([10, 20, 30]) == 60

# Test 3 - position_of_largest
#   input    : [300, 450, 200]
#   expected : 1   (450 is at index 1)
assert position_of_largest([300, 450, 200]) == 1

print("All 3 small-function tests passed.")


# ---- My data from exercise 4.0 --------------------------------------------
study_minutes = [
    45, 60, 0, 30, 90, 120, 15,     # week 1
    60, 75, 80, 50, 10, 0, 95,      # week 2
    120, 90, 60, 75, 100, 30, 150,  # week 3 (exam week)
]


# ---- Use the fourth function and display the answer -----------------------
best_week = best_study_week(study_minutes)

# Show the weekly totals too, so the answer can be checked by eye.
for number, week in enumerate(split_into_weeks(study_minutes), start=1):
    hours = total_minutes(week) / 60
    bar = "#" * round(hours)            # tiny text bar chart: 1 # = 1 hour
    print(f"Week {number}: {total_minutes(week):4d} min  {bar}")

print(f"Best study week: week {best_week}")


# ---- Edge case: empty list -------------------------------------------------
# No days -> no weeks -> no totals -> position_of_largest returns None.
# best_study_week passes that None on instead of crashing. Acceptable:
# with no data there is no "best week", and None says exactly that.
print(f"Empty list -> {best_study_week([])}")
assert best_study_week([]) is None