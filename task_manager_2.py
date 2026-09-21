# *********************************************************
# ********** * * * * * * * * * * * * * * * * * * **********
# ********** * Software Created and Developed  * **********
# ********** *       by Simone Calvaruso       * **********
# ********** *            based on             * **********
# ********** *      HyperionDev - Task 26      * **********
# ********** *      Capstone Project III       * **********
# ********** * * * * * * * * * * * * * * * * * * **********
# *********************************************************

# ======================================== Importing Libraries ========================================
from borders import frame
import bcrypt
from datetime import datetime
import hashlib
import hmac
import math
import os
import platform
import secrets
import textwrap
# from textlinebreaker import TextLineBreaker  # Borders handles wrapping internally


# ======================================== Application Settings ========================================

# Width of the text area inside every application frame.
#
# 72 characters gives enough room for task descriptions and statistics
# without making the application unnecessarily wide.
#
# The terminal itself should ideally be at least 80 columns wide.
# A 100-120 column terminal gives the application comfortable margins.
APP_WIDTH = 72


# Fixing compatibility errors for command 'os.system(CLEAR)'.
CLEAR = "cls" if platform.system() == "Windows" else "clear"


# ======================================== Frame Helpers ========================================

def print_frame(output, **kwargs):
    """
    Print a fixed-width application frame.

    min_width and max_width are both set to APP_WIDTH so that every
    normal application frame uses the same content width.

    Individual calls can still override these values if a different
    layout is genuinely required.
    """
    kwargs.setdefault("min_width", APP_WIDTH)
    kwargs.setdefault("max_width", APP_WIDTH)
    return frame(output, **kwargs)


def input_frame(output, **kwargs):
    """
    Display a fixed-width input frame and return the user's input.

    The existing program uses window='in', which is retained for
    compatibility with the installed version of Borders.
    """
    kwargs.setdefault("min_width", APP_WIDTH)
    kwargs.setdefault("max_width", APP_WIDTH)
    kwargs.setdefault("window", "in")
    return frame(output, **kwargs)


def clear_screen():
    """Clear the terminal screen."""
    os.system(CLEAR)


def move_cursor_up():
    """
    Move the cursor up two lines.

    Borders prints the frame and leaves the cursor below it. This is
    retained from the original program's display behaviour.
    """
    print("\033[A\033[A")


# ========================================    Main function    ========================================

def main():
    users = read_users()
    tasks = read_tasks()
    superusers = read_superusers()

    # Outer loop: lets "cu" switch to a different user without restarting
    # the program. Every branch below stays the same as a single-user
    # session; only "cu" (break) and "e" (exit()) ever leave the inner loop.
    while True:
        user_id, admin = login(users, superusers)

        # Assigning different colours to the welcome window.
        col = "Red" if admin else 0

        # Printing the welcome window.
        clear_screen()

        space = " " * math.floor((APP_WIDTH - len(user_id)) / 2)

        print_frame(
            [f"{space}Welcome {user_id}"],
            frame_colour="Green",
        )
        move_cursor_up()

        # Present the options menu to the user.
        while True:
            menu = input_frame(
                entry_menu(admin),
                frame_colour=col,
            ).lower()

            # Execute the function corresponding to the selected option.
            if menu == "r" and admin:
                clear_screen()
                users = reg_user(users)

            elif menu == "cr" and admin:
                clear_screen()
                superusers = change_role(users, superusers, user_id)

            elif menu == "up" and admin:
                clear_screen()
                users = change_user_password(users, user_id)

            elif menu == "cp":
                clear_screen()
                users = change_own_password(users, user_id, admin)

            elif menu == "a":
                clear_screen()
                tasks = add_task(users, tasks)

            elif menu == "va":
                clear_screen()

                for key in tasks.keys():
                    print_frame(view_all(tasks, key))
                    move_cursor_up()

            elif menu == "vm":
                clear_screen()

                # Edit menu.
                while True:
                    # Display the current user's tasks.
                    my_keys = view_mine(user_id, tasks)
                    move_cursor_up()

                    choice = int(
                        input_frame(
                            [
                                "Please, select one of the options below:",
                                "",
                                "Your tasks are:",
                                f"{my_keys}",
                                "",
                                "Task number - to edit the task",
                                "\t0 \t  - to go back to previous menu",
                            ]
                        )
                    )

                    if choice == 0:
                        clear_screen()
                        break

                    # Proceed to the edit menu only if the selected task
                    # belongs to the logged-in user.
                    elif choice not in my_keys:
                        print_frame(
                            ["Sorry you cannot select other users' tasks."],
                            frame_colour="Bright Red",
                        )
                        move_cursor_up()

                    else:
                        edit_task(tasks, users, choice, admin)

            elif menu == "gr" and admin:
                clear_screen()

                tasks_stats(tasks)
                user_stats(users, tasks)

                print_frame(
                    [
                        "Statistics successfully saved to:",
                        "",
                        "'task_overview.txt' and 'user_overview.txt'",
                    ],
                    colour="Bright Green",
                )
                move_cursor_up()

            elif menu == "ds" and admin:
                clear_screen()

                print_frame(display_statistics(users, tasks))
                move_cursor_up()

            # Switch to a different user without exiting the program.
            elif menu == "cu":
                clear_screen()
                break

            # Exit option.
            elif menu == "e":
                clear_screen()

                print_frame(
                    [
                        "Thank you for using Task Manager.",
                        "",
                        "Goodbye!!!",
                    ],
                    colour="cyan",
                )
                exit()

            else:
                clear_screen()

                print_frame(
                    [
                        "Sorry",
                        "The option selected is not valid.",
                        "Please try again",
                    ],
                    frame_colour="Bright Red",
                )
                move_cursor_up()


# ======================================== File Reading Functions ========================================

# Function to read users from the file "users.txt".
# Stores ONLY username and password hash - no role/group information at
# all. Admin rights are tracked separately, in superusers.txt.
def read_users():
    users = {}

    # Try to read the users list from "users.txt".
    try:
        with open("users.txt", "r", encoding="utf-8") as users_read:
            for line in users_read:
                line = line.strip("\n")

                if not line.strip():
                    continue  # Skip blank lines instead of crashing on them.

                name, password = line.split(", ")
                users[name] = password

            if len(users) < 1:
                raise ValueError("users.txt is empty")

    # If the file does not exist or is empty, initialise it with
    # the default "admin" user.
    except (FileNotFoundError, ValueError):
        default_user = "admin"
        default_password = hash_value(default_user)

        users[default_user] = default_password

        append_user_line(
            f"{default_user}, {default_password}\n"
        )

    return users


# Function to read tasks from the file "tasks.txt".
def read_tasks():
    tasks = {}
    pos = 0

    # Try to read the tasks list from "tasks.txt".
    try:
        with open("tasks.txt", "r", encoding="utf-8") as tasks_read:
            for line in tasks_read:
                line = line.strip("\n")

                if not line.strip():
                    continue  # Skip blank lines instead of crashing on them.

                pos += 1
                tasks[pos] = line.split(", ")

            if pos < 1:
                raise ValueError("tasks.txt is empty")

    # If the file does not exist or is empty, initialise it with
    # an initial task for user "admin".
    except (FileNotFoundError, ValueError):
        user_task = "admin"
        new_task = "First Tasks"
        description = "Initiating tasks.txt file"
        assignment_date = datetime.today().strftime("%d %b %Y")
        due_date = datetime.today().strftime("%d %b %Y")
        completed = "Yes"

        new_task_data = [
            user_task,
            new_task,
            description,
            assignment_date,
            due_date,
            completed,
        ]

        tasks[1] = new_task_data

        with open("tasks.txt", "a", encoding="utf-8") as tasks_append:
            tasks_append.write(
                f"{user_task}, {new_task}, {description}, "
                f"{assignment_date}, {due_date}, {completed}\n"
            )

    return tasks


# Function to read admin-granted users from "superusers.txt".
#
# This is kept entirely separate from users.txt, so a regular user
# record never carries any role information.
#
# Each entry is signed with the same HMAC key, so simply adding a
# username to this file does not grant admin rights.
def read_superusers():
    superusers = {}
    tampered = []

    try:
        with open("superusers.txt", "r", encoding="utf-8") as su_read:
            for line in su_read:
                line = line.strip("\n")

                if not line.strip():
                    continue

                name, signature = line.split(", ")

                if role_is_valid(name, "admin", signature):
                    superusers[name] = signature
                else:
                    tampered.append(name)

    except FileNotFoundError:
        # No file yet simply means nobody has been granted admin rights.
        pass

    if tampered:
        print_frame(
            [
                f"Warning: admin entry for '{name}' failed its "
                "integrity check and was ignored."
                for name in tampered
            ],
            frame_colour="Bright Red",
        )
        move_cursor_up()

    return superusers


# ========================================   Login Function    ========================================

# Program will ask and validate the user login and password:
# - terminates after 10 wrong ID entries.
# - terminates after 3 wrong password entries.
#
# Admin rights:
# - the literal username "admin" always gets admin rights once the
#   password is correct, by design.
# - any other username gets admin rights only if it appears - with a
#   valid signature - in superusers.txt.
def login(users, superusers):
    clear_screen()

    message = ["Enter your ID"]

    # Ask the user for their ID.
    retry = 10
    col = 0
    fr_col = 0

    while True:
        user_id = input_frame(
            message,
            colour=col,
            frame_colour=fr_col,
        )

        move_cursor_up()

        # Check if user is registered.
        if user_id in users.keys():
            break

        # Retry count for users.
        retry -= 1

        if retry > 0:
            clear_screen()

            if 1 < retry < 6:
                col = "Bright Yellow"
            elif retry == 1:
                col = 91

            message = [
                f"Sorry, '{user_id}' is not a valid ID!",
                f"{retry} more logon attempts left",
                "",
                "Please enter a valid ID",
            ]

            fr_col = "Bright Red"
            continue

        clear_screen()

        print_frame(
            [
                "Sorry, You have reached the maximum logon attempts!",
                "Please, try again later.",
            ],
            frame_colour=fr_col,
        )

        exit()

    # Ask the user for their password.
    message = ["Enter your Password"]

    retry = 3
    col = 0
    admin = False

    while True:
        user_pw = input_frame(
            message,
            colour=col,
            frame_colour=fr_col,
        )

        move_cursor_up()

        # Check validity of password.
        if verify_value(user_pw, users[user_id]):
            if user_id == "admin":
                admin = True
            else:
                admin = user_id in superusers

            break

        # Retry count for passwords.
        retry -= 1

        if retry > 0:
            clear_screen()

            col = "Bright Yellow" if retry > 1 else 91

            message = [
                "Incorrect Password!",
                "",
                f"{retry} more logon attempts left.",
                "Please enter a valid Password",
            ]

            fr_col = "Bright Red"

        else:
            clear_screen()

            print_frame(
                [
                    "Sorry, You have reached the maximum logon attempts!",
                    "Please, try again later.",
                ],
                frame_colour=fr_col,
            )

            exit()

    return user_id, admin


# ======================================== Menu Functions ========================================

# Generate a different menu for admin or regular users.
def entry_menu(extended):
    menu_options = [
        "Please, select one of the options below:",
        "",
    ]

    if extended:
        menu_options.append(("r -- Registering a user", "Red"))
    else:
        menu_options.append("")

    menu_options.extend(
        [
            "a -- Adding a task",
            "va - View all tasks",
            "vm - View my tasks",
            "cp - Change password",
        ]
    )

    if extended:
        menu_options.extend(
            [
                ("gr - Generate Reports", "Red"),
                ("ds - Display Statistics", "Red"),
                ("cr - Change a user's role", "Red"),
                ("up - Change user's password", "Red"),
            ]
        )
    else:
        menu_options.extend(["", "", "", ""])

    menu_options.append("cu - Change user")
    menu_options.append("e -- Exit")

    return menu_options


# ======================================== User Management ========================================

# Register a new user after checking if it already exists.
#
# Admin-only - and since admin is assigning this password, no strength
# rules are enforced here.
#
# New users get no role. Admin rights are granted afterwards via
# change_role(), which writes to superusers.txt.
def reg_user(old_users):
    # Check if the ID entered already exists.
    while True:
        new_user = input_frame(["Please, enter a new user"])

        if new_user in old_users.keys():
            clear_screen()

            print_frame(
                [f"The name '{new_user}' already exists."]
            )
            move_cursor_up()

        else:
            break

    clear_screen()

    # Ask for the new user's password.
    while True:
        new_password = input_frame(
            [f"Enter a new password for '{new_user}'"]
        )
        move_cursor_up()

        pw_confirmation = input_frame(["Confirm the password"])
        move_cursor_up()

        if new_password == pw_confirmation:
            break

        clear_screen()

        print_frame(["The passwords do not match!"])
        move_cursor_up()

    new_password = hash_value(new_password)

    # Update the variable containing the users and passwords
    # and write to the file "users.txt".
    old_users[new_user] = new_password

    append_user_line(
        f"{new_user}, {new_password}\n"
    )

    clear_screen()

    print_frame(
        [f"User '{new_user}' successfully recorded!"],
        colour="green",
    )
    move_cursor_up()

    return old_users


# Shared by "cr" and "up": pick a user other than the one currently logged
# in. Returns None if there are no other users or the admin goes back.
def select_target_user(users, current_user_id):
    eligible = [
        name for name in users.keys()
        if name != current_user_id
    ]

    if not eligible:
        clear_screen()

        print_frame(
            ["There are no other users."],
            frame_colour="Bright Red",
        )
        move_cursor_up()

        return None

    while True:
        target = input_frame(
            [
                "Select a user:",
                "",
                ", ".join(eligible),
                "",
                "Enter the username, or 0 to go back",
            ]
        )

        move_cursor_up()

        if target == "0":
            clear_screen()
            return None

        if target in eligible:
            return target

        clear_screen()

        print_frame(
            [f"The user '{target}' is not registered!"],
            frame_colour="Bright Red",
        )
        move_cursor_up()


# Admin-only ("cr"): grant or revoke admin rights for another user.
def change_role(users, superusers, current_user_id):
    target_user = select_target_user(
        users,
        current_user_id,
    )

    if target_user is None:
        return superusers

    clear_screen()

    while True:
        new_group = input_frame(
            [f"Enter {target_user}'s new role: [user/admin]"]
        ).lower()

        move_cursor_up()

        if new_group in ("root", "admin"):
            new_group = "admin"
            break

        elif new_group == "user":
            break

        else:
            clear_screen()

            print_frame(
                [f"The group '{new_group}' does not exist!"],
                colour="yellow",
            )
            move_cursor_up()

    if new_group == "admin":
        superusers[target_user] = sign_role(
            target_user,
            "admin",
        )
    else:
        superusers.pop(target_user, None)

    write_superusers_to_file(superusers)

    clear_screen()

    print_frame(
        [f"'{target_user}' role changed to: {new_group}"],
        colour="green",
    )
    move_cursor_up()

    return superusers


# Any logged-in user ("cp"): change their own password.
def change_own_password(users, user_id, admin):
    clear_screen()

    if admin:
        while True:
            new_password = input_frame(
                [f"Enter a new password for '{user_id}'"]
            )
            move_cursor_up()

            pw_confirmation = input_frame(
                ["Confirm the password"]
            )
            move_cursor_up()

            if new_password == pw_confirmation:
                break

            clear_screen()

            print_frame(["The passwords do not match!"])
            move_cursor_up()

    else:
        while True:
            new_password = input_frame(
                ["Enter your new password"]
            )
            move_cursor_up()

            if new_password != user_id and len(new_password) > 3:
                pw_confirmation = input_frame(
                    ["Confirm the password"]
                )
                move_cursor_up()

                if new_password == pw_confirmation:
                    break

                clear_screen()

                print_frame(["The passwords do not match!"])
                move_cursor_up()

            else:
                clear_screen()

                print_frame(
                    [
                        "Password must be at least 4 characters long!",
                        "Password cannot be the same as your user name!",
                    ],
                    colour="red",
                )
                move_cursor_up()

    users[user_id] = hash_value(new_password)

    write_users_to_file(users)

    clear_screen()

    print_frame(
        ["Password successfully updated!"],
        colour="green",
    )
    move_cursor_up()

    return users


# Admin-only ("up"): change another user's password.
def change_user_password(users, current_user_id):
    target_user = select_target_user(
        users,
        current_user_id,
    )

    if target_user is None:
        return users

    clear_screen()

    while True:
        new_password = input_frame(
            [f"Enter a new password for '{target_user}'"]
        )
        move_cursor_up()

        pw_confirmation = input_frame(
            ["Confirm the password"]
        )
        move_cursor_up()

        if new_password == pw_confirmation:
            break

        clear_screen()

        print_frame(["The passwords do not match!"])
        move_cursor_up()

    users[target_user] = hash_value(new_password)

    write_users_to_file(users)

    clear_screen()

    print_frame(
        [f"Password for '{target_user}' successfully updated!"],
        colour="green",
    )
    move_cursor_up()

    return users


# ======================================== Task Management ========================================

# Add a new task to an existing user.
def add_task(users, old_tasks):
    # Check if the user exists.
    user_task = valid_user(users)

    new_task = input_frame(
        ["Enter the name of the task"]
    )

    description = input_frame(
        ["Enter a short description of the task"]
    )

    assignment_date = datetime.today().strftime("%d %b %Y")

    # Check the date is entered in the format "DD Mmm YYYY".
    due_date = vali_date(
        ["Enter the due date in the format (DD Mmm YYYY)"]
    )

    # Update the variable containing the tasks and write it
    # to the file "tasks.txt".
    new_task_data = [
        user_task,
        new_task,
        description,
        assignment_date,
        due_date,
        "No",
    ]

    task_num = len(old_tasks.keys())

    old_tasks[task_num + 1] = new_task_data

    with open("tasks.txt", "a", encoding="utf-8") as tasks_append:
        tasks_append.write(
            f"{user_task}, {new_task}, {description}, "
            f"{assignment_date}, {due_date}, No\n"
        )

    clear_screen()

    print_frame(
        ["New task successfully recorded!"],
        colour="green",
    )

    return old_tasks


# Format and return a single task for display.
#
# The actual wrapping is now handled by Borders/textlinebreaker.
# We deliberately do NOT manually restrict the description to 70
# characters anymore.
def view_all(tasks, task_id):
    task = tasks[task_id]

    user_task = task[0]
    new_task = task[1]
    description = task[2]
    assignment_date = task[3]
    due_date = task[4]
    completed = task[5]

    # The description label occupies part of the 72-character content
    # area. Wrapping the description here allows continuation lines to
    # align underneath the description text rather than starting at the
    # left edge of the frame.
    description_label = "Description ······ : "
    description_width = max(
        8,
        APP_WIDTH - len(description_label),
    )

    description_lines = textwrap.wrap(
        description,
        width=description_width,
        break_long_words=True,
        break_on_hyphens=False,
    )

    if not description_lines:
        description_lines = [""]

    print_tasks = [
        f"Task number ······ : {task_id}",
        f"User ············· : {user_task}",
        f"Task ············· : {new_task}",
        f"{description_label}{description_lines[0]}",
    ]

    # Continuation lines are indented to the beginning of the
    # description value.
    description_indent = " " * len(description_label)

    for line in description_lines[1:]:
        print_tasks.append(
            f"{description_indent}{line}"
        )

    print_tasks.extend(
        [
            f"Date assignment ·· : {assignment_date}",
            f"Due Date ········· : {due_date}",
            f"Task completed ··· : {completed}",
        ]
    )

    return print_tasks


# Print all the tasks recorded for the user currently logged in.
def view_mine(user_id, tasks):
    task_ids = []

    for task_id, task in tasks.items():
        if user_id == task[0]:
            print_frame(view_all(tasks, task_id))
            move_cursor_up()

            task_ids.append(task_id)

    print()

    return task_ids


# ======================================== Task Editing ========================================

# This function allows to edit a selected task.
def edit_task(tasks_for_edit, users_for_edit, to_edit, admin):
    task = tasks_for_edit[to_edit]

    clear_screen()

    print_frame(view_all(tasks_for_edit, to_edit))

    # Check if the task has not been completed and can be edited.
    if task[5] == "Yes" and not admin:
        print_frame(
            [
                "Sorry the task selected has already been completed "
                "and cannot be modified.",
                (
                    "Please select another task",
                    "centre",
                ),
            ],
            colour="yellow",
        )

        return False

    # Present the possible edits.
    while True:
        move_cursor_up()

        to_change = input_frame(
            [
                "Please, select one of the options below:",
                "",
                "1 - mark the task as completed",
                "2 - change the due date",
                "3 - change the user",
                "",
                "0 - to go back to previous menu",
            ]
        )

        # Exit editing.
        if to_change == "0":
            clear_screen()
            return False

        # Change the task status.
        elif to_change == "1":
            tasks_for_edit[to_edit][5] = "Yes"

            write_to_file(tasks_for_edit)

            clear_screen()

            print_frame(
                view_all(tasks_for_edit, to_edit)
            )

            print_frame(
                [f"Task {to_edit} marked as completed!"],
                colour="green",
            )

            return False

        # Change the due date.
        elif to_change == "2":
            clear_screen()

            print_frame(
                view_all(tasks_for_edit, to_edit)
            )

            new_due = vali_date(
                ["Enter a new due date in the format (DD Mmm YYYY)"]
            )

            tasks_for_edit[to_edit][4] = new_due
            tasks_for_edit[to_edit][5] = "No"

            write_to_file(tasks_for_edit)

            clear_screen()

            print_frame(
                view_all(tasks_for_edit, to_edit)
            )

            print_frame(
                [f"New due date for task {to_edit} is: {new_due}"],
                colour="green",
            )

            return False

        # Change the user for the selected task.
        elif to_change == "3":
            new_user = valid_user(users_for_edit)

            tasks_for_edit[to_edit][0] = new_user
            tasks_for_edit[to_edit][5] = "No"

            write_to_file(tasks_for_edit)

            clear_screen()

            print_frame(
                view_all(tasks_for_edit, to_edit)
            )

            print_frame(
                [f"Task {to_edit} assigned to: {new_user}"],
                colour="green",
            )

            return True


# ======================================== Statistics ========================================

# Execute statistics on the tasks and save them to
# "task_overview.txt".
def tasks_stats(tasks_list):
    # Calculate total number of tasks.
    total_tasks = len(tasks_list.keys())

    # Calculate total number of completed tasks.
    tot_completed = 0

    for pos in range(1, total_tasks + 1):
        if tasks_list[pos][5] == "Yes":
            tot_completed += 1

    # Calculate total number of uncompleted tasks and total number
    # of uncompleted and overdue tasks.
    tot_incomplete = 0
    tot_overdue = 0

    for pos in range(1, total_tasks + 1):
        if tasks_list[pos][5] == "No":
            if overdue(tasks_list[pos][4]):
                tot_overdue += 1

            tot_incomplete += 1

    # Calculate percentage of incomplete tasks.
    perc_incomplete = (
        tot_incomplete / total_tasks * 100
    )

    # Calculate percentage of overdue tasks.
    perc_overdue = (
        tot_overdue / total_tasks * 100
    )

    # Save results.
    to_write = [
        "\t\t\t\t  Tasks Overview",
        "",
        f"Total tasks: {total_tasks}",
        f"Completed tasks: {tot_completed}",
        f"Incomplete tasks: {tot_incomplete}",
        f"Overdue tasks: {tot_overdue}",
        f"Percent of incomplete tasks: {perc_incomplete:.2f}%",
        f"Percent of overdue tasks: {perc_overdue:.2f}%",
    ]

    with open(
        "task_overview.txt",
        "w+",
        encoding="utf-8",
    ) as write_stats:
        for item in to_write:
            write_stats.write(f"{item}\n")


# Execute statistics about users and tasks and save them to
# "user_overview.txt".
def user_stats(users_list, tasks_list):
    # Total number of users.
    total_users = len(users_list.keys())

    # Total number of tasks.
    total_tasks = len(tasks_list.keys())

    to_write = [
        "\t\t\t\t  Users Overview",
        "",
        f"Total number of users: {total_users}",
        f"Total number of tasks: {total_tasks}",
        "",
    ]

    for user in users_list.keys():
        usr_tasks = 0
        usr_completed = 0
        usr_incomplete = 0
        usr_overdue = 0

        # Calculate:
        # - total tasks assigned
        # - total completed
        # - total incomplete
        # - total incomplete and overdue
        for pos in range(1, total_tasks + 1):
            if tasks_list[pos][0] == user:
                usr_tasks += 1

                if tasks_list[pos][5] == "Yes":
                    usr_completed += 1

                else:
                    usr_incomplete += 1

                    if overdue(tasks_list[pos][4]):
                        usr_overdue += 1

        # Calculate percentage of tasks assigned to the user.
        usr_perc = f"{(usr_tasks / total_tasks * 100):.2f}%"

        if usr_tasks == 0:
            usr_comp_perc = "N/A"
            usr_incomp_perc = "N/A"
            usr_over_perc = "N/A"

        else:
            # Calculate percentage of completed tasks.
            usr_comp_perc = (
                f"{(usr_completed / usr_tasks * 100):.2f}%"
            )

            # Calculate percentage of uncompleted tasks.
            usr_incomp_perc = (
                f"{(usr_incomplete / usr_tasks * 100):.2f}%"
            )

            # Calculate percentage of uncompleted and overdue tasks.
            usr_over_perc = (
                f"{(usr_overdue / usr_tasks * 100):.2f}%"
            )

        # Format the results in an easy-to-read way.
        space_usr = "·" * (16 - len(user))
        space_tot = " " * (5 - len(str(usr_tasks)))
        space_tperc = " " * (8 - len(usr_perc))
        space_cperc = " " * (8 - len(usr_comp_perc))
        space_iperc = " " * (8 - len(usr_incomp_perc))
        space_operc = " " * (8 - len(usr_over_perc))

        output = (
            f"Number of tasks for {user} {space_usr} "
            f":{space_tot}{usr_tasks}"
        )

        output += (
            f"    Percent of    Total tasks:{space_tperc}{usr_perc}"
        )

        output += (
            f"    Completed:{space_cperc}{usr_comp_perc}"
        )

        output += (
            f"    Incomplete:{space_iperc}{usr_incomp_perc}"
        )

        output += (
            f"    Overdue:{space_operc}{usr_over_perc}"
        )

        to_write.append(output)

    # Save results to "user_overview.txt".
    with open(
        "user_overview.txt",
        "w+",
        encoding="utf-8",
    ) as write_stats:
        for item in to_write:
            write_stats.write(f"{item}\n")


# Print the reports saved in "task_overview.txt" and
# "user_overview.txt".
def display_statistics(users, tasks):
    overview_print = []

    # Read the statistics from "task_overview.txt".
    #
    # If the file does not exist, generate it first.
    while True:
        try:
            with open(
                "task_overview.txt",
                "r",
                encoding="utf-8",
            ) as task_overview:

                for line in task_overview:
                    line = line.strip("\n")

                    if line[-8:] == "Overview" or line == "":
                        overview_print.append(line)

                    else:
                        text, val = line.split(": ")

                        space1 = "·" * (
                            36 - len(text.strip(" "))
                        )

                        space2 = " " * (
                            7 - len(val.strip(" "))
                        )

                        if val[-1] == "%":
                            space2 += "    "

                        line = (
                            text
                            + " "
                            + space1
                            + " :"
                            + space2
                            + val
                        )

                        overview_print.append(line)

            break

        except FileNotFoundError:
            tasks_stats(tasks)

    overview_print.extend(["", ""])

    # Read the statistics from "user_overview.txt".
    #
    # If the file does not exist, generate it first.
    while True:
        try:
            with open(
                "user_overview.txt",
                "r",
                encoding="utf-8",
            ) as user_overview:

                for line in user_overview:
                    line = line.strip("\n")

                    if line[0:5] == "Total":
                        text, val = line.split(": ")

                        space1 = "·" * (
                            36 - len(text.strip(" "))
                        )

                        space2 = " " * (
                            7 - len(val.strip(" "))
                        )

                        line = (
                            text
                            + " "
                            + space1
                            + " :"
                            + space2
                            + val
                        )

                        overview_print.append(line)

                    elif line[0:6] == "Number":
                        overview_print.append("")

                        line0, split1 = (
                            line.strip(" ")
                            .split("Percent of    Total tasks:")
                        )

                        val2, split2 = (
                            split1.strip(" ")
                            .split("Completed:")
                        )

                        val3, split3 = (
                            split2.strip(" ")
                            .split("Incomplete:")
                        )

                        val4, split4 = (
                            split3.strip(" ")
                            .split("Overdue:")
                        )

                        val5 = split4.strip(" ")

                        line1a, val1 = line0.split(" :")

                        line1a = line1a.replace("·", "")
                        val1 = val1.strip(" ")

                        space0 = "·" * (
                            37 - len(line1a)
                        )

                        space1 = " " * (
                            7 - len(val1)
                        )

                        line1 = (
                            line1a
                            + space0
                            + " :"
                            + space1
                            + val1
                        )

                        val2 = val2.strip(" ")
                        space2 = " " * (11 - len(val2))

                        line2 = (
                            "Percent of total tasks "
                            + "·" * 14
                            + " :"
                            + space2
                            + val2
                        )

                        val3 = val3.strip(" ")
                        space3 = " " * (11 - len(val3))

                        line3 = (
                            "Percent of Completed Tasks "
                            + "·" * 10
                            + " :"
                            + space3
                            + val3
                        )

                        val4 = val4.strip(" ")
                        space4 = " " * (11 - len(val4))

                        line4 = (
                            "Percent of Incomplete Tasks "
                            + "·" * 9
                            + " :"
                            + space4
                            + val4
                        )

                        val5 = val5.strip(" ")
                        space5 = " " * (11 - len(val5))

                        line5 = (
                            "Percent of Overdue Tasks "
                            + "·" * 12
                            + " :"
                            + space5
                            + val5
                        )

                        overview_print.append(line1)
                        overview_print.append(line2)
                        overview_print.append(line3)
                        overview_print.append(line4)
                        overview_print.append(line5)

                    else:
                        overview_print.append(line)

            break

        except FileNotFoundError:
            user_stats(users, tasks)

    # Return the printout of statistics.
    return overview_print


# ======================================== File Writing Functions ========================================

# Write all the tasks to the text file.
def write_to_file(task_to_write, txt_out="tasks.txt"):
    lines = []

    for item in range(1, len(task_to_write) + 1):
        task = task_to_write[item]

        # No trailing ", " after the last field.
        #
        # A trailing comma here previously left an empty string in the
        # "completed" column every time a task was edited, silently
        # breaking status checks.
        lines.append(
            f"{task[0]}, {task[1]}, {task[2]}, "
            f"{task[3]}, {task[4]}, {task[5]}"
        )

    with open(
        txt_out,
        "w",
        encoding="utf-8",
    ) as writefile:
        writefile.write(
            "\n".join(lines) + "\n"
        )


# ======================================== Validation Functions ========================================

# Check if the task is overdue.
def overdue(duedate):
    due_date = datetime.strptime(
        duedate,
        "%d %b %Y",
    )

    today = datetime.today()

    if due_date <= today:
        return True

    return False


# Check that the date is in the correct format.
def vali_date(message):
    while True:
        date_str = input_frame(message)

        try:
            date = datetime.strptime(
                date_str,
                "%d %b %Y",
            )

            return date.strftime("%d %b %Y")

        except ValueError:
            message = [
                "Invalid date",
                "",
                "Please, enter the date in this format:",
                "(DD Mmm YYYY)",
            ]


# Check that the input username exists in the list of users.
def valid_user(existing_users):
    while True:
        new_user = input_frame(
            ["Enter a user for the new task"]
        )

        if new_user in existing_users.keys():
            return new_user

        clear_screen()

        print_frame(
            [f"The user '{new_user}' is not registered!"],
            frame_colour="Bright Red",
        )


# ======================================== Password Hashing ========================================

# Hash a value with bcrypt.
#
# bcrypt generates and embeds its own random salt in the resulting hash,
# so no external "salt"/ID argument is needed.
def hash_value(raw_value):
    raw_bytes = raw_value.encode("utf-8")

    hashed = bcrypt.hashpw(
        raw_bytes,
        bcrypt.gensalt(),
    )

    return hashed.decode("utf-8")


# Verify a raw value against a previously stored bcrypt hash.
def verify_value(raw_value, hashed_value):
    raw_bytes = raw_value.encode("utf-8")
    hashed_bytes = hashed_value.encode("utf-8")

    try:
        return bcrypt.checkpw(
            raw_bytes,
            hashed_bytes,
        )

    except ValueError:
        # Raised if hashed_value isn't a valid bcrypt hash.
        # For example, this may be leftover data from the old
        # htd_encode scheme.
        return False


# ======================================== Role Signing ========================================

# superusers.txt lists usernames that have been granted admin rights.
#
# Each entry is signed with an HMAC key stored separately in
# SECRET_KEY_FILE.
#
# Hand-adding a username to superusers.txt without knowing the key
# therefore produces an invalid signature.
#
# IMPORTANT:
# This protects against someone modifying superusers.txt without
# access to secret.key.
#
# The actual security boundary remains the operating system's file
# permissions. The application therefore attempts to restrict the
# relevant files to the account running the application.
SECRET_KEY_FILE = "secret.key"


def _load_or_create_secret_key():
    # Load the existing signing key, or generate one on first run.
    if os.path.exists(SECRET_KEY_FILE):
        with open(
            SECRET_KEY_FILE,
            "rb",
        ) as key_file:
            return key_file.read()

    key = secrets.token_bytes(32)

    with open(
        SECRET_KEY_FILE,
        "wb",
    ) as key_file:
        key_file.write(key)

    try:
        os.chmod(
            SECRET_KEY_FILE,
            0o600,
        )

    except (
        AttributeError,
        NotImplementedError,
        OSError,
    ):
        pass

    return key


SECRET_KEY = _load_or_create_secret_key()


# Produce a signature binding a username to a role.
def sign_role(name, group):
    message = f"{name}:{group}".encode("utf-8")

    return hmac.new(
        SECRET_KEY,
        message,
        hashlib.sha256,
    ).hexdigest()


# Check whether a stored role still matches its signature.
def role_is_valid(name, group, signature):
    expected = sign_role(
        name,
        group,
    )

    return hmac.compare_digest(
        expected,
        signature,
    )


# ======================================== Secure File Handling ========================================

# Append a line to users.txt and lock the file down to the owner only.
def append_user_line(line):
    with open(
        "users.txt",
        "a",
        encoding="utf-8",
    ) as users_append:
        users_append.write(line)

    try:
        os.chmod(
            "users.txt",
            0o600,
        )

    except (
        AttributeError,
        NotImplementedError,
        OSError,
    ):
        pass


# Rewrite the whole users.txt file from the in-memory users dictionary.
def write_users_to_file(users):
    lines = [
        f"{name}, {password}"
        for name, password in users.items()
    ]

    with open(
        "users.txt",
        "w",
        encoding="utf-8",
    ) as users_write:
        users_write.write(
            "\n".join(lines) + "\n"
        )

    try:
        os.chmod(
            "users.txt",
            0o600,
        )

    except (
        AttributeError,
        NotImplementedError,
        OSError,
    ):
        pass


# Rewrite the whole superusers.txt file from the in-memory
# superusers dictionary.
def write_superusers_to_file(superusers):
    lines = [
        f"{name}, {sign_role(name, 'admin')}"
        for name in superusers.keys()
    ]

    with open(
        "superusers.txt",
        "w",
        encoding="utf-8",
    ) as su_write:
        su_write.write(
            ("\n".join(lines) + "\n")
            if lines
            else ""
        )

    try:
        os.chmod(
            "superusers.txt",
            0o600,
        )

    except (
        AttributeError,
        NotImplementedError,
        OSError,
    ):
        pass


# ======================================== Program Entry Point ========================================

# Run the main function if this file is executed as a script.
if __name__ == "__main__":
    main()
