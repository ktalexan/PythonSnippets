# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Update .env Files in GitHub Directory ----
# Description: This code updates or creates .env files in subdirectories
#              based on a master .env file.
# Author: Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Fx: Update .env files ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_env_files(
    project_name: str = None,
    create_if_missing: bool = True
    ) -> None:
    """
    Updates or creates .env files in subdirectories based on a master .env file.
    Args:
        project_name (str): The name of a specific project directory to check. If None, all subdirectories are checked.
        create_if_missing (bool, optional): Whether to create a .env file if it doesn't exist. Defaults to True.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> update_env_files()
        >>> update_env_files(project_name="OCTraffic", create_if_missing=False)
    Note:
        This function assumes that the master .env file is located in the current working directory.
    """
    # Get the content of the current `.env` file in the current working directory
    current_env_path = os.path.join(os.getcwd(), ".env")
    with open(current_env_path, "r", encoding = "utf-8") as f:
        current_env_content = f.read()

    # Get the path one level up from the current project working directory
    project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

    # If the name of the project root directory is not "GitHub", exit the function
    if os.path.basename(project_root) != "GitHub":
        print(f"The project root directory '{project_root}' is not 'GitHub'. Exiting function.")
        return

    # Define an empty list for folders to check
    folders = []


    # Determine the folders to check
    if project_name is None:
        # Get a list of the folders in the project_root directory, excluding the current directory itself
        folders = [f for f in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, f)) and f != os.path.basename(os.getcwd())]
    # else if a specific project directory is provided, check if it's a directory
    else:
        remote_folder = os.path.join(project_root, project_name)
        if os.path.isdir(remote_folder):
            # Get a list with just that directory
            folders = [remote_folder]
        else:
            print(f"The specified project directory '{project_name}' does not exist in '{project_root}'. No folders to check.")
            folders = []

    # Loop through each folder and check for .env files (if there is any folder to check)
    if folders:
        for folder in folders:
            print(f"\nChecking folder: {folder}")
            # Check if there is an `.env` folder in the folder
            env_path = os.path.join(project_root, folder, ".env")

            # Check if the .env file exists
            if os.path.exists(env_path):
                print(f"- Found .env in {folder}: {env_path}")
                with open(env_path, "r", encoding = "utf-8") as f:
                    content = f.read()
                
                # Compare the content with the current `.env` file
                if content != current_env_content:
                    print(f"- The content of the `.env` file in {folder} is different from the current `.env` file.")

                    # Update the .env file in the folder to match the current .env file
                    print(f"- Updating `.env` file in {folder} to match the current `.env` file.")
                    with open(env_path, "w", encoding = "utf-8") as f:
                        f.write(current_env_content)
                        print(f"Updated .env file in {folder} to match the current .env file.")
                else:
                    print(f"The content of the `.env` file in {folder} is the same as the current `.env` file.")
            else:
                print(f"- No .env file found in {folder}.")
                # Checking the create_if_missing flag to create the .env file if it doesn't exist
                if create_if_missing:
                    print(f"- Creating .env file in {folder}.")
                    with open(env_path, "w", encoding = "utf-8") as f:
                        f.write(current_env_content)
                else:
                    print(f"- Skipping creation of .env file in {folder}.")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Main: Example Usage ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Example usage: Update .env files in the current directory and its subdirectories
    # This will create .env files in all subdirectories of the project that don't have one.
    update_env_files()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
