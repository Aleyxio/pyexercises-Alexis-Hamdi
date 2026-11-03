import csv
with open("MOCK_EXAM/python_mock_exam_1_campaigns.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")

    row = next(reader)

    print(row["campaign"])
    print(row["clicks"])
    print(row["impressions"])

    clicks = int(row["clicks"])
    impressions = int(row["impressions"])
    ctr = (clicks / impressions) * 100
    print(f"CTR: {ctr:.2f}%")
