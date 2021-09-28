import keyboard
from termcolor import colored
import ctypes
import promptlib
import win32gui as win32
import sys
import os
import standard
import time as t
import random as r
from localStoragePy import localStoragePy



class Game:
    def __init__(self, screen_size: int, enemies_count: int, level: str):
        ctypes.windll.kernel32.SetConsoleTitleW("Shooter")
        self.clear_screen()

        self.enemies_count = enemies_count

        self.quit = False

        if level == "standard":
            self.level_dat = standard.level
        elif level == "own":
            prompter = promptlib.Files()
            with open(prompter.file(), "r") as f:
                self.level_dat = []
                for line in f:
                    self.level_dat.append(list(line.replace("\n", "").replace(" ", "")))

        self.score = 0
        self.localStorage = localStoragePy("text-shooter")
        self.highscore = self.localStorage.getItem("highscore")
        if self.highscore == None:
            self.localStorage.setItem("highscore", 0)
            self.highscore = 0
        self.highscore = int(self.highscore)

        self.colors = {"player": "white", "wall": "green", "enemy": "red", "bullet": "white", "text": "white"}
        self.VALID_COLROS = ["white", "red", "green", "blue"]
        self.get_colors()

        self.background = " "
        self.screen_size = screen_size
        self.screen = [[self.background for x in range(0, self.screen_size)] for y in range(0, self.screen_size)]

        self.walls = []
        self.set_walls()

        self.bullets = []

        self.enemies = []
        for i in range(enemies_count):
            self.enemies.append({"x_pos": r.randint(self.screen_size / 2, self.screen_size - 3),
                                "y_pos": r.randint(self.screen_size / 2, self.screen_size - 3),
                                "icon": "x", "is_active": True,
                                "move": True if r.randint(0, 1) == 0 else False})

        self.player = {"x_pos": 2, "y_pos": 2, "icon": ">", "is_active": True, "shoot_timer": 2}


    def loop(self):
        self.screen = [[self.background for x in range(0, self.screen_size)] for y in range(0, self.screen_size)]

        self.render_walls()

        self.player_pos()
        self.player_rot()
        self.shoot()
        self.render_player()

        self.bullets_pos()
        self.render_bullets()

        self.enemy_spawning()
        self.enemy_pos()
        self.render_enemies()

        self.print_screen()
        t.sleep(0.1)
        self.clear_screen()

        self.time_score = int(t.perf_counter())

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet["x_pos"] == enemy["x_pos"] and bullet["y_pos"] == enemy["y_pos"]:
                    bullet["is_active"] = False

        if self.enemies[0]["icon"] in self.screen[self.player["x_pos"]][self.player["y_pos"]] and self.player["is_active"]:
            self.lose()

        if keyboard.is_pressed("esc"):
            self.quit = True


    def get_colors(self):
        path = self.localStorage.getItem(r"colors_path")
        if not path == None:
            with open(path, "r") as f:
                for line in f:
                    try:
                        if line.split(":")[1].replace("\n", "") in self.VALID_COLROS:
                            self.colors[line.split(":")[0]] = line.split(":")[1].replace("\n", "")
                    except KeyError:
                        pass


    def shoot(self):
        self.player["shoot_timer"] += 1
        if keyboard.is_pressed("space") and self.player["shoot_timer"] >= 6:
            if self.player["icon"] == "v":
                self.bullets.append({"x_pos": self.player["x_pos"], "y_pos": self.player["y_pos"], "x_force": 1, "y_force": 0, "icon": "|", "is_active": True})
            elif self.player["icon"] == "^":
                self.bullets.append({"x_pos": self.player["x_pos"], "y_pos": self.player["y_pos"], "x_force": -1, "y_force": 0, "icon": "|", "is_active": True})
            elif self.player["icon"] == ">":
                self.bullets.append({"x_pos": self.player["x_pos"], "y_pos": self.player["y_pos"], "x_force": 0, "y_force": 1, "icon": "-", "is_active": True})
            elif self.player["icon"] == "<":
                self.bullets.append({"x_pos": self.player["x_pos"], "y_pos": self.player["y_pos"], "x_force": 0, "y_force": -1, "icon": "-", "is_active": True})
            self.player["shoot_timer"] = 0


    def enemy_pos(self):
        for enemy in self.enemies:
            if enemy["is_active"] and enemy["move"]:
                wanted_x_pos = enemy["x_pos"]
                wanted_y_pos = enemy["y_pos"]
                if enemy["x_pos"] < self.player["x_pos"]:
                    wanted_x_pos = enemy["x_pos"] + 1
                elif enemy["x_pos"] > self.player["x_pos"]:
                    wanted_x_pos = enemy["x_pos"] - 1

                if enemy["y_pos"] < self.player["y_pos"]:
                    wanted_y_pos = enemy["y_pos"] + 1
                elif enemy["y_pos"] > self.player["y_pos"]:
                    wanted_y_pos = enemy["y_pos"] - 1

                can_go = True
                for test_enemy in self.enemies:
                    if test_enemy["is_active"] and test_enemy["x_pos"] == wanted_x_pos and test_enemy["y_pos"] == wanted_y_pos:
                        can_go = False
                        break

                if can_go:
                    enemy["x_pos"] = wanted_x_pos
                    enemy["y_pos"] = wanted_y_pos
            enemy["move"] = not enemy["move"]


    def bullets_pos(self):
        for bullet in self.bullets:
            if bullet["is_active"]:
                bullet["x_pos"] += bullet["x_force"]
                bullet["y_pos"] += bullet["y_force"]
            if "o" in self.screen[bullet["x_pos"]][bullet["y_pos"]]:
                bullet["is_active"] = False


    def player_pos(self):
        if keyboard.is_pressed("w"): # x - 1
            if not "o" in self.screen[self.player["x_pos"] - 1][self.player["y_pos"]]:
                self.player["x_pos"] -= 1
        elif keyboard.is_pressed("s"):
            if not "o" in self.screen[self.player["x_pos"] + 1][self.player["y_pos"]]:
                self.player["x_pos"] += 1

        if keyboard.is_pressed("w"): # x + 1
            if not "o" in self.screen[self.player["x_pos"] - 1][self.player["y_pos"]]:
                self.player["x_pos"] -= 1
        elif keyboard.is_pressed("s"):
            if not "o" in self.screen[self.player["x_pos"] + 1][self.player["y_pos"]]:
                self.player["x_pos"] += 1

        if keyboard.is_pressed("a"): # y - 1
            if not "o" in self.screen[self.player["x_pos"]][self.player["y_pos"] - 1]:
                self.player["y_pos"] -= 1
        elif keyboard.is_pressed("d"):
            if not "o" in self.screen[self.player["x_pos"]][self.player["y_pos"] + 1]:
                self.player["y_pos"] += 1


    def player_rot(self):
        if keyboard.is_pressed("w"):
            self.player["icon"] = "^"
        elif keyboard.is_pressed("s"):
            self.player["icon"] = "v"
        elif keyboard.is_pressed("a"):
            self.player["icon"] = "<"
        elif keyboard.is_pressed("d"):
            self.player["icon"] = ">"


    def set_walls(self):
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                if self.level_dat[x][y] == "o":
                    self.walls.append({"x_pos": x, "y_pos": y, "icon": "o", "is_active": True})

        for x in range(self.screen_size):
            if x == 0 or x == self.screen_size - 1:
                for y in range(self.screen_size):
                    self.walls.append({"x_pos": x, "y_pos": y, "icon": "o", "is_active": True})
            for y in range(self.screen_size):
                if y == 0 or y == self.screen_size - 1:
                    self.walls.append({"x_pos": x, "y_pos": y, "icon": "o", "is_active": True})

    # entity rendering
    def render_player(self):
        if self.player["is_active"]:
            self.screen[self.player["x_pos"]][self.player["y_pos"]] = self.player["icon"]


    def render_walls(self):
        for wall in self.walls:
            if wall["is_active"]:
                self.screen[wall["x_pos"]][wall["y_pos"]] = wall["icon"]


    def render_enemies(self):
        for enemy in self.enemies:
            if enemy["is_active"]:
                if "|" in self.screen[enemy["x_pos"]][enemy["y_pos"]] or "-" in self.screen[enemy["x_pos"]][enemy["y_pos"]]:
                    enemy["is_active"] = False
                    self.score += 1
                    if self.score % 5 == 0:
                        self.enemies_count += 1
                self.screen[enemy["x_pos"]][enemy["y_pos"]] = enemy["icon"]


    def enemy_spawning(self):
        alive_enemies = 0
        for enemy in self.enemies:
            if enemy["is_active"]:
                alive_enemies += 1

        while alive_enemies < self.enemies_count:
            self.enemies.append({"x_pos": r.randint(3, self.screen_size - 3),
                                "y_pos": r.randint(3, self.screen_size - 3),
                                "icon": "x", "is_active": True,
                                "move": True if r.randint(0, 1) == 0 else False})
            alive_enemies = 0
            for enemy in self.enemies:
                if enemy["is_active"]:
                    alive_enemies += 1


    def render_bullets(self):
        for bullet in self.bullets:
            if bullet["is_active"]:
                self.screen[bullet["x_pos"]][bullet["y_pos"]] = bullet["icon"]


    # screen handling
    def clear_screen(self):
        cls_cmd = "clear"
        if sys.platform == "win32":
            cls_cmd = "cls"
        os.system(cls_cmd)


    def print_screen(self):
        time_played = str(t.perf_counter())
        string = colored(f"Time playing: {time_played[:time_played.find('.') + 3]}\n", self.colors["text"])
        for x in self.screen:
            for y in x:
                _y = ""
                if y in ["|", "-"]:
                    _y = colored(y, self.colors["bullet"])
                elif y in [">", "<", "v", "^"]:
                    _y = colored(y, self.colors["player"])
                elif y in ["o"]:
                    _y = colored(y, self.colors["wall"])
                elif y in ["x"]:
                    _y = colored(y, self.colors["enemy"])
                else:
                    _y = y
                string +=  _y + " "
            string += "\n"
        string += colored(f"Score: {self.score}\n", self.colors["text"])
        string += colored(f"Highscore: {self.highscore}\n", self.colors["text"])
        alive_enemies = 0
        for enemy in self.enemies:
            if enemy["is_active"]:
                alive_enemies += 1
        string += colored(f"Alive enemies: {alive_enemies}", self.colors["text"])
        print(string)


    def lose(self):
        print(colored("U ded", "red"))
        print(colored(f"Score: {str(self.score)}", "white"))
        if self.score > self.highscore:
            print("New Highscore!")
            self.localStorage.setItem("highscore", self.score)
        print("Enter to continue")
        while not keyboard.is_pressed("enter"):
            pass
        self.quit = True


def main(mode):
    app = Game(30, 10, mode)


if __name__ == "__main__":
    app = Game(30, 10, "standard")
