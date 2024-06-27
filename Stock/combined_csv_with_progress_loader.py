
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

def combine_csv_files_with_columns(directory_path, log_path):
    combined_df = pd.DataFrame()
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    log_entries = []
    for filename in tqdm(csv_files, desc="Combining files with columns"):
        try:
            stock_name = filename.split('.')[0]  # Assuming stock name is the file name without the extension
            df = pd.read_csv(os.path.join(directory_path, filename))
            df['Stock'] = stock_name
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            log_entries.append(f"Failed to process {filename}: {e}")
    combined_df.to_csv(os.path.join(directory_path, 'combined_with_columns.csv'), index=False)
    with open(log_path, 'a') as log_file:
        for entry in log_entries:
            log_file.write(f"{datetime.now()}: {entry}\n")

def combine_csv_files_with_rows(directory_path, log_path):
    combined_df = pd.DataFrame()
    log_entries = []
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    all_columns = set()
    for filename in csv_files:
        df = pd.read_csv(os.path.join(directory_path, filename))
        all_columns.update(df.columns.tolist())
    all_columns = list(all_columns)  # Ensuring 'Stock' is a part of the final DataFrame
    
    for filename in tqdm(csv_files, desc="Combining files with rows"):
        try:
            stock_name = filename.split('.')[0]
            df = pd.read_csv(os.path.join(directory_path, filename))
            df = df.reindex(columns=all_columns + ['Stock'], fill_value='NA')  # Ensure all dfs have the same columns
            df['Stock'] = stock_name  # Assigning stock name to each row
            separator_row = pd.DataFrame([['-----'] * len(all_columns) + [stock_name]], columns=all_columns + ['Stock'])
            combined_df = pd.concat([combined_df, separator_row, df], ignore_index=True)
        except Exception as e:
            log_entries.append(f"Failed to process {filename}: {e}")
    
    combined_df.to_csv(os.path.join(directory_path, 'combined_with_rows.csv'), index=False)
    with open(log_path, 'a') as log_file:
        for entry in log_entries:
            log_file.write(f"{datetime.now()}: {entry}\n")

script_directory = 'stocks'
log_file_path = os.path.join(script_directory, 'combine_log.txt')

combine_csv_files_with_columns(script_directory, log_file_path)
combine_csv_files_with_rows(script_directory, log_file_path)
