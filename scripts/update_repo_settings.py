# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Update Settings Files in GitHub Directory ----
# Description: This code updates or creates master settings files in subdirectories
#              based on a master settings files.
# Author: Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import shutil
import filecmp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Fx: Update .gitignore files ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_repo_settings(
    project_name: str = None,
    create_if_missing: bool = True
    ) -> None:
    """
    Updates or creates settings files in subdirectories based on master settings files.
    Args:
        project_name (str): The name of a specific project directory to check. If None, all subdirectories are checked.
    Returns:
        None
    Raises:
        None
    """

    settings_list = [".env", ".gitignore", ".lintr", "pylintrc", "pyrightconfig.json", ".markdownlint.json"]  # List of settings files to update


    def _update_single_settings_file(file_name: str) -> None:
        """
        Updates a single settings file.
        Args:
            file_name (str): The name of the settings file to update.
        Returns:
            None
        Raises:
            None
        """

        # Master settings file path in current working dir
        master_path = os.path.join(os.getcwd(), file_name)

        # Ensure master settings file exists
        if not os.path.exists(master_path):
            print(f"Master settings file not found: {master_path}. Skipping {file_name}.")
            return

        # Get the path one level up from the current project working directory
        project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

        # Ensure we're under the expected project root
        if os.path.basename(project_root) != "GitHub":
            print(f"The project root directory '{project_root}' is not 'GitHub'. Exiting function.")
            return

        # Build list of folders to update (full paths)
        if project_name is None:
            folders = [os.path.join(project_root, f) for f in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, f)) and f != os.path.basename(os.getcwd())]
        else:
            remote_folder = os.path.join(project_root, project_name)
            if os.path.isdir(remote_folder):
                folders = [remote_folder]
            else:
                print(f"The specified project directory '{project_name}' does not exist in '{project_root}'. No folders to check.")
                folders = []

        # Loop through each folder and copy/replace the settings file as needed
        for folder in folders:
            print(f"\nChecking folder: {folder}")
            dest_path = os.path.join(folder, file_name)

            if os.path.exists(dest_path):
                # Compare files; if different, replace destination with master file
                try:
                    same = filecmp.cmp(master_path, dest_path, shallow = False)
                except OSError:
                    same = False

                if not same:
                    print(f"- Replacing {dest_path} with master {master_path}.")
                    shutil.copy2(master_path, dest_path)
                else:
                    print(f"- {file_name} in {folder} is identical to master. Skipping.")
            else:
                if create_if_missing:
                    print(f"- Creating {dest_path} from master {master_path}.")
                    shutil.copy2(master_path, dest_path)
                else:
                    print(f"- {dest_path} does not exist and creation is disabled. Skipping.")


    for file in settings_list:
        print(f"\nUpdating settings file: {file}")
        _update_single_settings_file(file)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Main: Example Usage ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Example usage: Update settings files in the current directory and its subdirectories
    # This will create settings files in all subdirectories of the project that don't have one.
    update_repo_settings()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
