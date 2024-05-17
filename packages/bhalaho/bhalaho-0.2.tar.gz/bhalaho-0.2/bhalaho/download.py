import os
import shutil ,pkgutil
from pkg_resources import resource_filename

def download_files(target_dir):
    # Get the data directory content as bytes
    data_content = pkgutil.get_data(__name__, 'data')

    # Make sure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Iterate over files in the data directory and copy them to the target directory
    for filename in os.listdir(data_content):
        source_file = os.path.join(data_content, filename)
        target_file = os.path.join(target_dir, filename)
        with open(target_file, 'wb') as f:
            f.write(source_file)

if __name__ == "__main__":
    # Example usage: download files to the current directory
    download_files(".")
