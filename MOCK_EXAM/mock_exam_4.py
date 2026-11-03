"""Campaign Audit Quiz - My four planning answers

1. INPUTS: I read a campaign CSV and ask the player for their name and answers.
2. MATH: I calculate CTR, CPA and ROAS for valid campaigns. I compare campaigns
   and add conversions by channel to find the five correct quiz answers.
3. OUTPUTS: I show five questions and the final score, then save the player's
   name, score and date in result.csv.
4. CHECK: I will compare one CTR with a manual calculation (500 / 10000 x 100
   = 5%) and test missing impressions, decimal commas and zero conversions.

Usage: python campaign_audit.py [campaigns_X.csv]
"""
import csv, sys
from datetime import datetime
from pathlib import Path

# --- Settings ---------------------------------------------------------------
# The exam may use a different CSV. I keep the filename and possible column
# names together so I can adapt them quickly if the new headers are different.
DATA_FILE = "campaigns_A.csv"
COLUMNS = {"campaign": ["campaign", "name"], "channel": ["channel"],
           "impressions": ["impressions"], "clicks": ["clicks"], "conversions": ["conversions"],
           "cost": ["cost", "cost (€)", "cost_eur", "spend", "spend_eur"],
           "revenue": ["revenue", "revenue (€)", "revenue_eur"]}

# --- Helpers ----------------------------------------------------------------
# The CSV may use decimal commas, for example "11088,60". I convert them to
# Python numbers so advertising costs and revenue can be calculated correctly.
def to_number(text):
    return float(str(text).strip().replace(",", "."))

# A KPI with a zero denominator has no meaning (e.g. CPA with 0 conversions).
# Returning None instead of crashing lets me exclude these campaigns later.
def safe_div(a, b, factor=1):
    return a / b * factor if b > 0 else None

# --- Step 1: read the data ----------------------------------------------------
# I need reliable data before comparing campaign performance. I match the
# actual CSV headers, then skip rows with missing or invalid impressions and
# unreadable figures. I print a warning so I know which rows were excluded.
def read_data(path):
    campaigns = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        if not reader.fieldnames:
            sys.exit("CSV is empty or has no headers.")
        col = {k: next((h for h in reader.fieldnames if h.strip().lower() in v), None)
               for k, v in COLUMNS.items()}
        if None in col.values():
            sys.exit(f"Missing columns {[k for k, h in col.items() if not h]} in {reader.fieldnames}")
        for line, r in enumerate(reader, start=2):
            if not (r[col["impressions"]] or "").strip():
                print(f"Warning: line {line} has no impressions - skipped.")
                continue
            try:
                c = {k: r[col[k]].strip() for k in ("campaign", "channel")}
                c.update({k: int(to_number(r[col[k]])) for k in ("impressions", "clicks", "conversions")})
                c.update({k: to_number(r[col[k]]) for k in ("cost", "revenue")})
                if c["impressions"] <= 0:
                    print(f"Warning: line {line} has invalid impressions - skipped.")
                    continue
                campaigns.append(c)
            except (ValueError, TypeError, AttributeError):
                print(f"Warning: line {line} has an invalid value - skipped.")
    return campaigns

# --- Step 2: compute the KPIs -------------------------------------------------
# Each KPI answers a business question about a campaign:
#   CTR  -> does the ad catch people's attention? (clicks per 100 views)
#   CPA  -> how much do we pay to get one customer? (lower is better)
#   ROAS -> how much revenue is earned for every euro of advertising cost?
def compute_kpis(campaigns):
    for c in campaigns:
        c["ctr"] = safe_div(c["clicks"], c["impressions"], 100)
        c["cpa"] = safe_div(c["cost"], c["conversions"])
        c["roas"] = safe_div(c["revenue"], c["cost"])
    return campaigns

# Q1 and Q2 both ask "which campaign has the highest X", so one function does
# both. Campaigns where the KPI is undefined are ignored, which is how the
# zero-conversion campaigns are kept out of Q2. If two campaigns tie, I keep
# both names so the player is not marked wrong for a valid answer.
def best_of(campaigns, kpi):
    valid = [c for c in campaigns if c[kpi] is not None]
    top = max((c[kpi] for c in valid), default=None)
    return [c["campaign"] for c in valid if c[kpi] == top], top

# --- The 5 correct answers -------------------------------------------------------
# The answers are written nowhere, so the program computes them from the data:
#   Q1 most engaging campaign, Q2 most expensive customers, Q3 campaigns that
#   return strictly more than 3 EUR per EUR, Q4 channel bringing the most
#   conversions (summed per channel), Q5 average CTR of the valid campaigns,
#   rounded only at the end. I use the mean of campaign CTRs, not a weighted CTR.
def compute_answers(campaigns):
    totals = {}
    for c in campaigns:
         totals[c["channel"]] = totals.get(c["channel"], 0) + c["conversions"]
    ctrs = [c["ctr"] for c in campaigns if c["ctr"] is not None]
    return {"q1": best_of(campaigns, "ctr"),
            "q2": best_of(campaigns, "cpa"),
            "q3": sum(c["roas"] is not None and c["roas"] > 3 for c in campaigns),
            "q4": [ch for ch, t in totals.items() if t == max(totals.values())], "totals": totals,
            "q5": round(sum(ctrs) / len(ctrs), 2) if ctrs else None}

# --- Steps 3 and 4: quiz and scoring ----------------------------------------------
# I want the quiz to be fair and never crash because of what the player types.
# Names are compared without caring about capitals or spaces ("linkedin" is
# fine). Numbers accept "4,2" or "4.20%", and something like "abc" just
# counts as wrong. Q5 is compared with the already rounded correct answer.
def is_right(answer, correct, tolerance=0.0):
    if isinstance(correct, list):
        return answer.strip().lower() in [x.lower() for x in correct]
    try:
        return correct is not None and abs(to_number(answer.replace("%", "")) - correct) <= tolerance
    except ValueError:
        return False

# Each question is stored with its correct answer, so the loop below asks
# them one by one, gives immediate feedback and adds one point per good answer.
def ask_questions(a):
    questions = [("Which campaign achieved the highest CTR?", a["q1"][0], 0),
                 ("Which campaign had the highest CPA? (N/A if none)", a["q2"][0] or ["N/A"], 0),
                 ("How many campaigns have a ROAS strictly above 3?", a["q3"], 0),
                 ("Which channel produced the most total conversions?", a["q4"], 0),
                 ("Average CTR across all valid campaigns (%, 2 decimals)?", a["q5"], 0.000001)]
    score = 0
    for i, (text, correct, tol) in enumerate(questions, start=1):
        ok = is_right(input(f"\nQ{i}. {text}\n> "), correct, tol)
        print("Correct!" if ok else "Wrong.")
        score += ok
    return score

# --- Step 6: save the result ------------------------------------------------------
# result.csv keeps a history of every player, so I add a line at the end
# instead of overwriting the file. The header is written only the first time.
def export_result(player, score, path):
    new = not path.exists() or path.stat().st_size == 0
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if new:
            w.writerow(["player", "score", "date"])
        w.writerow([player, score, datetime.now().strftime("%Y-%m-%d %H:%M")])

# --- Main: the 6 steps in order -----------------------------------------------------
# I look for CSV files next to this script, even if I launch it elsewhere.
# If the file is missing or no campaign is usable, the program stops
# with a message instead of crashing. The answers are computed before the
# quiz starts, then the summary shows the real numbers so the player can
# see where they went wrong.
def main():
    folder = Path(__file__).parent
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DATA_FILE)
    if not path.is_absolute():
        path = folder / path
    if not path.is_file():
        sys.exit(f"File not found: {path}")
    campaigns = compute_kpis(read_data(path))
    if not campaigns:
        sys.exit("No valid campaign - nothing to audit.")
    a = compute_answers(campaigns)
    player = input(f"{len(campaigns)} valid campaigns loaded.\nPlayer name: ").strip() or "Anonymous"
    score = ask_questions(a)
    print(f"\n{player}, your score: {score}/5")
    print(f"Q1 Best CTR: {', '.join(a['q1'][0])} ({a['q1'][1]:.2f}%)")
    if a["q2"][1] is None:
        print("Q2 Highest CPA: unavailable (no conversions)")
    else:
        print(f"Q2 Highest CPA: {', '.join(a['q2'][0])} ({a['q2'][1]:.2f} EUR)")
    print(f"Q3 ROAS > 3: {a['q3']}\nQ4 Top channel: {', '.join(a['q4'])} {a['totals']}")
    print(f"Q5 Average CTR: {a['q5']:.2f}%")
    export_result(player, score, folder / "result.csv")
    print("Result saved to result.csv")

if __name__ == "__main__":
    main()
