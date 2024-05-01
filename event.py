import pandas as pd

def print_entities_column(csv_file_path):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path)
    
    # Check if the 'entities' column exists in the DataFrame
    if 'theme' in data.columns:
        # Print the 'entities' column
        print(data['theme'])
    else:
        # Inform the user if the 'entities' column is not found
        print("The 'entities' column does not exist in the CSV file.")

# Example usage: replace 'yourfile.csv' with the path to your CSV file
print_entities_column('thematic_analysis_results.csv')
