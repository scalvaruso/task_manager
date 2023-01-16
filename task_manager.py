# ========== importing libraries ==========

import os
from datetime import datetime

# ******************************   NOTE   ******************************
# The following module is an additional program to format the output.
# Please copy the file 'borders.py' in the same folder of 'task_manager.py'.
# **********************************************************************

from borders import frame


# Main function.

def main():

    # Read the existing Users.

    users = {}

    with open("user.txt", "r", encoding="utf-8") as users_list:
        
        for line in users_list:
            name, password = line.split(", ")
            users.update({name: password.strip("\n")})

    # Read the existing Tasks.

    tasks = {}

    with open("tasks.txt", "r", encoding="utf-8") as tasks_list:

        for pos, line in enumerate(tasks_list, 1):
            line_split = line.split(", ")
            line_split[-1] = line_split[-1].strip("\n")
            tasks.update({pos: line_split[0:]})

    # Login the user.

    user_id, admin = login(users)

    if admin:
        colour = "\033[93m"
    else:
        colour = "\033[0m"

    os.system("clear")
    print(colour + frame([f"\t\t\tWelcome {user_id}"]) + "\033[0m")

    # Present the options menu to the user.

    while True:

        menu = input(entry_menu(admin)).lower()
        
        # Execute the function corresponding to the selected option.

        if menu == "r" and admin:
            users = reg_user(users)
            pass

        elif menu == "a":
            tasks = add_task(users, tasks)
            pass

        elif menu == "va":
            view_all(tasks)
            pass

        elif menu == "vm":

            check = True  # Variable to check if the tasks should be printed or not.

            # Edit menu.
            
            while True:

                # The following 'if' allows to print the tasks only the first time,
                # and when the user connected to the tasks has been changed.
                                
                if check:
                    my_keys = view_mine(user_id, tasks)

                choice = int(input(frame(["Please, select one of the options below:",
                "",
                "Your task are:",
                f"{my_keys}",
                "",
                "Task number - to edit the task",
                "\t-1\t  - to go back to previous menu",
                ])))


                if choice == -1:
                    break

                # Proceed to the edit only if the task selected belong to the user logged in.

                elif choice not in my_keys:
                    print(frame(["Sorry you cannot select others tasks."]))
                    check = False
                    pass
                else:
                    check = edit_task(tasks, users, (choice))
                    
            pass
        
        elif menu == "gr" and admin:
            ...
            pass

        elif menu == "ds" and admin:
            display_statistics(users, tasks)
            pass

        elif menu == "e":
            os.system("clear")
            print(frame(["Thank you for using Task Manager.","","Goodbye!!!"]))
            exit()

        else:
            os.system("clear")
            print(frame(["Sorry","The option selected is not valid.","Please Try again"]))


# ==================== Login function ====================
# Program will ask and validate the user login and password:
# - terminates after 10 wrong ID entries.
# - terminates after 3 wrong password entries.

def login(login):

    print("\nEnter your ID: ", end="")

    # Ask the user for their ID.
    
    retry = 10
    while True:
        id = input("")
        
        # Check if user is registered.

        if id in login.keys():
            break

        # Retry count for users.

        retry -= 1
        
        if retry > 0:
            os.system("clear")
            colour = "\n\033[0m"
            if retry == 1:
                colour = "\n\033[91m"
            print(colour + frame([f"Sorry, '{id}' is not a valid ID!",f"{retry} more logon attempts left"]) + f"\nPlease enter a valid ID: " + "\n\033[0m", end="")
            continue
        else:
            os.system("clear")
            print(frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."]))
            exit()

    # Ask the user for their password.

    admin = False
    print("\nEnter your Password: ", end="")

    retry = 3
    while True:
        user_pw = input("")

        # Check validity of password.

        if user_pw == login[id]:
            if id == "admin":
                admin = True
            break
        
        # Retry count for passwords.

        retry -= 1

        if retry > 0:
            os.system("clear")
            colour = "\n\033[0m"
            if retry == 1:
                colour = "\n\033[91m"
            print(colour + frame(["Incorrect Password!",f"{retry} more logon attempts left.","Please enter a valid Password"]) + "\n\033[0m", end="")
            continue
        else:
            os.system("clear")
            print(frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."]))
            exit()

    return id, admin


# Generate a different menu for admin or users.

def entry_menu(extended):
    
    menu_options = ["Please, select one of the options below:",""]

    if extended:
        colour = "\033[93m"
        menu_options.append("r  - Registering a user")
    else:
        colour = "\033[0m"
        menu_options.append("")
    menu_options.append("a  - Adding a task")
    menu_options.append("va - View all tasks")
    menu_options.append("vm - View my task")

    if extended:
        menu_options.append("gr - Generate Reports")
        menu_options.append("ds - Display Statistics")
    else:
        menu_options.append("")
        
    menu_options.append("e  - Exit")
    
    return f"{colour}{frame(menu_options)}\033[0m"


# Register a new user after checking if it is already existing.

def reg_user(old_users):
    
    # Check if the ID enter already exists.

    while True:
        new_user = input("Enter a new user: ")

        if new_user in old_users.keys():
            print(f"The name '{new_user}' is already existing.\nPlease")
            continue
        else:
            break

    # Ask for a valid password.

    while True:
        new_password = input("Enter a new password: ")
        pw_confirmation = input("Confirm the password: ")

        if new_password == pw_confirmation:
            break
        else:
            print("The passwords do not match!")

    # Update the variable containing the users and passwords
    # and write to the file 'user.txt'.

    old_users.update({new_user: new_password})
    
    with open("user.txt", "a", encoding="utf-8") as users_list:
        users_list.write(f"\n{new_user}, {new_password}")
    
    return old_users


# Add a new task to an existing user.

def add_task(users, old_tasks):

    user_task = input_user(users)
    new_task = input("Enter the name of the task: ")
    description = input("Enter a short description of the task: ")
    assignment_date = (datetime.today()).strftime("%d %b %Y")
    due_date = input("Enter the due date in the format (DD Mmm YYYY): ")

    # Update the variable containing the tasks
    # and write it to the file 'tasks.txt'.

    new_task_data = [user_task, new_task, description, assignment_date, due_date, "No"]
    task_num = len(old_tasks.keys())
    old_tasks.update({(task_num+1): new_task_data})

    with open("tasks.txt", "a", encoding="utf-8") as tasks_list:
        tasks_list.write(f"\n{user_task}, {new_task}, {description}, {assignment_date}, {due_date}, No")
    
    return old_tasks


# Print all the tasks recorded.

def view_all(tasks):
    os.system("clear")

    for key in tasks.keys():

        print_tasks = [f"Task number:\t \t{key}"]
        print_tasks.append(f"User:\t\t\t\t{tasks[key][0]}")
        print_tasks.append(f"Task:\t\t\t\t{tasks[key][1]}")
        print_tasks.append(f"Description:\t \t{tasks[key][2]}")
        print_tasks.append(f"Date assignement:\t{tasks[key][3]}")
        print_tasks.append(f"Due Date:\t\t\t{tasks[key][4]}")
        print_tasks.append(f"Task completed:\t  {tasks[key][5]}")
        
        print(frame(print_tasks))


# Print all the tasks recorded for the user logged in.

def view_mine(id, tasks):
    my_tasks = {}
    my_keys = []
    for key in tasks.keys():
        if id == tasks[key][0]:
            my_tasks.update({key: tasks[key]})
            my_keys.append(key)
        else:
            pass

    view_all(my_tasks)
    return my_keys


def edit_task(tasks_list, users_list, to_edit):

    task = tasks_list[to_edit]

    # Check if the task has not been completed and can be edited.

    if task[5] == "Yes":
        print(frame(["Sorry the task selected has been already completed and cannot be modified",
        "",
        "Please select another task",
        ]))
        return False

    # Present the possible edits.

    while True:

        todo = input(frame(["Please, select one of the options below:",
                "",
                "1 - mark the task as completed",
                "2 - change the due date",
                "3 - change the user",
                "",
                "0 - to go back to previous menu",
                ]))

        # Exit editing.

        if todo == "0":
            return False

        # Change the task status.

        elif todo == "1":

            tasks_list[to_edit][5] = "Yes"
            write_to_file(tasks_list)
            return False

        # Change the due date.
        
        elif todo == "2":

            new_due = input("Enter a new due date in the format (DD Mmm YYYY): ")
            tasks_list[to_edit][4] = new_due
            write_to_file(tasks_list)
            return False
        
        # Change the user for the selected task.

        elif todo == "3":
            
            new_user = input_user(users_list)
            tasks_list[to_edit][0] = new_user
            write_to_file(tasks_list)
            return True


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


# Check if the input name is existing in the list of users. 

def input_user(existing_users):
    
    while True:
        new_user = input(f"Enter a user for the new task: ")
        
        if new_user in existing_users.keys():
            break
        else:
            print(frame(["The user you selected does not exist."]))
            continue
    
    return new_user


def gen_reports():
    
    ...


def display_statistics(users, tasks):
    display_stat(users, tasks)  # NOTE to be removed when function is implemented.
    ...


# Print the total number of users and tasks registered.

def display_stat(users, tasks):  # Temp function

    users_number = f"Number of user: \t{str(len(users.keys()))}"
    tasks_number = f"Number of tasks:\t{str(len(tasks.keys()))}"

    os.system("clear")
    print(frame(["", users_number, tasks_number, ""]))


if __name__ == "__main__":
    main()
