import game
import keyboard
import level_builder
import os
import sys
import win32gui as win32
import ctypes


class Menu:
    def __init__(self):
        ctypes.windll.kernel32.SetConsoleTitleW("Shooter")

        print("Standard (space)")
        print("Own (o)")
        print("Level Builder (b)")
        print("Quit (esc)")

        continued = False
        is_game = False
        map = ""
        while not continued:
            if "Shooter" in win32.GetWindowText(win32.GetForegroundWindow()):
                if keyboard.is_pressed("space"):
                    continued = True
                    is_game = True
                    app = game.Game(30, 10, "standard")
                elif keyboard.is_pressed("o"):
                    continued = True
                    is_game = True
                    app = game.Game(30, 10, "own")
                elif keyboard.is_pressed("b"):
                    continued = True
                    self.clear_screen()
                    builder = level_builder.Builder(input("Leveldir: "))
                elif keyboard.is_pressed("esc"):
                    quit()

        if is_game:
            for i in range(150):
                keyboard.block_key(i)
            is_paused = False
            while True:
                if "Shooter" in win32.GetWindowText(win32.GetForegroundWindow()):
                    is_paused = False
                else:
                    is_paused = True

                if not is_paused:
                    app.loop()


    def clear_screen(self):
        clear_cmd = "clear"
        if sys.platform == "win32":
            clear_cmd = "cls"
        os.system(clear_cmd)


def main():
    menu = Menu()


if __name__ == "__main__":
    main()
