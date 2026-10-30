"""Exercise 1.0 — Hello World

WHAT THE PROGRAM MUST DO
    Display a message of your choice, five times, with each line numbered.

ANSWER THESE FIRST, in comments at the top of your file, before any code
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What message did you choose, and why that one?

WHAT THE AI CANNOT KNOW
    The message is yours. Choose something you would actually want a program to say,
    not "Hello, World!". Your comment has to justify it.

CHECK IT YOURSELF
    Count the lines your program produced. Five, not four and not six.
    Then change the number to 3 and run it again. If you had to rewrite more than one
    character, your program is not built the way it should be.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: my message, "I love Python" and 5 times it is repeated.
# 2. Process: what does the code do? It repeats the "I love Python" 5 times 
#    and it adds something in front of the sentence (a number).
#    Range, through the start of 1 and stop of 6 (or whatever number) at the stop 
#    this count just before stop.
# 3. Out: printing 5 lines, each one starting with a number (1 to 5)
#    followed by "I love Python" (5 times).
# 4. My message, and why:
#    I have printed "I love Python", 
#    Because I never did this in my life.
#    I really believe that we can create something helpful 
#    and truly unbelievable with Python. There's so much to learn!

# Your code below
# The first line counts from 1 and stops before 6 (so the last number is 5).
# The second line prints, for each number, the number followed by "I love Python".
for number in range(1, 6):
    print(f"{number}. I love Python")

# Check: with range(1, 6) I got the 5 lines I wanted, each one with its
# number and the same sentence. When I changed the 6 into a 4, I got 3 lines.
# This shows that I only need to change one character to get as many lines
# as I want, with one simple modification.