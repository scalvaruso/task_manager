
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

    os.system("clear")
    print("\033[94m" + border(menu_list) + "\033[0m")


def border(menu_list):

    menu_width = 48

    # max_width = max([(len(i)+4) for i in menu_list])

    new_list = []

    for item in menu_list:
        words = []
        line = ""
        words = item.split(" ")

        for word in words:

            word = word.replace("\t", "    ")


            if len(line) < 70:
                line += word + " "
            else:
                new_list.append(line)
                line = "\t"*5 + " " + word + " "
            line = line.replace("\t", "    ")
        
        new_list.append(line)

    #max_width = max(max_width, title_width)

    menu_list = new_list

    max_width = max([(len(i)+4) for i in menu_list])

    if max_width > menu_width-4:
        menu_width = max_width + 4

    or_line = "═" * menu_width
    filling = " " * menu_width
    display_menu = "\n╔" + or_line + "╗\n"
    display_menu += "║" + filling + "║\n"

    for item in menu_list:
        item = " "*4 + item + " "*4
        item_width = len(item)
        filling = " " * (menu_width - item_width)
        display_menu += "║" + item + filling + "║\n"

    filling = " " * menu_width
    display_menu += "║" + filling + "║\n"
    display_menu += "╚" + or_line + "╝\n"

    return display_menu


if __name__ == "__main__":
    main()