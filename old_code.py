import pymongo
from pymongo import MongoClient
import sys

# Constants
MONGO_URI = "mongodb://pasin:s6810545794@localhost:27017/"
DB_NAME = "student_db"
COLLECTION_NAME = "students"

def connect_db():
    try:
        client = MongoClient(MONGO_URI)
        # Check connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        return client[DB_NAME][COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

# --- Task 2: Create (Insert Data) ---

def create_student(collection):
    # TODO: Check if student exists, then insert the new student document
    print("\n--- Add New Student ---")
    while True:
        student_id = input("Enter Student ID (e.g., S001): ").strip()
    
        # --- Answer Start: Check validation and insert document ---
        # TODO 1: Check if a student with this 'student_id' already exists in MongoDB
        # Hint: Use collection.find_one() and check if it returns a document

        if collection.find_one({"student_id": student_id}):
            # Error Message if ID exists:
            print(f"Error: Student with ID {student_id} already exists!")
            continue

        break    
    
    name = input("Enter Name: ").strip()
    age = int(input("Enter Age: "))
    department = input("Enter Department: ").strip()
    gpa = float(input("Enter GPA: "))
    
    # Input courses as comma-separated list
    courses_input = input("Enter Courses (comma separated): ")
    courses = [c.strip() for c in courses_input.split(",") if c.strip()]

    # TODO 2: Create a Python dictionary for the student document
    student_doc = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "gpa": gpa,
        "courses": courses
    }
    
    # TODO 3: Insert the dictionary into the 'students' collection
    # Hint: Use collection.insert_one() and handle potential errors
    try:
        result = collection.insert_one(student_doc)

        # Message Format to use:
        print(f"\nStudent inserted successfully with _id: {result.inserted_id}")
    except Exception as e:
        # Error Message if insertion fails:
        print(f"\nError inserting student: {e}")
    
    # --- Answer End ---

# --- Task 3: Read (Query Data) ---

# --- Task 3: Read (Get by ID) ---

def get_student_by_id(collection):
    # TODO: Find a single student by student_id
    print("\n--- Get Student by ID ---")
    student_id = input("Enter Student ID: ").strip()
    
    # --- Answer Start: Find One document ---
    # TODO: Use find_one() to get the student where "student_id" matches the user input
    res = collection.find_one({"student_id": student_id})

    if not res:
        # If not found, print "Student not found."
        print("Student not found.")
    else:
        # Message Format if found:
        print(f"\nFound: ID: {res['student_id']}, Name: {res['name']}, Dept: {res['department']}, GPA: {res['gpa']}, Courses: {res['courses']}")  
          
    # --- Answer End ---

def get_all_students(collection):
    # TODO: Retrieve and print all students from the collection
    print("\n--- All Students ---")
    # --- Answer Start: Fetch all documents ---
    # TODO: Use collection.find() to retrieve all student documents

    res = collection.find()
    if not res:
        # Message Format if no students:
        print("No students found.")
    else:
    # Message Format for each student if found:
        for i in res:
            print(f"ID: {i['student_id']}, Name: {i['name']}, Dept: {i['department']}, GPA: {i['gpa']}, Courses: {i['courses']}")
            # print(i)
    
    # --- Answer End ---

def search_by_gpa(collection):
    # TODO: Find students with GPA >= min_gpa
    print("\n--- Search by GPA ---")
    try:
        min_gpa = float(input("Enter minimum GPA: "))
        # --- Answer Start: Filter by GPA ---
        # TODO: Query students with GPA >= min_gpa using the $gte operator
        res = collection.find({"gpa": {"$gte": min_gpa}})
        
        # Message Format if not found:
        if not res:
            print(f"No students found with GPA >= {min_gpa}")
        else:
            print("")
            for i in res:
                # Message Format for each student if found (Show ID, Name, and GPA):
                print(f"ID: {i['student_id']}, Name: {i['name']}, GPA: {i['gpa']}")
  
        # --- Answer End ---
    except ValueError:
        print("Invalid GPA input.")

# --- Task 4: Update ---

def update_student(collection):
    # TODO: Update GPA ($set) or Add Course ($push) for a specific student_id
    print("\n--- Update Student ---")
    student_id = input("Enter Student ID to update: ").strip()
    
    # --- Answer Start: Update document ($set or $push) ---
    # TODO 1: Check if the student exists first
    res = collection.find_one({"student_id": student_id})
    if not res:
        print("Student not found.")
    else:
        print("1. Update GPA")
        print("2. Add Course")
        choice = input("Choose option: ")

        if choice == "1":
            new_gpa = float(input("Enter new GPA: "))
            # TODO 2: Update the student's gpa using the $set operator
            
            try:
                query_filter = { 'student_id' : student_id }
                update_operation = { '$set' : {'gpa' : new_gpa} }
                result = collection.update_one(query_filter, update_operation)
                print("GPA updated successfully.")
            except Exception:
                print("Error occur while updating courses !")
        
        elif choice == "2":
            new_course = input("Enter new course name: ").strip()
            # TODO 3: Add a new course to the courses array using the $push operator
            
            try:
                query_filter = { 'student_id' : student_id }
                update_operation = { '$push' : {'courses' : new_course} }
                result = collection.update_one(query_filter, update_operation)
                print("Course added successfully.")
            except Exception:
                print("Error occur while updating courses !")
        else:
            print("Invalid option.")
        # --- Answer End ---

# --- Task 5: Delete ---

def delete_student(collection):
    # TODO: Delete a student by student_id
    print("\n--- Delete Student ---")
    student_id = input("Enter Student ID to delete: ").strip()
    
    # --- Answer Start: Delete document ---
    # TODO: Delete the document with the given student_id using delete_one()
    # Hint: Check deleted_count to confirm if the operation was successful

    try:
        res = collection.delete_one({"student_id": student_id})
        if res.deleted_count == 0:
            print("Student not found.")
        else:
            print("Student deleted successfully.")
    except Exception as e:
        print("Error while deleting student.")
    
    # --- Answer End ---

def clear_all_data(collection):
    print("\n--- Clear All Data ---")
    confirm = input("Are you sure you want to delete ALL students? (yes/no): ").strip().lower()
    if confirm == 'yes':
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} students.")
    else:
        print("Operation cancelled.")

# --- Task 3: Read (Advanced Search) ---

def advanced_search(collection):
    print("\n--- Advanced Search ---")
    print("1. Find by Department AND Minimum GPA ($and)")
    print("2. Find by Department A OR Department B ($or)")
    choice = input("Choose option: ")

    if choice == '1':
        dept = input("Enter Department: ").strip()
        try:
            min_gpa = float(input("Enter minimum GPA: "))
        except ValueError:
            print("Invalid GPA input.")
            return

        students = list(collection.find({
            "$and": [
                {"department": dept},
                {"gpa": {"$gte": min_gpa}}
            ]
        }))

        print(f"\nFound {len(students)} students in {dept} with GPA >= {min_gpa}:")
        for s in students:
            print(f"- {s['name']} (GPA: {s['gpa']})")

    elif choice == '2':
        dept1 = input("Enter Department 1: ").strip()
        dept2 = input("Enter Department 2: ").strip()

        students = list(collection.find({
            "$or": [
                {"department": dept1},
                {"department": dept2}
            ]
        }))

        print(f"\nFound {len(students)} students in {dept1} OR {dept2}:")
        for s in students:
            print(f"- {s['name']} (Dept: {s['department']})")
    else:
        print("Invalid option")

def main():
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
        
        if choice == '1':
            create_student(collection)
        elif choice == '2':
            get_all_students(collection)
        elif choice == '3':
            get_student_by_id(collection)
        elif choice == '4':
            search_by_gpa(collection)
        elif choice == '5':
            update_student(collection)
        elif choice == '6':
            delete_student(collection)
        elif choice == '7':
            clear_all_data(collection)
        elif choice == '8':
            advanced_search(collection)
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
