import os, sys
#from scripts.tl_metadata import tl_metadata_from_path
#from scripts.update_master_env import update_env_files
from scripts.update_master_gitignore import update_gitignore_files


# Check all subdirectories and create .gitignore files if missing
update_gitignore_files()

# Check a specific project directory
#update_gitignore_files(project_name = "OCTraffic")

# Check all subdirectories and create .env files if missing
#update_env_files()

# Check a specific project directory
#update_env_files(project_name = "OCTraffic")


# path = "D:\\Professional\\OCPW Projects\\OCGD\\OCTL\\OCTLRaw"

# metadata = tl_metadata_from_path(path, export = True)
# metadata["2025"]

# metadata["2020"]["cd"]



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






project_name = None
create_if_missing = True

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

        # Check if there is a .github folder in the folder
        folder_github = os.path.join(project_root, folder, ".github")
        # If folder_github exists and it is a directory
        if os.path.exists(folder_github) and os.path.isdir(folder_github):
            # Check if there is 'copilot-instructions.md' in the .github folder
            copilot_instructions = os.path.join(folder_github, "copilot-instructions.md")
            
            if os.path.exists(copilot_instructions):
                print(f"- Found copilot-instructions.md in {folder}")

            folder_instructions = os.path.join(folder_github, "instructions")
            if os.path.exists(folder_instructions) and os.path.isdir(folder_instructions):
                print(f"- Found instructions folder in {folder}")

                coding_instructions = os.path.join(folder_instructions, "general-coding-instructions.md")
                if os.path.exists(coding_instructions):
                    print(f"- Found general-coding-instructions.md in {folder}")

        # Check if there is an .agent folder in the folder
        folder_agent = os.path.join(project_root, folder, ".agent")
        if os.path.exists(folder_agent):
            continue

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
