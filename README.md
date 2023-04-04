# google-photos-takeout-timestamp-fix
A python script to fix the timestamp issues in Google Photos Takeout  
  
*NOTE: tested on Windows 11 only*  

# Repository Contents
exif_folder.py - Python Script  
exif_folder_multiprocess.py - Python Script which uses concurrent.features module to run tasks in parallel   
exiftool.exe - ExifTool by Phil Harvey (https://exiftool.org/)  
README.md - Documentation  

# Quick Start
For large datasets, exif_folder_multiprocess.py is recommended. Syntax is same for both scripts. Please follow below instructions.   
1) Checkout repository  
2) Run the multiprocess script to run file processing tasks in parallel. Default MAX_WORKERS is set to 8.  
python.exe .\exif_folder_multiprocess.py <FOLDER_PATH> <FILE_EXTENSION>  
e.g.  
python.exe .\exif_folder_multiprocess.py 'D:\Google Photos\Photos XYZ' '.jpg'  

# Overview
The Python script expects two command line arguments. 1) Folder Path, 2) File extension.  
 
The Python script uses the os.walk() function to loop through all files and subdirectories in the folder. For each file, we check if it is a JSON file and, if so, get the path to the corresponding image/video file (depending on the extension provided as a second commandline argument). We then read the metadata from the JSON file, extract the photoTakenTime timestamp, convert the timestamp to required format, and build the ExifTool command using the formatted timestamp and the image path. Finally, we execute the command using the subprocess.run() method and print the output to the console.  
  
Below is the key value pair we are extracting from the .json file and using it to update/overwrite image/video FileCreateDate and FileModifyDate timestamps.  
  
"photoTakenTime": {  
    "timestamp": "1469858111",  
    "formatted": "30 Jul 2016, 05:55:11 UTC"  
}  

## Multi Processing  
The Python script uses the concurrent.futures module which provides a higher-level interface for asynchronously executing callables (running parallel tasks). The asynchronous execution can be performed with threads, using ThreadPoolExecutor, or separate processes, using ProcessPoolExecutor. Both implement the same interface, which is defined by the abstract Executor class.  
For details, please refer to https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor.  
The default setting creates a thread pool with 8 (default) worker threads, and use it to process the JSON files in parallel. You can adjust the max_workers parameter to control the number of threads.  
 
# Credits
This python script uses the amazing ExifTool by Phil Harvey (https://exiftool.org/).  
I tried to use https://github.com/laurentlbm/google-photos-takeout-date-fixer.git which is a fork of https://github.com/mattwilson1024/google-photos-exif but it was failing and had little control so thought to write a simple script instead. 

