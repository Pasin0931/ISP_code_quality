from __future__ import annotations

import os
import sys
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

# Constants (set MONGO_URI in the environment to include credentials)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "student_db"
COLLECTION_NAME = "students"

StudentCollection = Collection[dict[str, Any]]


def connect_db() -> StudentCollection:
    try:
        client: MongoClient[dict[str, Any]] = MongoClient(MONGO_URI)
        # Check connection
        client.admin.command("ping")
        print("Connected to MongoDB successfully!")
        return client[DB_NAME][COLLECTION_NAME]
    except PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)


def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid number, please try again.")


def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number, please try again.")


def print_student(student: dict[str, Any]) -> None:
    print(
        f"ID: {student['student_id']}, Name: {student['name']}, "
        f"Dept: {student['department']}, GPA: {student['gpa']}, "
        f"Courses: {student['courses']}"
    )


# --- Task 2: Create (Insert Data) ---

def create_student(collection: StudentCollection) -> None:
    print("\n--- Add New Student ---")
    while True:
        student_id = input("Enter Student ID (e.g., S001): ").strip()
        if collection.find_one({"student_id": student_id}):
            print(f"Error: Student with ID {student_id} already exists!")
            continue
        break

    name = input("Enter Name: ").strip()
    age = read_int("Enter Age: ")
    department = input("Enter Department: ").strip()
    gpa = read_float("Enter GPA: ")

    # Input courses as comma-separated list
    courses_input = input("Enter Courses (comma separated): ")
    courses = [c.strip() for c in courses_input.split(",") if c.strip()]

    student_doc: dict[str, Any] = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "gpa": gpa,
        "courses": courses,
    }

    try:
        result = collection.insert_one(student_doc)
        print(f"\nStudent inserted successfully with _id: {result.inserted_id}")
    except PyMongoError as e:
        print(f"\nError inserting student: {e}")


# --- Task 3: Read (Query Data) ---

def get_student_by_id(collection: StudentCollection) -> None:
    print("\n--- Get Student by ID ---")
    student_id = input("Enter Student ID: ").strip()

    student = collection.find_one({"student_id": student_id})
    if not student:
        print("Student not found.")
    else:
        print("\nFound: ", end="")
        print_student(student)


def get_all_students(collection: StudentCollection) -> None:
    print("\n--- All Students ---")

    # A cursor is always truthy, so convert to a list before checking it.
    students = list(collection.find())
    if not students:
        print("No students found.")
    else:
        for student in students:
            print_student(student)


def search_by_gpa(collection: StudentCollection) -> None:
    print("\n--- Search by GPA ---")
    try:
        min_gpa = float(input("Enter minimum GPA: "))
    except ValueError:
        print("Invalid GPA input.")
        return

    students = list(collection.find({"gpa": {"$gte": min_gpa}}))
    if not students:
        print(f"No students found with GPA >= {min_gpa}")
    else:
        print("")
        for student in students:
            print(
                f"ID: {student['student_id']}, Name: {student['name']}, "
                f"GPA: {student['gpa']}"
            )


# --- Task 4: Update ---

def update_student(collection: StudentCollection) -> None:
    print("\n--- Update Student ---")
    student_id = input("Enter Student ID to update: ").strip()

    if not collection.find_one({"student_id": student_id}):
        print("Student not found.")
        return

    print("1. Update GPA")
    print("2. Add Course")
    choice = input("Choose option: ")
    query_filter = {"student_id": student_id}

    if choice == "1":
        new_gpa = read_float("Enter new GPA: ")
        try:
            collection.update_one(query_filter, {"$set": {"gpa": new_gpa}})
            print("GPA updated successfully.")
        except PyMongoError:
            print("Error occurred while updating GPA!")
    elif choice == "2":
        new_course = input("Enter new course name: ").strip()
        try:
            collection.update_one(query_filter, {"$push": {"courses": new_course}})
            print("Course added successfully.")
        except PyMongoError:
            print("Error occurred while adding course!")
    else:
        print("Invalid option.")


# --- Task 5: Delete ---

def delete_student(collection: StudentCollection) -> None:
    print("\n--- Delete Student ---")
    student_id = input("Enter Student ID to delete: ").strip()

    try:
        res = collection.delete_one({"student_id": student_id})
        if res.deleted_count == 0:
            print("Student not found.")
        else:
            print("Student deleted successfully.")
    except PyMongoError:
        print("Error while deleting student.")


def clear_all_data(collection: StudentCollection) -> None:
    print("\n--- Clear All Data ---")
    confirm = input(
        "Are you sure you want to delete ALL students? (yes/no): "
    ).strip().lower()
    if confirm == "yes":
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} students.")
    else:
        print("Operation cancelled.")


# --- Task 3: Read (Advanced Search) ---

def advanced_search(collection: StudentCollection) -> None:
    print("\n--- Advanced Search ---")
    print("1. Find by Department AND Minimum GPA ($and)")
    print("2. Find by Department A OR Department B ($or)")
    choice = input("Choose option: ")

    if choice == "1":
        dept = input("Enter Department: ").strip()
        try:
            min_gpa = float(input("Enter minimum GPA: "))
        except ValueError:
            print("Invalid GPA input.")
            return

        students = list(collection.find({
            "$and": [
                {"department": dept},
                {"gpa": {"$gte": min_gpa}},
            ]
        }))

        print(f"\nFound {len(students)} students in {dept} with GPA >= {min_gpa}:")
        for student in students:
            print(f"- {student['name']} (GPA: {student['gpa']})")

    elif choice == "2":
        dept1 = input("Enter Department 1: ").strip()
        dept2 = input("Enter Department 2: ").strip()

        students = list(collection.find({
            "$or": [
                {"department": dept1},
                {"department": dept2},
            ]
        }))

        print(f"\nFound {len(students)} students in {dept1} OR {dept2}:")
        for student in students:
            print(f"- {student['name']} (Dept: {student['department']})")
    else:
        print("Invalid option")


def main() -> None:
    collection = connect_db()

    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search by ID")
        print("4. Search by GPA")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Clear All Data")
        print("8. Advanced Search (AND/OR)")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_student(collection)
        elif choice == "2":
            get_all_students(collection)
        elif choice == "3":
            get_student_by_id(collection)
        elif choice == "4":
            search_by_gpa(collection)
        elif choice == "5":
            update_student(collection)
        elif choice == "6":
            delete_student(collection)
        elif choice == "7":
            clear_all_data(collection)
        elif choice == "8":
            advanced_search(collection)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()