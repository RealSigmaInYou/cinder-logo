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
            "pos2": {"vertical": 13, "horizontal": 15},
            "pos3": {"vertical": 9, "horizontal": 18}
        }
        self.enemy_start_positions = {
            "pos1": {"vertical": 25, "horizontal": 26},
            "pos2": {"vertical": 27, "horizontal": 27},
            "pos3": {"vertical": 23, "horizontal": 25}
        }

        self.selected_characters =["marph", "baileph", "krome"]
        self.number_of_units = 0
        for ally_positions in self.ally_start_positions:
            self.number_of_units +=1
            self.characters[self.selected_characters[self.number_of_units-1]]["position"] = self.ally_start_positions[f"pos{self.number_of_units}"]
            self.characters[self.selected_characters[self.number_of_units-1]]["misc"]["id"] = self.number_of_units

        self.number_of_allies = self.number_of_units
        for enemy_positions in self.enemy_start_positions:
            self.number_of_units +=1
        self.number_of_enemies = self.number_of_units-self.number_of_allies
        
        print(self.characters["marph"]["position"])
        print(self.characters["baileph"]["position"])

        self.cursor_placement = {
            "vertical": self.characters[self.selected_characters[0]]["position"]["vertical"],
            "horizontal": self.characters[self.selected_characters[0]]["position"]["horizontal"]
        }
        self.unit_selected = ""
        self.diagonal_menu_text = ["Attack   |   ", "Guard   |   ", "Items   |   ", "Wait"]
        self.diagonal_menu_up = False
        self.diagonal_menu_cursor = 0

        self.gridmap = {}
        self.gridnr = 1
        self.mapstring = ""
        self.show_range = ""

        self.preview_move = []

        self.show_attack_range_diagonal_cursor_tf = False
        self.diagonal_menu_cursor = 1

        self.something_in_range = False

        self.ally_character = termcolor.colored("9 ", "green")

        self.move_cursor()

    def get_add_to_map(self):


        if self.show_attack_range_diagonal_cursor_tf == False:
            for slot in self.gridmap:
                for character in self.characters:
                    if (self.characters[character]["position"]["vertical"] == self.gridmap[slot][0]) and (self.characters[character]["position"]["horizontal"] == self.gridmap[slot][1]): # and (self.characters[character]["position"]["vertical"] == self.ally_start_positions[pos]["vertical"] and self.characters[character]["position"]["horizontal"] == self.ally_start_positions[pos]["horizontal"]):
                        self.gridmap[slot] = self.characters[character]["position"]["vertical"], self.characters[character]["position"]["horizontal"], self.ally_character
                    elif (self.cursor_placement["vertical"] == self.gridmap[slot][0])and (self.cursor_placement["horizontal"] == self.gridmap[slot][1]):
                        self.gridmap[slot] = self.cursor_placement["vertical"], self.cursor_placement["horizontal"], termcolor.colored("O ", "yellow")

                    elif (abs(self.gridmap[slot][0] - self.characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range) and (self.show_attack_range_diagonal_cursor_tf == False):
                        for charonslot in self.characters:
                            if (self.gridmap[slot][0], self.gridmap[slot][1] != self.characters[charonslot]["position"]["vertical"], self.characters[charonslot]["position"]["horizontal"]):
                                self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "cyan")
                            else:
                                pass
                    elif (abs(self.gridmap[slot][0] - self.characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["walk_distance"] + self.characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range) and self.show_attack_range_diagonal_cursor_tf == False:
                        for charonslot in self.characters:
                            if (self.gridmap[slot][0], self.gridmap[slot][1] != self.characters[charonslot]["position"]["vertical"], self.characters[charonslot]["position"]["horizontal"]):
                                self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")
                            else:
                                pass
                    elif (abs(self.gridmap[slot][0] - self.characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.characters[character]["position"]["horizontal"]) <= self.characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.characters[character]["position"] or character in self.show_range) and self.show_attack_range_diagonal_cursor_tf == True:
                        for charonslot in self.characters:
                            if (self.gridmap[slot][0], self.gridmap[slot][1] != self.characters[charonslot]["position"]["vertical"], self.characters[charonslot]["position"]["horizontal"]):
                                self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")
                            else:
                                self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][0], termcolor.colored("9", "light_red")
                                self.something_in_range = True
        elif self.show_attack_range_diagonal_cursor_tf == True:
            for slot in self.gridmap:
                if self.characters[self.unit_selected]["position"]["vertical"] == self.gridmap[slot][0] and self.characters[self.unit_selected]["position"]["horizontal"] == self.gridmap[slot][1]:
                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], self.ally_character
                elif self.cursor_placement["vertical"] == self.gridmap[slot][0] and self.cursor_placement["horizontal"] == self.gridmap[slot][1]:
                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("O ", "yellow")
                elif (abs(self.gridmap[slot][0] - self.cursor_placement["vertical"]) + abs(self.gridmap[slot][1] - self.cursor_placement["horizontal"]) <= self.characters[self.unit_selected]["misc"]["attack_range"]):
                    for charonslot in self.characters:
                        if self.gridmap[slot][2] != self.ally_character:
                            self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")
                            break
                        else:
                            self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][0], termcolor.colored("9 ", "light_red")

    def draw_map(self):
        self.gridmap = {}
        self.mapstring = ""
        self.gridnr = 1

        os.system("cls")

        for y in range(self.vertical):
            for x in range(self.horizontal):
                self.gridmap[self.gridnr] = y+1, x, "# "
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

        if self.diagonal_menu_up:
            print(self.diagonal_menu_text)
        
        print(self.cursor_placement)
        print(self.diagonal_menu_cursor)
        print(self.something_in_range)

    def on_pressed(self, key):
        if self.diagonal_menu_up == False and self.show_attack_range_diagonal_cursor_tf == False:
            if key == keyboard.Key.up and self.cursor_placement["vertical"] > 1:
                self.cursor_placement["vertical"] -= 1
                self.draw_map()
            elif key == keyboard.Key.down and self.cursor_placement["vertical"] < self.vertical:
                self.cursor_placement["vertical"] += 1
                self.draw_map()
            elif key == keyboard.Key.left and self.cursor_placement["horizontal"] > 0:
                self.cursor_placement["horizontal"] -= 1
                self.draw_map()
            elif key == keyboard.Key.right and self.cursor_placement["horizontal"] < self.horizontal - 1:
                self.cursor_placement["horizontal"] += 1
                self.draw_map()
            elif key == keyboard.Key.enter:
                if self.unit_selected != "":
                    if (abs(self.cursor_placement["vertical"] - self.characters[self.unit_selected]["position"]["vertical"]) + abs(self.cursor_placement["horizontal"] - self.characters[self.unit_selected]["position"]["horizontal"])) <= self.characters[self.unit_selected]["misc"]["walk_distance"]:
                        self.show_diagonal_menu()
                else:
                    for character in self.characters:
                        if self.cursor_placement == self.characters[character]["position"]:
                            self.unit_selected = character
                            self.show_range=character
                self.draw_map()
            elif key == keyboard.Key.backspace and self.unit_selected != "":
                for character in self.characters:
                    self.unit_selected = ""
                    if character in self.show_range:
                        self.show_range = ""
                self.draw_map()
        elif self.show_attack_range_diagonal_cursor_tf == True and self.diagonal_menu_up == False:
            if key == keyboard.Key.enter:
                
                self.characters[self.unit_selected]["position"]["vertical"] = self.cursor_placement["vertical"]
                self.characters[self.unit_selected]["position"]["horizontal"] = self.cursor_placement["horizontal"]
                self.show_attack_range_diagonal_cursor_tf = False
                self.diagonal_menu_up = False
            
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
            if (abs(self.cursor_placement["vertical"] - self.characters[self.unit_selected]["position"]["vertical"]) + abs(self.cursor_placement["horizontal"] - self.characters[self.unit_selected]["position"]["horizontal"]) <= self.characters[self.unit_selected]["misc"]["walk_distance"]):
                
                if self.diagonal_menu_cursor == 0:
                    self.show_attack_range_diagonal_cursor_tf =True
                elif self.diagonal_menu_cursor == 1:
                    print("guarding GRUUUUUUUAAAAAAUGGHHH")
                    self.guarding_diagonal_menu = True
                    for character in self.characters:
                        if (character != self.unit_selected) and (self.cursor_placement["vertical"] != self.characters[character]["position"]["vertical"]) and (self.cursor_placement["horizontal"] != self.characters[character]["position"]["horizontal"]):
                            self.characters[self.unit_selected]["position"]["vertical"] = self.cursor_placement["vertical"]
                            self.characters[self.unit_selected]["position"]["horizontal"] = self.cursor_placement["horizontal"]

                elif self.diagonal_menu_cursor == 2:
                    print("item used or something")
                    self.show_item_menu = True
                    for character in self.characters:
                        if (character != self.unit_selected) and (self.cursor_placement["vertical"] != self.characters[character]["position"]["vertical"]) and (self.cursor_placement["horizontal"] != self.characters[character]["position"]["horizontal"]):
                            self.characters[self.unit_selected]["position"]["vertical"] = self.cursor_placement["vertical"]
                            self.characters[self.unit_selected]["position"]["horizontal"] = self.cursor_placement["horizontal"]
                elif self.diagonal_menu_cursor == 3:
                    for character in self.characters:
                        if (character != self.unit_selected) and (self.cursor_placement["vertical"] != self.characters[character]["position"]["vertical"]) and (self.cursor_placement["horizontal"] != self.characters[character]["position"]["horizontal"]):
                            self.characters[self.unit_selected]["position"]["vertical"] = self.cursor_placement["vertical"]
                            self.characters[self.unit_selected]["position"]["horizontal"] = self.cursor_placement["horizontal"]
            else:
                self.cursor_placement = self.characters[self.selected_characters[0]]
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