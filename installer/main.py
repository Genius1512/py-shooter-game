import os
import sys
from git import Repo
import promptlib


valid = False
while not valid:
    y_n = input("Install (y/n)? ").lower()
    if y_n == "y":
        valid = True
    elif y_n == "n":
        quit()
del valid
del y_n

prompter = promptlib.Files()
dir = prompter.dir()

try:
    print("Installing...")
    Repo.clone_from(r"https://github.com/Genius1512/console-based.git", dir + r"\Shooter")
except Exception as error:
    print("An error occured. Please check your internet connection")


move_cmd = "move " + dir + r"\Shooter\exe\Shooter.exe " + dir
del_cmd = "rmdir /S /Q " + dir + r"\Shooter"

os.popen(move_cmd)
os.popen(del_cmd)

sys.path += [dir]
