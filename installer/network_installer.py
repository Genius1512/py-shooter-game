import promptlib
import wget
import os
import zipfile


url = "http://192.168.0.230/Shooter.zip"
print("Select the dir you want to install")
folder_dir = promptlib.Files().dir()
file_dir = folder_dir + r"\Shooter.zip"

print("Downloading...")
wget.download(url, folder_dir)

print("Extracting")
with zipfile.ZipFile(file_dir, "r") as zip:
    zip.extractall(folder_dir + r"\Shooter")
print("Deleting zip")
os.popen("del " + file_dir)
print("Installed succesfully")
input("Enter to quit")
