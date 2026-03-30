# ============================================================
# Student Grade Tracker
# ============================================================


# ============================================================
# TASK 1 — Data Parsing & Profile Cleaning
# ============================================================

raw_students = [
    {"name": "  ayesha SHARMA  ", "roll": "101", "marks_str": "88, 72, 95, 60, 78"},
    {"name": "ROHIT verma",       "roll": "102", "marks_str": "55, 68, 49, 72, 61"},
    {"name": "  Priya Nair  ",    "roll": "103", "marks_str": "91, 85, 88, 94, 79"},
    {"name": "karan MEHTA",       "roll": "104", "marks_str": "40, 55, 38, 62, 50"},
    {"name": " Sneha pillai ",    "roll": "105", "marks_str": "75, 80, 70, 68, 85"},
]

cleaned_students = []

for student in raw_students:
    # strip whitespace first, then title case fixes mixed casing like "ayesha SHARMA"
    clean_name = student["name"].strip().title()

    # roll is a string in raw data, need it as int for proper use later
    clean_roll = int(student["roll"])

    # split the comma-separated string into a list, then convert each to int
    marks_list = [int(m) for m in student["marks_str"].split(", ")]

    cleaned = {
        "name": clean_name,
        "roll": clean_roll,
        "marks": marks_list
    }
    cleaned_students.append(cleaned)

    # check if every word in the name is purely alphabetic (no digits, symbols, etc.)
    words = clean_name.split()
    name_ok = all(word.isalpha() for word in words)

    if name_ok:
        validity = "✓ Valid name"
    else:
        validity = "✗ Invalid name"

    # print the profile card
    print("================================")
    print(f"Student : {clean_name}   {validity}")
    print(f"Roll No : {clean_roll}")
    print(f"Marks   : {marks_list}")
    print("================================")

# find roll 103 and print name in CAPS and lowercase
for s in cleaned_students:
    if s["roll"] == 103:
        print(f"\nRoll 103 name in ALL CAPS   : {s['name'].upper()}")
        print(f"Roll 103 name in lowercase  : {s['name'].lower()}")
        break


# ============================================================
# TASK 2 — Marks Analysis Using Loops & Conditionals
# ============================================================

print("\n\n--- TASK 2: Marks Analysis ---")

student_name = "Ayesha Sharma"
subjects     = ["Math", "Physics", "CS", "English", "Chemistry"]
marks        = [88, 72, 95, 60, 78]

# grade function — just a helper to avoid repeating this if-else block
def get_grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

print(f"\nStudent: {student_name}")
print(f"{'Subject':<12} {'Marks':>6}   Grade")
print("-" * 30)

for i in range(len(subjects)):
    grade = get_grade(marks[i])
    print(f"{subjects[i]:<12} {marks[i]:>6}   {grade}")

# basic stats
total = sum(marks)
average = round(total / len(marks), 2)

# find highest and lowest by tracking index
highest_i = 0
lowest_i  = 0
for i in range(1, len(marks)):
    if marks[i] > marks[highest_i]:
        highest_i = i
    if marks[i] < marks[lowest_i]:
        lowest_i = i

print(f"\nTotal marks   : {total}")
print(f"Average marks : {average}")
print(f"Highest       : {subjects[highest_i]} ({marks[highest_i]})")
print(f"Lowest        : {subjects[lowest_i]}  ({marks[lowest_i]})")

# --- while loop: marks entry system ---
print("\n[Marks Entry] Type a subject name, then enter marks (0-100). Type 'done' to stop.")

# keep copies so originals stay intact
all_subjects = subjects[:]
all_marks    = marks[:]
new_count    = 0

while True:
    sub_input = input("Subject name: ").strip()

    if sub_input.lower() == "done":
        break

    # ask for marks only if a subject name was actually given
    marks_input = input(f"Marks for {sub_input} (0-100): ").strip()

    # validate: must be numeric
    if not marks_input.isdigit():
        print("  ⚠ Invalid input — marks must be a number. Entry skipped.")
        continue

    m = int(marks_input)

    # validate: must be in range
    if m < 0 or m > 100:
        print("  ⚠ Marks must be between 0 and 100. Entry skipped.")
        continue

    all_subjects.append(sub_input)
    all_marks.append(m)
    new_count += 1
    print(f"  ✓ Added {sub_input}: {m}")

updated_avg = round(sum(all_marks) / len(all_marks), 2)
print(f"\nNew subjects added  : {new_count}")
print(f"Updated average     : {updated_avg}")


# ============================================================
# TASK 3 — Class Performance Summary
# ============================================================

print("\n\n--- TASK 3: Class Performance Summary ---\n")

class_data = [
    ("Ayesha Sharma",  [88, 72, 95, 60, 78]),
    ("Rohit Verma",    [55, 68, 49, 72, 61]),
    ("Priya Nair",     [91, 85, 88, 94, 79]),
    ("Karan Mehta",    [40, 55, 38, 62, 50]),
    ("Sneha Pillai",   [75, 80, 70, 68, 85]),
]

# header row
print(f"{'Name':<18}| {'Average':^7} | Status")
print("-" * 40)

passed = 0
failed = 0
all_avgs = []

# track topper manually — start with first student as placeholder
topper_name = ""
topper_avg  = -1

for name, student_marks in class_data:
    avg = round(sum(student_marks) / len(student_marks), 2)
    all_avgs.append(avg)

    if avg >= 60:
        status = "Pass"
        passed += 1
    else:
        status = "Fail"
        failed += 1

    # update topper if this student scored higher
    if avg > topper_avg:
        topper_avg  = avg
        topper_name = name

    print(f"{name:<18}| {avg:^7.2f} | {status}")

class_avg = round(sum(all_avgs) / len(all_avgs), 2)

print(f"\nPassed : {passed} student(s)")
print(f"Failed : {failed} student(s)")
print(f"Topper : {topper_name} ({topper_avg})")
print(f"Class average : {class_avg}")


# ============================================================
# TASK 4 — String Manipulation Utility
# ============================================================

print("\n\n--- TASK 4: String Manipulation ---\n")

essay = "  python is a versatile language. it supports object oriented, functional, and procedural programming. python is widely used in data science and machine learning.  "

# step 1: strip whitespace — all further steps use clean_essay
clean_essay = essay.strip()
print(f"Stripped essay:\n{clean_essay}\n")

# step 2: title case
print(f"Title Case:\n{clean_essay.title()}\n")

# step 3: count occurrences of "python" — clean_essay is lowercase so no need for lower()
py_count = clean_essay.count("python")
print(f"'python' appears {py_count} time(s)\n")

# step 4: replace "python" with "Python 🐍"
replaced = clean_essay.replace("python", "Python 🐍")
print(f"After replace:\n{replaced}\n")

# step 5: split into sentences on ". " (period + space)
sentences = clean_essay.split(". ")
print(f"Sentences list:\n{sentences}\n")

# step 6: print each sentence numbered, ensure it ends with a period
print("Numbered sentences:")
for idx, sent in enumerate(sentences, start=1):
    # only add a period if the sentence doesn't already end with one
    if not sent.endswith("."):
        sent = sent + "."
    print(f"{idx}. {sent}")
