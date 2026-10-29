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
        
        
        
        
if __name__ == "__main__":
    write_sample_csv()
    print("Created:", STUDENTS_CSV)