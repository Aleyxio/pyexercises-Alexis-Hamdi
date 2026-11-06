"""Exercise 9.0 — Surviving what you did not expect

Useful for the final exam: two campaigns in the exam dataset have zero conversions.

WHAT THE PROGRAM MUST DO
    Ask the user for a number, divide something by it, and keep running whatever the
    user types. Never crash.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two different failures can happen here, and should they produce the same
       message to the user? Decide before coding.

WHAT THE AI CANNOT KNOW
    Your answer to question 4, and how many attempts you allow before giving up.

    An assistant will often propose catching every error at once. Find out why catching
    each failure separately is better, and write the reason in a comment.

CHECK IT YOURSELF
    Run it with: a normal number, then zero, then the word "abc", then an empty line.
    Four runs, four behaviours, all described in a comment. If any of them stopped your
    program, it is not finished.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In:
#    My program asks the user to enter the number of conversions.
#    I use a campaign with an advertising spend of 1200 euros.
#    The user can enter a number, zero or an invalid value.
# 2. Process:
#    First, I try to convert the user's answer into an integer.
#    Then, I divide the advertising spend by the conversions.
#    If an error happens, I display a message and allow another attempt.
#    I decided to give the user a maximum of 5 attempts.
# 3. Out:
#    If the number is valid, my program displays the CPA in euros.
#    If the input is incorrect, the program explains the problem.
#    The program should finish without crashing.
# 4. The two failures, and whether they deserve the same message:
#    The first error is ValueError when the user enters text instead of a number.
#    The second error is ZeroDivisionError when the user enters zero.
#    I decided to use different messages because these errors are not the same.
#    This helps the user understand what needs to be corrected.

# WHY DO I USE TWO EXCEPT BLOCKS?
# I think catching errors separately is more useful.
# ValueError means Python cannot convert the user's answer.
# ZeroDivisionError means Python cannot divide by zero.
# With different messages, I can explain each problem more clearly.

# Your code below

# MY CAMPAIGN DATA

# I use an example of 1200 euros spent on a marketing campaign.
spend = 1200

# I allow a maximum of 5 attempts before stopping the program.
max_attempts = 5
attempts = 0

# I use this variable to check if the calculation was successful.
success = False


# ASK THE USER FOR A NUMBER

# I use a while loop because I want to allow several attempts.
while attempts < max_attempts:

    # I count each attempt made by the user.
    attempts += 1

    try:
        # I ask for the number of conversions.
        conversions = int(input("Enter the number of conversions: "))

        # I do not accept negative conversions.
        if conversions < 0:
            print("Conversions cannot be negative. Please try again.")
            continue

        # I calculate the CPA by dividing spend by conversions.
        cpa = spend / conversions

    except ValueError:
        # This error happens if the user enters "abc" or an empty answer.
        print("Invalid input. Please enter a whole number.")

    except ZeroDivisionError:
        # This error happens if the number of conversions is zero.
        print("Division by zero is impossible. CPA is not available.")

    except (EOFError, KeyboardInterrupt):
        # I also handle the user closing or cancelling the input.
        print("\nInput cancelled. The program will stop safely.")
        break

    else:
        # If there is no error, I display the CPA with two decimals.
        print(f"CPA: {cpa:.2f} euros")

        # I confirm that my calculation was successful.
        success = True

        # I stop the loop because I already have my result.
        break


# FINAL RESULT

# If the user reaches the limit, I stop without crashing.
if not success and attempts >= max_attempts:
    print("Maximum attempts reached. No CPA was calculated.")

# I display a final message to confirm the program has finished.
print("My program finished without crashing!")

# CHECK IT YOURSELF

# I decided to test my program with four different inputs.
# I want to make sure that my program handles errors without crashing.

# Test 1 - Normal number
# First, I entered 20 conversions.
# I expected a CPA of 60 euros because 1200 / 20 = 60.
# The program should display the correct result without any error.

# Test 2 - Zero conversions
# Then, I entered 0 conversions.
# I expected a ZeroDivisionError to be handled by my except block.
# The program should explain that the CPA cannot be calculated.
# It should also allow me to try again.

# Test 3 - Invalid text
# For my third test, I entered "abc" instead of a number.
# I expected Python to detect a ValueError.
# The program should display an error message and ask for another number.

# Test 4 - Empty input
# Finally, I pressed Enter without writing anything.
# I expected another ValueError because an empty string is not an integer.
# The program should continue running and allow another attempt.

# My final verification
# I want to check that all four situations are handled correctly.
# I also decided to limit the user to 5 attempts.
# After 5 unsuccessful attempts, the program should stop safely.

# I think using two different except blocks is important because
# an invalid number and a division by zero are different problems.
# This exercise helps me understand how to make my Python code
# more reliable and easier for the user to understand.