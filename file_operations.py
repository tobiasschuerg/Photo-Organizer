# file_operation.py
import os
import shutil

from date_extraction import get_date_taken


def copy_file(source_path, destination_path):
    """
    Copies a file from source_path to destination_path.
    """
    shutil.copy2(source_path, destination_path)


def move_file(source_path, destination_path):
    """
    Moves a file from source_path to destination_path.
    """
    shutil.move(source_path, destination_path)


import os

def get_destination_directory(output_directory, date_taken):
    """
    Get the destination directory based on the date taken.

    Args:
        output_directory: The base output directory.
        date_taken: A datetime object representing the date the file was taken.

    Returns:
        The path of the destination directory.
    """

    if date_taken is None:
        print("Date taken is None, cannot determine destination directory.")
        return None

    # Format the date into year, month, and day with leading zeros for month and day
    year = date_taken.strftime('%Y')
    month = date_taken.strftime('%m')
    day = date_taken.strftime('%d')
    sub_dir_name = f"{year}-{month}-{day}"

    year_directory = os.path.join(output_directory, year)
    destination_directory = os.path.join(year_directory, sub_dir_name)

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory, exist_ok=True)  # Create new directory if it doesn't exist

    return destination_directory



def organize_files(input_directory, output_directory, operation):
    """
    Organizes files in the input directory into subdirectories in the output directory based on the date the file was taken.
    """
    if not os.path.isdir(input_directory):
        print(f"Input directory {input_directory} does not exist.")
        return

    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except OSError:
            print(f"Creation of the output directory {output_directory} failed.")
            return
    elif not os.path.isdir(output_directory):
        print(f"Output directory {output_directory} already exists and is not a directory.")
        return

    file_count = 0
    processed_files_count = 0
    error_files_count = 0

    for item in os.listdir(input_directory):
        file_path = os.path.join(input_directory, item)
        if os.path.isfile(file_path):  # Check if it's a file
            file_count += 1
            date_taken = get_date_taken(file_path)

            if date_taken:
                destination_directory = get_destination_directory(output_directory, date_taken)
                new_file_path = os.path.join(destination_directory, item)

                try:
                    if operation.lower() == 'move':
                        move_file(file_path, new_file_path)
                    else:
                        copy_file(file_path, new_file_path)
                    processed_files_count += 1
                except Exception as e:
                    print(f"An error occurred while processing file {file_path}: {e}")
                    error_files_count += 1
            else:
                print(f"Could not determine date taken for file {file_path}. Skipping.")
                error_files_count += 1
        else:
            print(f"Skipping directory: {file_path}")

    print(f"Finished processing. {processed_files_count} files processed, {error_files_count} errors.")
