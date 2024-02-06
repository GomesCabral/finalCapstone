#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def create_tasks_file_if_not_exists():
    """Create tasks.txt file if it doesn't exist."""
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass


def load_tasks():
    """Load tasks from 'tasks.txt' and return a list of task dictionaries."""
    create_tasks_file_if_not_exists()

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        task_list.append(parse_task_string(t_str))

    return task_list


def parse_task_string(task_string):
    """Parse a task string and return a dictionary."""
    task_components = task_string.split(";")
    return {
        'username': task_components[0],
        'title': task_components[1],
        'description': task_components[2],
        'due_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
        'assigned_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
        'completed': True if task_components[5] == "Yes" else False
    }


def create_user_file_if_not_exists():
    """Create user.txt file with a default account if it doesn't exist."""
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")


def parse_user_data(user_data):
    """Parse user data and return a dictionary of usernames and passwords."""
    username_password = {}
    for user in user_data:
        if ';' in user:
            username, password = user.split(';', 1)
            username_password[username] = password

    return username_password


def load_user_data():
    """Load user data from 'user.txt' and return a dictionary of usernames and passwords."""
    create_user_file_if_not_exists()

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().splitlines()

    return parse_user_data(user_data)


def user_login(username_password):
    """Handle user login."""
    logged_in = False

    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        if curr_user not in username_password.keys():
            print("User does not exist")
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
        else:
            print("Login Successful!")
            logged_in = True


task_list = load_tasks()
username_password = load_user_data()


def reg_user(username_password):
    """Add a new user to the user.txt file."""
    while True:
        new_username = input("New Username: ")

        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
            continue  # Continue to the next iteration of the loop

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            update_user_file(username_password)
            break  # Exit the loop if the user is successfully registered
        else:
            print("Passwords do not match")


def update_user_file(username_password):
    """Update the user.txt file with the new user data."""
    with open("user.txt", "a") as out_file:  # Use "a" for append mode
        new_user = list(username_password.keys())[-1]  # Get the last added username
        new_password = username_password[new_user]
        out_file.write(f"{new_user};{new_password}\n")


def add_task(task_list):
    """Allow a user to add a new task to task.txt file."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    update_task_file(task_list)
    print("Task successfully added.")


def update_task_file(task_list):
    """Update the tasks.txt file with the new task data."""
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [format_task_to_string(task) for task in task_list]
        task_file.write("\n".join(task_list_to_write))


def format_task_to_string(task):
    """Format a task dictionary to a string for writing to the tasks.txt file."""
    return ";".join([
        task['username'],
        task['title'],
        task['description'],
        task['due_date'].strftime(DATETIME_STRING_FORMAT),
        task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
        "Yes" if task['completed'] else "No"
    ])


def view_all(task_list):
    """Read and print all tasks from tasks.txt file."""
    for task in task_list:
        display_task(task)


def mark_task_as_completed(task_list, task_index):
    """Mark a task as completed."""
    task_list[task_index]['completed'] = "Yes"
    update_task_file(task_list)
    print("Task marked as completed.")


def edit_task(task_list, task_index, curr_user):
    """Edit a task."""
    edited_task = task_list[task_index]

    if edited_task['completed']:
        print("Cannot edit a completed task.")
        return

    # Check if the task belongs to the currently logged-in user
    if edited_task['username'] != curr_user:
        print("You can only edit tasks assigned to you.")
        return

    print("Editing Task:")
    display_task(edited_task)

    print("Choose what to edit:")
    print("1. Title")
    print("2. Description")
    print("3. Due date of the task")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == "1":
        edited_task['title'] = input("New Title of Task: ")
    elif choice == "2":
        edited_task['description'] = input("New Description of Task: ")
    elif choice == "3":
        if not edited_task['completed']:
            while True:
                try:
                    edited_due_date = input("New Due date of task (YYYY-MM-DD): ")
                    edited_due_date_time = datetime.strptime(edited_due_date, DATETIME_STRING_FORMAT)
                    edited_task['due_date'] = edited_due_date_time
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
        else:
            print("Cannot edit the due date of a completed task.")
    else:
        print("Invalid choice.")

    update_task_file(task_list)
    print("Task successfully edited.")


def view_mine(task_list):
    """Read and print tasks assigned to the logged-in user."""
    curr_user = input("Enter your username: ")

    user_tasks = [task for task in task_list if task['username'] == curr_user]

    if not user_tasks:
        print("No tasks assigned to you.")
        return

    print("Your Tasks:")
    for i, task in enumerate(user_tasks, start=1):
        display_task(task, i)

    while True:
        task_choice = input("Enter the task number you want to select (or -1 to return to the main menu): ")

        if task_choice == "-1":
            break  # Exit the loop and return to the main menu

        try:
            task_choice = int(task_choice)
            if 1 <= task_choice <= len(user_tasks):
                selected_task_index = task_choice - 1
                selected_task = user_tasks[selected_task_index]
                display_task(selected_task)

                task_action = input("Enter 'c' to mark as completed, 'e' to edit, or any other key to return: ").lower()

                if task_action == 'c':
                    mark_task_as_completed(task_list, selected_task_index)
                elif task_action == 'e':
                    edit_task(task_list, selected_task_index, curr_user)  # Pass the current username
            else:
                print("Invalid task number. Please enter a valid task number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number or -1 to return to the main menu.")
            

def display_task(task, task_number=None):
    """Display a formatted task."""
    if task_number is not None:
        print(f"Task Number: \t {task_number}")

    disp_str = f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {task['description']}\n"
    disp_str += f"Completed: \t {'Yes' if task['completed'] else 'No'}\n"
    print(disp_str)


def display_statistics(username_password, task_list):
    """Display statistics about the number of users and tasks."""
    # Check if tasks.txt and user.txt exist, generate them if not
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print("Generating required files...")
        generate_reports(task_list)
        generate_user_overview(username_password, task_list)

    num_users = len(username_password)
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


def generate_reports(task_list):
    """Generate reports based on tasks."""
    print("Generating Reports...")

    # Counters for various statistics
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())

    # Calculate percentages
    percent_uncompleted = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    percent_overdue = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    # Create task overview file
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n\n")
        task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
        task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of tasks that are incomplete: {percent_uncompleted:.2f}%\n")
        task_overview_file.write(f"Percentage of tasks that are overdue: {percent_overdue:.2f}%\n")

    print("Reports generated. Check task_overview.txt for details.")


def generate_user_overview(username_password, task_list):
    """Generate user overview based on tasks."""
    print("Generating User Overview...")

    total_users = len(username_password)
    total_tasks = len(task_list)

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview\n\n")
        user_overview_file.write(f"Total number of users: {total_users}\n")
        user_overview_file.write(f"Total number of tasks: {total_tasks}\n\n")

        for username in username_password:
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)

            if total_tasks > 0:
                percent_user_tasks = (total_user_tasks / total_tasks) * 100
            else:
                percent_user_tasks = 0

            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            percent_completed_user_tasks = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            percent_remaining_user_tasks = 100 - percent_completed_user_tasks

            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())
            percent_overdue_user_tasks = (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0

            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total number of tasks assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {percent_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {percent_completed_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of remaining tasks: {percent_remaining_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {percent_overdue_user_tasks:.2f}%\n\n")

    print("User Overview generated. Check user_overview.txt for details.")


def main():

    user_login(username_password)

    while True:
        print()
        menu = input('''Select one of the following Options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate Reports
    ds - Display statistics
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user(username_password)

        elif menu == 'a':
            add_task(task_list)

        elif menu == 'va':
            view_all(task_list)

        elif menu == 'vm':
            view_mine(task_list)

        elif menu == 'gr':
            generate_reports(task_list)
            generate_user_overview(username_password, task_list)

        elif menu == 'ds':
            display_statistics(username_password, task_list)

        elif menu == 'e':
            print('Goodbye!!!')
            break

        else:
            print("You have made a wrong choice. Please try again")


main()