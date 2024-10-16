import json
import termcolor
from pynput import keyboard
import os

class Game:
    def __init__(self):
        with open("characters.json", "r") as characters_raw:
            self.characters = json.load(characters_raw)

        with open("maps.json", "r") as maps_raw:
            maps = json.load(maps_raw)

        self.current_map = 1
        self.vertical = maps[str(self.current_map)]["size"][0]
        self.horizontal = maps[str(self.current_map)]["size"][1]
        self.ally_start_positions = {
            "pos1": {"vertical": 15, "horizontal": 18},
            "pos2": {"vertical": 1, "horizontal": 3},
            "pos3": {"vertical": 1, "horizontal": 18}
        }
        self.selected_characters =["marph", "baileph"]

        self.characters[self.selected_characters[0]]["position"] = self.ally_start_positions["pos1"]
        self.characters[self.selected_characters[1]]["position"] = self.ally_start_positions["pos2"]
        
        print(self.characters["marph"]["position"])
        print(self.characters["baileph"]["position"])


        self.cursor_placement = {
            "vertical": self.characters[self.selected_characters[0]]["position"]["vertical"],
            "horizontal": self.characters[self.selected_characters[0]]["position"]["horizontal"]
        }
        self.unit_selected = False
        self.diagonal_menu_text = ["Attack   |   ", "Guard   |   ", "Items   |   ", "Wait"]
        self.diagonal_menu_up = False
        self.diagonal_menu_cursor = 0

        # self.char_position = self.characters[self.slot_1_character]["position"]
        # self.char_vertical = self.char_position["vertical"]
        # self.char_horizontal = self.char_position["horizontal"]
        # self.walk_distance = self.characters[self.slot_1_character]["misc"]["walk_distance"]
        # self.attack_range = self.characters[self.slot_1_character]["misc"]["attack_range"]

        self.gridmap = {}
        self.gridnr = 1
        self.mapstring = ""
        self.show_range = []

        self.preview_move = []

        self.show_attack_range_diagonal_cursor_tf = False
        self.diagonal_menu_cursor = 1

        self.move_cursor()

    def get_add_to_map(self):

        for slot in self.gridmap:
            for character in self.characters:
                    if (self.characters[character]["position"]["vertical"] == self.gridmap[slot][0]) and (self.characters[character]["position"]["horizontal"] == self.gridmap[slot][1]): # and (self.characters[character]["position"]["vertical"] == self.ally_start_positions[pos]["vertical"] and self.characters[character]["position"]["horizontal"] == self.ally_start_positions[pos]["horizontal"]):
                        self.gridmap[slot] = self.characters[character]["position"]["vertical"], self.characters[character]["position"]["horizontal"], termcolor.colored("9 ", "green")
                    elif (self.cursor_placement["vertical"] == self.gridmap[slot][0])and (self.cursor_placement["horizontal"] == self.gridmap[slot][1]):
                        self.gridmap[slot] = self.cursor_placement["vertical"], self.cursor_placement["horizontal"], termcolor.colored("O ", "yellow")

                    elif (abs(self.gridmap[slot][0] - self.characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range):
                        self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "cyan")
                    elif (abs(self.gridmap[slot][0] - self.characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"] + self.characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range):
                        self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")




    def draw_map(self):
        self.gridmap = {}
        self.mapstring = ""
        self.gridnr = 1
        # self.char_position = {"vertical": self.char_vertical, 
        #                       "horizontal":self.char_horizontal}

        os.system("cls")
        if self.show_attack_range_diagonal_cursor_tf == False:
                for y in range(self.vertical):
                    for x in range(self.horizontal):
                        # if self.characters[character]["position"]["vertical"] == y and self.characters[character]["position"]["horizontal"] == x:
                        #     self.gridmap[self.gridnr] = y, x, termcolor.colored("9 ", "green")
                        # elif self.cursor_placement["vertical"] == y and self.cursor_placement["horizontal"] == x:
                        #     self.gridmap[self.gridnr] = y, x, termcolor.colored("O ", "yellow")
                        # elif (abs(y - self.characters[character]["position"]["vertical"]) + abs(x - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range):
                        #     self.gridmap[self.gridnr] = y, x, termcolor.colored("¤ ", "cyan")
                        # elif (abs(y - self.characters[character]["position"]["vertical"]) + abs(x - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"] + self.characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range):
                        #     self.gridmap[self.gridnr] = y, x, termcolor.colored("¤ ", "red")
                        # else:
                        self.gridmap[self.gridnr] = y+1, x+1, "# "

                        self.gridnr += 1


        elif self.show_attack_range_diagonal_cursor_tf == True:
            for y in range(self.vertical):
                for x in range(self.horizontal):
                    for character in self.characters:
                        if self.char_vertical == y and self.char_horizontal == x:
                            self.gridmap[self.gridnr] = y+1, x+1, termcolor.colored("9 ", "green")
                        elif self.cursor_placement["vertical"] == y and self.cursor_placement["horizontal"] == x:
                            self.gridmap[self.gridnr] = y+1, x+1, termcolor.colored("O ", "yellow")
                        elif (abs(y - self.cursor_placement["vertical"]) + abs(x - self.cursor_placement["horizontal"]) <= self.characters[character]["misc"]["attack_range"]):
                            self.gridmap[self.gridnr] = y+1, x+1, termcolor.colored("¤ ", "red")
                        else:
                            self.gridmap[self.gridnr] = y+1, x+1, "# "

                        self.gridnr += 1
        

        self.get_add_to_map()
        self.gridmapline = ""
        line_count = 0
        for z in self.gridmap:

            self.mapstring += self.gridmap[z][2]
            line_count += 1
            if self.gridmap[z][1] == self.horizontal - 1:
                self.mapstring += "\n"
        print(self.mapstring)
        #if self.diagonal_menu_up:
            #print(self.diagonal_menu_text)
        # print(self.cursor_placement)
        # print(self.diagonal_menu_cursor)

    def on_pressed(self, key):
        if self.diagonal_menu_up == False and self.show_attack_range_diagonal_cursor_tf == False:
            if key == keyboard.Key.up and self.cursor_placement["vertical"] > 0:
                self.cursor_placement["vertical"] -= 1
                self.draw_map()
            elif key == keyboard.Key.down and self.cursor_placement["vertical"] < self.vertical - 1:
                self.cursor_placement["vertical"] += 1
                self.draw_map()
            elif key == keyboard.Key.left and self.cursor_placement["horizontal"] > 0:
                self.cursor_placement["horizontal"] -= 1
                self.draw_map()
            elif key == keyboard.Key.right and self.cursor_placement["horizontal"] < self.horizontal - 1:
                self.cursor_placement["horizontal"] += 1
                self.draw_map()
            elif key == keyboard.Key.enter:
                if self.unit_selected == True:
                    if (abs(self.cursor_placement["vertical"] - self.char_vertical) + abs(self.cursor_placement["horizontal"] - self.char_horizontal)) <= self.walk_distance:
                        self.show_diagonal_menu()
                else:
                    if self.cursor_placement == self.char_position:
                        self.unit_selected = True
                        self.show_range.append(self.slot_1_character)
                self.draw_map()
            elif key == keyboard.Key.backspace and self.unit_selected == True:
                self.unit_selected = False
                self.show_range.remove(self.slot_1_character)
                self.draw_map()
        elif self.show_attack_range_diagonal_cursor_tf == True and self.diagonal_menu_up == False:
            if key == keyboard.Key.enter:
                self.char_vertical = self.cursor_placement["vertical"]
                self.char_horizontal = self.cursor_placement["horizontal"]
                self.show_attack_range_diagonal_cursor_tf = False
                self.diagonal_menu_up = False
                self.draw_map()
            elif key == keyboard.Key.backspace:
                self.show_attack_range_diagonal_cursor_tf = False
                self.draw_map()
        elif self.diagonal_menu_up == True: 
            self.handle_diagonal_menu(key)

    def handle_diagonal_menu(self, key):
        if key == keyboard.Key.left:
            self.diagonal_menu_cursor = max(0, self.diagonal_menu_cursor - 1)
            self.show_diagonal_menu()
        elif key == keyboard.Key.right:
            self.diagonal_menu_cursor = min(len(self.diagonal_menu_text) - 1, self.diagonal_menu_cursor + 1)
            self.show_diagonal_menu()
        elif key == keyboard.Key.enter:
            print(f"Selected: {self.diagonal_menu_text[self.diagonal_menu_cursor]}")
            self.diagonal_menu_up = False
            if (abs(self.cursor_placement["vertical"] - self.char_vertical) + abs(self.cursor_placement["horizontal"] - self.char_horizontal) <= self.walk_distance):
                
                if self.diagonal_menu_cursor == 0:
                    self.show_attack_range_diagonal_cursor_tf =True
                elif self.diagonal_menu_cursor == 1:
                    self.guarding_diagonal_menu = True
                elif self.diagonal_menu_cursor == 2:
                    self.show_item_menu = True
                elif self.diagonal_menu_cursor == 3:
                    self.char_vertical = self.cursor_placement["vertical"]
                    self.char_horizontal = self.cursor_placement["horizontal"]
            else:
                self.cursor_placement = self.char_position
            self.draw_map()
        elif key == keyboard.Key.backspace:
            self.diagonal_menu_up = False
            self.draw_map()

    def move_cursor(self):
        with keyboard.Listener(on_press=self.on_pressed) as listener:
            self.draw_map()
            listener.join()

    def show_diagonal_menu(self):
        self.diagonal_menu_up = True
        self.draw_map()

if __name__ == "__main__":
    Game()
