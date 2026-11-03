"""campaign_audit.py - Campaign Audit Quiz (rewrite the 4 answers in YOUR words)

1. INPUTS:  European CSV (";" separator, decimal commas, BOM) + player name and answers.
2. MATH:    CTR = clicks/impressions*100, CPA = cost/conversions, ROAS = revenue/cost.
3. OUTPUTS: 5-question quiz, score out of 5 with correct numbers, a line in result.csv.
4. CHECK:   one campaign computed by hand (500 clicks / 10000 impr = 5 %) + a test CSV with traps.
Usage: python campaign_audit.py [campaigns_X.csv]
"""
import csv, sys
from datetime import datetime
from pathlib import Path

DATA_FILE = "campaigns_A.csv"  # change to your assigned dataset (A, B or C)
# Accepted header names (lower case): the exact headers are unknown before the exam.
COLUMNS = {"campaign": ["campaign", "name"], "channel": ["channel"],
           "impressions": ["impressions"], "clicks": ["clicks"], "conversions": ["conversions"],
           "cost": ["cost", "cost (€)", "cost_eur", "spend", "spend_eur"],
           "revenue": ["revenue", "revenue (€)", "revenue_eur"]}


def to_number(text):
    """European Excel writes 11088,60 -> Python needs 11088.60."""
    return float(str(text).strip().replace(",", "."))


def safe_div(a, b, factor=1):
    """Guard before dividing: a 0 denominator means the KPI is UNDEFINED (None)."""
    return a / b * factor if b > 0 else None


def read_data(path):
    """Step 1 - Keep only trustworthy rows; skip AND report bad ones (never crash)."""
    campaigns = []
    # utf-8-sig removes Excel's BOM (else KeyError on the 1st column); ";" = European separator.
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        col = {k: next((h for h in reader.fieldnames if h.strip().lower() in v), None)
               for k, v in COLUMNS.items()}
        if None in col.values():
            sys.exit(f"Missing columns {[k for k, h in col.items() if not h]} in {reader.fieldnames}")
        for line, r in enumerate(reader, start=2):
            if not (r[col["impressions"]] or "").strip():  # incomplete row: required skip
                print(f"Warning: line {line} has no impressions - skipped.")
                continue
            try:
                c = {k: r[col[k]].strip() for k in ("campaign", "channel")}
                c.update({k: int(to_number(r[col[k]])) for k in ("impressions", "clicks", "conversions")})
                c.update({k: to_number(r[col[k]]) for k in ("cost", "revenue")})
                campaigns.append(c)
            except (ValueError, TypeError, AttributeError):
                print(f"Warning: line {line} has an invalid value - skipped.")
    return campaigns


def compute_kpis(campaigns):
    """Step 2 - CTR: does the ad attract? CPA: cost of one customer. ROAS: EUR back per EUR spent."""
    for c in campaigns:
        c["ctr"] = safe_div(c["clicks"], c["impressions"], 100)
        c["cpa"] = safe_div(c["cost"], c["conversions"])  # 0 conversions -> excluded from Q2
        c["roas"] = safe_div(c["revenue"], c["cost"])
    return campaigns


def best_of(campaigns, kpi):
    """Campaign(s) with the highest KPI, ignoring undefined values. A list: ties are all correct."""
    valid = [c for c in campaigns if c[kpi] is not None]
    top = max((c[kpi] for c in valid), default=None)
    return [c["campaign"] for c in valid if c[kpi] == top], top


def compute_answers(campaigns):
    """The 5 correct answers, computed from the data (never written by hand)."""
    totals = {}  # Q4: conversions added up per channel
    for c in campaigns:
        totals[c["channel"]] = totals.get(c["channel"], 0) + c["conversions"]
    ctrs = [c["ctr"] for c in campaigns if c["ctr"] is not None]
    return {"q1": best_of(campaigns, "ctr"),              # most engaging campaign
            "q2": best_of(campaigns, "cpa"),              # most expensive customers
            "q3": sum(c["roas"] is not None and c["roas"] > 3 for c in campaigns),  # STRICTLY > 3
            "q4": [ch for ch, t in totals.items() if t == max(totals.values())], "totals": totals,
            "q5": round(sum(ctrs) / len(ctrs), 2) if ctrs else None}  # mean of individual CTRs


def is_right(answer, correct, tolerance=0.0):
    """Names: case/spaces ignored. Numbers: '4,2', '4.20%' accepted; 'abc' is wrong, not a crash."""
    if isinstance(correct, list):
        return answer.strip().lower() in [x.lower() for x in correct]
    try:
        return correct is not None and abs(to_number(answer.replace("%", "")) - correct) <= tolerance
    except ValueError:
        return False


def ask_questions(a):
    """Steps 3 & 4 - Ask the 5 questions in the terminal and count the correct answers."""
    questions = [("Which campaign achieved the highest CTR?", a["q1"][0], 0),
                 ("Which campaign had the highest CPA?", a["q2"][0], 0),
                 ("How many campaigns have a ROAS strictly above 3?", a["q3"], 0),
                 ("Which channel produced the most total conversions?", a["q4"], 0),
                 ("Average CTR across all valid campaigns (%, 2 decimals)?", a["q5"], 0.01)]
    score = 0
    for i, (text, correct, tol) in enumerate(questions, start=1):
        ok = is_right(input(f"\nQ{i}. {text}\n> "), correct, tol)
        print("Correct!" if ok else "Wrong.")
        score += ok
    return score


def export_result(player, score, path):
    """Step 6 - Append (mode "a") so previous players are kept; header only on creation."""
    new = not path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if new:
            w.writerow(["player", "score", "date"])
        w.writerow([player, score, datetime.now().strftime("%Y-%m-%d %H:%M")])


def main():
    folder = Path(__file__).parent  # files found wherever the script is launched from
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / DATA_FILE
    if not path.exists():
        sys.exit(f"File not found: {path}")
    campaigns = compute_kpis(read_data(path))
    if not campaigns:
        sys.exit("No valid campaign - nothing to audit.")
    a = compute_answers(campaigns)
    player = input(f"{len(campaigns)} valid campaigns loaded.\nPlayer name: ").strip() or "Anonymous"
    score = ask_questions(a)
    # Step 5 - Summary with the computed numbers so the player can review.
    print(f"\n{player}, your score: {score}/5")
    print(f"Q1 Best CTR: {', '.join(a['q1'][0])} ({a['q1'][1]:.2f}%)")
    print(f"Q2 Highest CPA: {', '.join(a['q2'][0]) or 'unavailable'} ({a['q2'][1] or 0:.2f} EUR)")
    print(f"Q3 ROAS > 3: {a['q3']}\nQ4 Top channel: {', '.join(a['q4'])} {a['totals']}")
    print(f"Q5 Average CTR: {a['q5']:.2f}%")
    export_result(player, score, folder / "result.csv")
    print("Result saved to result.csv")


if __name__ == "__main__":
    main()