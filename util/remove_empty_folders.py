import os

def remove_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            folder_path = os.path.join(root, name)
            if not os.listdir(folder_path):  # Check if the folder is empty
                os.rmdir(folder_path)        # Delete the empty folder
                print(f"Deleted empty folder: {folder_path}")

def main():
    # Prompting the user for the directory path
    print("Please enter the path to the directory from which you want to remove empty folders:")
    directory = input("Directory Path: ")

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    remove_empty_folders(directory)
    print("Operation completed. All empty directories have been removed.")

if __name__ == "__main__":
    main()
