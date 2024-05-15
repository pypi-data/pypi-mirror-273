# SITES Spectral Thematic Center (SSTC)
# maintainer: @jobelund


import os


def get_files_dictionary(dirpath: str, file_extensions: list = ['.TIF', '.JPG', '.tiff', '.jpg'], keep_extension_in_key:bool = True) -> dict:
    """
    Recursively search for files with the specified `file_extension` in the given `dirpath` and return a dictionary
    with the filename (without extension) as the key and the full normalized path of the file as the value.

    Args:
        dirpath (str): The directory path to start the search.
        file_extensions (str): The file extension to filter the files.
        keep_extension_in_key (bool, optional): If True, the file extension will be kept in the key of the dictionary.

    Returns:
        dict: A dictionary where the keys are the filenames (without extension) and the values are the full normalized paths of the files.
    """
    if dirpath is None:
        raise ValueError("The directory path cannot be None.")
    
    if not os.path.isdir(dirpath):
        raise ValueError(f"The specified directory path '{dirpath}' does not exist or is not a directory.")

    files_dictionary = {}
    
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            # Splitting the file path to get the extension
            file_name, file_extension = os.path.splitext(file)
            if file_extension in file_extensions:
                full_path = os.path.join(root, file)
                if keep_extension_in_key:
                    files_dictionary[file] = os.path.normpath(full_path)
                else:
                    filename_without_extension = os.path.splitext(file)[0]
                    files_dictionary[filename_without_extension] = os.path.normpath(full_path)

    return files_dictionary

