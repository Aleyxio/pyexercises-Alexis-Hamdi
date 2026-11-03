"""Mock exam - answers the 5 campaign questions from a European CSV (; and 1234,56).
Usage: python mock_exam_short.py [file.csv]   (default: data.csv next to this script)"""
import csv, sys
from pathlib import Path

# Safe division: returns None instead of crashing when the denominator is 0.
# Used for CTR, CPA and ROAS: a metric with a 0 denominator is UNDEFINED, not 0.
def ratio(a, b, factor=1):
    return a / b * factor if b > 0 else None

def to_num(text):
    # European decimals: "1234,56" -> 1234.56 (Python's float() needs a dot).
    return float(text.strip().replace(",", "."))

# Path(__file__).parent finds data.csv wherever the script is launched from.
csv_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data.csv"
rows = []
# utf-8-sig removes Excel's hidden BOM; ";" is the European column separator.
with open("MOCK_EXAM/test_data.csv", encoding="utf-8-sig", newline="") as f:
    for line, r in enumerate(csv.DictReader(f, delimiter=";"), start=2):
        try:
            # Each row is converted ONCE; .strip() merges "Facebook " and "Facebook".
            rows.append({"name": r["campaign"].strip(), "channel": r["channel"].strip(),
                         "imp": int(r["impressions"]), "clicks": int(r["clicks"]),
                         "conv": int(r["conversions"]), "spend": to_num(r["spend_eur"]),
                         "rev": to_num(r["revenue_eur"])})
        except (ValueError, TypeError, AttributeError, KeyError):
            # Invalid row: skipped and REPORTED, never silently ignored.
            print(f"Warning: line {line} is invalid and was skipped.")
print(f"{len(rows)} valid campaigns read from {csv_file.name}\n")

# Pre-compute the metrics once per campaign (None = undefined).
for c in rows:
    c["ctr"] = ratio(c["clicks"], c["imp"], 100)  # CTR % = clicks / impressions * 100
    c["cpa"] = ratio(c["spend"], c["conv"])       # CPA EUR = spend / conversions
    c["roas"] = ratio(c["rev"], c["spend"])       # ROAS = revenue / spend
with_ctr = [c for c in rows if c["ctr"] is not None]  # campaigns with impressions > 0
with_cpa = [c for c in rows if c["cpa"] is not None]  # campaigns with conversions > 0

# Q1 - Best CTR. 0-impression campaigns are excluded (CTR undefined, not 0 %).
# max() keeps the FIRST campaign in case of a tie (same as a strict ">").
best = max(with_ctr, key=lambda c: c["ctr"], default=None)
print(f"1. Best CTR: {best['name']} ({best['ctr']:.2f}%)" if best else "1. Best CTR: unavailable")

# Q2 - Highest CPA = the LEAST efficient campaign (each conversion cost the most).
# 0-conversion campaigns are excluded: their CPA cannot be computed.
worst = max(with_cpa, key=lambda c: c["cpa"], default=None)
print(f"2. Highest CPA: {worst['name']} ({worst['cpa']:.2f} EUR)" if worst else "2. Highest CPA: unavailable")

# Q3 - "Above 3" means STRICTLY > 3 (a ROAS of exactly 3.00 is not counted).
# True counts as 1 in sum(); campaigns with 0 spend (ROAS None) are skipped.
print(f"3. Campaigns with ROAS above 3: {sum(c['roas'] is not None and c['roas'] > 3 for c in rows)}")

# Q4 - A dictionary groups the conversions by channel. ALL valid campaigns
# count, even with 0 impressions: their conversions really happened.
totals = {}
for c in rows:
    totals[c["channel"]] = totals.get(c["channel"], 0) + c["conv"]
top = max(totals, key=totals.get)  # the channel NAME with the largest total
print(f"4. Channel with most conversions: {top} ({totals[top]} conversions)")
print(f"   Details per channel: {totals}")

# Q5 - Mean of the INDIVIDUAL CTRs (each campaign counts equally), rounded only
# at the end. The weighted CTR (total clicks / total impressions) is shown too:
# it gives more weight to big campaigns and can differ.
if with_ctr:
    avg = round(sum(c["ctr"] for c in with_ctr) / len(with_ctr), 2)
    weighted = round(ratio(sum(c["clicks"] for c in with_ctr), sum(c["imp"] for c in with_ctr), 100), 2)
    print(f"5. Average CTR: {avg:.2f}%\n   (weighted CTR = total clicks / total impressions: {weighted:.2f}%)")
else:
    print("5. Average CTR: unavailable")