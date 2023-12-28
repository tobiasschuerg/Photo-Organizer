# date_extractions.py
import os
import re
import time
from datetime import datetime

import pillow_heif
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

pillow_heif.register_heif_opener()  # Register HEIF/HEIC opener with Pillow


def get_date_from_image_exif(file_path):
    """
    Extract the date from the EXIF data of an image (including HEIC).

    Args:
        file_path: The path of the image file.

    Returns:
        The date the image was taken in the format YYYY-MM-DD if it is found in the EXIF data, otherwise None.
    """
    try:
        with Image.open(file_path) as img:
            if hasattr(img, '_getexif'):
                exif_data = img._getexif()
                if exif_data is not None and 36867 in exif_data:
                    return exif_data[36867].replace(':', '-').split()[0]  # Extract only the date part
    except Exception as e:
        print(f"An error occurred while trying to get the date from the EXIF data for file {file_path}: {e}")
    return None


def get_date_from_movie_metadata(file_path):
    """
    Extract the date from the metadata of a movie file.

    Args:
        file_path: The path of the movie file.

    Returns:
        The date the movie was created in the format YYYY-MM-DD if it is found in the metadata, otherwise None.
    """
    try:
        parser = createParser(file_path)
        if parser:
            with parser:
                metadata = extractMetadata(parser)
                if metadata:
                    date_taken = metadata.get('creation_date')
                    if date_taken:
                        return str(date_taken.date())
    except Exception as e:
        print(f"An error occurred while trying to get the date from the metadata for file {file_path}: {e}")
    return None


def get_date_from_filename(file_path):
    """
    Extract the date from the filename.

    Args:
        file_path: The path of the file.

    Returns:
        The date in the format YYYY-MM-DD if it is found in the filename, otherwise None.
    """
    try:
        # Try to extract the date from the filename (format: PXL_YYYYMMDD_HHMMSS...)
        match = re.search(r'PXL_(\d{8})', os.path.basename(file_path))
        if match:
            date = match.group(1)
            return date[:4] + "-" + date[4:6] + "-" + date[6:8]
        else:
            # Try to extract the date from the filename (format: YYYY-MM-DD)
            match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', os.path.basename(file_path))
            if match:
                return match.group(1)
    except Exception as e:
        print(f"An error occurred while trying to get the date from the filename for file {file_path}: {e}")
    return None


def parse_date(date_str):
    """
    Parse a date string and return a datetime object if valid and after 1970, otherwise None.

    Args:
        date_str: The date string in the format YYYY-MM-DD.

    Returns:
        A datetime object or None.
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj.year > 1970:
            return date_obj
    except ValueError:
        pass
    return None


def get_date_taken(file_path):
    """
    Get the date the file was taken as a datetime object. If the metadata is not available,
    try to extract the date from the filename, and then the file creation date.
    If the date is on or before 1970, it is ignored.

    Args:
        file_path: The path of the file.

    Returns:
        A datetime object representing the date the file was taken, if it can be found, otherwise None.
    """
    filename, file_extension = os.path.splitext(file_path)

    # Check file extension and extract date string
    if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.heic']:
        date_str = get_date_from_image_exif(file_path)
    elif file_extension.lower() in ['.mp', '.mp4', '.mov', '.avi', '.mkv']:
        date_str = get_date_from_movie_metadata(file_path)
    else:
        print(f"Unsupported file extension {file_extension} for file {file_path}")
        return None

    if not date_str:
        date_str = (get_date_from_filename(file_path)
                    or time.strftime('%Y-%m-%d', time.gmtime(os.path.getctime(file_path))))

    date_obj = parse_date(date_str) if date_str else None

    if not date_obj:
        return None
    else:
        return date_obj
