import random as r


level_path = input("Level path: ")
mode = input("Mode: ").lower()

if mode == "grid":
    with open(level_path, "w") as f:
        for i in range(30):
            f.write(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n")
elif mode == "random":
    with open(level_path, "w") as f:
        for x in range(30):
            string = ""
            for y in range(30):
                if r.randint(0, 12) == 0:
                    string += "o "
                else:
                    string += ". "
            f.write(string + "\n")
