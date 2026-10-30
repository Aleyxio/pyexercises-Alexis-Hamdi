"""Exercise 4.1 — Reordering without losing the original (homework)

WHAT THE PROGRAM MUST DO
    Starting from the list you built in exercise 4.0, display it in four different
    orders, and prove at the end that the original list has not been damaged.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which four orders did you choose, and in which of them is your original list
       modified rather than copied?

WHAT THE AI CANNOT KNOW
    That your original must survive. Some ways of reordering a list change it in place,
    others return a new one. Find out which is which, and say so in your comments.
    That distinction is the entire exercise.

CHECK IT YOURSELF
    The last line of your program must display the original list. Compare it, item by
    item, with what you wrote in 4.0. If it has moved, your program is wrong even
    though it ran.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In: the list of eight monthly ETF investments in euros, list from exercise 4.0.
# 2. Process: The program displays the investments in four different orders: 
#   reversed list, ascending order, descending order and starting from April.
# 3. Out: The reversed list, ascending order, descending order, starting from April 
#   then the original list at the last line (4 lines of orders and 1 original line).
# 4. My four orders, and which ones modify the original:
#   The ascending and descending orders, the reversed list and the starting from April, 
#   none of them changes the original list because I use sorted() and slicing.
#   I used sorted() and slicing because they create new lists
#   without changing my original investments.
#   I avoided sort() and reverse() because they modify the
#   original list directly, which I want to keep for future use.

# Your code below

# I create my original list of ETF investments.
investments = [120, 180, 150, 200, 220, 170, 250, 210]

# I display the investments in four different orders.
print("Reversed list:", investments[::-1])
print("Ascending order:", sorted(investments))
print("Descending order:", sorted(investments, reverse=True))
print("Starting from April:", investments[3:] + investments[:3])

# I check that my original list has not changed.
print("Original list after sorting:", investments)

# CHECK YOURSELF
# The reversed list shows the investments from last to first.
# The ascending list goes from the smallest to the largest amount.
# The descending list goes from the largest to the smallest amount.
# The April-first list starts from April to August, 
#   then continues from January to March.
# The final list is identical to the original one (4.0).
# [120, 180, 150, 200, 220, 170, 250, 210]
# This confirms that none of the operations changed my original data.