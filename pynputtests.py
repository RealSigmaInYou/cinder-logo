import json
import termcolor
from pynput import keyboard
import os


with open("characters.json", "r") as characters_raw:
    characters = json.load(characters_raw)

with open("maps.json", "r") as maps_raw:
    maps = json.load(maps_raw)

current_map = 1
vertical = maps[str(current_map)]["size"][0]
horizontal = maps[str(current_map)]["size"][1]
ally_start_positions = {
    "pos1": {"vertical": 15, "horizontal": 18},
    "pos2": {"vertical": 1, "horizontal": 3},
    "pos3": {"vertical": 1, "horizontal": 18}
}
slot_1_character = "marph"
slot_2_character = "krome"
characters[slot_1_character]["position"] = ally_start_positions["pos1"]
characters[slot_2_character]["position"] = ally_start_positions["pos3"]

cursor_placement = {
    "vertical": characters[slot_1_character]["position"]["vertical"],
    "horizontal": characters[slot_1_character]["position"]["horizontal"]
}


unit_selected = False
diagonal_menu_text = ["Attack   |   ", "Guard   |   ", "Items   |   ", "Wait"]
diagonal_menu_up = False

diagonal_menu_cursor = 0

gridmap = {}
gridnr = 0
mapstring = ""

show_range = ""

blank_gridmap = {}
gridmap = {}

def draw_map(cursor_placement):
    global gridmap
    global gridnr
    global mapstring
    char_position = characters[slot_1_character]["position"]
    char_vertical = char_position["vertical"]
    char_horizontal = char_position["horizontal"]
    walk_distance = characters[slot_1_character]["misc"]["walk_distance"]
    attack_range = characters[slot_1_character]["misc"]["attack_range"]
    os.system("cls")
    
    mapstring = ""

# if char_vertical == y and char_horizontal == x:
#                 gridmap[gridnr] = y, x, termcolor.colored("9 ", "green")
#             elif cursor_placement["vertical"] == y and cursor_placement["horizontal"] == x:
#                 gridmap[gridnr] =  y, x, termcolor.colored("O ", "yellow")
#             elif ((abs(y - char_vertical) + abs(x - char_horizontal)) <= walk_distance) and (cursor_placement == char_position or slot_1_character in show_range):
#                 gridmap[gridnr] =  y, x, termcolor.colored("¤ ", "cyan")
#             elif (abs(y - char_vertical) + abs(x - char_horizontal)) <= walk_distance + attack_range and (cursor_placement == char_position or slot_1_character in show_range):
#                 gridmap[gridnr] = y, x, termcolor.colored("¤ ", "red")
#             else:
    
    #create gridmap
    for y in range(vertical):
        for x in range(horizontal):
            blank_gridmap[gridnr] = y, x, "# "
            gridnr += 1
    gridmap = blank_gridmap

    #update gridmap
    for z in blank_gridmap:
        for character in characters:
            if characters[character]["position"]["vertical"] == gridmap[z][0] and characters[character]["position"]["horizontal"] == gridmap[z][1]:
                gridmap[z] = gridmap[z][0], gridmap[z][1], termcolor.colored("9 ", "green")
            elif cursor_placement["vertical"] == gridmap[z][0] and cursor_placement["horizontal"] == gridmap[z][1]:
                gridmap[z] =  gridmap[z][0], gridmap[z][1], termcolor.colored("O ", "yellow")
            elif ((abs(gridmap[z][0] - characters[character]["position"]["vertical"]) + abs(gridmap[z][1] - characters[character]["position"]["horizontal"])) <= characters[character]["misc"]["walk_distance"]) and (cursor_placement == characters[character]["position"] or character in show_range):
                gridmap[z] =  gridmap[z][0], gridmap[z][1], termcolor.colored("¤ ", "cyan")
            elif (abs(gridmap[z][0] - characters[character]["position"]["vertical"]) + abs(gridmap[z][1] - characters[character]["position"]["horizontal"])) <= characters[character]["misc"]["walk_distance"] + characters[character]["misc"]["attack_range"] and (cursor_placement == characters[character]["position"] or character in show_range):
                gridmap[z] = gridmap[z][0], gridmap[z][1], termcolor.colored("¤ ", "red")
        
        mapstring += gridmap[z][2]
        if gridmap[z][1] == horizontal-1:
            mapstring += "\n"

    print(mapstring)
    if diagonal_menu_up == True:
        print(diagonal_menu_text)
    



def on_pressed(key):
    global diagonal_menu_up
    global unit_selected
    global cursor_placement
    global show_range
    char_position = characters[slot_1_character]["position"]
    char_vertical = char_position["vertical"]
    char_horizontal = char_position["horizontal"]
    walk_distance = characters[slot_1_character]["misc"]["walk_distance"]
    attack_range = characters[slot_1_character]["misc"]["attack_range"]

    if diagonal_menu_up == False:
        if key == keyboard.Key.up and cursor_placement["vertical"] > 0:
            cursor_placement["vertical"] -= 1
            draw_map(cursor_placement)
        elif key == keyboard.Key.down and cursor_placement["vertical"] < vertical - 1:
            cursor_placement["vertical"] += 1
            draw_map(cursor_placement)
        elif key == keyboard.Key.left and cursor_placement["horizontal"] > 0:
            cursor_placement["horizontal"] -= 1
            draw_map(cursor_placement)
        elif key == keyboard.Key.right and cursor_placement["horizontal"] < horizontal - 1:
            cursor_placement["horizontal"] += 1
            draw_map(cursor_placement)
        elif key == keyboard.Key.enter:
            print(unit_selected)
            for character in characters:
                if unit_selected == True:
                    if (abs(cursor_placement["vertical"] - characters[character]["position"]["vertical"]) + abs(cursor_placement["horizontal"] - characters[character]["position"]["horizontal"])) <= walk_distance:
                        show_diagonal_menu()
                        move_cursor()
                    else:
                        move_cursor()
                elif cursor_placement == characters[character]["position"] and unit_selected == False:
                    unit_selected = True
                    show_range =character
        elif key == keyboard.Key.backspace and unit_selected == True:
            for character in characters:
                unit_selected = False
                show_range = character
                draw_map(cursor_placement)
    elif diagonal_menu_up == True:
        global diagonal_menu_cursor
        if key == keyboard.Key.left:
            diagonal_menu_cursor = diagonal_menu_cursor -1
            if diagonal_menu_cursor < 0:
                diagonal_menu_cursor = 0
            show_diagonal_menu()
            move_cursor()

        elif key == keyboard.Key.right:
            diagonal_menu_cursor = diagonal_menu_cursor +1
            if diagonal_menu_cursor > 4:
                diagonal_menu_cursor = 4
                show_diagonal_menu() 
            move_cursor()

        elif key == keyboard.Key.enter:
            for character in characters: 
                if (abs(cursor_placement["vertical"] - characters[character]["position"]["vertical"]) + abs(cursor_placement["horizontal"] - characters[character]["position"]["horizontal"])) <= characters[character]["misc"]["walk_distance"]:
                    characters[character]["position"] = cursor_placement
                    print(characters[character]["position"])
                    move_cursor()
        elif key == keyboard.Key.backspace:
            diagonal_menu_up = False
            move_cursor()
    else:
        print("huh?")


def move_cursor():
    with keyboard.Listener(on_press=on_pressed) as listener:
        draw_map(cursor_placement)
        listener.join()


def show_diagonal_menu():
    global diagonal_menu_up
    diagonal_menu_up = True
    move_cursor(diagonal_menu_up)


move_cursor()
