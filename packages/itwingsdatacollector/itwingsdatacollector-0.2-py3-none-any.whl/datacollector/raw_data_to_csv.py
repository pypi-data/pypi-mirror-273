import os
import csv

def raw_data_to_csv(source, data, file_suffix='', append=False):
    """
    Saves data to a CSV file under 'data/raw_data'. This function can handle both a single dictionary and a list of dictionaries.
    If a row with the same 'url' exists, it will be overwritten.

    :param source: The source name, which will be used as the base file name.
    :param data: A single dictionary or a list of dictionaries. Each dictionary represents a row.
    :param file_suffix: An optional suffix for the file name.
    :param append: If False, the file will be overwritten. If True, check for duplicate URLs and append or overwrite as necessary.
    """
    # Generate file path
    directory = os.path.join("temp")
    os.makedirs(directory, exist_ok=True)
    
    if file_suffix:
        file_name = f"{source}_{file_suffix}.csv"
    else:
        file_name = f"{source}.csv"
    file_path = os.path.join(directory, file_name)
    
    # Prepare data
    if not isinstance(data, list):
        data = [data]  # Convert to list for consistency
    
    # Read existing data if append mode is on
    existing_data = []
    if append and os.path.exists(file_path):
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = [row for row in reader]

        # Check and replace/update data based on 'url'
        urls_in_data = {item['url'] for item in data}
        existing_data = [item for item in existing_data if item['url'] not in urls_in_data]
    
    # Combine old data with new data, overwriting duplicates
    combined_data = existing_data + data
    
    # Determine fieldnames
    fieldnames = combined_data[0].keys() if combined_data else []

    # Write combined data to file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)


