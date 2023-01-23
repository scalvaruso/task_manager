
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

    frame(menu_list, colour=col)


def frame(menu_list, colour=0, spacing=1, window="print"):
    """
    This function create a frame around the content of a list.
    Any item of the list is considered a new line.
    
    Parameters:
        colour: allows to change the colour of the window
            default value = 'white'
        spacing: allows to increase or decrease the space between the frame and the text
            default value = 1
        window: allows the function to behave as input
            default value = 'print'

    Returns:
        Print a frame around the output or the input prompt
    """

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

    new_list = []

    # Split the lines if they are longer than 70 characters.

    if spacing < 1:
        border_space = 0
        menu_width = 50
    else:
        border_space = spacing * 4
        menu_width = 58
    side_space = border_space * " "

    for item in menu_list:
        line = ""
        words = item.split(" ")
        space = " "
        for word in words:
            word = word.replace("\t", "    ")
            
            if len(word) >= 70:
                line = word[:70]
                new_list.append(line.rstrip(" "))
                line = word[70:] + space
            elif len(line+word) < 71:
                line += word + space
            else:
                new_list.append(line.rstrip(" "))
                line = word + space

        new_list.append(line.rstrip(" "))

    menu_list = new_list

    # Create the frame.

    max_width = max([(len(i.rstrip(" "))) for i in menu_list])

    if max_width > (menu_width-(border_space*2)):
        menu_width = max_width + (border_space*2)

    or_line = "═" * menu_width
    filling = " " * menu_width
    display_menu = f"\033[{colour}m" + "╔" + or_line + "╗\n"

    for i in range(spacing):
        display_menu += "║" + filling + "║\n"

    for item in menu_list:
        out_item = side_space + item + side_space
        item_width = len(out_item)
        filling = " " * (menu_width - item_width)
        display_menu += "║" + out_item + filling + "║\n"

    filling = " " * menu_width

    for i in range(spacing):
        display_menu += "║" + filling + "║\n"

    display_menu += "╚" + or_line + "╝\033[0m\n"

    # Change the behaviour of the function from 'print' to 'input'.

    if window=="in" or window=="input":
        return input(display_menu)
    else:
        print(display_menu)

if __name__ == "__main__":
    main()
    