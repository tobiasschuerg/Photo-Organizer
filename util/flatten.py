import os
import shutil

def move_files_to_parent_dir(current_dir, parent_dir, max_files):
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)

        if os.path.isdir(item_path):
            num_files = count_files_in_directory(item_path)
            print(f"Checking '{item_path}' with {num_files} file(s)...")

            if num_files <= max_files:
                print(f"Flattening '{item_path}'...")
                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    if os.path.isfile(sub_item_path):
                        shutil.move(sub_item_path, parent_dir)
                        print(f"Moved file: {sub_item_path} to {parent_dir}")
                    elif os.path.isdir(sub_item_path):
                        move_files_to_parent_dir(sub_item_path, parent_dir, max_files)

                if not os.listdir(item_path):
                    os.rmdir(item_path)
                    print(f"Deleted empty directory: {item_path}")
            else:
                print(f"'{item_path}' has more than {max_files} files. Checking subdirectories...")
                move_files_to_parent_dir(item_path, parent_dir, max_files)

def count_files_in_directory(directory):
    return sum(os.path.isfile(os.path.join(directory, f)) for f in os.listdir(directory))

def flatten_directory(parent_dir, max_files):
    if not os.path.exists(parent_dir):
        print(f"The directory {parent_dir} does not exist.")
        return

    print(f"Starting to flatten the directory '{parent_dir}' with a maximum of {max_files} files per folder...")
    move_files_to_parent_dir(parent_dir, parent_dir, max_files)
    print("Flattening operation completed.")

# Prompting the user for the directory path and maximum number of files
print("Please enter the path to the directory you want to flatten:")
parent_directory = input("Directory Path: ")
print("Enter the maximum number of files a folder can have to be flattened:")
max_files = int(input("Maximum Number of Files: "))

flatten_directory(parent_directory, max_files)
