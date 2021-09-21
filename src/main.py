import game
import keyboard
import level_builder
import os
import sys
import win32gui as win32
import ctypes
import traceback
import promptlib


# pyinstaller main.py --icon=../logo.ico --onefile -n Shooter


class CustomError(Exception):
    pass


class Menu:
    def __init__(app):
        ctypes.windll.kernel32.SetConsoleTitleW("Shooter")

        print("Standard (space)")
        print("Own (o)")
        print("Level Builder (b)")
        print("Quit (esc)")

        continued = False
        map = ""
        while not continued:
            is_game = False
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
                    app.clear_screen()
                    builder = level_builder.Builder(promptlib.Files().file())
                elif keyboard.is_pressed("esc"):
                    raise CustomError


        if is_game:
            is_paused = False
            while not app.quit:
                if "Shooter" in win32.GetWindowText(win32.GetForegroundWindow()):
                    is_paused = False
                else:
                    is_paused = True

                if not is_paused and not keyboard.is_pressed("q"):
                    app.loop()


    def clear_screen(app):
        clear_cmd = "clear"
        if sys.platform == "win32":
            clear_cmd = "cls"
        os.system(clear_cmd)


def main():
    while True:
        menu = Menu()


if __name__ == "__main__":
    try:
        main()
    except CustomError as error:
        pass
    except Exception as error:
        print("Error. Please contact Silvan Schmidt")
        traceback.print_exc()
        input("")
