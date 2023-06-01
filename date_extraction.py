import re

from PIL import Image


def get_date_taken(path):
    """
    Returns the date the image at the specified path was taken. If the date cannot be extracted from the EXIF data,
    attempts to extract the date from the filename. If the date cannot be extracted from the filename either, returns None.
    """
    try:
        return Image.open(path)._getexif()[36867]
    except (KeyError, AttributeError, TypeError, IOError):
        # Try to extract date from filename
        date_taken = re.search(r'\d{4}-\d{2}-\d{2}', path)
        if date_taken:
            return date_taken.group(0).replace('-', ':')
        else:
            return None
