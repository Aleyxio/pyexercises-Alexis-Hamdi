"""Exercise 2.1 — Transforming text (homework)

WHAT THE PROGRAM MUST DO
    Ask the user for a sentence, then display four different transformations of it.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which four transformations did you choose, and in what situation would each of
       them be useful? One line each.

WHAT THE AI CANNOT KNOW
    Your four transformations. Pick them yourself. Open ../examples/strings/string_methods.py
    to see what is available, then choose, then justify.

    A transformation that produces the same thing as another one does not count as two.

CHECK IT YOURSELF
    Run it with a sentence that has spaces at both ends and a capital in the middle.
    For each of your four results, say in a comment whether it is what you expected.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: asked the user to write a sentence.
# 2. Process: used four methods to change the sentence: 
#    strip(), lower(), swapcase(), and replace().
# 3. Out: four different results, 4 different lines, each with the transformation.
# 4. My four transformations, and when each is useful: 
#    strip(): I use it to remove spaces that I don't need.
#    lower(): I use it to make the text easier to read and compare.
#    swapcase(): I chose it to see how capital letters can change.
#    replace(): I use it when I need to change a meeting location from London to Tokyo.

# Your code below

# First, I ask the user to write a sentence.
sentence = input("Write a sentence: ")

# I use strip() to remove extra spaces at the beginning and end.
# I use lower() to change all letters into lowercase.
# I use swapcase() to change uppercase letters into lowercase and the opposite.
# I use replace() to change "London" into "Tokyo" in the sentence.
print(sentence.strip())
print(sentence.lower())
print(sentence.swapcase())
print(sentence.replace("London", "Tokyo"))
# Finally, I display the four different results.

# CHECK YOURSELF
# sentence test: " hi i am From London "
# Strip:     (hi i am From London)
# Lower:     ( hi i am from london )
# Swapcase:  ( HI I AM fROM lONDON )
# Replace:   ( hi i am From Tokyo )

# Strip(): is as expected because it removed the spaces 
#   at both ends but kept the sentence.
# Lower(): is as expected because all capital letters became lowercase 
#   while spaces stayed.
# Swapcase(): is as expected because uppercase letters became lowercase 
#   and lowercase became uppercase.
# Replace(): is as expected because London changed to Tokyo 
#   while the rest of the sentence stayed the same.