from tkinter import *
from functools import partial
import keyboard
import traceback
import promptlib
import sys


class Builder:
    def __init__(self, level_dir):
        self.level_dir = level_dir

        self.builder = Tk("Builder")
        self.builder.protocol("WM_DELETE_WINDOW", self.on_close)

        self.get_level_dat()
        self.buttons = {}
        self.set_buttons()
        self.get_buttons_state()

        self.builder.mainloop()


    def get_level_dat(self):
        self.level_dat = []
        with open(self.level_dir, "r") as f:
            for line in f:
                self.level_dat.append(list(line.replace("\n", "").replace(" ", "")))
        if len(self.level_dat) == 0:
            self.level_dat = [["." for x in range(30)] for y in range(30)]


    def set_buttons(self):
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                self.buttons[f"{x}/{y}"] = Button(self.builder, command=partial(self.toggle_field, x, y), width=2, height=1, bg="grey")
                self.buttons[f"{x}/{y}"].grid(row=x, column=y)


    def get_buttons_state(self):
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                if self.level_dat[x][y] == "o":
                    self.buttons[f"{x}/{y}"].configure(bg="red")
                else:
                    self.buttons[f"{x}/{y}"].configure(bg="grey")


    def toggle_field(self, x, y):
        if self.level_dat[x][y] == "o":
            self.buttons[f"{x}/{y}"].configure(bg="grey")
            self.level_dat[x][y] = "."
        elif self.level_dat[x][y] == ".":
            self.buttons[f"{x}/{y}"].configure(bg="red")
            self.level_dat[x][y] = "o"


    def on_close(self):
        string = ""
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                string += self.level_dat[x][y]
            string += "\n"
        with open(self.level_dir, "w") as f:
            f.write(string)
        self.builder.destroy()
        sys.exit()


if __name__ == "__main__":
    app = Builder(promptlib.Files().file())
