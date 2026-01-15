# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Create Tiger Line Metadata from Path Tree ----
# Description: This code generates Tiger Line metadata from root
# file name structure tree and naming conventions.
# Author: OpenAI ChatGPT, Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os, sys
import json


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Tiger Line Metadata Function ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tl_metadata_from_path(path: str, export = False) -> dict:
    """tl_metadata_from_path: Generate Tiger Line metadata from file path structure.

    Args:
        path (str): The root file path of the Tiger Line dataset.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """

    # Initialize metadata dictionary
    metadata = {}

    # Extract components from the path
    base_name = os.path.basename(path)

    # Read all directories in the path
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    if "tl_xxxx" in directories:
        directories.remove("tl_xxxx")

    # Loop through each directory to extract metadata
    for d in directories:
        
        # Set the directory path
        d_path = os.path.join(path, d)
        
        # Extract year from directory name
        year = d.split("_")[1]
        
        #Populate the metadata dictionary for each folder year
        metadata[year] = {"folder": d, "year": int(year)}

        # Get the directories inside each d_path
        tl_levels = [sd for sd in os.listdir(d_path) if os.path.isdir(os.path.join(d_path, sd))]
        metadata[year]["levels"] = {}
        
        # Loop through each level in the directory
        for level in tl_levels:
            # Set the level path
            level_path = os.path.join(d_path, level)
            
            # Populate the metadata dictionary for each level
            metadata[year]["levels"][level] = {}

            # Find if there are any files with .shp extension
            if any(f.endswith(".shp") for f in os.listdir(level_path)):
                f_type = "Shapefile"
            elif any(f.endswith(".dbf") for f in os.listdir(level_path)):
                f_type = "Table"
            else:
                f_type = "Unknown"
            
            # Get all the unique files inside each level_path
            tl_files = list(set([f.split(".")[0] for f in os.listdir(level_path) if os.path.isfile(os.path.join(level_path, f))]))
            
            # Loop through each file in the level
            for f in tl_files:
                # Extract the file year
                file_year = f.split("_")[1]

                # Extract the spatial level
                file_spatial = f.split("_")[2]
                match file_spatial:
                    case "us":
                        spatial_level = "US"
                    case "06":
                        spatial_level = "CA"
                    case "06059":
                        spatial_level = "OC"
                    case _:
                        spatial_level = "Unknown"
                
                # Extract the file abbreviation
                file_abbrev = f.split("_")[3]
                
                # Populate the metadata dictionary for each file
                metadata[year]["levels"][level]["type"] = f_type
                metadata[year]["levels"][level]["file"] = f
                metadata[year]["levels"][level]["year"] = int(file_year)
                metadata[year]["levels"][level]["scale"] = spatial_level
                metadata[year]["levels"][level]["spatial"] = file_spatial

                # Calculate postfix information
                len_diff = len(file_abbrev) - len(level)
                file_postfix = ""
                if len_diff > 0:
                    file_postfix = file_abbrev[len(level):]
                
                # Populate abbreviation and postfix
                metadata[year]["levels"][level]["abbrev"] = level.lower()
                metadata[year]["levels"][level]["postfix"] = file_postfix
                
                # Populate postfix description
                match len_diff:
                    case 2:
                        metadata[year]["levels"][level]["postfix_desc"] = f"20{file_postfix} US Census"
                    case 3:
                        metadata[year]["levels"][level]["postfix_desc"] = f"{file_postfix}th US Congress"
                    case _:
                        metadata[year]["levels"][level]["postfix_desc"] = ""
    
    if export:
        # Export metadata to JSON file
        json_path = os.path.join(path, "tl_metadata.json")
        with open(json_path, "w", encoding = "utf-8") as json_file:
            json.dump(metadata, json_file, indent=4)
            print(f"Metadata exported to {json_path}")
    
    # Return the populated metadata dictionary
    return metadata
