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

