import os
import shutil

def copy_files(src_dir, dst_dir, recursive=False):
    """
    Copies all files from the source directory to the destination directory.
    
    Args:
    src_dir (str): The source directory path.
    dst_dir (str): The destination directory path.
    recursive (bool): If True, copy files from subdirectories recursively.
    """
    # Ensure the destination directory exists
    os.makedirs(dst_dir, exist_ok=True)
    
    if recursive:
        # Walk through all directories and files in the source directory
        for root, dirs, files in os.walk(src_dir):
            # Calculate the relative path to the source directory
            rel_path = os.path.relpath(root, src_dir)
            # Create the corresponding directory in the destination
            dest_path = os.path.join(dst_dir, rel_path)
            os.makedirs(dest_path, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_path, file)
                shutil.copy2(src_file, dst_file)  # copy2 preserves metadata
            print(f"Copied files from {root} to {dest_path}")
    else:
        # Copy only the files in the given directory, not subdirectories
        for item in os.listdir(src_dir):
            src_file = os.path.join(src_dir, item)
            if os.path.isfile(src_file):
                dst_file = os.path.join(dst_dir, item)
                shutil.copy2(src_file, dst_file)  # copy2 preserves metadata
        print(f"Copied files from {src_dir} to {dst_dir}")

def combine_files(file_list):
    """
    Combine multiple files into a single string.
    
    Args:
    file_list (list): A list of file paths in the order that they should be combined.

    Returns:
    str: The combined content of all files as a single string.
    """
    combined_content = ""
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_content += file.read() + "\n"  # Add a newline to separate files
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except IOError as e:
            print(f"Error: Unable to read file - {file_path}. Reason: {e}")
    return combined_content


def transform_files(input_dir, output_dir, recursive, transform_function):
    def process_directory(directory, base_output_dir):
        try:
            entries = os.listdir(directory)

            for entry in entries:
                absolute_entry_path = os.path.join(directory, entry)
                relative_entry_path = os.path.relpath(absolute_entry_path, input_dir)
                output_entry_path = os.path.join(base_output_dir, relative_entry_path)

                if os.path.isdir(absolute_entry_path) and recursive:
                    os.makedirs(output_entry_path, exist_ok=True)
                    process_directory(absolute_entry_path, output_entry_path)
                elif os.path.isfile(absolute_entry_path):
                    with open(absolute_entry_path, 'r', encoding='utf8') as file:
                        content = file.read()
                    transformed_content = transform_function(content, relative_entry_path)
                    with open(output_entry_path, 'w', encoding='utf8') as file:
                        file.write(transformed_content)
        except Exception as error:
            print("Error processing directory:", error)
            raise  # Re-raise to handle it in the calling context

    try:
        # Check if input and output directories are the same
        if input_dir == output_dir:
            raise ValueError("Input directory and output directory should not be the same.")

        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
        process_directory(input_dir, output_dir)
    except Exception as error:
        print("Error in transform_files:", error)
        raise  # Re-raise to handle it in the calling context
