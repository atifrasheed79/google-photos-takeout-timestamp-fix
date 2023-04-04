import os
import subprocess
from datetime import datetime
import json
import sys
import logging

# set the logging leve to debug if required
logging.basicConfig(level=logging.INFO)

# Path to the ExifTool executable file
exiftool_path = ".\exiftool"

# Path to the folder containing the images and metadata files
folder_path = sys.argv[1]
file_ext = sys.argv[2]

logging.debug(folder_path)
logging.debug(file_ext)

# Loop through all files and subdirectories in the folder
for root, dirs, files in os.walk(folder_path):
    # Loop through all files in the current directory
    for file_name in files:
        # Check if the file is a JSON file
        logging.debug(file_name)
        if file_name.endswith(".json"):
            # Get the path to the JSON file
            json_path = os.path.join(root, file_name)
            # Get the path to the corresponding image file
            image_path = os.path.splitext(json_path)[0]
            logging.debug(image_path)
            # Check if the image file exists and has the correct extension
            if os.path.isfile(image_path) and image_path.endswith(file_ext):
                logging.debug("Loading metadata from ", json_path)
                # Read the metadata from the JSON file
                with open(json_path, 'r') as f:
                    metadata = json.load(f)
                # Extract the create and modify dates from the metadata
                #create_date = metadata.get("create_date")
                modify_date_timestamp = metadata["photoTakenTime"]["timestamp"]
                date_time = datetime.fromtimestamp(int(modify_date_timestamp)).strftime("%Y:%m:%d %H:%M:%S")
                # Build the ExifTool command
                logging.debug("Using exif to update timestamp ", date_time,"of ", image_path)
                exiftool_cmd = [exiftool_path, "-overwrite_original",
                                "-FileCreateDate=" + date_time, "-FileModifyDate=" + date_time, image_path]
                logging.info(exiftool_cmd)
                # Execute the ExifTool command
                result = subprocess.run(exiftool_cmd, capture_output=True)
                # Print the output of the ExifTool command
                logging.info(result.stdout.decode("utf-8"))