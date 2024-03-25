def check_duplicates(file_path):
    # Read the file and extract the links
    with open(file_path, 'r', encoding='utf-8') as file:
        links = file.readlines()
    
    # Convert the list to a set to remove duplicates
    unique_links = set(links)
    
    # Check if the length of the original list and the set are the same
    if len(links) == len(unique_links):
        print("No duplicate links found.")
    else:
        num_duplicates = len(links) - len(unique_links)
        print(f"Found {num_duplicates} duplicate links.")


file_path = "all_links.txt"
# Call the function to check for duplicates
check_duplicates(file_path)
