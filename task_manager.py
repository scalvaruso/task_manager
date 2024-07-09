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
import ctypes
from datetime import datetime
import math
import os
import platform
# from textlinebreaker import split_line # Implementation needed

# Fixing compatibility errors for command 'os.system(CLEAR)'
CLEAR = "cls" if platform.system() == "Windows" else "clear"


# ========================================    Main function    ========================================
def main():
    users = read_users()
    tasks = read_tasks()

    # Login the user.
    user_id, admin = login(users)
    # Assigning differnt colors to the welcome window
    col = "Red" if admin else 0
    # Printing the welcome window
    os.system(CLEAR)
    space = " " * math.floor((32 - len(user_id)) / 2)
    frame([f"{space}Welcome {user_id}"], frame_colour="Green", min_width=48)
    print("\033[A\033[A") # NOTE This is to move cursor up one line
    
    # Present the options menu to the user.
    while True:
        menu = frame(entry_menu(admin), frame_colour=col, window="in").lower()
        
        # Execute the function corresponding to the selected option.
        if menu == "r" and admin:
            os.system(CLEAR)
            users = reg_user(users)
        elif menu == "a":
            os.system(CLEAR)
            tasks = add_task(users, tasks)
        elif menu == "va":
            os.system(CLEAR)
            for key in tasks.keys():
                frame(view_all(tasks, key),max_width=70)
                print("\033[A\033[A") # NOTE This is to move cursor up one line
        elif menu == "vm":
            os.system(CLEAR)
            check = True  # Variable to check if the tasks should be printed or not.

            # Edit menu.
            while True:
                # The following 'if' allows to print the tasks only the first time,
                # and when the user connected to the tasks has been changed.
                #if check:
                my_keys = view_mine(user_id, tasks)
                print("\033[A\033[A") # NOTE This is to move cursor up one line
                choice = int(frame([
                    "Please, select one of the options below:",
                    "",
                    "Your task are:",
                    f"{my_keys}",
                    "",
                    "Task number - to edit the task",
                    "\t0 \t  - to go back to previous menu",
                    ], window="in"))
                if choice == 0:
                    os.system(CLEAR)
                    break
                # Proceed to the edit menu only if the task selected belong to the user logged in.
                elif choice not in my_keys:
                    frame(["Sorry you cannot select others tasks."], frame_colour="Bright Red")
                    check = False
                    pass
                else:
                    check = edit_task(tasks, users, choice, admin)
    
        elif menu == "gr" and admin:
            os.system(CLEAR)
            tasks_stats(tasks)
            user_stats(users, tasks)
            frame(["Statistics successfully saved to:","","'task_overview.txt' and 'user_overview.txt'"], colour="Bright Green")
            print("\033[A\033[A") # NOTE This is to move cursor up one line
        elif menu == "ds" and admin:
            os.system(CLEAR)
            frame(display_statistics(users, tasks))
            print("\033[A\033[A") # NOTE This is to move cursor up one line
        # Exit option
        elif menu == "e":
            os.system(CLEAR)
            frame(["Thank you for using Task Manager.","","Goodbye!!!"], colour="cyan")
            exit()
        else:
            os.system(CLEAR)
            frame(["Sorry","The option selected is not valid.","Please Try again"], frame_colour="Bright Red")
            print("\033[A\033[A") # NOTE This is to move cursor up one line


# Function to read users from the file "users.txt"
def read_users():
    users = {}
    # Try to read the users lists from "users.txt"
    try:
        with open("users.txt", "r", encoding="utf-8") as users_read:
            for line in users_read:
                name, group, password = line.split(", ")
                users[name] = (group, password.strip("\n"))
            if len(users) < 1:
                raise ValueError
    # If file does not exists or is empty initialise it with the default "admin" user
    except:
        default_user = "admin"
        default_group = htd_encode("root", default_user)
        default_password = htd_encode(default_user, default_user)
        users[default_user] = (default_group, default_password)
        with open("users.txt", "a", encoding="utf-8") as users_append:
            users_append.write(f"{default_user}, {default_group}, {default_password}\n")
    return users


# Function to read tasks from the file "tasks.txt"
def read_tasks():
    tasks = {}
    # Try to read the tasks lists from "tasks.txt"
    try:
        with open("tasks.txt", "r", encoding="utf-8") as tasks_read:
            for pos, line in enumerate(tasks_read, 1):
                line_split = line.split(", ")
                line_split[-1] = line_split[-1].strip("\n")
                tasks[pos] = line_split
            if pos < 1:
                raise ValueError
    # If file does not exists or is empty initialise it with an initial task for user "admin"
    except:
        user_task = "admin"
        new_task = "First Tasks"
        description = "Initiating tasks.txt file"
        assignment_date = datetime.today().strftime("%d %b %Y")
        due_date = datetime.today().strftime("%d %b %Y")
        completed = "Yes"
        new_task_data = [user_task, new_task, description, assignment_date, due_date, completed]
        tasks[1] = new_task_data
        with open("tasks.txt", "a", encoding="utf-8") as tasks_append:
            tasks_append.write(f"{user_task}, {new_task}, {description}, {assignment_date}, {due_date}, {completed}\n")
    return tasks


# ========================================   Login Function    ========================================
# Program will ask and validate the user login and password:
# - terminates after 10 wrong ID entries.
# - terminates after 3 wrong password entries.
def login(login):
    os.system(CLEAR)
    message = ["Enter your ID"]
    # Ask the user for their ID.
    retry = 10
    col = 0
    fr_col = 0
    while True:
        id = frame(message, colour=col, frame_colour=fr_col, window="in")
        print("\033[A\033[A") # NOTE This is to move cursor up one line
        # Check if user is registered.
        if id in login.keys():
            break
        # Retry count for users.
        retry -= 1
        if retry > 0:
            os.system(CLEAR)
            if 1 < retry < 6:
                col = "Bright Yellow"
            elif retry == 1:
                col = 91
            message = [f"Sorry, '{id}' is not a valid ID!",f"{retry} more logon attempts left","","Please enter a valid ID"]
            fr_col = "Bright Red"
            continue
        else:
            os.system(CLEAR)
            frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."], frame_colour=fr_col)
            exit()

    # Ask the user for their password.
    message = ["Enter your Password"]
    retry = 3
    col = 0
    admin = False
    while True:
        user_pw = frame(message, colour=col, frame_colour=fr_col, window="in")
        print("\033[A\033[A") # NOTE This is to move cursor up one line
        # Check validity of password.
        if htd_encode(user_pw, id) == login[id][1]:
            admin = login[id][0] == htd_encode("root", id)
            break
        # Retry count for passwords.
        retry -= 1
        if retry > 0:
            os.system(CLEAR)
            col = "Bright Yellow" if retry > 1 else 91
            message = ["Incorrect Password!","",f"{retry} more logon attempts left.","Please enter a valid Password"]
            fr_col = "Bright Red"
        else:
            os.system(CLEAR)
            frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."], frame_colour=fr_col)
            exit()
    return id, admin


# Generate a different menu for admin or users.
def entry_menu(extended):
    menu_options = ["Please, select one of the options below:",""]
    if extended:
        menu_options.append(("r  - Registering a user","Red"))
    else:
        menu_options.append("")
    menu_options.extend([
        "a  - Adding a task",
        "va - View all tasks",
        "vm - View my tasks"
    ])
    if extended:
        menu_options.extend([
            ("gr - Generate Reports", "Red"),
            ("ds - Display Statistics", "Red")
        ])
    else:
        menu_options.extend(["",""])
    menu_options.append("e  - Exit")
    return menu_options


# Register a new user after checking if it is already existing.
def reg_user(old_users):
    # Check if the ID entered already exists.
    while True:
        new_user = frame(["Please, enter a new user"], window="in")
        if new_user in old_users.keys():
            os.system(CLEAR)
            frame([f"The name '{new_user}' is already existing."])
            print("\033[A\033[A") # NOTE This is to move cursor up one line
        else:
            break

    os.system(CLEAR)

    # Ask if the new user should be added to the admin group
    while True:
        new_user_group = frame([f"Please, enter {new_user}'s group: [user/admin]"], window="in")
        print("\033[A\033[A") # NOTE This is to move cursor up one line
        if new_user_group in ["root", "admin"]:
            group = htd_encode(new_user_group, new_user)
            break
        elif new_user_group == "user":
            group = htd_encode(new_user_group, new_user)
            break
        else:
            os.system(CLEAR)
            frame([f"The group '{new_user_group}' does not exist!"], colour="yellow")
            print("\033[A\033[A") # NOTE This is to move cursor up one line
    os.system(CLEAR)

    # Ask for a valid password.
    while True:
        new_password = frame([f"Enter a new password for '{new_user}'"], window="in")
        print("\033[A\033[A") # NOTE This is to move cursor up one line
        if new_password not in ["user", "admin", "root", new_user] and len(new_password) > 3:
            pw_confirmation = frame(["Confirm the password"], window="in")
            if new_password == pw_confirmation:
                break
            # add check for empty passwords, also to taskmaster.py
            else:
                os.system(CLEAR)
                frame(["The passwords do not match!"])
                print("\033[A\033[A") # NOTE This is to move cursor up one line
        else:
            os.system(CLEAR)
            frame(["Password must be at least 4 characters long!", "Password cannot be the same as the user name or group!"], colour="red")
            print("\033[A\033[A") # NOTE This is to move cursor up one line
    new_password = htd_encode(new_password, new_user)

    # Update the variable containing the users and passwords
    # and write to the file 'users.txt'.
    old_users[new_user] = (group, new_password)
    with open("users.txt", "a", encoding="utf-8") as users_append:
        users_append.write(f"\n{new_user}, {group}, {new_password}")
    os.system(CLEAR)
    frame([f"User '{new_user}' successfully recorded!"], colour="green")
    print("\033[A\033[A") # NOTE This is to move cursor up one line
    return old_users


# Add a new task to an existing user.
def add_task(users, old_tasks):
    # Check if the user exist.
    user_task = valid_user(users)
    new_task = frame(["Enter the name of the task"], window="in")
    description = frame(["Enter a short description of the task"], window="in")
    assignment_date = datetime.today().strftime("%d %b %Y")

    # Check the date is entered in the format 'DD Mmm YYYY'.
    due_date = vali_date(["Enter the due date in the format (DD Mmm YYYY)"])

    # Update the variable containing the tasks
    # and write it to the file 'tasks.txt'.
    new_task_data = [user_task, new_task, description, assignment_date, due_date, "No"]
    task_num = len(old_tasks.keys())
    old_tasks[task_num + 1] = new_task_data
    with open("tasks.txt", "a", encoding="utf-8") as tasks_append:
        tasks_append.write(f"\n{user_task}, {new_task}, {description}, {assignment_date}, {due_date}, No")
    os.system(CLEAR)
    frame(["New task successfully recorded!"], colour="green")
    return old_tasks


# Format and print all the tasks recorded.
def view_all(tasks, task_id):
    task = tasks[task_id]
    user_task = task[0]
    new_task = task[1]
    description_line = (f"Description ······ :\t{task[2]}").strip("\n")
    description = ""
    assignment_date = task[3]
    due_date = task[4]
    completed = task[5]

    print_tasks = [f"Task number ······ :\t{task_id}"]
    print_tasks.append(f"User ············· :\t{user_task}")
    print_tasks.append(f"Task ············· :\t{new_task}")

    words = description_line.split(" ")
    # Splits lines wider than 70 characters 
    for word in words:
        word = word.replace("\t", "    ")
        if len(description+word) < 71:
            description += word + " "
        else:
            print_tasks.append(description)
            description = "\t"*6 + word + " "
        description = description.replace("\t", "    ")

    print_tasks.append(description)
    print_tasks.append(f"Date assignement · :\t{assignment_date}")
    print_tasks.append(f"Due Date ········· :\t{due_date}")
    print_tasks.append(f"Task completed ··· :\t{completed}")

    return print_tasks

    # Implementation needed to use the following code
    """
    return [
        f"Task number ······ :\t{task_id}",
        f"User ············· :\t{user_task}",
        f"Task ············· :\t{new_task}",
        f"Description ······ :\t{description}",
        f"Date assignement · :\t{assignment_date}",
        f"Due Date ········· :\t{due_date}",
        f"Task completed ··· :\t{completed}"
    ]

    """


# Print all the tasks recorded for the user logged in.
def view_mine(user_id, tasks):
    task_ids = []
    for task_id, task in tasks.items():
        if user_id == task[0]:
            frame(view_all(tasks, task_id))
            print("\033[A\033[A") # NOTE This is to move cursor up one line
            task_ids.append(task_id)
    print()
    return task_ids


# This function allows to edit a selected task.
def edit_task(tasks_for_edit, users_for_edit, to_edit, admin):
    task = tasks_for_edit[to_edit]
    os.system(CLEAR)
    frame(view_all(tasks_for_edit,to_edit))

    # Check if the task has not been completed and can be edited.
    if task[5] == "Yes" and not admin:
        frame(["Sorry the task selected has been already completed and cannot be modified",
        ("Please select another task","centre"),
        ], colour="yellow", max_width=73)
        return False

    # Present the possible edits.
    while True:
        print("\033[A\033[A") # NOTE This is to move cursor up one line
        to_change = frame(
            ["Please, select one of the options below:",
            "",
            "1 - mark the task as completed",
            "2 - change the due date",
            "3 - change the user",
            "",
            "0 - to go back to previous menu",
            ],
            window="in"
            )

        # Exit editing.
        if to_change == "0":
            os.system(CLEAR)
            return False

        # Change the task status.
        elif to_change == "1":
            tasks_for_edit[to_edit][5] = "Yes"
            write_to_file(tasks_for_edit)
            os.system(CLEAR)
            frame(view_all(tasks_for_edit,to_edit))
            frame([f"Task {to_edit} marked as completed!"], colour="green")
            return False

        # Change the due date.
        elif to_change == "2":
            os.system(CLEAR)
            frame(view_all(tasks_for_edit,to_edit))
            new_due = vali_date(["Enter a new due date in the format (DD Mmm YYYY)"])
            tasks_for_edit[to_edit][4] = new_due
            tasks_for_edit[to_edit][5] = "No"
            write_to_file(tasks_for_edit)
            os.system(CLEAR)
            frame(view_all(tasks_for_edit,to_edit))
            frame([f"New due date for task {to_edit} is: {new_due}"], colour="green")
            return False
        
        # Change the user for the selected task.
        elif to_change == "3":
            new_user = valid_user(users_for_edit)
            tasks_for_edit[to_edit][0] = new_user
            tasks_for_edit[to_edit][5] = "No"
            write_to_file(tasks_for_edit)
            os.system(CLEAR)
            frame(view_all(tasks_for_edit,to_edit))
            frame([f"Task {to_edit} assigned to: {new_user}"], colour="green")
            return True


# Execute statistics on the tasks and save them to 'task_overview.txt'.
def tasks_stats(tasks_list):
    # Calculate total number of tasks.
    total_tasks = len(tasks_list.keys())

    # Calculate total number of completed tasks.
    tot_completed = 0
    for pos in range(1,total_tasks+1):
        if tasks_list[pos][5] == "Yes":
            tot_completed += 1

    # Calculate total number of uncompleted tasks
    # and total number of uncompleted and overdue tasks.
    tot_incomplete = 0
    tot_overdue = 0
    for pos in range(1,total_tasks+1):
        if tasks_list[pos][5] == "No":
            if overdue(tasks_list[pos][4]):
                tot_overdue += 1
            tot_incomplete += 1

    # Calculate Percent of incomplete tasks.
    perc_incomplete = tot_incomplete/total_tasks * 100

    # Calculate Percent of overdue tasks.
    perc_overdue = tot_overdue/total_tasks * 100

    # Save results.
    to_write = ["\t\t\t\t  Tasks Overview",
        "",
        f"Total tasks: {total_tasks}",
        f"Completed tasks: {tot_completed}",
        f"Incomplete tasks: {tot_incomplete}",
        f"Overdue tasks: {tot_overdue}",
        f"Percent of incomplete tasks: {perc_incomplete:.2f}%",
        f"Percent of overdue tasks: {perc_overdue:.2f}%",
    ]
    with open("task_overview.txt", "w+", encoding="utf-8") as write_stats:
        for item in to_write:
            write_stats.write(f"{item}\n")


# Execute statistics about users and tasks and save them to 'user_overview.txt'.
def user_stats(users_list, tasks_list):
    # Total number of users.
    total_users = len(users_list.keys())

    # Total number of tasks.
    total_tasks = len(tasks_list.keys())
    to_write = ["\t\t\t\t  Users Overview",
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
        # - total incomplete and overdue.
        for pos in range(1,total_tasks+1):
            if tasks_list[pos][0] == user:
                usr_tasks += 1
                if tasks_list[pos][5]=="Yes":
                    usr_completed += 1
                else:
                    usr_incomplete += 1
                    if overdue(tasks_list[pos][4]):
                        usr_overdue += 1

        # Calculate Percent of tasks assigned to the user.
        usr_perc = f"{(usr_tasks/total_tasks * 100):.2f}%"
        if usr_tasks == 0:
            usr_comp_perc = "N/A"
            usr_incomp_perc = "N/A"
            usr_over_perc = "N/A"
            pass
        else:
   
            # Calculate Percent of completed tasks.
            usr_comp_perc = f"{(usr_completed/usr_tasks * 100):.2f}%"

            # Calculate Percent of uncompleted tasks.
            usr_incomp_perc = f"{(usr_incomplete/usr_tasks * 100):.2f}%"

            # Calculate Percent of uncompleted and overdue tasks.
            usr_over_perc = f"{(usr_overdue/usr_tasks * 100):.2f}%"

        # Format the results in an easy to read way.
        space_usr = "·" * (16 - len(user))
        space_tot = " " * (5 - len(str(usr_tasks)))
        space_tperc = " " * (8 - len(usr_perc))
        space_cperc = " " * (8 - len(usr_comp_perc))
        space_iperc = " " * (8 - len(usr_incomp_perc))
        space_operc = " " * (8 - len(usr_over_perc))
        output = f"Number of tasks for {user} {space_usr} :{space_tot}{usr_tasks}"
        output += f"    Percent of    Total tasks:{space_tperc}{usr_perc}"
        output += f"    Completed:{space_cperc}{usr_comp_perc}"
        output += f"    Incomplete:{space_iperc}{usr_incomp_perc}"
        output += f"    Overdue:{space_operc}{usr_over_perc}"
        to_write.append(output)

    # Save results to the file 'user_overview.txt'.
    with open("user_overview.txt", "w+", encoding="utf-8") as write_stats:
        for item in to_write:
            write_stats.write(f"{item}\n")


# Print out the reports saved in 'task_overview.txt' and 'user_overview.txt'.
def display_statistics(users, tasks):
    overview_print = []

    # Read the statistics from the file 'task_overview.txt'
    # and create a formatting for printing it out.
    # If the file does not exist, it execute the function to generate the file.
    while True:
        try:
            with open("task_overview.txt", "r", encoding="utf-8") as task_overview:
                for line in task_overview:
                    line = line.strip("\n")
                    if line[-8:]=="Overview" or line=="":
                        overview_print.append(line)
                    else:
                        text, val = line.split(": ")
                        space1 = "·" * (36 - len(text.strip(" ")))
                        space2 = " " * (7 - len(val.strip(" ")))
                        if val[-1] == "%":
                            space2 += "    "
                        line = text + " " + space1 + " :" + space2 + val
                        overview_print.append(line)
            break

        except FileNotFoundError:
            tasks_stats(tasks)

    overview_print.extend(["", ""])
    
    # Read the statistics from the file 'user_overview.txt'
    # and create a formatting for printing it out.
    # If the file does not exist, it execute the function to generate the file.
    while True:
        try:
            with open("user_overview.txt", "r", encoding="utf-8") as user_overview:
                for line in user_overview:
                    line = line.strip("\n")
                    if line[0:5] == "Total":
                        text, val = line.split(": ")
                        space1 = "·" * (36 - len(text.strip(" ")))
                        space2 = " " * (7 - len(val.strip(" ")))
                        line = text + " " + space1 + " :" + space2 + val
                        overview_print.append(line)
                    elif line[0:6] == "Number":
                        overview_print.append("")
                        line0, split1 = line.strip(" ").split("Percent of    Total tasks:")
                        val2, split2 = split1.strip(" ").split("Completed:")
                        val3, split3 = split2.strip(" ").split("Incomplete:")
                        val4, split4 = split3.strip(" ").split("Overdue:")
                        val5 = split4.strip(" ")
                        line1a, val1 = line0.split(" :")
                        line1a = line1a.replace("·","")
                        val1 = val1.strip(" ")
                        space0 = "·" * (37 - len(line1a))
                        space1 = " " * (7 - len(val1))
                        line1 = line1a + space0 + " :" + space1 + val1
                        val2 = val2.strip(" ")
                        space2 = " " * (11 - len(val2))
                        line2 = "Percent of total tasks " + "·"*14 + " :" + space2 + val2
                        val3 = val3.strip(" ")
                        space3 = " " * (11 - len(val3))
                        line3 = "Percent of Completed Tasks " + "·"*10 + " :" + space3 + val3
                        val4 = val4.strip(" ")
                        space4 = " " * (11 - len(val4))
                        line4 = "Percent of Incomplete Tasks " + "·"*9 + " :" + space4 + val4
                        val5 = val5.strip(" ")
                        space5 = " " * (11 - len(val5))
                        line5 = "Percent of Overdue Tasks " + "·"*12 + " :" + space5 + val5
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

    # Return the print out of statistics.
    return overview_print


# Write all the tasks to the txt file.
def write_to_file(task_to_write, txt_out="tasks.txt"):
    writefile = open(txt_out, "w+", encoding="utf-8")
    to_write = ""
    for item in range(1,(len(task_to_write)+1)):
        if item > 1:
            to_write = f"\n"
        to_write += f"{task_to_write[item][0]}, "
        to_write += f"{task_to_write[item][1]}, "
        to_write += f"{task_to_write[item][2]}, "
        to_write += f"{task_to_write[item][3]}, "
        to_write += f"{task_to_write[item][4]}, "
        to_write += f"{task_to_write[item][5]}, "
        writefile.write(to_write)
    writefile.close()


# Check if the task is overdue.
def overdue(duedate):
    due_date = datetime.strptime(duedate, '%d %b %Y')
    today = datetime.today()
    if due_date <= today:
        return True
    else:
        return False


# Check the date is in the correct format.
def vali_date(message):
    while True:
        date_str = frame(message, window="in")
        try:
            date = datetime.strptime(date_str, "%d %b %Y")
            return date.strftime("%d %b %Y")
        except:
            message = ["Invalid date","","Please, enter the date in this format: (DD Mmm YYYY)"]


# Check if the input name is existing in the list of users. 
def valid_user(existing_users):
    while True:
        new_user = frame(["Enter a user for the new task"], window="in")
        if new_user in existing_users.keys():
            return new_user
        else:
            os.system(CLEAR)
            frame([f"The user '{new_user}' is not registered!"], frame_colour="Bright Red")


# Encoding function
def htd_encode(raw_pw, encif=""):
    # Load the shared library
    lib = ctypes.CDLL(os.path.abspath("encode.so"))

    # Define the argument and return types of the encode function
    lib.encode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.encode.restype = ctypes.c_char_p
    raw_pw_bytes = raw_pw.encode('utf-8')
    encif_bytes = encif.encode('utf-8')
    result = lib.encode(ctypes.c_char_p(raw_pw_bytes), ctypes.c_char_p(encif_bytes))
    return result.decode('utf-8')


# Run the main function if this file is executed as a script
if __name__ == "__main__":
    main()
