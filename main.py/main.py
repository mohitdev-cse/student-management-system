import mysql.connector
from mysql.connector import Error
from getpass import getpass


def connect_database():
    password = getpass("Enter MySQL root password: ")
    
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=password,
        database="student_management",
        use_pure=True
    )

    return connection


def add_student(connection):
    roll_no = input("Roll number: ")
    name = input("Name: ")
    course = input("Course: ")
    email = input("Email: ")
    phone = input("Phone: ")

    cursor = connection.cursor()
    query = """
        INSERT INTO students (roll_no, name, course, email, phone)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (roll_no, name, course, email, phone))
        connection.commit()
        print("Student added successfully.")
    except Error as error:
        print("Error:", error)
    finally:
        cursor.close()


def view_students(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id, roll_no, name, course, email, phone FROM students")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
    else:
        print("\n--- Student Records ---")
        for student in students:
            print(
                f"ID: {student[0]} | Roll No: {student[1]} | "
                f"Name: {student[2]} | Course: {student[3]} | "
                f"Email: {student[4]} | Phone: {student[5]}"
            )

    cursor.close()


def search_student(connection):
    roll_no = input("Enter roll number: ")

    cursor = connection.cursor()
    cursor.execute(
        "SELECT roll_no, name, course, email, phone FROM students WHERE roll_no = %s",
        (roll_no,)
    )
    student = cursor.fetchone()
    cursor.close()

    if student:
        print("\nStudent found:")
        print(f"Roll No: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Course: {student[2]}")
        print(f"Email: {student[3]}")
        print(f"Phone: {student[4]}")
    else:
        print("Student not found.")


def delete_student(connection):
    roll_no = input("Enter roll number to delete: ")

    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
    connection.commit()

    if cursor.rowcount:
        print("Student deleted successfully.")
    else:
        print("Student not found.")

    cursor.close()


def main():
    try:
        connection = connect_database()
        print("Connected to MySQL database.")

        while True:
            print("\n--- Student Management System ---")
            print("1. Add student")
            print("2. View students")
            print("3. Search student")
            print("4. Delete student")
            print("5. Exit")

            choice = input("Enter choice (1-5): ")

            if choice == "1":
                add_student(connection)
            elif choice == "2":
                view_students(connection)
            elif choice == "3":
                search_student(connection)
            elif choice == "4":
                delete_student(connection)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

        connection.close()

    except Error as error:
        print("Database connection error:", error)


if __name__=="__main__":
    main()