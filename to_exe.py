import zipfile
import os


def to_zip():
    file = "Shooter.zip"  # zip file name
    directory = r"C:\Users\silva\Coding\Python\games\console-based\exe"
    with ZipFile(file, 'w') as zip:
       for path, directories, files in os.walk(directory):
           for file in files:
               file_name = os.path.join(path, file)
               zip.write(file_name) # zipping the file
    print("Contents of the zip file:")
    with ZipFile(file, 'r') as zip:
       zip.printdir()

os.chdir(r"cd C:\Users\silva\Coding\Python\games\console-based\exe")
os.system(r"pyinstaller C:\Users\silva\Coding\Python\games\console-based\src\main.py --icon=C:\Users\silva\Coding\Python\games\console-based\logo.ico --onefile -n Shooter")
to_zip()
