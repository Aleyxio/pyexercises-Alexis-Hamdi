"""Exercise 8.1 — Bitwise operators (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Represent a set of permissions as bits, combine two of them, test whether a third is
    present, then add it and remove one.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What are your permissions about? Not files: invent a set from your own field,
       such as who may view, edit and publish a campaign.

WHAT THE AI CANNOT KNOW
    Your permission set and what each one means in your context.

CHECK IT YOURSELF
    Display the value in binary at each step and read the bits yourself.

DELIVERABLE
    This file, with your comments and your code.
"""

# Your code below

# 1. What goes in?
#    My program uses three permissions represented by numbers.
#    Each number represents a different action in Asset Management.
#    I use 1 for viewing, 2 for editing and 4 for approving trades.

# 2. What happens to it?
#    First, I combine two permissions using the OR operator.
#    Then, I check if the third permission is already included.
#    After that, I add the third permission and remove another one.
#    I use bitwise operators to change these permissions.

# 3. What comes out?
#    My program displays the permissions as binary numbers.
#    It also shows if a specific permission is True or False.
#    This helps me understand how each permission changes.

# 4. What are my permissions about?
#    I decided to use permissions related to Asset Management.
#    VIEW_PORTFOLIO allows an analyst to see portfolio investments.
#    EDIT_ALLOCATION allows an analyst to change the portfolio allocation.
#    APPROVE_TRADE allows an analyst to approve an investment transaction.
#    I think this example is useful because permissions are important
#    when different employees have different responsibilities.

# MY THREE PERMISSIONS

# I give each permission a different binary value.
# Each permission uses one specific bit.

VIEW_PORTFOLIO = 1
EDIT_ALLOCATION = 2
APPROVE_TRADE = 4


# DISPLAY THE ORIGINAL PERMISSIONS

# I display the three permissions in binary.
# I use 03b to show each value with three binary digits.

print("MY ASSET MANAGEMENT PERMISSIONS")
print("--------------------------------")

print(f"View portfolio:   {VIEW_PORTFOLIO:03b}")
print(f"Edit allocation:  {EDIT_ALLOCATION:03b}")
print(f"Approve trade:    {APPROVE_TRADE:03b}")


# STEP 1 - COMBINE TWO PERMISSIONS

# I combine viewing and editing permissions.
# I use the bitwise OR operator | to activate both permissions.

permissions = VIEW_PORTFOLIO | EDIT_ALLOCATION

print()
print("STEP 1 - COMBINE PERMISSIONS")
print(f"Combined permissions: {permissions:03b}")


# STEP 2 - CHECK THE THIRD PERMISSION

# I want to know if the analyst can already approve trades.
# I use the bitwise AND operator & to check this permission.

can_approve = (permissions & APPROVE_TRADE) == APPROVE_TRADE

print()
print("STEP 2 - CHECK PERMISSION")
print(f"Can approve trades: {can_approve}")


# STEP 3 - ADD THE THIRD PERMISSION

# I decide to give the analyst permission to approve trades.
# I use OR again to add this permission without removing the others.

permissions = permissions | APPROVE_TRADE

print()
print("STEP 3 - ADD PERMISSION")
print(f"New permissions: {permissions:03b}")

# I check if the new permission is now active.
can_approve = (permissions & APPROVE_TRADE) == APPROVE_TRADE

print(f"Can approve trades now: {can_approve}")


# STEP 4 - REMOVE ONE PERMISSION

# I decide to remove the permission to edit portfolio allocation.
# I use AND with NOT to turn off only this permission.
# The other permissions should stay active.

permissions = permissions & ~EDIT_ALLOCATION

print()
print("STEP 4 - REMOVE PERMISSION")
print(f"Final permissions: {permissions:03b}")

# FINAL RESULTS

# I display the final status of each permission.
# I want to understand which actions are still allowed.

can_view = (permissions & VIEW_PORTFOLIO) == VIEW_PORTFOLIO
can_edit = (permissions & EDIT_ALLOCATION) == EDIT_ALLOCATION
can_approve = (permissions & APPROVE_TRADE) == APPROVE_TRADE

print()
print("FINAL PERMISSIONS")
print("----------------------------")

print(f"View portfolio: {can_view}")
print(f"Edit allocation: {can_edit}")
print(f"Approve trades: {can_approve}")

# FINAL MESSAGE

# My program shows how permissions can be stored using bits.
# I learned that OR adds permissions and AND checks them.
# I also understand that AND with NOT can remove a permission
# without changing the other permissions.

print()
print("My permission system is complete!")

# CHECK IT YOURSELF

# I decided to check the binary values of my permissions step by step.
# I want to make sure that each bitwise operator works correctly.

# First, I combined VIEW_PORTFOLIO (001) and EDIT_ALLOCATION (010).
# I expected to get 011 because both permissions should be active.
# I checked the binary result and it matches my calculation.

# Then, I checked if APPROVE_TRADE (100) was already included.
# I expected False because the third bit was not active in 011.

# After that, I added APPROVE_TRADE using the OR operator.
# I expected to get 111 because all three permissions are now active.

# Finally, I removed EDIT_ALLOCATION using AND with NOT.
# I expected 101 because I only wanted to remove the middle bit.
# This means I can still view portfolios and approve trades.

# I compared the binary results with my manual predictions.
# The results match the expected values: 011, 111 and 101.

# I think this exercise helped me understand how bitwise operators work.
# I learned that OR can add permissions, AND can check them,
# and AND with NOT can remove one without changing the others.