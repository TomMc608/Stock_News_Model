def cleanup_links(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.startswith('https://edition.cnn.com/'):
            modified_lines.append(line)

    with open(file_path, 'w',encoding='utf-8') as file:
        file.writelines(modified_lines)


cleanup_links('all_links.txt')
