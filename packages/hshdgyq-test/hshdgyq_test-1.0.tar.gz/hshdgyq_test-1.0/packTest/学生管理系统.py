class Student:
    def __init__(self, student_id, name, sex):
        self.student_id = student_id
        self.name = name
        self.sex = sex

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Sex: {self.sex}"


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        sex = input("Enter student sex: ")
        new_student = Student(student_id, name, sex)
        self.students.append(new_student)
        print(f"Student {name} added successfully.")

    def delete_student(self):
        student_id = input("Enter the student ID to delete: ")
        student = self.find_student(student_id)
        if student:
            self.students.remove(student)
            print(f"Student {student.name} deleted successfully.")
        else:
            print("Student not found.")

    def view_students(self):
        if not self.students:
            print("No students available.")
        else:
            for student in self.students:
                print(student)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def menu(self):
        while True:
            print("\n1. Add Student")
            print("2. Delete Student")
            print("3. View Students")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.delete_student()
            elif choice == '3':
                self.view_students()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    manager = StudentManager()
    manager.menu()