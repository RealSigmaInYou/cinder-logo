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
        self.slot_1_character = "marph"
        self.characters[self.slot_1_character]["position"] = self.ally_start_positions["pos1"]

        self.cursor_placement = {
            "vertical": self.characters[self.slot_1_character]["position"]["vertical"],
            "horizontal": self.characters[self.slot_1_character]["position"]["horizontal"]
        }
        self.unit_selected = False
        self.diagonal_menu_text = ["Attack   |   ", "Guard   |   ", "Items   |   ", "Wait"]
        self.diagonal_menu_up = False
        self.diagonal_menu_cursor = 0

        self.gridmap = {}
        self.gridnr = 0
        self.mapstring = ""
        self.show_range = []

        self.move_cursor()

    def draw_map(self):
        self.gridmap = {}
        self.mapstring = ""
        self.gridnr = 0

        char_position = self.characters[self.slot_1_character]["position"]
        char_vertical = char_position["vertical"]
        char_horizontal = char_position["horizontal"]
        walk_distance = self.characters[self.slot_1_character]["misc"]["walk_distance"]
        attack_range = self.characters[self.slot_1_character]["misc"]["attack_range"]

        os.system("cls")

        for y in range(self.vertical):
            for x in range(self.horizontal):
                if char_vertical == y and char_horizontal == x:
                    self.gridmap[self.gridnr] = y, x, termcolor.colored("9 ", "green")
                elif self.cursor_placement["vertical"] == y and self.cursor_placement["horizontal"] == x:
                    self.gridmap[self.gridnr] = y, x, termcolor.colored("O ", "yellow")
                elif (abs(y - char_vertical) + abs(x - char_horizontal) <= walk_distance) and (self.cursor_placement == char_position or self.slot_1_character in self.show_range):
                    self.gridmap[self.gridnr] = y, x, termcolor.colored("¤ ", "cyan")
                elif (abs(y - char_vertical) + abs(x - char_horizontal) <= walk_distance + attack_range) and (self.cursor_placement == char_position or self.slot_1_character in self.show_range):
                    self.gridmap[self.gridnr] = y, x, termcolor.colored("¤ ", "red")
                else:
                    self.gridmap[self.gridnr] = y, x, "# "

                self.gridnr += 1

        for z in self.gridmap:
            self.mapstring += self.gridmap[z][2]
            if self.gridmap[z][1] == self.horizontal - 1:
                self.mapstring += "\n"

        print(self.mapstring)
        if self.diagonal_menu_up:
            print(self.diagonal_menu_text)

    def on_pressed(self, key):
        char_position = self.characters[self.slot_1_character]["position"]
        char_vertical = char_position["vertical"]
        char_horizontal = char_position["horizontal"]
        walk_distance = self.characters[self.slot_1_character]["misc"]["walk_distance"]

        if not self.diagonal_menu_up:
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
                if self.unit_selected:
                    if (abs(self.cursor_placement["vertical"] - char_vertical) +
                            abs(self.cursor_placement["horizontal"] - char_horizontal)) <= walk_distance:
                        self.show_diagonal_menu()
                else:
                    if self.cursor_placement == char_position:
                        self.unit_selected = True
                        self.show_range.append(self.slot_1_character)
                self.draw_map()
            elif key == keyboard.Key.backspace and self.unit_selected:
                self.unit_selected = False
                self.show_range.remove(self.slot_1_character)
                self.draw_map()
        else:
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
