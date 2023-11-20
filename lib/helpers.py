from models.department import Department
from models.employee import Employee


def exit_program():
    print("Goodbye!")
    exit()

# We'll implement the department functions in this lesson


def list_departments():
    departments = Department.get_all()
    for department in departments:
        print(department)


def find_department_by_name():
    name = input("Enter the department's name: ")
    department = Department.find_by_name(name)
    print(department) if department else print(
        f'Department {name} not found')


def find_department_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the department's id: ")
    department = Department.find_by_id(id_)
    print(department) if department else print(f'Department {id_} not found')


def create_department():
    name = input("Enter the department's name: ")
    location = input("Enter the department's location: ")
    try:
        department = Department.create(name, location)
        print(f'Success: {department}')
    except Exception as exc:
        print("Error creating department: ", exc)


def update_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        try:
            name = input("Enter the department's new name: ")
            department.name = name
            location = input("Enter the department's new location: ")
            department.location = location

            department.update()
            print(f'Success: {department}')
        except Exception as exc:
            print("Error updating department: ", exc)
    else:
        print(f'Department {id_} not found')


def delete_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        department.delete()
        print(f'Department {id_} deleted')
    else:
        print(f'Department {id_} not found')


# You'll implement the employee functions in the lab

def list_employees():
    pass


def find_employee_by_name():
    pass


def find_employee_by_id():
    pass


def create_employee():
    pass


def update_employee():
    try:
        employee_id = input("Enter the employee id: ")

        if not employee_exists_in_database(employee_id):
            print("Error: Employee not found in the database.")
            return
        new_name = input("Enter the new name: ")

        # Prompt for a new job title
        new_job_title = input("Enter the new job title: ")

        # Prompt for the employee's new department id
        new_department_id = input("Enter the new department id: ")

        # Update the employee in the database
        update_employee_in_database(employee_id, new_name, new_job_title, new_department_id)

        # Print a success message
        print("Employee information updated successfully.")

    except Exception as e:
        # Print an error message if an exception is thrown
        print(f"Error: {e}")


def delete_employee():
    try:
        # Prompt for and read in the employee id
        employee_id = input("Enter the employee id: ")

        # Check if the employee is in the database
        if employee_exists_in_database(employee_id):
            # Delete the employee from the database
            delete_employee_from_database(employee_id)

            # Print a confirmation message
            print(f"Employee with ID {employee_id} deleted successfully.")
        else:
            # Print an error message if the employee is not in the database
            print("Error: Employee not found in the database.")

    except Exception as e:
        # Print an error message if an exception is thrown
        print(f"Error: {e}")



def list_department_employees():
    try:
        # Prompt for and read in the department id
        department_id = input("Enter the department id: ")

        # Find the department with the given id from the database
        department = get_department_by_id(department_id)

        # Check if the department exists in the database
        if department:
            # Get the department's employees using the employees() instance method
            department_employees = department.employees()

            # Loop to print each employee's data on a separate line
            for employee in department_employees:
                print_employee_data(employee)

        else:
            # Print an error message if the department does not exist in the database
            print("Error: Department not found in the database.")

    except Exception as e:
        # Print an error message if an exception is thrown
        print(f"Error: {e}")