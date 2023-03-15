# ************************************************************
# ********** * Program created by Simon Calvaruso * **********
# ************************************************************


# ========== importing libraries ==========

import math
import os
from datetime import datetime
from borders import frame


# Main function.

def main():

    # Read the existing Users.

    users = {}

    with open("user.txt", "r", encoding="utf-8") as users_read:
        
        for line in users_read:
            name, password = line.split(", ")
            users.update({name: password.strip("\n")})

    # Read the existing Tasks.

    tasks = {}

    with open("tasks.txt", "r", encoding="utf-8") as tasks_read:

        for pos, line in enumerate(tasks_read, 1):
            line_split = line.split(", ")
            line_split[-1] = line_split[-1].strip("\n")
            tasks.update({pos: line_split[0:]})

    # Login the user.

    user_id, admin = login(users)

    if admin:
        col = 93
    else:
        col = 0

    os.system("clear")
    space = " " * math.floor((42-len(user_id))/2)
    frame([f"{space}Welcome {user_id}"], colour=col)

    # Present the options menu to the user.

    while True:

        menu = frame(entry_menu(admin), colour=col, window="in").lower()
        
        # Execute the function corresponding to the selected option.

        if menu == "r" and admin:
            os.system("clear")
            users = reg_user(users)

        elif menu == "a":
            os.system("clear")
            tasks = add_task(users, tasks)

        elif menu == "va":
            os.system("clear")
            for key in tasks.keys():
                frame(view_all(tasks, key))

        elif menu == "vm":
            os.system("clear")
            check = True  # Variable to check if the tasks should be printed or not.

            # Edit menu.
            
            while True:

                # The following 'if' allows to print the tasks only the first time,
                # and when the user connected to the tasks has been changed.
                                
                if check:
                    my_keys = view_mine(user_id, tasks)

                choice = int(frame(
                    [
                    "Please, select one of the options below:",
                    "",
                    "Your task are:",
                    f"{my_keys}",
                    "",
                    "Task number - to edit the task",
                    "\t-1\t  - to go back to previous menu",
                    ], window="in"))

                if choice == -1:
                    break

                # Proceed to the edit menu only if the task selected belong to the user logged in.

                elif choice not in my_keys:
                    frame(["Sorry you cannot select others tasks."])
                    check = False
                    pass

                else:
                    check = edit_task(tasks, users, (choice))

        elif menu == "gr" and admin:
            
            os.system("clear")
            tasks_stats(tasks)
            user_stats(users, tasks)
            frame(["Statistics successfully saved to:","","'task_overview.txt' and 'user_overview.txt'"], colour="green")


            pass

        elif menu == "ds" and admin:
            
            os.system("clear")
            frame(display_statistics(users, tasks))
            
            pass

        elif menu == "e":
            
            os.system("clear")
            frame(["Thank you for using Task Manager.","","Goodbye!!!"], colour="cyan")
            exit()

        else:
            
            os.system("clear")
            frame(["Sorry","The option selected is not valid.","Please Try again"])


# ==================== Login function ====================
# Program will ask and validate the user login and password:
# - terminates after 10 wrong ID entries.
# - terminates after 3 wrong password entries.

def login(login):

    os.system("clear")
    message = ["Enter your ID"]

    # Ask the user for their ID.
    
    retry = 10
    col = 0
    while True:
        id = frame(message, colour=col, window="in")
        
        # Check if user is registered.

        if id in login.keys():
            break

        # Retry count for users.

        retry -= 1
        
        if retry > 0:
            os.system("clear")

            if retry == 1:
                col = 91
            message = [f"Sorry, '{id}' is not a valid ID!",f"{retry} more logon attempts left","","Please enter a valid ID"]
            continue
        else:
            os.system("clear")
            frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."])
            exit()

    # Ask the user for their password.

    admin = False
    message = ["Enter your Password"]

    retry = 3
    col = 0
    while True:
        user_pw = frame(message, colour=col, window="in")

        # Check validity of password.

        if user_pw == login[id]:
            if id == "admin":
                admin = True
            break
        
        # Retry count for passwords.

        retry -= 1

        if retry > 0:
            os.system("clear")
    
            if retry == 1:
                col = 91
            message = ["Incorrect Password!","",f"{retry} more logon attempts left.","Please enter a valid Password"]
            continue
        else:
            os.system("clear")
            frame(["Sorry, You have reached the maximum logon attempts!","Please, try again later."])
            exit()

    return id, admin


# Generate a different menu for admin or users.

def entry_menu(extended):
    
    menu_options = ["Please, select one of the options below:",""]

    if extended:
        menu_options.append("r  - Registering a user")
    else:
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
    
    return menu_options


# Register a new user after checking if it is already existing.

def reg_user(old_users):
    
    # Check if the ID entered already exists.

    while True:
        new_user = frame(["Please, enter a new user"], window="in")

        if new_user in old_users.keys():
            os.system("clear")
            frame([f"The name '{new_user}' is already existing."])
            continue
        else:
            break
    
    os.system("clear")

    # Ask for a valid password.

    while True:
        new_password = frame(["Enter a new password"], window="in")
        pw_confirmation = frame(["Confirm the password"], window="in")

        if new_password == pw_confirmation:
            break
        else:
            os.system("clear")
            frame(["The passwords do not match!"])

    # Update the variable containing the users and passwords
    # and write to the file 'user.txt'.

    old_users.update({new_user: new_password})
    
    with open("user.txt", "a", encoding="utf-8") as users_append:
        users_append.write(f"\n{new_user}, {new_password}")
    
    os.system("clear")
    frame(["New user successfully recorded!"], colour="green")

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
    old_tasks.update({(task_num+1): new_task_data})

    with open("tasks.txt", "a", encoding="utf-8") as tasks_append:
        tasks_append.write(f"\n{user_task}, {new_task}, {description}, {assignment_date}, {due_date}, No")
    
    os.system("clear")
    frame(["New task successfully recorded!"], colour="green")

    return old_tasks


# Check the date is in the correct format.

def vali_date(message):
    
    while True:
        in_date = frame(message, window="in")
        
        try:
            datetime.strptime(in_date, '%d %b %Y')
            return in_date
        except:
            message = ["Invalid date","","Please, enter the date in this format: (DD Mmm YYYY)"]


# Format and print all the tasks recorded.

def view_all(tasks, key):

    print_tasks = [f"Task number ······ :\t{key}"]
    print_tasks.append(f"User ············· :\t{tasks[key][0]}")
    print_tasks.append(f"Task ············· :\t{tasks[key][1]}")

    description_line = (f"Description ······ :\t{tasks[key][2]}").strip("\n")
    description = ""
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
    print_tasks.append(f"Date assignement · :\t{tasks[key][3]}")
    print_tasks.append(f"Due Date ········· :\t{tasks[key][4]}")
    print_tasks.append(f"Task completed ··· :\t{tasks[key][5]}")
        
    return print_tasks


# Print all the tasks recorded for the user logged in.

def view_mine(id, tasks):
    my_keys = []

    for key in tasks.keys():

        if id == tasks[key][0]:
            frame(view_all(tasks, key))
            my_keys.append(key)
        else:
            pass

    return my_keys


# This function allows to edit a selected task.

def edit_task(tasks_for_edit, users_for_edit, to_edit):

    task = tasks_for_edit[to_edit]

    # Check if the task has not been completed and can be edited.

    if task[5] == "Yes":
        frame(["Sorry the task selected has been already completed and cannot be modified",
        "",
        "Please select another task",
        ], colour="yellow")
        return False

    # Present the possible edits.

    while True:

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
            return False

        # Change the task status.

        elif to_change == "1":

            tasks_for_edit[to_edit][5] = "Yes"
            write_to_file(tasks_for_edit)
            frame([f"Task {to_edit} marked as completed!"], colour="green")
            return False

        # Change the due date.
        
        elif to_change == "2":

            new_due = vali_date(["Enter a new due date in the format (DD Mmm YYYY)"])
            tasks_for_edit[to_edit][4] = new_due
            write_to_file(tasks_for_edit)
            frame([f"New due date for task {to_edit} is: {new_due}"], colour="green")
            return False
        
        # Change the user for the selected task.

        elif to_change == "3":
            
            new_user = valid_user(users_for_edit)
            tasks_for_edit[to_edit][0] = new_user
            write_to_file(tasks_for_edit)
            frame([f"Task {to_edit} assigned to: {new_user}"], colour="green")
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

def valid_user(existing_users):
    
    while True:
        new_user = frame(["Enter a user for the new task"], window="in")
        
        if new_user in existing_users.keys():
            break
        else:
            os.system("clear")
            frame(["The user you selected does not exist."])
            continue
    
    return new_user


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

    to_write = ["\t\t\t\t   Task Overview",
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
    
    to_write = ["\t\t\t\t   User Overview",
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


# Check if the task is overdue.

def overdue(duedate):
    due_date = datetime.strptime(duedate, '%d %b %Y')
    today = datetime.today()

    if due_date <= today:
        return True
    else:
        return False


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

    overview_print.append(""*2)

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


if __name__ == "__main__":
    main()
