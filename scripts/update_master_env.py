"""
This script provides a function to update or create .env files in subdirectories
based on a master .env file.
"""

import os


def update_env_files(directory_path, create_if_missing=False, master_env_path=".env"):
    """
    Updates or creates .env files in subdirectories based on a master .env file.

    Args:
        directory_path (str): The path to the directory to scan for .env files.
        create_if_missing (bool, optional): Whether to create a .env file if it doesn't exist. Defaults to False.
        master_env_path (str, optional): The path to the master .env file. Defaults to ".env".
    """
    if not os.path.exists(master_env_path):
        print(f"Master .env file not found at {master_env_path}")
        return

    with open(master_env_path, "r") as f:
        master_content = f.read()

    for dirpath, _, _ in os.walk(directory_path):
        env_file_path = os.path.join(dirpath, ".env")
        if os.path.exists(env_file_path):
            print(f"Updating {env_file_path}")
            with open(env_file_path, "w") as f:
                f.write(master_content)
        elif create_if_missing:
            print(f"Creating {env_file_path}")
            with open(env_file_path, "w") as f:
                f.write(master_content)

if __name__ == "__main__":
    # Example usage: Update .env files in the current directory and its subdirectories
    # This will create .env files in all subdirectories of the project that don't have one.
    update_env_files(directory_path = ".", create_if_missing = True)