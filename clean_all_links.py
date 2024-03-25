def clean_links(input_file, output_file):
    """
    Reads links from a text file, strips extraneous text, and saves cleaned links.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to the output text file.
    """

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            start_index = line.find('https://')  # Find the start of the URL
            if start_index != -1:  # If a URL is found
                end_index = line.find('"}')  # Find the closing "}"
                cleaned_link = line[start_index:end_index] + '\n'  # Extract and add newline
                outfile.write(cleaned_link)


input_file = 'all_links.txt'  
output_file = 'all_links_cleaned.txt'
clean_links(input_file, output_file)
