
from datetime import datetime

# --------------------------------------------------
# FILE SETUP
# --------------------------------------------------

# Create the files if they do not already exist.
for filename in ["user.txt", "tasks.txt"]:
    with open(filename, "a") as file:
        pass


# Read usernames and passwords.
users = {}

with open("user.txt", "r") as user_file:
    for line in user_file:
        line = line.strip()

        # Ignore blank lines.
        if line == "":
            continue

        username, password = line.split(", ", 1)
        users[username] = password


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def append_record(filename, record):
    """Append a record without joining it to the previous line."""

    with open(filename, "a+", encoding="utf-8") as file:
        file.seek(0, 2)

        if file.tell() > 0:
            file.seek(file.tell() - 1)
            last_character = file.read(1)

            if last_character != "\n":
                file.write("\n")

        file.seek(0, 2)
        file.write(record + "\n")


def load_tasks():
    """Read tasks from tasks.txt."""

    tasks = []

    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            line = line.strip()

            if line == "":
                continue

            task = line.split(", ", 5)

            if len(task) == 6:
                tasks.append(task)

    return tasks


def save_tasks(tasks):
    """Save all tasks to tasks.txt."""

    with open("tasks.txt", "w") as task_file:
        for task in tasks:
            task_file.write(", ".join(task) + "\n")


def display_task(number, task):
    """Display one task in a readable format."""

    print("\n--------------------------------")
    print(f"Task number: {number}")
    print(f"Assigned to: {task[0]}")
    print(f"Task: {task[1]}")
    print(f"Description: {task[2]}")
    print(f"Date assigned: {task[3]}")
    print(f"Due date: {task[4]}")
    print(f"Completed: {task[5]}")
    print("--------------------------------")


def valid_date(date_text):
    """Check whether a date follows the required format."""

    try:
        datetime.strptime(date_text, "%d %b %Y")
        return True
    except ValueError:
        return False


# --------------------------------------------------
# REGISTER A USER
# --------------------------------------------------

def reg_user():

    while True:
        new_username = input("Enter a new username: ").strip()

        if new_username == "":
            print("Username cannot be blank.")

        elif new_username in users:
            print("That username already exists. Please try another.")

        else:
            break

    new_password = input("Enter a new password: ")
    confirm_password = input("Confirm the password: ")

    if new_password == "":
        print("Password cannot be blank.")

    elif new_password == confirm_password:

        append_record(
            "user.txt",
            f"{new_username}, {new_password}"
        )

        users[new_username] = new_password

        print("User registered successfully!")

    else:
        print("Passwords do not match. User not registered.")


# --------------------------------------------------
# ADD A TASK
# --------------------------------------------------

def add_task():

    assigned_user = input("Enter the assigned username: ").strip()

    if assigned_user not in users:
        print("Username does not exist.")

    else:
        title = input("Enter the task title: ").strip()
        description = input("Enter the task description: ").strip()

        while True:
            due_date = input("Enter the due date (e.g. 20 Nov 2026): ")

            if valid_date(due_date):
                break

            print("Invalid date. Please use DD Mon YYYY.")

        assigned_date = datetime.now().strftime("%d %b %Y")

        task = [
            assigned_user,
            title,
            description,
            assigned_date,
            due_date,
            "No"
        ]

        append_record("tasks.txt", ", ".join(task))

        print("Task added successfully!")


# --------------------------------------------------
# VIEW ALL TASKS
# --------------------------------------------------

def view_all():

    tasks = load_tasks()

    if not tasks:
        print("No tasks have been recorded.")

    else:
        for number, task in enumerate(tasks, start=1):
            display_task(number, task)


# --------------------------------------------------
# VIEW MY TASKS
# --------------------------------------------------

def view_mine():

    tasks = load_tasks()

    my_tasks = [
        task for task in tasks
        if task[0] == username
    ]

    if not my_tasks:
        print("You have no tasks assigned to you.")
        return

    while True:

        print("\nMY TASKS")

        for number, task in enumerate(my_tasks, start=1):
            display_task(number, task)

        print("\nEnter a task number to select it.")
        print("Enter -1 to return to the main menu.")

        try:
            choice = int(input("Select a task: "))

        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == -1:
            break

        if choice < 1 or choice > len(my_tasks):
            print("Invalid task number.")
            continue

        selected_task = my_tasks[choice - 1]
        selected_task = my_tasks[choice - 1]

        if selected_task[5].lower() == "yes":
            print("This task has already been completed.")
            continue

        print("\nSelect an action:")
        print("c - Mark task as complete")
        print("e - Edit task")
        print("b - Go back")

        action = input("Enter your choice: ").lower()

        if action == "c":

            selected_task[5] = "Yes"
            save_tasks(tasks)

            print("Task marked as complete.")

        elif action == "e":

            print("Press Enter to keep the existing value.")

            new_username = input(
                "Enter new assigned username: "
            ).strip()

            if new_username != "":
                if new_username in users:
                    selected_task[0] = new_username
                    print("Assigned username updated.")
                else:
                    print("Username does not exist. No change made.")

            while True:

                new_due_date = input(
                    "Enter new due date: "
                ).strip()

                if new_due_date == "":
                    break

                if valid_date(new_due_date):
                    selected_task[4] = new_due_date
                    print("Due date updated.")
                    break

                print("Invalid date. Please use DD Mon YYYY.")

            save_tasks(tasks)

        elif action == "b":
            continue

        else:
            print("Invalid option.")


# --------------------------------------------------
# VIEW COMPLETED TASKS
# --------------------------------------------------

def view_completed():

    tasks = load_tasks()

    completed_tasks = [
        task for task in tasks
        if task[5].lower() == "yes"
    ]

    if not completed_tasks:
        print("There are no completed tasks.")

    else:
        for number, task in enumerate(completed_tasks, start=1):
            display_task(number, task)


# --------------------------------------------------
# DELETE A TASK
# --------------------------------------------------

def delete_task():

    tasks = load_tasks()

    if not tasks:
        print("There are no tasks to delete.")
        return

    for number, task in enumerate(tasks, start=1):
        display_task(number, task)
    try:
        choice = int(input("Enter the task number to delete: "))

    except ValueError:
        print("Please enter a valid number.")
        return

    if choice < 1 or choice > len(tasks):
        print("Invalid task number.")
        return

    deleted_task = tasks.pop(choice - 1)

    save_tasks(tasks)

    print(f"Task '{deleted_task[1]}' deleted successfully.")


# --------------------------------------------------
# GENERATE REPORTS
# --------------------------------------------------

def generate_reports():

    tasks = load_tasks()

    total_tasks = len(tasks)

    completed_tasks = [
        task for task in tasks
        if task[5].lower() == "yes"
    ]

    incomplete_tasks = [
        task for task in tasks
        if task[5].lower() != "yes"
    ]

    overdue_tasks = []

    today = datetime.now().date()

    for task in incomplete_tasks:

        try:
            due_date = datetime.strptime(
                task[4], "%d %b %Y"
            ).date()

            if due_date < today:
                overdue_tasks.append(task)

        except ValueError:
            continue

    percentage_incomplete = (
        len(incomplete_tasks) / total_tasks * 100
        if total_tasks > 0 else 0
    )

    percentage_overdue = (
        len(overdue_tasks) / total_tasks * 100
        if total_tasks > 0 else 0
    )

    # Create task overview report.

    with open("task_overview.txt", "w") as report:

        report.write("TASK OVERVIEW\n")
        report.write("==============================\n")

        report.write(f"Total tasks: {total_tasks}\n")
        report.write(f"Completed tasks: {len(completed_tasks)}\n")
        report.write(f"Incomplete tasks: {len(incomplete_tasks)}\n")
        report.write(f"Overdue tasks: {len(overdue_tasks)}\n")

        report.write(
            f"Percentage incomplete: {percentage_incomplete:.1f}%\n"
        )

        report.write(
            f"Percentage overdue: {percentage_overdue:.1f}%\n"
        )

    # Create user overview report.

    with open("user_overview.txt", "w") as report:

        report.write("USER OVERVIEW\n")
        report.write("==============================\n")

        report.write(f"Total users: {len(users)}\n")
        report.write(f"Total tasks: {total_tasks}\n\n")

        for user in users:

            user_tasks = [
                task for task in tasks
                if task[0] == user
            ]

            user_completed = [
                task for task in user_tasks
                if task[5].lower() == "yes"
            ]

            user_incomplete = [
                task for task in user_tasks
                if task[5].lower() != "yes"
            ]

            user_overdue = []

            for task in user_incomplete:

                try:
                    due_date = datetime.strptime(
                        task[4], "%d %b %Y"
                    ).date()

                    if due_date < today:
                        user_overdue.append(task)

                except ValueError:
                    continue

            total_user_tasks = len(user_tasks)

            percentage_assigned = (
                total_user_tasks / total_tasks * 100
                if total_tasks > 0 else 0
            )

            percentage_completed = (
                len(user_completed) / total_user_tasks * 100
                if total_user_tasks > 0 else 0
            )

            percentage_user_incomplete = (
                len(user_incomplete) / total_user_tasks * 100
                if total_user_tasks > 0 else 0
            )

            percentage_user_overdue = (
                len(user_overdue) / total_user_tasks * 100
                if total_user_tasks > 0 else 0
            )

            report.write(f"Username: {user}\n")
            report.write(f"Tasks assigned: {total_user_tasks}\n")

            report.write(
                f"Percentage of all tasks assigned: "
                f"{percentage_assigned:.1f}%\n"
            )

            report.write(
                f"Percentage completed: "
                f"{percentage_completed:.1f}%\n"
            )

            report.write(
                f"Percentage incomplete: "
                f"{percentage_user_incomplete:.1f}%\n"
            )

            report.write(
                f"Percentage overdue: "
                f"{percentage_user_overdue:.1f}%\n\n"
            )

    print("Reports generated successfully!")


# --------------------------------------------------
# DISPLAY STATISTICS
# --------------------------------------------------

def display_statistics():

    # Generate fresh reports before displaying them.
    generate_reports()

    print("\nTASK OVERVIEW")
    print("==============================")

    with open("task_overview.txt", "r") as report:
        print(report.read())

    print("\nUSER OVERVIEW")
    print("==============================")

    with open("user_overview.txt", "r") as report:
        print(report.read())


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

while True:

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")

    if username in users and users[username] == password:

        print("Login successful!")
        break

    else:
        print("Invalid username or password. Please try again.")


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

while True:

    print("\nSelect one of the following options:")

    if username == "admin":

        print("r - Register a user")
        print("a - Add a task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("vc - View completed tasks")
        print("del - Delete a task")
        print("ds - Display statistics")
        print("gr - Generate reports")
        print("e - Exit")

    else:

        print("a - Add a task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("e - Exit")

    choice = input("Enter your choice: ").lower().strip()

    if choice == "r" and username == "admin":
        reg_user()

    elif choice == "a":
        add_task()

    elif choice == "va":
        view_all()

    elif choice == "vm":
        view_mine()

    elif choice == "vc" and username == "admin":
        view_completed()

    elif choice == "del" and username == "admin":
        delete_task()

    elif choice == "ds" and username == "admin":
        display_statistics()

    elif choice == "gr" and username == "admin":
        generate_reports()

    elif choice == "e":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
