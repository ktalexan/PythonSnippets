# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Create Tiger Line Metadata from Path Tree ----
# Description: This code generates Tiger Line metadata from root
# file name structure tree and naming conventions.
# Author: OpenAI ChatGPT, Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os, sys
import json


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Fx: Tiger Line Metadata ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tl_metadata_from_path(path: str, export = False) -> dict:
    """tl_metadata_from_path: Generate Tiger Line metadata from file path structure.

    Args:
        path (str): The root file path of the Tiger Line dataset.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """
    # Initialize metadata dictionary
    metadata = {}

    # Read all directories in the path
    folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Loop through each folder
    for folder in folders:
        
        # Set the directory path
        folder_path = os.path.join(path, folder)

        # Extract year from directory name
        year = folder.removeprefix("tl_")

        # Initialize year in metadata dictionary
        metadata[year] = {}

        # Define the layers to be checked
        layers = ["addr", "addrfeat", "addrfn", "arealm", "areawater", "bg", "cbsa", "cd", "coastline", "county", "cousub", "csa", "edges", "elsd", "faces", "facesah", "facesal", "facesml", "featnames", "linearwater", "metdiv", "mil", "place", "pointlm", "primaryroads", "prisecroads", "puma", "rails", "roads", "scsd", "sldl", "sldu", "tabblock", "tract", "uac", "unsd", "zcta5"]

        # Get the list of files in the folder
        files = sorted(list(set([f.split(".")[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])))

        # Get the list of files if the file has a .shp extension
        shp_files = sorted(list(set([f.split(".")[0] for f in os.listdir(folder_path) if f.endswith(".shp")])))

        # Get the list of files that are on files but not in shp_files
        dbf_files = sorted([f for f in files if f not in shp_files])
    
        # Print the count of files by type
        print(f"Year: {year}\n- Total Files: {len(files)}\n- Shapefiles: {len(shp_files)}\n- Tables: {len(dbf_files)}")

        # Loop through each file
        for f in files:
            # Split the file name into components
            file_components = f.split("_")
            # Extract the year, spatial level, and abbreviation
            file_year = file_components[1]
            file_spatial = file_components[2]
            file_abbrev = file_components[3]

            # Check if the file is a shapefile or table
            if f in shp_files:
                file_type = "Shapefile"
            elif f in dbf_files:
                file_type = "Table"
            else:
                file_type = "Unknown"

            # Check if the file layer is in the defined layers
            if file_abbrev in layers:
                file_layer = file_abbrev
                file_postfix = ""
            else:
                # Find all the matches in file_abbrev that start with the layer
                matches = [layer for layer in layers if file_abbrev.startswith(layer)]
                # Check if any matches were found
                if matches:
                    # Get the match with the longest length
                    file_layer = max(matches, key = len)
                    # Extract the postfix from the file_abbrev
                    file_postfix = file_abbrev.removeprefix(file_layer)
                else:
                    file_layer = "Unknown"
                    file_postfix = ""

            # Determine spatial level description
            match file_spatial:
                case "us":
                    spatial_level = "US"
                case "06":
                    spatial_level = "CA"
                case "06059":
                    spatial_level = "OC"
                case _:
                    spatial_level = "Unknown"

            # Calculate the length of the postfix
            len_postfix = len(file_postfix)

            # Determine postfix description
            if len_postfix == 2:
                file_postfix_desc = f"20{file_postfix} US Census"
            elif len_postfix == 3:
                file_postfix_desc = f"{file_postfix}th US Congress"
            else:
                file_postfix_desc = ""

            # Populate the metadata dictionary
            metadata[year][file_layer] = {
                "type": file_type,
                "file": f,
                "path": folder_path,
                "year": int(file_year),
                "scale": spatial_level,
                "spatial": file_spatial,
                "abbrev": file_abbrev,
                "postfix": file_postfix,
                "postfix_desc": file_postfix_desc
            }
    
    # Sort the metadata dictionary by year and file_layer
    metadata = {year: dict(sorted(metadata[year].items())) for year in sorted(metadata.keys())}

    # Check if export is True
    if export:
        # Export metadata to JSON file
        json_path = os.path.join(path, "tl_metadata.json")
        with open(json_path, "w", encoding = "utf-8") as json_file:
            json.dump(metadata, json_file, indent=4)
            print(f"Metadata exported to {json_path}")
    
    # Return the populated metadata dictionary
    return metadata

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
