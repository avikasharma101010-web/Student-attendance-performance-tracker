"""
PS 45 - Student Attendance & Performance Tracker
Language: Python 3
Concepts: Pandas, Dictionaries, Calculations, Visualization

CSV columns: Name, Classes_Held, Classes_Attended, Marks (out of 100)
A student is At Risk if attendance < 75% or marks < 40.
"""

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "students.csv"
MIN_ATTENDANCE = 75
MIN_MARKS = 40


def load_data(filename):
    """Load CSV with Pandas, skip invalid rows, return a clean DataFrame."""
    try:
        raw = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        print("File not found:", filename)
        return None
    except Exception:
        print("Could not read the CSV file.")
        return None

    clean_rows = []
    for i in range(len(raw)):
        row_no = i + 1
        row = raw.iloc[i]

        name = str(row["Name"]).strip()

        # check Classes_Held
        try:
            held = int(row["Classes_Held"])
        except (ValueError, TypeError):
            print(f"Row {row_no} skipped: invalid Classes_Held '{row['Classes_Held']}'.")
            continue

        # check Classes_Attended
        try:
            attended = int(row["Classes_Attended"])
        except (ValueError, TypeError):
            print(f"Row {row_no} skipped: invalid Classes_Attended '{row['Classes_Attended']}'.")
            continue

        # check Marks
        try:
            marks = int(row["Marks"])
        except (ValueError, TypeError):
            print(f"Row {row_no} skipped: invalid Marks '{row['Marks']}'.")
            continue

        # logic checks
        if held <= 0:
            print(f"Row {row_no} skipped: classes held must be greater than 0.")
            continue
        if attended < 0 or attended > held:
            print(f"Row {row_no} skipped: attended ({attended}) cannot exceed held ({held}).")
            continue
        if marks < 0 or marks > 100:
            print(f"Row {row_no} skipped: marks {marks} out of range (0-100).")
            continue

        # dictionary for one student
        student = {
            "Name": name,
            "Classes_Held": held,
            "Classes_Attended": attended,
            "Marks": marks,
        }
        clean_rows.append(student)

    if len(clean_rows) == 0:
        print("No valid data to analyse.")
        return None

    df = pd.DataFrame(clean_rows)

    # Pandas column calculations
    df["Attendance"] = df["Classes_Attended"] / df["Classes_Held"] * 100
    # boolean filtering columns
    df["Low_Attendance"] = df["Attendance"] < MIN_ATTENDANCE
    df["Low_Marks"] = df["Marks"] < MIN_MARKS
    df["At_Risk"] = df["Low_Attendance"] | df["Low_Marks"]
    return df


def show_report(df):
    """Menu option 1: per-student report."""
    for i in range(len(df)):
        s = df.iloc[i]
        status = "OK"
        if s["Low_Attendance"] and s["Low_Marks"]:
            status = "At Risk (attendance below 75% and marks below 40)"
        elif s["Low_Attendance"]:
            status = "At Risk (attendance below 75%)"
        elif s["Low_Marks"]:
            status = "At Risk (marks below 40)"
        print(f"{s['Name']}: {s['Attendance']:.2f}% | Marks {s['Marks']} | {status}")


def show_summary(df):
    """Menu option 2: averages, at risk list and charts."""
    avg_att = df["Attendance"].mean()
    avg_marks = df["Marks"].mean()
    at_risk = df[df["At_Risk"]]["Name"].tolist()

    print(f"Average attendance: {avg_att:.2f}% | Average marks: {avg_marks:.2f}")
    print(f"At Risk students: {len(at_risk)} ({', '.join(at_risk)})")

    # Chart 1: bar chart of attendance
    plt.figure(figsize=(7, 5))
    colors = ["red" if r else "green" for r in df["At_Risk"]]
    plt.bar(df["Name"], df["Attendance"], color=colors)
    plt.axhline(MIN_ATTENDANCE, color="black", linestyle="--", label="75% limit")
    plt.title("Attendance of Students")
    plt.xlabel("Student")
    plt.ylabel("Attendance (%)")
    plt.legend()

    # Chart 2: scatter chart of attendance vs marks
    plt.figure(figsize=(7, 5))
    plt.scatter(df["Attendance"], df["Marks"], color="blue")
    for i in range(len(df)):
        plt.annotate(df["Name"][i], (df["Attendance"][i], df["Marks"][i]))
    plt.title("Attendance vs Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Marks")

    print("Bar chart and scatter chart 'Attendance vs Marks' displayed")
    plt.show()


def main():
    df = load_data(CSV_FILE)
    if df is None:
        return

    while True:
        print("\n--- Student Attendance & Performance Tracker ---")
        print("1. Report")
        print("2. Summary and charts")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_report(df)
        elif choice == "2":
            show_summary(df)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()