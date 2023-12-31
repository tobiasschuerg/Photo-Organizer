import os
import shutil

def move_files_to_parent_dir(current_dir, parent_dir):
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            # Recursively move files from subdirectories
            move_files_to_parent_dir(item_path, parent_dir)
            # After moving files, check if the directory is empty and delete if it is
            if not os.listdir(item_path):
                os.rmdir(item_path)
        elif os.path.isfile(item_path):
            # Move file to parent directory
            shutil.move(item_path, parent_dir)

def flatten_directory(parent_dir):
    if not os.path.exists(parent_dir):
        print(f"The directory {parent_dir} does not exist.")
        return

    move_files_to_parent_dir(parent_dir, parent_dir)
    print("Operation completed. All files moved to parent directory and empty directories removed.")

# Prompting the user for the directory path
print("Please enter the path to the directory you want to flatten:")
print("All files from subdirectories will be moved to this parent directory, and empty subdirectories will be deleted.")
parent_directory = input("Directory Path: ")
flatten_directory(parent_directory)
