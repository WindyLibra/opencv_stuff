import os
import re
from natsort import natsorted


def rename_files_with_increment(directory):
    # List all files in the directory and sort them in reverse order
    files = natsorted(os.listdir(directory), reverse=True)

    # Regular expression to find the integer in the filename
    pattern = re.compile(r'(\d+)(\.\w+)$')

    for filename in files:
        # Try to find an integer in the filename
        match = pattern.search(filename)
        if match:
            # Extract the integer and extension
            num = int(match.group(1))
            extension = match.group(2)

            # Construct the new filename by incrementing the integer
            new_name = pattern.sub(lambda x: str(num + 1) + x.group(2), filename, count=1)

            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))


if __name__ == "__main__":
    # Specify the directory containing the files
    directory_path = r"C:\Users\aram_\PycharmProjects\PrepareDataForTracking\a1\a1_cars"

    # Call the function to rename files with increment
    rename_files_with_increment(directory_path)