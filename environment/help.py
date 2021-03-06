"""
This module contains helper functions that don't fit in other ones.
"""

import os


def format_size(num, suffix='B'):
    """
    Returns a well formatted string representation
    of the given number of bytes.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def locate_files_rec(path, suffix):
    """
    Returns a list of all files with the given suffix
    in the given directory and its subdirectories.
    """
    files = []
    abs_path = os.path.abspath(path)

    # r=root, f=files
    for r, _, f in os.walk(abs_path):
        files.extend([
            os.path.join(r, file) for file in f if file.endswith(f'.{suffix}')
        ])

    return files
