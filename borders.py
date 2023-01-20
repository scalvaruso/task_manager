
import os

def main():
    menu_list = ["",
    "\t\t   This is border.py",
    "",
    "This is an original module created by",
    "",
    "\t\t   Simone Calvaruso",
    "",
    ]

    col = frame(["Enter a colour"], window="in")
    os.system("clear")
    #print("\033[94m" + frame(menu_list) + "\033[0m")
    frame(menu_list, colour=col)


# This function create a frame around the content of a list.
# Any item of the list is considered a new line.
# The colour can be changed specifying a value for 'colour'.
# Changing the value of 'window' to 'input' it will take an input from the user.

def frame(menu_list, colour=0, window="print"):

    # Set the colour of the frame.

    if type(colour) == str:
        colour = colour.lower()

    if colour in [0,91,92,93,96,94,95]:
        pass
    elif colour == "red":
        colour = "91"
    elif colour == "green":
        colour = "92"
    elif colour == "yellow":
        colour = "93"
    elif colour == "cyan":
        colour = "96"
    elif colour == "blue":
        colour = "94"
    elif colour == "pink":
        colour = "95"
    else:
        colour = "0"

    menu_width = 50

    new_list = []

    # Split the lines if they are longer than 74 characters.

    for item in menu_list:
        line = ""
        words = item.split(" ")

        for word in words:

            word = word.replace("\t", "   ")

            if len(line+word) < 75:
                line += word + " "
            else:
                new_list.append(line)
                line = word + " "

        new_list.append(line)

    menu_list = new_list

    # Create the frame.

    max_width = max([(len(i)+4) for i in menu_list])

    if max_width > menu_width-4:
        menu_width = max_width + 4

    or_line = "═" * menu_width
    filling = " " * menu_width
    display_menu = f"\033[{colour}m" + "╔" + or_line + "╗\n"
    display_menu += "║" + filling + "║\n"

    for item in menu_list:
        item = " "*4 + item + " "*4
        item_width = len(item)
        filling = " " * (menu_width - item_width)
        display_menu += "║" + item + filling + "║\n"

    filling = " " * menu_width
    display_menu += "║" + filling + "║\n"
    display_menu += "╚" + or_line + "╝\033[0m\n"

    # Change the behaviour of the function from 'print' to 'input'.

    if window=="in" or window=="input":
        return input(display_menu)
    else:
        print(display_menu)

if __name__ == "__main__":
    main()
    