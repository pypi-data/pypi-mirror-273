import os
import yaml
from sstc_utils.utils import check_nested_dict


def get_yaml_files_with_keys(dirpath:dict, keys_list:list):
    """
    This function navigates through a directory and its subdirectories to find .yaml files.
    It then checks if these files contain all the specified keys from a provided list.
    
    Args:
        dirpath (str): The path of the directory to search.
        keys_list (list): The list of keys to check for in the .yaml files.
    
    Returns:
        dict: A dictionary with filenames as keys and boolean values indicating whether the file contains all the specified keys.
    
    """
    # Dictionary to store results
    file_dict = {}

    # Check if the provided directory exists
    if not os.path.exists(dirpath):
        raise ValueError(f"The provided directory {dirpath} does not exist.")
    
    # Walk through the directory
    for root, _, files in os.walk(dirpath):
        for file in files:
            # Check if the file is a .yaml file
            if file.endswith(".yaml"):
                # Construct the full file path
                file_path = os.path.join(root, file)
                
                # Open and load the yaml file
                try:
                    with open(file_path, 'r') as stream:
                        data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(f"Error loading YAML file {file_path}: {exc}")
                    continue
                
                # Check if all keys in the keys_list are in the data
                if check_nested_dict(data, keys_list):
                    file_dict[file] = True
                else:
                    file_dict[file] = False
                    
    return file_dict




def yaml_to_markdown(yaml_file:str, output_dir:str):
    """
    Converts a YAML file to a Markdown formatted file.

    This function reads the contents of a specified YAML file, 
    formats it as a code block in Markdown, and then saves this 
    formatted content to a new Markdown file in a specified output directory.

    Args:
        yaml_file (str): The path to the YAML file to be converted.
        output_dir (str): The directory where the Markdown file will be saved.

    Notes:
        The Markdown file is named after the YAML file (with the .md extension)
        and is saved in the specified output directory. The directory is created
        if it does not exist.

    Exceptions:
        FileNotFoundError: Raised if the YAML file is not found.
        yaml.YAMLError: Raised if there is an error in parsing the YAML file.
        IOError: Raised if there is an error in writing the Markdown file.

    Example:

        yaml_to_markdown("../src/sstc_config/yamls/uavs_image_tags.yaml", "./markdown_output")
    ---
    """

    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Extract filename without extension for the markdown file
        filename_without_ext = os.path.splitext(os.path.basename(yaml_file))[0]

        # Define the path for the output markdown file
        output_file = os.path.join(output_dir, f"{filename_without_ext}.md")

        # Read YAML content
        with open(yaml_file, 'r') as file:
            yaml_content = yaml.safe_load(file)

        # Convert YAML content to Markdown format (as a code block)
        markdown_content = "```yaml\n" + yaml.dump(yaml_content, default_flow_style=False, sort_keys=False) + "```"

        # Write the formatted content to the markdown file
        with open(output_file, 'w') as file:
            file.write(markdown_content)

        print(f"Markdown file created: {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {yaml_file} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")