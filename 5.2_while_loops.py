"""Exercise 5.2 — Repeating until something changes

WHAT THE PROGRAM MUST DO
    Keep asking the user something until a condition you define is met, then display a
    summary of what happened during the loop.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What is your stop condition, what is your maximum number of attempts, and what
       does your summary contain?

WHAT THE AI CANNOT KNOW
    Your stop condition and your safety limit. An assistant asked for a while loop will
    write one that can run for ever if the user never gives the expected answer. Decide
    how many attempts you allow, and what your program does when that limit is reached.

    Accepting "Yes", "yes" and " yes " as the same answer is your decision too. Make it
    and write it down.

CHECK IT YOURSELF
    Run it and never give the expected answer. If your program is still running after
    your stated maximum, it is wrong. Then run it and answer with capitals and extra
    spaces.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: user answers a question and has 3 attempts: 
#    Have you reviewed your ETF portfolio?
# 2. Process: the program keeps asking until the user answers "yes" 
#    or reaches the maximum number of attempts. Using strip()and lower().
# 3. Out: a summary showing the number of attempts and whether the review was confirmed.
# 4. My stop condition, my attempt limit, my summary:
#    I chose "yes" as my stop condition and a maximum of 3 attempts.
#    I think 3 attempts are enough to avoid an infinite loop.
#    I also accept capital letters and extra spaces to make it easier for the user.
#    My summary shows how many attempts were needed and the final result.

# Your code below

# I start with zero attempts and no confirmation.
attempts = 0
confirmed = False

# I repeat the question until the review is confirmed or after 3 attempts.
while attempts < 3 and not confirmed:
    answer = input("Have you reviewed your ETF portfolio? (yes/no): ").strip().lower()
    attempts += 1

    if answer == "yes":
        confirmed = True

# Finally, I display a summary of the results.
print(f"Total attempts: {attempts}")

if confirmed:
    print("Portfolio review confirmed!")
else:
    print("Portfolio review not confirmed after 3 attempts.")

# CHECK YOURSELF

# Test 1: I answered "no" three times.
# The program stopped after 3 attempts instead of running forever.
# It displayed a message saying: "Portfolio review not confirmed after 3 attempts".

# Test 2: I answered "  YES  " with capital letters and spaces.
# The program accepted my answer, stopped after 1 attempt and displayed a message:
#   "Portfolio review confirmed!".
# This worked because strip() removes extra spaces
# and lower() changes capital letters into lowercase.

# Both tests gave the expected results.