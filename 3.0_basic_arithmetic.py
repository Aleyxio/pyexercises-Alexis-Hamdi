"""Exercise 3.0 — Computing with what the user typed

WHAT THE PROGRAM MUST DO
    Ask for two numbers and display the result of the four operations.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What should your program do when the second number is zero? Decide, write your
       decision down, and only then implement it.

WHAT THE AI CANNOT KNOW
    Your answer to question 4. There are at least three defensible ones: refuse the
    value and ask again, display a message instead of a result, or stop the program.
    Pick one and be able to defend it.

CHECK IT YOURSELF
    Compute 7 divided by 2 in your head. Run your program with 7 and 2. If your program
    shows 3, it is not wrong by accident: find out why, and write the reason in a comment.
    Then run it with 0 as the second number.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: the user enters two investment amounts.
# 2. Process: the program calculates four basic operations: +, -, * and /.
# 3. Out: the four results are displayed in the terminal, per operation.
# 4. If the second number is zero, it displays a message: 
#    "division: Cannot divide by zero.", instead of crashing.
#    I chose this solution because the user can still see the other three results 
#    without the program crashing.

# Your code below
# I ask the user to enter two amounts.
a = float(input("First investment amount: "))
b = float(input("Second investment amount: "))

# I calculate and display the four operations.
print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")

# I check if division is possible.
if b != 0:
    print(f"Division: {a / b}")
else:
    print("Division: Cannot divide by zero.")

# CHECK YOURSELF
# With 7 and 2, division gives 3.5 because / is normal division.
# The // operator would give 3 because it uses floor division.
# With 7 and 0, the program displays "Division: Cannot divide by zero.",
#   instead of crashing.