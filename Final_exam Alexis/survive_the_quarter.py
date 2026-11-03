# Name: Alexis Hamdi  -  Group number: A  -  Scenario file: A
#
# 1. What goes in?
#    I use scenarios_A.csv. The file uses commas to separate the columns, and
#    some texts are in quotes because they also have commas inside.
#    There are 14 columns: an ID, the scenario, 3 choices (OptionA/B/C),
#    the money changes (BudgetA/B/C), the reputation changes
#    (ReputationA/B/C), and the feedback for each choice (FeedbackA/B/C).
#    The numbers are integers. For example, -800 means I lose 800 EUR.
#    If I choose B, I take BudgetB and ReputationB from the same scenario.
#    The teacher's file has 30 scenarios, and I added my own 3 scenarios at
#    the end, numbered 31, 32 and 33, in the same format as the others:
#    a heatwave that melts the croissants, a football club sponsorship, and
#    drones writing the brand name in the sky without permission.
#
# 2. What happens during one day?
#    First I show the day, the budget, the reputation and the situation.
#    Then the player sees choices A, B and C and chooses one.
#    I ask again if the letter is not valid. After that, I update the two
#    gauges, show the feedback and keep the choice in a history list.
#    If the budget or reputation reaches zero or less, the player is fired
#    at once. Otherwise, I check if the player can receive the streak bonus.
#
# 3. What comes out?
#    The player sees if they survived or got fired, and why.
#    If they survive, I calculate a score with reputation + budget // 200
#    and give them a title. In both cases, I show a recap of the days played
#    and the best and worst choices (biggest and smallest reputation change).
#    I also save one line in results.csv with the name, budget, reputation,
#    title and date. Example: Alexis;6350;100;CMO Material;2026-11-03 14:05
#
# 4. What could go wrong?
#    If the player types the wrong letter, I ask the question again.
#    If the budget or reputation reaches zero or less, I end the game at once.
#    If the file is missing, I stop and explain which file is missing.
#    If a row has a missing or incorrect value, I skip it with a warning.
#    If scenarios 31, 32 or 33 are missing, I display a warning too.
#    If the player interrupts the game with Ctrl+C or Ctrl+D, I exit cleanly.
#
# My extra feature: a) Streak bonus.
#    I chose this because I want to reward good decisions over several days.
#    After 3 positive reputation changes in a row, the player wins 500 EUR.
#    It can help the player, but they still need to protect the budget.
#
# To start my game: python survive_the_quarter.py

import csv
import random
import sys
from datetime import datetime
from pathlib import Path

# --- Settings ---
# I put the main values here because it is easier to find them and make
# changes without searching through all the code.
SCENARIO_FILE = "scenarios_A.csv"
RESULTS_FILE = "results.csv"
START_BUDGET = 10000          # I start with 10,000 EUR.
START_REPUTATION = 50         # I start with 50 reputation points.
MAX_REPUTATION = 100          # The reputation cannot be higher than 100.
DAYS = 10                     # The player needs to survive 10 days.
SCORE_DIVIDER = 200           # Every full 200 EUR left adds 1 score point.
STREAK_LENGTH = 3             # I need 3 positive reputation changes in a row.
STREAK_BONUS = 500            # The reward is 500 EUR.
MY_SCENARIO_IDS = ("31", "32", "33")   # The IDs of my 3 personal scenarios.

# These values only show a warning when the player is in danger.
# They do not change the real game-over rule, which is zero or less.
LOW_BUDGET, LOW_REPUTATION = 2000, 20

# I put the titles from the highest score to the lowest one.
# For example, 120 gives CMO Material, but 140 gives Viral Legend.
# The player only receives a title from this list if they survive.
TITLES = [(140, "Viral Legend"), (120, "CMO Material"), (95, "Growth Hacker"), (0, "Eternal Intern")]


# --- Step 1: Read the CSV ---
# I use csv.DictReader() because it lets me read values with column names.
# For A, B and C, I put the text, budget change, reputation change and
# feedback together in a tuple. This makes each option easier to use later.
# int() changes the numbers from CSV text into numbers I can calculate with.
# I keep the ID and situation with the options in my scenarios list.
# If one row is incorrect, I skip that row instead of stopping the game.
def load_scenarios(path):
    scenarios = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        # The first CSV line contains the headings, so data starts at line 2.
        for line, row in enumerate(csv.DictReader(f), start=2):
            try:
                options = {}
                for letter in "ABC":
                    options[letter] = (row[f"Option{letter}"].strip(),
                                       int(row[f"Budget{letter}"]),
                                       int(row[f"Reputation{letter}"]),
                                       row[f"Feedback{letter}"].strip())
                scenarios.append((row["ID"].strip(), row["Scenario"].strip(), options))
            except (KeyError, ValueError, TypeError, AttributeError):
                print(f"Warning: line {line} of {path.name} is invalid - skipped.")
    return scenarios


# The assignment asks me to add scenarios 31, 32 and 33.
# I check their IDs so I can see if I forgot one or if it was invalid.
# This is only a warning: I still have to add them to the real CSV file.
def check_my_scenarios(scenarios):
    loaded_ids = {scenario_id for scenario_id, _, _ in scenarios}
    missing = [i for i in MY_SCENARIO_IDS if i not in loaded_ids]
    if missing:
        print(f"Warning: my own scenarios {missing} are missing or invalid in {SCENARIO_FILE}.")


# --- Step 2: Show the gauges and ask for a choice ---
# I use a small bar made of # and dots to make the gauges easier to read.
# The formula value / maximum * width gives the filled part of the bar.
# round() gives a whole number of characters, and min()/max() keep the
# result between zero and the bar width, even if the budget goes higher.
def gauge_bar(value, maximum, width=20):
    filled = max(0, min(width, round(value / maximum * width)))
    return "#" * filled + "." * (width - filled)


# I show the day number, both gauges and their bars before each decision.
# I also add a warning if the budget or reputation is getting low,
# so the player knows they should be careful with the next choice.
def show_gauges(day, budget, reputation):
    print(f"\n--- Day {day}/{DAYS} ---")
    print(f"[Budget: {budget} EUR | Reputation: {reputation}/{MAX_REPUTATION}]")
    print(f" Budget     {gauge_bar(budget, START_BUDGET)}")
    print(f" Reputation {gauge_bar(reputation, MAX_REPUTATION)}")
    if budget < LOW_BUDGET:
        print(" Warning: the bank is getting nervous, budget is low!")
    if reputation < LOW_REPUTATION:
        print(" Warning: the internet is turning against you, reputation is low!")


# I use a while loop because the player might enter a wrong letter.
# strip() removes spaces and upper() changes a, b or c to capital letters.
# I only return the choice when it is A, B or C.
def ask_choice():
    answer = input("Your choice (A, B or C): ").strip().upper()
    while answer not in ("A", "B", "C"):
        answer = input("Please type A, B or C: ").strip().upper()
    return answer


# I update the budget and reputation based on the selected option.
# New budget = old budget + the money gained or lost with that option.
# New reputation = old reputation + the change from that option.
# I use min() so reputation never goes above 100.
# I return both values as a tuple, so I can use them together in the game.
def apply_choice(budget, reputation, option):
    text, budget_change, reputation_change, feedback = option
    new_budget = budget + budget_change
    new_reputation = min(MAX_REPUTATION, reputation + reputation_change)
    return new_budget, new_reputation


# --- Step 3: Play the 10 days ---
# random.sample() chooses scenarios randomly, without repeating one.
# Normally I play 10 days. If fewer valid scenarios are loaded, this code
# currently plays fewer days, so I still need to check my file has enough.
# I save each day in history as a tuple with the reputation change first.
# This is useful because max() and min() compare the first tuple value
# to find the best and worst reputation changes. If they are equal,
# the day number is used to decide between them.
# This function returns the budget, reputation, history and firing reason.
def play_game(scenarios):
    budget, reputation = START_BUDGET, START_REPUTATION
    history = []
    streak = 0  # I count positive reputation changes in a row here.
    days_played = random.sample(scenarios, min(DAYS, len(scenarios)))

    # For every day, I show the situation, then all three possible choices.
    # start=1 makes the first day Day 1 instead of Day 0.
    for day, (_, situation, options) in enumerate(days_played, start=1):
        show_gauges(day, budget, reputation)
        print(situation)
        for letter, (text, _, _, _) in options.items():
            print(f"  {letter}: {text}")

        # I read the player's choice, take its tuple, and update the gauges.
        # The + in the print format shows if the change is positive or negative.
        # I also keep the choice in history for the final recap.
        letter = ask_choice()
        option = options[letter]
        text, budget_change, reputation_change, feedback = option
        budget, reputation = apply_choice(budget, reputation, option)
        print(feedback)
        print(f"Budget {budget_change:+} EUR, Reputation {reputation_change:+}")
        history.append((reputation_change, day, letter, text, budget_change))

        # I check the two gauges before giving any bonus.
        # If one is zero or negative, the player is fired immediately.
        if budget <= 0:
            return budget, reputation, history, "the budget hit zero, the bank cut you off"
        if reputation <= 0:
            return budget, reputation, history, "the reputation hit zero, the internet won"

        # This is my extra feature. I add 1 to streak after a positive
        # reputation change. Otherwise, I reset it to 0.
        # At 3 gains in a row, I add 500 EUR and start counting again.
        streak = streak + 1 if reputation_change > 0 else 0
        if streak == STREAK_LENGTH:
            budget += STREAK_BONUS
            streak = 0
            print(f"Streak bonus! {STREAK_LENGTH} reputation gains in a row: +{STREAK_BONUS} EUR")
        elif streak > 0:
            print(f"Streak: {streak}/{STREAK_LENGTH}")

    # None means that the player was not fired during the days played.
    return budget, reputation, history, None


# --- Step 4: Calculate and show the final result ---
# I use the score to choose a title when the player survives.
# The title list is ordered from highest to lowest, so I return the
# first title whose minimum score is reached.
def get_title(score):
    for minimum, title in TITLES:
        if score >= minimum:
            return title


# I use the history list to show the choices made on each day.
# :>2 keeps the day number aligned; + shows the sign of each change.
def show_recap(history):
    print("\nYour quarter:")
    for reputation_change, day, letter, text, budget_change in history:
        print(f"  Day {day:>2}: {letter} - {text} ({budget_change:+} EUR, {reputation_change:+} rep)")


# I show either the reason for being fired or the score and final title.
# The score formula is reputation + budget // 200. // removes the decimal
# part of the division: for example, 6350 // 200 = 31 points from the budget.
# Then I use max(history) and min(history) to show the best and worst moves,
# based on the reputation change, which is the first value of each tuple.
# I return the title because I need to save it in results.csv.
def show_result(name, budget, reputation, history, fired_reason):
    print("\n" + "=" * 30)
    if fired_reason:
        title = "Fired"
        print(f"{name}, you are fired: {fired_reason}.")
        print(f"Budget left: {budget} EUR, reputation: {reputation}/{MAX_REPUTATION}")
    else:
        score = reputation + budget // SCORE_DIVIDER
        title = get_title(score)
        print("Quarter survived!")
        print(f"Budget left: {budget} EUR, reputation: {reputation}/{MAX_REPUTATION}")
        print(f"Final score: {score}")
        print(f"{name}, your title: {title}")

    show_recap(history)
    best_change, best_day, _, best_text, _ = max(history)
    worst_change, worst_day, _, worst_text, _ = min(history)
    print(f'\nBest move:  day {best_day}, "{best_text}" ({best_change:+})')
    print(f'Worst move: day {worst_day}, "{worst_text}" ({worst_change:+})')
    return title


# --- Step 5: Save a game ---
# I use the "a" mode because I want to add one result without deleting
# the previous games. I only write the column names when the file is new.
# The date helps me keep track of when each game was played.
def save_result(path, name, budget, reputation, title):
    is_new = not path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        if is_new:
            writer.writerow(["name", "budget", "reputation", "title", "date"])
        writer.writerow([name, budget, reputation, title, datetime.now().strftime("%Y-%m-%d %H:%M")])


# --- Main program ---
# I look for the CSV in the same folder as my Python file.
# If I cannot find it, or no scenario is valid, I stop with a message.
# Otherwise, I load the file once and allow the player to play again.
# Each completed game is added to results.csv, and Ctrl+C or Ctrl+D
# stops the program without showing a long error message.
def main():
    folder = Path(__file__).parent
    scenario_path = folder / SCENARIO_FILE
    if not scenario_path.exists():
        sys.exit(f"Scenario file not found: {scenario_path}")
    scenarios = load_scenarios(scenario_path)
    if not scenarios:
        sys.exit(f"No valid scenario in {SCENARIO_FILE}.")
    check_my_scenarios(scenarios)
    print(f"{len(scenarios)} scenarios loaded. Survive {DAYS} days at Croissant Rocket!")

    # I repeat the game while the player wants to continue.
    # At the end I show the result and save one line for this game.
    try:
        while True:
            name = input("\nWelcome to Croissant Rocket! Your name: ").strip() or "Anonymous"
            budget, reputation, history, fired_reason = play_game(scenarios)
            title = show_result(name, budget, reputation, history, fired_reason)
            save_result(folder / RESULTS_FILE, name, budget, reputation, title)
            print(f"Saved in {RESULTS_FILE}")
            if input("\nPlay again? (y/n): ").strip().lower() not in ("y", "yes"):
                print("See you next quarter!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. See you next quarter!")


# This starts the game only when I run this file directly.
if __name__ == "__main__":
    main()