import csv
import json
from datetime import datetime
from pathlib import Path

BASE =  Path(__file__).parent/ "data"
BASE.mkdir(exist_ok=True)

STUDENTS_CSV = BASE/ "students.csv"
STUDENTS_JASON = BASE/ "students.json"

LOG_BASE = BASE/ "log.csv"
FIELDS = ["name", "age", "grade"]

def write_sample_csv():
    rows = [{"name": "Ana", "age": 12, "grade": 90},
            {"name": "Paul", "age": 13, "grade": 88},
            {"name": "Mario", "age": "abc", "grade": 70.9},
            {"name": "Martha", "age": 12, "grade": 100}
            ]

    with open(STUDENTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        
def read_csv(path):
    students, errors = [], []
    with open (path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                students.append({
                    "name": row["name"].strip(),
                    "age": int(row["age"]),
                    "grade": float(row["grade"]),
                })
            except (ValueError, KeyError) as e:
                errors.append((line_no, row, str(e)))
    return students, errors
        
        
if __name__ == "__main__":
    write_sample_csv()
    students, errors = read_csv(STUDENTS_CSV)
    print(students)
    print("Skipped:", errors)