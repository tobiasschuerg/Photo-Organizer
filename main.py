from file_operations import organize_files

input_directory = input("Enter the input directory: ")
output_directory = input("Enter the output directory: ")
operation = input("Enter 'copy' to copy files or 'move' to move files (default is 'copy'): ")
operation = operation if operation else 'copy'

organize_files(input_directory, output_directory, operation)
