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


