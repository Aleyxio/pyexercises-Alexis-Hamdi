"""Exercise 7.1 — Loading a file, cleaning it, saving the result (homework)

This is the direct rehearsal for the final exam. Session 8 starts with it.

WHAT THE PROGRAM MUST DO
    Load names.txt, clean what is inside, sort it by last name, and write the result to
    a new file. The original file must not be modified.

DO THIS BEFORE ANYTHING ELSE
    Open names.txt and read it with your eyes. Then write, in comments at the top of
    your file, everything that is wrong with it. There are at least four different
    problems. Find them yourself.

    This step is not optional and it is graded. An assistant cannot see your file.

ANSWER THESE, in comments, after the list of problems
    1. What goes in?
    2. What happens to it?  (one line per problem you found, and how you deal with it)
    3. What comes out?
    4. What does "sort by last name" mean when a line contains two words, and how do you
       know which one is the last name?

WHAT THE AI CANNOT KNOW
    The actual content of names.txt. If you paste this brief into an assistant without
    describing the file, it will write a program for a clean file, and that program will
    crash or produce nonsense on the real one.

    Describe the file to it. That description is the exercise.

CHECK IT YOURSELF
    Count the lines in names.txt, then in your output file. The numbers should differ,
    and you should be able to say exactly why. Then check the first and last name of
    your sorted list by hand.

DELIVERABLE
    This file, plus the output file your program produced.
"""

# What is wrong with names.txt (found by reading it, not by guessing):
# 1. There are two empty lines, and I do not want them in the result.
# 2. Some names have extra spaces at the beginning, like alan and linus.
# 3. Capital letters are not consistent, for example ada LOVELACE and GUIDO.
# 4. Guido van Rossum has a last name with two words. I need to keep them together.

# 1. In:
#    My program reads names.txt, which contains one person's name per line.
# 2. Process, problem by problem:
#    First, I remove empty lines and extra spaces.
#    Then, I correct the capital letters while keeping "van" in lowercase.
#    I keep the first word as the first name and the rest as the last name.
#    Finally, I sort the names alphabetically by last name.
# 3. Out:
#    I create names_cleaned_sorted.txt with one cleaned name per line.
#    I do not change names.txt.
# 4. How I decide which word is the last name:
#    I compare family names, not first names. For example, Hopper comes before Turing.
#    I treat "van Rossum" as Guido's last name, not only "Rossum".
#    With this file, I use the first word as the first name and all other words as the last name.


# Your code below

from pathlib import Path


# I use the folder of my Python file to find the input and output files.
folder = Path(__file__).parent
input_file = folder / "names.txt"
output_file = folder / "names_cleaned_sorted.txt"


# I read the original names without changing the file.
with input_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()


cleaned_names = []


# I check each line, then clean it before adding it to my list.
for line in lines:
    words = line.split()

    # I skip empty lines or lines without a full name.
    if len(words) < 2:
        continue

    # I correct the first name.
    first_name = words[0].capitalize()

    # I use all the remaining words for the last name.
    last_name_words = []

    for word in words[1:]:
        if word.lower() == "van":
            last_name_words.append("van")
        else:
            last_name_words.append(word.capitalize())

    last_name = " ".join(last_name_words)
    full_name = first_name + " " + last_name

    # I keep the last name with the full name to make sorting easier.
    cleaned_names.append((last_name.lower(), full_name))


# I sort the names using their last names, not their first names.
cleaned_names.sort()


# I write the cleaned names into a NEW file, one name per line.
with output_file.open("w", encoding="utf-8") as file:
    for last_name, full_name in cleaned_names:
        file.write(full_name + "\n")


# I display a short summary so I can see what my program did.
print(f"Original lines: {len(lines)}")
print(f"Names saved: {len(cleaned_names)}")
print(f"Lines removed: {len(lines) - len(cleaned_names)}")
print(f"Output file: {output_file.name}")

# CHECK IT YOURSELF

# I decided to compare my original file with my cleaned file.
# My original names.txt contains 10 lines, including 2 empty lines.
# After cleaning, my new file contains 8 names.

# The difference comes from the 2 empty lines that I removed.
# I also corrected the capital letters and removed extra spaces.
# I kept the original file unchanged.

# I checked the first and last names of my sorted list manually.
# The first name is Margaret Hamilton because H comes before the other last names.
# The last name is Guido van Rossum because V comes after the other last names.

# I think my program works correctly because the number of lines is correct.
# The names are also sorted alphabetically by last name.
# This test helped me verify my results and understand my code better.