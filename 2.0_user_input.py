"""Exercise 2.0 — Asking the user

WHAT THE PROGRAM MUST DO
    Ask the user for two pieces of information, then display a sentence that uses both.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two pieces of information did you choose, and for what purpose?
       Imagine a real form in your future job. Not "name and age" unless you can
       say what you would do with them.

WHAT THE AI CANNOT KNOW
    Your two fields, and the sentence you want at the end. Decide both before you ask.

    One of your two values will almost certainly need to be a number. Find out what
    happens when you try to add 1 to something the user typed, and deal with it.

CHECK IT YOURSELF
    Run your program and answer with an empty line. Then with a space. Then with text
    where you expected a number. Write in a comment what happened each time.
    You are not asked to fix it yet, only to see it.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: The user enters a stock name and the number of shares they own.
# 2. Process: The program changes the share quantity into an integer and
#    multiplies it by an example share price of 75 euros.
# 3. One sentence shows the stock name, the number of shares,
#    and the estimated value of the position.
# 4. I chose the stock name and the number of shares because I want to
#    understand how investors calculate the value of a stock position.
#    This could be useful in my future job in asset management.


# Your code below

# First, I ask which stock the user owns.
stock_name = input("Enter the stock name: ")

# Next, I ask for the number of shares and turn the answer into a number.
shares = int(input("How many shares do you own? "))

# I use a made-up share price to calculate the position's value.
example_share_price = 75
position_value = shares * example_share_price

# Finally, I put both answers and the calculated value into one sentence.
print(
    f"Your {stock_name} position contains {shares} shares "
    f"and has an estimated value of {position_value:.2f} euros "
    f"at an example price of {example_share_price} euros per share."
)

# CHECK YOURSELF
# Empty line for the number of shares: ValueError: 
#   invalid literal for int() with base 10: ''
# One space for the number of shares: 
#   ValueError: invalid literal for int() with base 10: ' '
# Text such as 'abc' for the number of shares: 
#   ValueError: invalid literal for int() with base 10: 'abc'
# If the stock name is empty but the share quantity is valid, 
#   the program still prints a sentence with an empty name ("Your ...").
# Amount (12) + 1 without int(), TypeError: can only concatenate str (not "int") to str.