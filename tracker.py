import csv
import json
from datetime import datetime
from pathlib import Path

BASE =  Path(__file__).parent/ "data"
BASE.mkdir(exist_ok=True)

STUDENTS_CSV = BASE/ "students.csv"
STUDENTS_JSON = BASE/ "students.json"

LOG_CSV = BASE/ "log.csv"
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
        
def save_json(students,path = STUDENTS_JSON):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"students": students}, f, indent= 2)
            
def load_json (path =STUDENTS_JSON):
    if not path.exists():
        return {"students ": []}
    try:
        with open(path, encoding= "utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
            print( f"Corrupt JSON at line {e.lineno}: {e.msg}")
            return {"students": []}
        
def add_student(name, age, grade, courses=None):
    data = load_json()
    students = data.setdefault("students", [])
    students.append({
        "name": name,
        "age": age,
        "grade": grade,
        "courses": courses or [],
    })
    save_json(students)
    log_action("add", name)
    
    
def log_action(action, name):
    needs_header = not LOG_CSV.exists() or LOG_CSV.stat().st_size == 0
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["time", "action", "name"])
        if needs_header:
            writer.writeheader()
        writer.writerow({
            "time": datetime.now().isoformat(timespec="seconds"),
            "action": action,
            "name": name,
        })
        
            
        
if __name__ == "__main__":
    write_sample_csv()
    students, errors = read_csv(STUDENTS_CSV)
    save_json(students)
    print(load_json())
    print(students)
    add_student("Sofia", 20, 93, ["CS101", "MATH201"])
    print("Skipped:", errors)