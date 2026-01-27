# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Update .gitignore Files in GitHub Directory ----
# Description: This code updates or creates .gitignore files in subdirectories
#              based on a master .gitignore file.
# Author: Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Fx: Update .gitignore files ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_gitignore_files(
    project_name: str = None,
    create_if_missing: bool = True
    ) -> None:
    """
    Updates or creates .gitignore files in subdirectories based on a master .gitignore file.
    Args:
        project_name (str): The name of a specific project directory to check. If None, all subdirectories are checked.
        create_if_missing (bool, optional): Whether to create a .gitignore file if it doesn't exist. Defaults to True.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> update_env_files()
        >>> update_env_files(project_name="OCTraffic", create_if_missing=False)
    Note:
        This function assumes that the master .gitignore file is located in the current working directory.
    """
    # Get the content of the current `.gitignore` file in the current working directory
    current_env_path = os.path.join(os.getcwd(), ".gitignore")
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

    # Loop through each folder and check for .gitignore files (if there is any folder to check)
    if folders:
        for folder in folders:
            print(f"\nChecking folder: {folder}")
            # Check if there is an `.gitignore` folder in the folder
            env_path = os.path.join(project_root, folder, ".gitignore")

            # Check if the .gitignore file exists
            if os.path.exists(env_path):
                print(f"- Found .gitignore in {folder}: {env_path}")
                with open(env_path, "r", encoding = "utf-8") as f:
                    content = f.read()
                
                # Compare the content with the current `.gitignore` file
                if content != current_env_content:
                    print(f"- The content of the `.gitignore` file in {folder} is different from the current `.gitignore` file.")

                    # Update the .gitignore file in the folder to match the current .gitignore file
                    print(f"- Updating `.gitignore` file in {folder} to match the current `.gitignore` file.")
                    with open(env_path, "w", encoding = "utf-8") as f:
                        f.write(current_env_content)
                        print(f"Updated .gitignore file in {folder} to match the current .gitignore file.")
                else:
                    print(f"The content of the `.gitignore` file in {folder} is the same as the current `.gitignore` file.")
            else:
                print(f"- No .gitignore file found in {folder}.")
                # Checking the create_if_missing flag to create the .gitignore file if it doesn't exist
                if create_if_missing:
                    print(f"- Creating .gitignore file in {folder}.")
                    with open(env_path, "w", encoding = "utf-8") as f:
                        f.write(current_env_content)
                else:
                    print(f"- Skipping creation of .gitignore file in {folder}.")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Main: Example Usage ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Example usage: Update .gitignore files in the current directory and its subdirectories
    # This will create .gitignore files in all subdirectories of the project that don't have one.
    update_env_files()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
