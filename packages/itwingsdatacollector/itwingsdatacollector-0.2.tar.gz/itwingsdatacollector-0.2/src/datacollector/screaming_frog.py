from datacollector.config import *
from datacollector.raw_data_to_csv import raw_data_to_csv
import os
import subprocess

def generate_export_tabs(tabs):
    return ','.join(tabs)


def screaming_frog(parameters):

    try:
        export_tabs = generate_export_tabs(parameters["tabs"])
        temp_directory = parameters["temp_folder"]
        os.makedirs(temp_directory, exist_ok=True)

        # Define the command to crawl the website using Screaming Frog SEO Spider and export issues data to a CSV file
        command = (
            f'screamingfrogseospider '
            f'--crawl {parameters["crawl_parameters"]["url"]} '
            # Use user-provided config file path
            f'--config "{parameters["config_file_path"]}" '
            # Use user-provided temp folder
            f'--output-folder {temp_directory} '
            f'--headless '
            f'--export-tabs "{export_tabs}" '  # Pass tabs dynamically
            f'--save-crawl '  # Corrected option
        )
        # Execute the command using subprocess
        subprocess.run(command, shell=True, check=True)
        print(f"CSV file downloaded successfully.")
    except Exception as e:
        print("Error:", e)

