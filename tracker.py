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
    
    if any(s["name"].lower() == name.lower() for s in data["students"]):
        print(f"{name} already exists. ")
        return
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
    
def report():
    students = load_json()["students"]
    if not students:
        print("No students. ")
        return
    grades = [s["grade"]for s in students]
    best = max(students, key= lambda s: s["grade"])
    print(f"\nStudents:   {len(students)}")
    print(f"Average:    {sum(grades)/ len(grades):.1f}")
    print(f"Top:        {best['name']} ({best['grade']})\n")
    for s in sorted(students, key= lambda s:s["grade"], reverse=True):
        print(f"    {s["name"]:<10} {s['grade']:>6} {', '.join(s.get("courses", []))} ")
                
def export_csv(path = BASE/ "export.csf"):
    students = load_json()["students"]
    fields =  ["name", "age", "grade", "courses"]
    with open(path, "w", newline="", encoding="utf-8")as f:
        writer = csv.DictWriter(f, fieldnames= fields)
        writer.writeheader()
        for s in students:
            row= dict(s)
            row["courses"] = ";".join(s.get("courses",[]))
            writer.writerow(row)
    print("Exported: ",path)

def menu():
    while True:
        print("\n1) Import CSV \n2) Add Student \n3) Report \n4) Export CSV \n5) Quit")
        choice = input("\n> ").strip()
        
        if choice == "1":
            students, errors = read_csv(STUDENTS_CSV)
            for s in students:
                s["courses"] = []
            save_json(students)
            print(f"Imported {len(students)}, skipped {len(errors)}")
            
        elif choice == '2':
            try:
                name = input("Name: ").strip()
                age = int(input("Age: "))
                grade = float(input("Grade: "))
                raw = input("Courses (comma separated): ")
                courses = [c.strip() for c in raw.split(",") if c.strip()]
                add_student(name, age, grade, courses)        
            except ValueError:
                print("Age and grade must be numbers. ")
                
        elif choice == "3":    
            report()
        
        elif choice == "4":
            export_csv()
            
        elif choice == "5":
            print("Bye! ")
            break

if __name__ == "__main__":
    if not STUDENTS_CSV.exists():
        write_sample_csv()
    
    print("Welcome to the student registration system! ")
    menu()