from tkinter import *
from functools import partial


class Builder:
    def __init__(self, level_dir):
        self.level_dir = level_dir
        self.level_dat = ""
        try:
            with open(self.level_dir, "r") as f:
                self.level_dat = f.read()[:-1]
            self.get_level_dat()
        except FileNotFoundError:
            self.level_dat = [["." for x in range(30)] for y in range(30)]


        self.builder = Tk("Builder")
        self.builder.protocol("WM_DELETE_WINDOW", self.save_field)

        self.buttons = {}
        self.set_buttons()
        self.get_fields()

        self.builder.mainloop()

    def get_level_dat(self):
        self.level_dat = self.level_dat.split("\n")
        for line_num in range(len(self.level_dat)):
            self.level_dat[line_num] = self.level_dat[line_num].split(" ")


    def set_buttons(self):
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                self.buttons[f"{x}/{y}"] = Button(command=partial(self.toggle_fields, x, y), width=2, height=1, bg="grey")
                self.buttons[f"{x}/{y}"].grid(row=x, column=y)


    def toggle_fields(self, x, y):
        if self.level_dat[x][y] == "o":
            self.buttons[f"{x}/{y}"].configure(bg="grey")
            self.level_dat[x][y] = "."
        else:
            self.buttons[f"{x}/{y}"].configure(bg="red")
            self.level_dat[x][y] = "o"


    def get_fields(self):
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                if self.level_dat[x][y] == "o":
                    self.buttons[f"{x}/{y}"].configure(bg="red")


    def save_field(self):
        string = ""
        for x in range(len(self.level_dat)):
            for y in range(len(self.level_dat[x])):
                string += self.level_dat[x][y] + " "
            string += "\n"
        string = string[:-1]
        with open(self.level_dir, "w") as f:
            f.write(string)

        self.builder.destroy()



if __name__ == "__main__":
    try:
        app = Builder(input("Leveldir: "))
    except Exception as error:
        print(error)
        input("")
