"""Exercise 3.1 — Odd or even (homework)

WHAT THE PROGRAM MUST DO
    Ask the user for a number N, then say for every number from 1 to N whether it is
    odd or even.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What should happen if the user types 0, a negative number, or 5000?
       Decide the three behaviours before writing anything.

WHAT THE AI CANNOT KNOW
    Your three decisions. An assistant asked for "odd or even from 1 to N" will produce
    a program that behaves absurdly on 0 and on -4, and will happily print five thousand
    lines. Those are your calls, not its.

CHECK IT YOURSELF
    Run it with 6. You should see three odd and three even. Count them.
    Then run it with your three edge cases and confirm each does what you decided.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: the user enters the number of transactions to check (N).
# 2. Process: the program checks each number from 1 to N
#    and uses % 2 to see if it is odd or even.
# 3. Out: each transaction is assigned to odd or even 
#    and is counted from Transaction 1 to Transaction N.
# 4. For 0, I display a message because there are no transactions to check.
#    For negative numbers, there's a message: "Please enter a positive number".
#    a warning because a number of transactions cannot be negative.
#    For 5000, I display a warning because too many results are hard to read.
#    The program is limited to 100 transactions, if > 100, then a message like:
#    "Too many transactions. Maximum is 100."
#    I chose a limit of 100 to keep the results short and easy to read.

# Your code below

# First, I ask how many transactions the user wants to check.
n = int(input("Enter the number of transactions: "))

# I check if the number is valid.
if n == 0:
    print("No transactions to check.")
elif n < 0:
    print("Please enter a positive number.")
elif n > 100:
    print("Too many transactions. Maximum is 100.")
else:
    # Checked each transaction.
    for i in range(1, n + 1):
        if i % 2 == 0:
            print(f"Transaction {i}: Even")
        else:
            print(f"Transaction {i}: Odd")

# CHECK YOURSELF
# With 6, I got 3 odd (1, 3, 5) and 3 (2, 4, 6) even transactions, as expected.
# With 0, the program displayed a message: "No transactions to check.",
# because there was nothing to check.
# With -4, the program displayed a message asking for a positive number.
# message: "Please enter a positive number."
# With 5000, the program displayed a warning because the limit is 100,
# the message is: "Too many transactions. Maximum is 100."