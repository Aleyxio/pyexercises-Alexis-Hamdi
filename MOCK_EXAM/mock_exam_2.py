import csv
with open("MOCK_EXAM/python_mock_exam_1_campaigns.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:

        if row["impressions"] == "":
            continue

        print(row["campaign"])
        print(row["clicks"])
        print(row["impressions"])

