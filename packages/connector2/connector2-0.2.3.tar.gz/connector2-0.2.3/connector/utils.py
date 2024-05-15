#!/usr/bin/env python3

"""
This module contains utility functions for file and directory operations.
"""

import os

def create_directory_for_path(target_path):
    """
    Create a directory for the given path.

    This function checks if the target path includes a file extension or a 
    trailing slash to determine if it's a file or a directory. If the target 
    path is a file, it obtains the directory part only. If the target path is 
    a directory, it uses the path directly. If it's not clear (no file 
    extension and no trailing slash), it assumes it's a directory. Then it 
    creates the directory if it does not exist.

    Parameters
    ----------
    target_path : str
        The target path for which to create a directory.

    Returns
    -------
    None

    Examples
    --------
    >>> create_directory_for_path("data/analysis/output_files/")
    Directory created or already exists at: data/analysis/output_files

    >>> create_directory_for_path("data/analysis/output_files/data.csv")
    Directory created or already exists at: data/analysis/output_files

    >>> create_directory_for_path("data/analysis/output_files_no_extension")
    Directory created or already exists at: data/analysis/output_files_no_extension
    """
    # Determine if the path has a file extension
    if os.path.splitext(target_path)[1]:  # Path includes a file extension
        # Assume this is a file, so obtain the directory part only
        directory_path = os.path.dirname(target_path)
    elif target_path.endswith('/'):
        # Directly assumes it's a directory with a proper trailing slash
        directory_path = target_path.rstrip('/')
    else:
        # It's not clear; no file extension and no trailing slash; assume directory
        directory_path = target_path
    if not os.path.isdir(directory_path):
        # Create the directory if not exist
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory created at: {directory_path}")
