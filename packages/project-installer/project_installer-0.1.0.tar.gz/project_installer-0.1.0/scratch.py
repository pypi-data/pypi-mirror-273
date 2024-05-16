import re

def matches_rule(file_path, rule):
    # Function to check if a file path matches a rule
    return re.match(rule.replace('.', r'\.').replace('*', '.*'), file_path)

def apply_ignore_rules(file_list, ignore_rules):
    filtered_list = []
    for file_path in file_list:
        ignore_file = False
        for rule in ignore_rules:
            if matches_rule(file_path, rule):
                ignore_file = True
                break
        if not ignore_file:
            filtered_list.append(file_path)
    return filtered_list

# Example list of files and ignore rules
file_list = [
    "folder/file1.txt",
    "folder/subfolder/file2.txt",
    "important_file.txt",
    "image.png"
]

ignore_rules = [
    "*.txt",        # Ignore all txt files
    "folder/",      # Ignore entire folder
    "!important_file.txt"  # But don't ignore this specific file
]

# Apply ignore rules
filtered_files = apply_ignore_rules(file_list, ignore_rules)
print("Filtered files:", filtered_files)
