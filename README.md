# google-photos-takeout-timestamp-fix
A python script to fix the timestamp issues in Google Photos Takeout

*NOTE: tested on Windows 11 only*

# Repository Contents
exif_folder.py - Python Script 
exiftool.exe - ExifTool by Phil Harvey (https://exiftool.org/) 
README.md - Documentation 

# Quick Start
1) Checkout repository 
2) Run the script 
python.exe .\exif_folder.py <FOLDER_PATH> <FILE_EXTENSION> 
e.g. 
python.exe .\exif_folder.py 'D:\Google Photos\Photos XYZ' '.jpg' 

# Overview
The Python script expects two command line arguments. 1) Folder Path, 2) File extension. 
 
The Python script uses the os.walk() function to loop through all files and subdirectories in the folder. For each file, we check if it is a JSON file and, if so, get the path to the corresponding image/video file (depending on the extension provided as a second commandline argument). We then read the metadata from the JSON file, extract the photoTakenTime timestamp, convert the timestamp to required format, and build the ExifTool command using the formatted timestamp and the image path. Finally, we execute the command using the subprocess.run() method and print the output to the console. 
 
Below is the key value pair we are extracting from the .json file and using it to update/overwrite image/video FileCreateDate and FileModifyDate timestamps. 
 
"photoTakenTime": { 
    "timestamp": "1469858111", 
    "formatted": "30 Jul 2016, 05:55:11 UTC" 
} 
 
# Credits
This python script uses the amazing ExifTool by Phil Harvey (https://exiftool.org/). 
I tried to use https://github.com/laurentlbm/google-photos-takeout-date-fixer.git which is a fork of https://github.com/mattwilson1024/google-photos-exif but it was failing and had little control so thought to write a simple script instead. 

