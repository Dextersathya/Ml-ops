import os
import pandas as pd

def clean_data():
    # Ensure the file exists
    file_path = '/tmp/xrate.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Load raw data into DataFrame
    try:
        data = pd.read_csv(file_path, header=None)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Cleanse Data
    cleaned_data = data.fillna('')  # Fill missing values with empty strings

    # Get the current date components
    now = pd.Timestamp.now()
    year = now.year
    month = now.month
    day = now.day

    # Create the directory path if it doesn't exist
    data_dir = f'/opt/airflow/data/xrate_cleansed/{year}/{month}/{day}'
    os.makedirs(data_dir, exist_ok=True)

    # Save the cleaned data to a new file
    output_path = f'{data_dir}/xrate.csv'
    cleaned_data.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
