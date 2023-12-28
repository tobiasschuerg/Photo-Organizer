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


def get_destination_directory(output_directory, date_taken):
    """
    Get the destination directory based on the date taken.
    """
    year, month, day = date_taken[:4], date_taken[5:7], date_taken[
                                                        8:10]  # Extract year, month, and day from the EXIF data or filename

    # Check if a directory starting with the correct date string already exists
    year_directory = os.path.join(output_directory, year)
    date_string = f"{year}-{month}-{day}"
    destination_directory = None
    if os.path.exists(year_directory):
        for dir_name in os.listdir(year_directory):
            if dir_name.startswith(date_string):
                destination_directory = os.path.join(year_directory, dir_name)
                break

    if not destination_directory:
        destination_directory = os.path.join(year_directory, date_string)
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

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".mp", ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv")):
            file_count += 1
            file_path = os.path.join(input_directory, filename)
            date_taken = get_date_taken(file_path)

            if date_taken:
                destination_directory = get_destination_directory(output_directory, date_taken)
                new_file_path = os.path.join(destination_directory, filename)

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

            print(f"Processed {processed_files_count} out of {file_count} files. {error_files_count} errors occurred.")

    print(f"Finished processing. {processed_files_count} files processed, {error_files_count} errors.")
