import os
import sys
import time as t
import random as r

try:
    import keyboard
    from termcolor import colored
    import ctypes
    import promptlib
    import win32gui as win32
except ImportError:
    print("Not all packages are installed. Installing... ")
    os.system("pip install -r requirements.txt")

    import keyboard
    from termcolor import colored
    import ctypes
    import promptlib
    import win32gui as win32
clear_cmd = "clear"
if sys.platform == "win32":
    clear_cmd = "cls"
os.system(clear_cmd)



class Game:
    def __init__(self, screen_size: int, enemies_count: int, level_path: str):
        ctypes.windll.kernel32.SetConsoleTitleW("Shooter - playing")
        self.clear_screen()

        self.quit = False

        self.level_path = r"assets\standard_level.shtlvl"
        if level_path == "own":
            self.level_path = promptlib.Files().file()
        else:
            pass

        self.score = 0
        self.highscore = 0
        with open(r"assets\highscore.txt", "r") as f:
            self.highscore = int(f.read())

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

        self.enemie_pos()
        self.render_enemies()

        self.print_screen()
        t.sleep(0.1) # TODO: time with perf_counter
        self.clear_screen()

        self.time_score = int(t.perf_counter())

        for bullet in self.bullets:
            for enemie in self.enemies:
                if bullet["x_pos"] == enemie["x_pos"] and bullet["y_pos"] == enemie["y_pos"]:
                    bullet["is_active"] = False

        if self.screen[self.player["x_pos"]][self.player["y_pos"]] == colored(self.enemies[0]["icon"], "red") and self.player["is_active"]:
            self.lose()

        if keyboard.is_pressed("esc"):
            quit()


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


    def enemie_pos(self):
        for enemie in self.enemies:
            if enemie["is_active"] and enemie["move"]:
                wanted_x_pos = enemie["x_pos"]
                wanted_y_pos = enemie["y_pos"]
                if enemie["x_pos"] < self.player["x_pos"]:
                    wanted_x_pos = enemie["x_pos"] + 1
                elif enemie["x_pos"] > self.player["x_pos"]:
                    wanted_x_pos = enemie["x_pos"] - 1

                if enemie["y_pos"] < self.player["y_pos"]:
                    wanted_y_pos = enemie["y_pos"] + 1
                elif enemie["y_pos"] > self.player["y_pos"]:
                    wanted_y_pos = enemie["y_pos"] - 1

                can_go = True
                for test_enemie in self.enemies:
                    if test_enemie["is_active"] and test_enemie["x_pos"] == wanted_x_pos and test_enemie["y_pos"] == wanted_y_pos:
                        can_go = False
                        break

                if can_go:
                    enemie["x_pos"] = wanted_x_pos
                    enemie["y_pos"] = wanted_y_pos
            enemie["move"] = not enemie["move"]


    def bullets_pos(self):
        for bullet in self.bullets:
            if bullet["is_active"]:
                bullet["x_pos"] += bullet["x_force"]
                bullet["y_pos"] += bullet["y_force"]
            if self.screen[bullet["x_pos"]][bullet["y_pos"]] == "o":
                bullet["is_active"] = False


    def player_pos(self):
        if keyboard.is_pressed("w"): # x - 1
            if not self.screen[self.player["x_pos"] - 1][self.player["y_pos"]] == "o":
                self.player["x_pos"] -= 1
        elif keyboard.is_pressed("s"):
            if not self.screen[self.player["x_pos"] + 1][self.player["y_pos"]] == "o":
                self.player["x_pos"] += 1

        if keyboard.is_pressed("w"): # x + 1
            if not self.screen[self.player["x_pos"] - 1][self.player["y_pos"]] == "o":
                self.player["x_pos"] -= 1
        elif keyboard.is_pressed("s"):
            if not self.screen[self.player["x_pos"] + 1][self.player["y_pos"]] == "o":
                self.player["x_pos"] += 1

        if keyboard.is_pressed("a"): # y - 1
            if not self.screen[self.player["x_pos"]][self.player["y_pos"] - 1] == "o":
                self.player["y_pos"] -= 1
        elif keyboard.is_pressed("d"):
            if not self.screen[self.player["x_pos"]][self.player["y_pos"] + 1] == "o":
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
        with open(self.level_path, "r") as f:
            level_dat = []
            for line in f:
                level_dat.append(line.replace("\n", "").split(" "))
        for x in range(len(level_dat)):
            for y in range(len(level_dat[x])):
                if level_dat[x][y] == "o":
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
            self.screen[self.player["x_pos"]][self.player["y_pos"]] = colored(self.player["icon"], "white")


    def render_walls(self):
        for wall in self.walls:
            if wall["is_active"]:
                self.screen[wall["x_pos"]][wall["y_pos"]] = wall["icon"]


    def render_enemies(self):
        for enemie in self.enemies:
            if enemie["is_active"]:
                if self.screen[enemie["x_pos"]][enemie["y_pos"]] == colored("|", "white") or self.screen[enemie["x_pos"]][enemie["y_pos"]] == colored("-", "white"):
                    enemie["is_active"] = False
                    self.score += 1
                    self.enemies.append({"x_pos": r.randint(3, self.screen_size - 3),
                                        "y_pos": r.randint(3, self.screen_size - 3),
                                        "icon": "x", "is_active": True,
                                        "move": True if r.randint(0, 1) == 0 else False})
                self.screen[enemie["x_pos"]][enemie["y_pos"]] = colored(enemie["icon"], "red")


    def render_bullets(self):
        for bullet in self.bullets:
            if bullet["is_active"]:
                self.screen[bullet["x_pos"]][bullet["y_pos"]] = colored(bullet["icon"], "white")


    # screen handling
    def clear_screen(self):
        cls_cmd = "clear"
        if sys.platform == "win32":
            cls_cmd = "cls"
        os.system(cls_cmd)


    def print_screen(self):
        time_played = str(t.perf_counter())
        string = colored(f"Time playing: {time_played[:time_played.find('.') + 3]}\n", "white")
        for x in self.screen:
            for y in x:
                string +=  y + " "
            string += "\n"
        string += colored(f"Score: {self.score}\n", "white")
        string += colored(f"Highscore: {self.highscore}\n", "white")
        print(string)


    def lose(self):
        print(colored("U ded", "red"))
        print(colored(f"Score: {str(self.score)}", "white"))
        if self.score > self.highscore:
            print("New Highscore!")
            with open(r"assets\highscore.txt", "w") as f:
                f.write(str(self.score))
        print("Enter to continue")
        while not keyboard.is_pressed("enter"):
            pass
        self.quit = True


def main(mode):
    app = Game(30, 10, mode)


if __name__ == "__main__":
    app = Game(30, 10, "standard")
