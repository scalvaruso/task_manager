# ========== importing libraries ==========

import os
from datetime import datetime

# ******************************   NOTE   ******************************
# The following module is an additional program to format the output.
# Please copy the file 'border.py' in the same folder of 'task_manager.py'.
# **********************************************************************

from border import border


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
    print(colour + border([f"\t\t\tWelcome {user_id}"]) + "\033[0m")

    # Present the options menu to the user.

    while True:

        menu = input(menu_option_1(admin)).lower()
        
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
            view_mine(user_id, tasks)
            pass

        elif menu == "s" and admin:
            display_stat(users, tasks)
            pass

        elif menu == "e":
            os.system("clear")
            print(border(["Thank you for using Task Manager.","","Goodbye!!!"]))
            exit()

        else:
            os.system("clear")
            print(border(["Sorry","The option selected is not valid.","Please Try again"]))


# ========== Login function ==========
# Program will ask and validate the user login and password:
# - terminates after 10 wrong ID entries.
# - terminates after 3 wrong password entries.

def login(login):

    print("\nEnter your ID: ", end="")

    # Ask the user for their ID.
    
    retry = 10
    while True:
        id = input("")
        
        if id in login.keys():
            break
        
        retry -= 1
        
        if retry > 0:
            os.system("clear")
            colour = "\n\033[0m"
            if retry == 1:
                colour = "\n\033[91m"
            print(colour + border([f"Sorry, '{id}' is not a valid ID!",f"{retry} more logon attempts left"]) + f"\nPlease enter a valid ID: " + "\n\033[0m", end="")
            continue
        else:
            os.system("clear")
            print(border(["Sorry, You have reached the maximum logon attempts!","Please, try again later."]))
            exit()

    # Ask the user for their password.

    admin = False
    print("\nEnter your Password: ", end="")

    retry = 3
    while True:
        user_pw = input("")

        # Check validity of password

        if user_pw == login[id]:
            if id == "admin":
                admin = True
            break

        retry -= 1

        if retry > 0:
            os.system("clear")
            colour = "\n\033[0m"
            if retry == 1:
                colour = "\n\033[91m"
            print(colour + border(["Incorrect Password!",f"{retry} more logon attempts left.","Please enter a valid Password"]) + "\n\033[0m", end="")
            continue
        else:
            os.system("clear")
            print(border(["Sorry, You have reached the maximum logon attempts!","Please, try again later."]))
            exit()

    return id, admin


# Generate a different menu for admin or users.

def menu_option_1(menu):
    
    menu_options = ["Please, select one of the options below:",""]

    if menu:
        colour = "\033[93m"
        menu_options.append("r  - Registering a user")
    else:
        colour = "\033[0m"
        menu_options.append("")
    menu_options.append("a  - Adding a task")
    menu_options.append("va - View all tasks")
    menu_options.append("vm - View my task")

    if menu:
        menu_options.append("s  - Statistics")
    else:
        menu_options.append("")
        
    menu_options.append("e  - Exit")
    
    return f"{colour}{border(menu_options)}\033[0m"


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
        
    while True:
        user_task = input(f"Enter a user for the new task: ")
        
        if user_task in users.keys():
            break
        else:
            print("The user you selected does not exist.\n")
            continue
    
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
        
        print(border(print_tasks))


# Print all the tasks recorded for the user logged in.

def view_mine(id, tasks):
    my_tasks = {}

    for key in tasks.keys():
        if id == tasks[key][0]:
            my_tasks.update({key: tasks[key]})
        else:
            pass

    view_all(my_tasks)

    # NOTE function to be completed
    """
    if id == "admin":
        to_edit = tasks
    else:
        to_edit = my_tasks
    """
    # edit_task(to_edit)


def edit_task(ed_task):
    ...


def gen_reports():
    ...


# Print the total number of users and tasks registered.

def display_stat(users, tasks):

    users_number = f"Number of user: \t{str(len(users.keys()))}"
    tasks_number = f"Number of tasks:\t{str(len(tasks.keys()))}"

    os.system("clear")
    print(border(["", users_number, tasks_number, ""]))


if __name__ == "__main__":
    main()
