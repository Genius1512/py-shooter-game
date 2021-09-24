import zipfile
import promptlib
import os


# pyinstaller --onefile -n shooter_installer_1.3 main.py

is_valid = False
y_n = ""
while not is_valid:
    y_n = input("Install Shooter (y/n): ").lower()
    if y_n == "y":
        is_valid = True
    elif y_n == "n":
        print("Installing cancelled")
        quit()
    else:
        print("Invalid input")

print("adf")
quit()

prompter = promptlib.Files()

print("Select the zip file")
zip_dir = prompter.file()
print("Select the dir you want to install")
install_dir = prompter.dir()

with zipfile.ZipFile(zip_dir, "r") as zip:
    zip.extractall(install_dir + r"\Shooter")
os.popen("del " + zip_dir)
print("Installed succesfully")
input("")
