import os
import shutil
import requests
import csv


def check_api_balance(semrush_key):
    url = "http://www.semrush.com/users/countapiunits.html"
    params = {
        "key": semrush_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return int(response.text.strip())
    else:
        print("Error:", response.status_code)
        return None


def create_folder_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_folder_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def download_csv_files(requests_attributes, directory):
    invalid_params = []

    for request in requests_attributes:
        response = requests.get(request["url"], params=request["params"])
        if response.status_code == 200:
            file_name = f"{request['params']['type']}.csv"
            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"CSV file '{file_name}' downloaded successfully.")
            except Exception as e:
                print(f"Error downloading CSV file '{file_name}': {e}")
                invalid_params.append(request)
        else:
            print(f"Failed to download CSV file for request: {request}")
            invalid_params.append(request)

    if invalid_params:
        invalid_params_file = os.path.join(
            directory, "invalid_params.csv")
        with open(invalid_params_file, "w", newline="") as csvfile:
            fieldnames = ["url", "params"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for request in invalid_params:
                writer.writerow({"url": request.get("url", ""),
                                "params": request.get("params", "")})


def semrush(requests_attributes):
    invalid_params = []

    # Define the directory
    temp_directory = "temp/semrush"

    # Remove existing semrush folder and create new
    remove_folder_if_exists(temp_directory)
    create_folder_if_not_exists(temp_directory)

    if not isinstance(requests_attributes, list) or len(requests_attributes) == 0:
        print("Error: 'requests_attributes' should be a non-empty list.")
        return

    for request in requests_attributes:
        if not isinstance(request, dict) or "params" not in request or not isinstance(request["params"], dict):
            invalid_params.append(
                {"error": "Each request should be a dictionary containing 'params'.", "request": request})
            print("Error: Each request should be a dictionary containing 'params'.")
            continue
        if "key" not in request["params"]:
            invalid_params.append(
                {"error": "'key' parameter is missing in request.", "request": request})
            print("Error: 'key' parameter is missing in request.")
            continue
        if not request["params"]["key"]:
            invalid_params.append(
                {"error": "'key' parameter cannot be empty.", "request": request})
            print("Error: 'key' parameter cannot be empty.")
            continue

    if invalid_params:
        invalid_params_file = os.path.join(
            temp_directory, "invalid_params.csv")
        with open(invalid_params_file, "w", newline="") as csvfile:
            fieldnames = ["error", "url", "params"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in invalid_params:
                writer.writerow({"error": item["error"], "url": item["request"].get(
                    "url", ""), "params": item["request"].get("params", "")})
        return

    balance = check_api_balance(requests_attributes[0]['params']["key"])
    if balance is not None:
        print("Semrush API unit balance:", balance)

    # Download CSV files
    download_csv_files(requests_attributes, temp_directory)
