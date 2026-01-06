import os

def get_data_dir():
    try:
        # Assumes the script is either in the 'main_code' directory or in the "scripts" one
        script_dir = os.path.dirname(__file__)
    except NameError:
        # Fallback if __file__ is not defined (common in notebooks/interactive)
        # Assumes the current working directory is 'main_code' or 'OPT_scriptshw'
        script_dir = os.getcwd()
        # If your notebook/script is actually in OPT_hw, adjust the path construction:
        # data_dir = os.path.abspath(os.path.join(script_dir, 'data', 'raw', 'archive'))
    # Construct the path relative to the parent directory of script_dir
    # Goes up one level from script_dir (main_code) to OPT_hw, then into data/raw/archive
    data_dir_relative = os.path.join(script_dir, '..', 'data', 'raw', 'archive')

    # Get the absolute, normalized path (resolves '..')
    data_dir = os.path.abspath(data_dir_relative)

    print(f"Data directory path: {data_dir}")
    return data_dir
