@echo off
cd C:\Users\silva\Coding\Python\games\console-based\exe
pyinstaller C:\Users\silva\Coding\Python\games\console-based\src\main.py --icon=C:\Users\silva\Coding\Python\games\console-based\logo.ico --onefile -n Shooter
rmdir /S /Q build
move C:\Users\silva\Coding\Python\games\console-based\exe\dist\Shooter.exe C:\Users\silva\Coding\Python\games\console-based\exe
rmdir /S /Q dist
del Shooter.spec
powershell Compress-Archive C:\Users\silva\Coding\Python\games\console-based\exe C:\Users\silva\Coding\Python\games\console-based\installer\Shooter.zip
cd ..
