import zipfile
import promptlib
import os


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
