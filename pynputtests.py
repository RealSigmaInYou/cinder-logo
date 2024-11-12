import json
import termcolor
from pynput import keyboard
import os
import attacks_and_scaling

class Game:
    def __init__(self):
        with open("characters.json", "r") as characters_raw:
            self.characters = json.load(characters_raw)
        
        with open("enemies.json", "r") as enemies_raw:
            self.enemies = json.load(enemies_raw)

        with open("maps.json", "r") as maps_raw:
            maps = json.load(maps_raw)
        

        self.current_map = 1
        self.vertical = maps[str(self.current_map)]["size"][0]
        self.horizontal = maps[str(self.current_map)]["size"][1]

        self.map_ally_start_tiles = maps[str(self.current_map)]["ally_start_tiles"]
        pos_number = 0
        self.ally_start_positions = {}
        for allypos in self.map_ally_start_tiles:
            print(self.map_ally_start_tiles)
            print(allypos)
            self.ally_start_positions[f"pos{pos_number+1}"] =  {"vertical": allypos[0], "horizontal": allypos[1]}
            pos_number +=1

        self.map_enemy_start_tiles = maps[str(self.current_map)]["enemy_start_tiles"]
        pos_number = 0
        self.enemy_start_positions = {}
        for enemypos in self.map_enemy_start_tiles:
            self.enemy_start_positions[f"pos{pos_number+1}"] =  {"vertical": enemypos[0], "horizontal": enemypos[1]}
            pos_number +=1

        self.all_characters = {}

        self.selected_characters =["marph", "baileph", "krome"]
        self.number_of_units = 0
        for ally_positions in self.ally_start_positions:
            self.number_of_units +=1
            self.characters[self.selected_characters[self.number_of_units-1]]["position"] = self.ally_start_positions[f"pos{self.number_of_units}"]
            self.characters[self.selected_characters[self.number_of_units-1]]["misc"]["id"] = self.number_of_units
            self.all_characters[self.selected_characters[self.number_of_units-1]] = self.characters[self.selected_characters[self.number_of_units-1]]
        
        
        self.all_enemies = []
        for enemy in self.enemies:
            self.all_enemies.append(enemy)
        self.number_of_allies = self.number_of_units

        for enemy_positions in self.enemy_start_positions:
            self.number_of_units +=1
            self.number_of_enemies = self.number_of_units - self.number_of_allies
            self.enemies[self.all_enemies[self.number_of_enemies-1]]["position"] = self.enemy_start_positions[f"pos{self.number_of_enemies}"]
            self.enemies[self.all_enemies[self.number_of_enemies-1]]["misc"]["id"] = self.number_of_units
            self.all_characters[self.all_enemies[self.number_of_enemies-1]] = self.enemies[self.all_enemies[self.number_of_enemies-1]]
        self.number_of_enemies = self.number_of_units-self.number_of_allies

        for character in self.all_characters:
            self.all_characters[character]["misc"]["hp"] = self.all_characters[character]["stats"]["vigor"] * 2.5
            self.all_characters[character]["misc"]["max_hp"] = self.all_characters[character]["misc"]["hp"]
            


        self.cursor_placement = {
            "vertical": self.characters[self.selected_characters[0]]["position"]["vertical"],
            "horizontal": self.characters[self.selected_characters[0]]["position"]["horizontal"]
        }
        self.unit_selected = ""
        self.diagonal_menu1 = "x"
        self.diagonal_menu2 = " "
        self.diagonal_menu3 = " "
        self.diagonal_menu4 = " "
        self.diagonal_menu_text = f"Attack [{self.diagonal_menu1}]  |   ", f"Guard [{self.diagonal_menu2}]  |   ", f"Items [{self.diagonal_menu3}]  |   ", f"Wait [{self.diagonal_menu4}]"
        self.diagonal_menu_up = False
        self.diagonal_menu_cursor = 0

        self.gridmap = {}
        self.gridnr = 1
        self.mapstring = ""
        self.show_range = ""

        self.hover_character = ""

        self.preview_move = []

        self.show_attack_range_diagonal_cursor_tf = False
        self.diagonal_menu_cursor = 1

        self.something_in_range = False

        self.ally_character = termcolor.colored("9 ", "green")

        self.enemy_character = termcolor.colored("8 ", "light_red")

        self.bludwat = []


        self.move_cursor()

    def get_add_to_map(self):
        
            for slot in self.gridmap:
                for character in self.all_characters:
                    if (self.cursor_placement == self.all_characters[character]["position"]) or (self.hover_character == "" and character in self.show_range):
                        self.hover_character = character
                    if (self.all_characters[character]["position"]["vertical"] == self.gridmap[slot][0]) and (self.all_characters[character]["position"]["horizontal"] == self.gridmap[slot][1]) and (self.all_characters[character]["misc"]["id"] < self.number_of_allies +1): # and (self.characters[character]["position"]["vertical"] == self.ally_start_positions[pos]["vertical"] and self.characters[character]["position"]["horizontal"] == self.ally_start_positions[pos]["horizontal"]):
                        self.gridmap[slot] = self.characters[character]["position"]["vertical"], self.characters[character]["position"]["horizontal"], self.ally_character
                    elif (self.all_characters[character]["position"]["vertical"] == self.gridmap[slot][0]) and (self.all_characters[character]["position"]["horizontal"] == self.gridmap[slot][1]) and (self.all_characters[character]["misc"]["id"] > self.number_of_allies):
                        self.gridmap[slot] = self.enemies[character]["position"]["vertical"], self.enemies[character]["position"]["horizontal"], self.enemy_character
                    elif (self.cursor_placement["vertical"] == self.gridmap[slot][0])and (self.cursor_placement["horizontal"] == self.gridmap[slot][1]):
                        self.gridmap[slot] = self.cursor_placement["vertical"], self.cursor_placement["horizontal"], termcolor.colored("O ", "yellow")
                    if self.show_attack_range_diagonal_cursor_tf == False:
                        if (abs(self.gridmap[slot][0] - self.all_characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.all_characters[character]["position"]["horizontal"]) <= self.all_characters[character]["misc"]["walk_distance"]) and (self.cursor_placement == self.all_characters[character]["position"] or character in self.show_range) and (self.show_attack_range_diagonal_cursor_tf == False) and (self.gridmap[slot][2] != self.ally_character) and (self.gridmap[slot][2] != self.enemy_character):
                            for charonslot in self.all_characters:
                                if (self.gridmap[slot][0], self.gridmap[slot][1] != self.all_characters[charonslot]["position"]["vertical"], self.all_characters[charonslot]["position"]["horizontal"]):
                                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "cyan")
                                    self.hover_character = character
                                else:
                                    pass
                        elif (abs(self.gridmap[slot][0] - self.all_characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.all_characters[character]["position"]["horizontal"]) <= self.all_characters[character]["misc"]["walk_distance"] + self.all_characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.all_characters[character]["position"] or character in self.show_range) and (self.show_attack_range_diagonal_cursor_tf == False) and (self.gridmap[slot][2] != self.ally_character) and (self.gridmap[slot][2] != self.enemy_character):
                            for charonslot in self.all_characters:
                                if (self.gridmap[slot][0], self.gridmap[slot][1] != self.all_characters[charonslot]["position"]["vertical"], self.all_characters[charonslot]["position"]["horizontal"]):
                                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")
                                else:
                                    pass
                        elif (abs(self.gridmap[slot][0] - self.all_characters[character]["position"]["vertical"]) + abs(self.gridmap[slot][1] - self.all_characters[character]["position"]["horizontal"]) <= self.all_characters[character]["misc"]["attack_range"]) and (self.cursor_placement == self.all_characters[character]["position"] or character in self.show_range) and (self.show_attack_range_diagonal_cursor_tf == True) and (self.gridmap[slot][2] != self.ally_character) and (self.gridmap[slot][2] != self.enemy_character):
                            for charonslot in self.all_characters:
                                if (self.gridmap[slot][0], self.gridmap[slot][1] != self.all_characters[charonslot]["position"]["vertical"], self.all_characters[charonslot]["position"]["horizontal"]):
                                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], termcolor.colored("¤ ", "red")
                                else:
                                    self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][0], termcolor.colored("9", "light_red")
                                    self.something_in_range = True
                    elif self.show_attack_range_diagonal_cursor_tf == True:
                        if (abs(self.gridmap[slot][0] - self.cursor_placement["vertical"]) + abs(self.gridmap[slot][1] - self.cursor_placement["horizontal"]) <= self.all_characters[self.unit_selected]["misc"]["attack_range"]):
                            if character in self.all_enemies:
                                if self.gridmap[slot][2] == self.enemy_character:
                                    self.bludwat.append(self.gridmap[slot])

                                    if (self.gridmap[slot][0] == self.enemies[character]["position"]["vertical"]) and (self.gridmap[slot][1] == self.enemies[character]["position"]["horizontal"]):
                                        self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][1], self.enemy_character
                                        break
                                else:
                                        if self.gridmap[slot][2] !=self.enemy_character:
                                            self.gridmap[slot] = self.gridmap[slot][0], self.gridmap[slot][0],  termcolor.colored("¤ ", "red")

    def draw_map(self):
        self.gridmap = {}
        self.mapstring = ""
        self.gridnr = 1

        os.system("cls")

        for y in range(self.vertical):
            for x in range(self.horizontal):
                self.gridmap[self.gridnr] = y + 1, x, "# "
                self.gridnr += 1

        self.get_add_to_map()
        
        for z in self.gridmap:
            self.mapstring += self.gridmap[z][2]
            if self.gridmap[z][1] == self.horizontal - 1:
                self.mapstring += "\n"

        print(self.mapstring)
        if self.diagonal_menu_cursor == 0:
            self.diagonal_menu1 = "x"
            self.diagonal_menu2 = " "
            self.diagonal_menu3 = " "
            self.diagonal_menu4 = " "
        elif self.diagonal_menu_cursor == 1:
            self.diagonal_menu1 = " "
            self.diagonal_menu2 = "x"
            self.diagonal_menu3 = " "
            self.diagonal_menu4 = " "
        elif self.diagonal_menu_cursor == 2:
            self.diagonal_menu1 = " "
            self.diagonal_menu2 = " "
            self.diagonal_menu3 = "x"
            self.diagonal_menu4 = " "
        elif self.diagonal_menu_cursor == 3:
            self.diagonal_menu1 = " "
            self.diagonal_menu2 = " "
            self.diagonal_menu3 = " "
            self.diagonal_menu4 = "x"
        self.diagonal_menu_text = f"Attack [{self.diagonal_menu1}]  |   ", f"Guard [{self.diagonal_menu2}]  |   ", f"Items [{self.diagonal_menu3}]  |   ", f"Wait [{self.diagonal_menu4}]"

            
        print(self.cursor_placement)
        print(self.diagonal_menu_text)
        print(self.something_in_range)
        print(self.hover_character)
        if self.hover_character != "":
            print(f"[{self.all_characters[self.hover_character]['misc']['hp']}|{self.all_characters[self.hover_character]['misc']['max_hp']}]")
        print(self.bludwat)

        

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
                            attacks_defence_and_scaling(self.all_characters, self.unit_selected)

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

class attacks_defence_and_scaling():
    def preperation_variables(self, all_characters_importvar, selected_unit_importvar):
        self.all_characters = all_characters_importvar
        self.selected_unit = selected_unit_importvar
        selected_hp = self.all_characters[self.selected_unit]["stats"]["vigor"] * 2.5
        selected_physdmg_raw = self.all_characters[self.selected_unit]["stats"]["strength"]
        selected_magdmg_raw = self.all_characters[self.selected_unit]["stats"]["inteligence"]
        selected_hexdmg_raw = self.all_characters[self.selected_unit]["stats"]["arcane"]
        selected_dodge_raw = self.all_characters[self.selected_unit]["stats"]["dexterity"] #tenker noe sånn ta begges agility, og så ha 100-forksjellen^2 som blir hitrate
        selected_crit_raw = self.all_characters[self.selected_unit]["stats"]["dexterity"] #motsatt hvor det blir forksjellen^2-100
        selected_endurance_raw = (self.all_characters[self.selected_unit]["stats"]["endurance"]/100)*10 # damage offsetten. kanskje endurance på 7 eller noe og så fjerne hva det blir som prosent fra raw damage


if __name__ == "__main__":
    Game()

# når karakter velger angrip greie
# frigjør cursor og la spiller velge target (eller bla gjennom en liste)
# hover over karakter og select
# om karakter i range og ikke er karakteren som angriper (vi tillater ikke selvskading)
# så lagrer den navnet på hvem den hoverer og bruker den som en inportvar til attack_defence_and_scaling klassen. 
#
#
#
