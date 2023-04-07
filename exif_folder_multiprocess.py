import os
import json
import subprocess
from datetime import datetime
import concurrent.futures
import logging
import sys

# set the logging leve to debug if required
logging.basicConfig(level=logging.INFO)
    
# Function to process a JSON file and update image metadata
def process_json_file(json_path, ext):
    # Read JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    # Get the path to the corresponding image file
    image_path = os.path.splitext(json_path)[0]

    # Check if the image file exists and has the correct extension
    if os.path.isfile(image_path) and image_path.endswith(ext):
        # Fetch image timestamp from json
        modify_date_timestamp = json_data["photoTakenTime"]["timestamp"]
        date_time = datetime.fromtimestamp(int(modify_date_timestamp)).strftime("%Y:%m:%d %H:%M:%S")
        # Update image metadata        
        logging.debug("Using exif to update timestamp ", date_time,"of ", image_path)
        exiftool_cmd = ['exiftool', '-overwrite_original', '-CreateDate=' + date_time, '-DateTimeOriginal=' + date_time, '-FileCreateDate=' + date_time, '-FileModifyDate=' + date_time, image_path]
        logging.info(exiftool_cmd)
        subprocess.run(exiftool_cmd)

# Function to process a folder and its subfolders recursively
def process_folder(folder_path, ext):
    # Create list of JSON files in folder
    json_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() == '.json']

    # Process JSON files in parallel [DEFAULT MAX WORKERS = 8]    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(process_json_file, os.path.join(folder_path, json_file), ext) for json_file in json_files]
        concurrent.futures.wait(futures)

    # Recursively process subfolders
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    for subfolder in subfolders:
        process_folder(os.path.join(folder_path, subfolder), ext)

    # Recursively process subfolders
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    for subfolder in subfolders:
        process_folder(os.path.join(folder_path, subfolder), ext)

# Main function
if __name__ == '__main__':
    folder_path = sys.argv[1] # Path to folder to process
    ext = sys.argv[2] # Extension of image files to update metadata for

    process_folder(folder_path, ext)
