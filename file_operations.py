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

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv")):
            file_path = os.path.join(input_directory, filename)
            date_taken = get_date_taken(file_path)

            if date_taken:
                year, month = date_taken[:4], date_taken[5:7]  # Extract year and month from the EXIF data or filename

                new_directory = os.path.join(output_directory, year, month)
                os.makedirs(new_directory, exist_ok=True)  # Create new directory if it doesn't exist

                new_file_path = os.path.join(new_directory, filename)

                if operation.lower() == 'move':
                    move_file(file_path, new_file_path)
                else:
                    copy_file(file_path, new_file_path)
