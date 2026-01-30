# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Project: Project Template
# Title: Project Template Main Class ----
# Author: Dr. Kostas Alexandridis, GISP
# Date: January 2026
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import necessary libraries ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from __future__ import annotations
import os
import sys
import datetime
from pathlib import Path
import json
import re
import logging
import unicodedata
from typing import Union, Optional, Dict, Any
#from fontTools.misc.plistlib import Data
import wmi
import pytz
import pandas as pd
import arcpy
from arcpy import metadata as md
from arcgis.features import GeoAccessor, GeoSeriesAccessor


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the DualOutput class for logging ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DualOutput:
    """
    A class to duplicate console output to a log file.
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, filename: Optional[str] = None, meta: Optional[dict] = None):
        self._orig = None
        self._log = None
        self._filename = filename
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._filetype = "log"  # Default filetype
        # Store optional project metadata so other methods can access it
        self.meta: Optional[dict] = meta
        self.project_name: Optional[str] = meta.get("name") if meta else None
        self.project_title: Optional[str] = meta.get("title") if meta else None
        self.project_version: Optional[float] = meta.get("version") if meta else None
        self.project_author: Optional[str] = meta.get("author") if meta else None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Open log file ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _open_log(self, meta: dict, filename: str):
        # From the filename, determine if it's a .log, .txt, or .md file
        if filename.endswith(".md"):
            self._filetype = "markdown"
        elif filename.endswith(".log") or filename.endswith(".txt"):
            self._filetype = "log"
        if meta is not None:
            self.project_name = meta.get("name")
            self.project_title = meta.get("title")
            self.project_version = meta.get("version")
            self.project_author = meta.get("author")
        # Open the log file in append mode in the tests directory
        path = os.path.join(os.getcwd(), "tests", os.path.basename(filename))
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok = True)
        # If the file does not exist, open it and writh an initial line
        if not os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as f:
                # If it is a markdown file, write the header as the meta.get("project_name")
                if self._filetype == "markdown":
                    f.write(f"# {self.project_name}\n- Title: {self.project_title}\n- Version: {self.project_version}\n- Author: {self.project_author}\n- Filename: **{os.path.basename(filename)}**\n")
                elif self._filetype == "log":
                    # Wtite the project name and title in uppercase
                    f.write(f"Project Name: {self.project_name.upper()}\nProject Title: {self.project_title.upper()}\nVersion: {self.project_version}\nAuthor: {self.project_author}\nFilename: {os.path.basename(filename)}\n\n")
        # Return the opened file object
        return open(path, "a", encoding="utf-8")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Enable logging ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def enable(self, meta: Optional[dict] = None, filename: Optional[str] = None):
        logid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if self._orig is not None:
            return
        # Prefer provided meta, otherwise use stored meta
        if meta is not None:
            self.meta = meta
        # Determine the filetype based on the filename extension
        fn = filename or self._filename or "output.log"
        if fn.endswith(".md"):
            self._filetype = "markdown"
        elif fn.endswith(".log"):
            self._filetype = "log"
        elif fn.endswith(".txt"):
            self._filetype = "text"
        else:
            print("Warning: Unrecognized file extension. Defaulting to .log")
            self._filetype = "log"  # Default to log if no extension provided
            # Change filename to have .log extension
            fn = os.path.splitext(fn)[0] + ".log"
        self._orig = sys.stdout
        self._log = self._open_log(meta, fn)
        sys.stdout = self
        self._start_time = datetime.datetime.now()

        if self._filetype == "markdown":
            print("----\n")
            print(f"\n> [!NOTE]\n> - Log ID: {logid}\n> - Date: {datetime.datetime.now().strftime('%B %d, %Y')}\n> - Logging started at {self._start_time.strftime('%m/%d/%Y %H:%M:%S')}\n")
        else:
            print(f"---- Start of log ID: {logid} ----")
            print(f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}")
            print(f"Logging started at {self._start_time.strftime('%m/%d/%Y %H:%M:%S')}\n\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Disable logging ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def disable(self):
        self._end_time = datetime.datetime.now()
        if self._filetype == "markdown":
            print(f"\n> [!NOTE]\n> - Logging ended at {self._end_time.strftime('%m/%d/%Y %H:%M:%S')}")
        else:
            print(f"\n\nLogging ended at {self._end_time.strftime('%m/%d/%Y %H:%M:%S')}")
        self._duration = self._end_time - self._start_time
        if self._duration.total_seconds() < 60:
            if self._filetype == "markdown":
                print(f"> - Elapsed Time: {self._duration.total_seconds():.0f} seconds\n")
                print("----\n")
            else:
                print(f"Elapsed Time: {self._duration.total_seconds():.0f} seconds")
                print("---- End of log ----\n")
        else:
            # Display time in days, hours, minutes and seconds
            days, remainder = divmod(self._duration.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            # Only show non-zero values
            if days > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            elif hours > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            elif minutes > 0:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(minutes)} minutes and {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(minutes)} minutes and {int(seconds)} seconds")
                    print("---- End of log ----\n")
            else:
                if self._filetype == "markdown":
                    print(f"> - Elapsed Time: {int(seconds)} seconds\n")
                    print("----\n")
                else:
                    print(f"Elapsed Time: {int(seconds)} seconds")
                    print("---- End of log ----\n")
        
        if self._orig is None:
            return
        sys.stdout = self._orig
        try:
            if self._log:
                self._log.close()
        finally:
            self._orig = None
            self._log = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Context manager enter ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __enter__(self):
        # Use stored metadata when entering context if available
        self.enable(meta=self.meta, filename=self._filename)
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Context manager exit ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __exit__(self, exc_type, exc, tb):
        self.disable()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Write output ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def write(self, message):
        if self._orig:
            self._orig.write(message)
        if self._log:
            try:
                self._log.write(message)
            except (OSError, UnicodeEncodeError):
                # Ignore known I/O/encoding errors when writing to the log; allow other exceptions to propagate
                pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Flush output ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def flush(self):
        if self._orig:
            self._orig.flush()
        if self._log:
            try:
                self._log.flush()
            except OSError:
                # Ignore known I/O errors when flushing the log; allow other exceptions to propagate
                pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the main class ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ClassTemplate:
    """
    A class containing functions and methods for the Project Template.
    Attributes:
        None
    Methods:
        project_metadata(part: int, version: float, silent: bool = False) -> dict:
            Generates project metadata for the OCUP data processing project.
        project_directories(silent: bool = False) -> dict:
            Generates project directories for the OCSWITRS data processing project.
    Returns:
        None
    Raises:
        None
    Examples:
        >>> metadata = project_metadata(1, 1)
        >>> prj_dirs = project_directories()
    Notes:
        This class is used to generate project metadata and directories for the project.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Class initialization ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, part: int, version: float):
        """
        Initializes the ProjectTemplate class.
        """
        # Create a DualOutput instance for logging
        self.logger = DualOutput()

        # Set the part and version
        self.part = part
        self.version = version

        # Set the base path and data date
        self.base_path = os.getcwd()
        self.data_date = datetime.datetime.now().strftime("%B %Y")

        # Create an prj_meta variable calling the function using the part and version variables from the initialization
        self.prj_meta = self.project_metadata(silent = False)

        # Create an prj_dir variable calling the function using the part and version variables from the initialization
        self.prj_dirs = self.project_directories(silent = False)

        # Attach project directories to logger so it's available to all logger methods
        try:
            self.logger.meta = self.prj_dirs
        except AttributeError:
            # Logger does not support 'meta' attribute; ignore safely
            pass

        # Set the Spatia Reference to Web Mercator
        self.sr = arcpy.SpatialReference(4269)  # NAD83

        # Load the codebook
        #self.cb_path = os.path.join(self.prj_dirs["codebook"], "cb.json")
        #self.cb, self.df_cb = self.load_cb(silent = False)
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project metadata function ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_metadata(self, silent: bool = False) -> dict:
        """
        Function to generate project metadata for the OCUP data processing project.
        Args:
            silent (bool, optional): Whether to print the metadata information. Defaults to False.
        Returns:
            prj_meta (dict): A dictionary containing the project metadata.
        Raises:
            ValueError: If part is not an integer, or if version is not numeric.
        Example:
            >>> metadata = project_metadata(1, 1)
        Notes:
            The project_metadata function is used to generate project metadata for the OCUP data processing project.
        """

        # Match the part to a specific step and description (with default case)
        match self.part:
            case 1:
                step = "Part 1: Raw Data Processing"
                desc = "Importing the raw data files and perform initial geocoding"
            case 2:
                step = "Part 2: Imported Data Geocoding"
                desc = "Geocoding the imported data and preparing it for GIS processing."
            case 3:
                step = "Part 3: GIS Data Processing"
                desc = "GIS Geoprocessing and formatting of the OCUP data."
            case 4:
                step = "Part 4: GIS Map Processing"
                desc = "Creating maps and visualizations of the OCUP data."
            case 5:
                step = "Part 5: GIS Data Sharing"
                desc = "Exporting and sharing the GIS data to ArcGIS Online."
            case _:
                step = "Part 0: General Data Processing"
                desc = "General data processing and analysis (default)."

        # Import the ocup_metadata json file
        metadata_file = os.path.join(os.getcwd(), "metadata", "ocup_metadata.json")
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
        
        # Load the metadata file
        with open(metadata_file, "r", encoding = "utf-8") as f:
            prj_meta = json.load(f)

        # Set the metadata date as the current date
        current_date = datetime.date.today()
        prj_meta["date"] = current_date.strftime("%Y-%m-%d")

        # Set the metadata version:
        prj_meta["version"] = self.version

        # Set the folder version:
        folder_version = str(self.version).replace(".", "-")

        data_dir = os.path.join(os.getcwd(), "data", "original", folder_version)

        # create a table with the subdirectories of the current_data_dir folder
        data_folders = os.listdir(data_dir)

        # Obtain the data folder metadata and populate the prj_meta dictionary
        for folder in data_folders:
            folder_path = os.path.join(data_dir, folder)
            if os.path.isdir(folder_path):
                # Get the first 2 characters of the folder name
                folder_id = folder[:2]
                folder_name = folder.split(f"{folder_id}_")[-1]
                # Count the number of files in the folder
                file_count = len(os.listdir(folder_path))
                prj_meta["folders"][folder_id]["folder"] = folder
                prj_meta["folders"][folder_id]["count"] = file_count
                prj_meta["folders"][folder_id]["names"] = {}
                for file in os.listdir(folder_path):
                    file_number = file.split(f"{folder_name}_")[-1].replace(".csv", "").split("_of_")[0]
                    # file_number = int(file.split("File_")[-1].replace(".csv", "").split("_of_")[0])
                    if os.path.isfile(os.path.join(folder_path, file)):
                        # Store the file name in the dictionary
                        prj_meta["folders"][folder_id]["names"][str(file_number)] = {
                            "no": file_number,
                            "name": file,
                            "path": os.path.join(folder_path, file)
                        }
                # Sort the prj_meta["folders"][folder_id]["names"] by file number
                prj_meta["folders"][folder_id]["names"] = dict(sorted(prj_meta["folders"][folder_id]["names"].items(), key = lambda item: item[1]["no"]))
        # Export the metadata dictionary to a JSON file and replace the existing one
        with open(metadata_file, 'w', encoding = "utf-8") as f:
            json.dump(prj_meta, f, indent = 4)

        # Print the project metadata if silent is False
        if not silent:
            print(f"{prj_meta['title']} ({prj_meta['name']})")
            print(f"- {step}")
            print(f"- Description: {desc}")
            print(f"- Date: {prj_meta['date']}")
            print(f"- Version: {prj_meta['version']}")
            print("- Folders:")
            print(f"  - $0 to $10: {prj_meta['folders']['01']['count']} files")
            print(f"  - $10 to $100: {prj_meta['folders']['02']['count']} files")
            print(f"  - $100 to $500: {prj_meta['folders']['03']['count']} files")
            print(f"  - $500+: {prj_meta['folders']['04']['count']} files")

        # Return the project metadata dictionary
        return prj_meta


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## fx: Project Directories function ----
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def project_directories(self, silent: bool = False) -> dict:
        """
        Function to generate project directories for the OCSWITRS data processing project.
        Args:
            silent (bool, optional): Whether to print the project directories. Defaults to False.
        Returns:
            prj_dirs (dict): A dictionary containing the project directories.
        Raises:
            None
        Example:
            >>> prj_dirs = projectDirectories("/path/to/project")
        Notes:
            The project_directories function is used to generate project directories for the OCSWITRS data processing project.
        """
        prj_dirs = {
            "root": self.base_path,
            "admin": os.path.join(self.base_path, "admin"),
            "analysis": os.path.join(self.base_path, "analysis"),
            "codebook": os.path.join(self.base_path, "codebook"),
            "data": os.path.join(self.base_path, "data"),
            "data_original": os.path.join(self.base_path, "data", "original"),
            "data_archived": os.path.join(self.base_path, "data", "archived"),
            "gis": os.path.join(self.base_path, "gis"),
            "gis_folder": os.path.join(self.base_path, "gis", "FOLDER_NAME"),
            "gis_folder_aprx": os.path.join(self.base_path, "gis", "FOLDER_NAME", "FOLDER_NAME.aprx"),
            "gis_folder_gdb": os.path.join(self.base_path, "gis", "FOLDER_NAME", "FOLDER_NAME.gdb"),
            "gis_supporting_gdb": os.path.join(self.base_path, "gis", "supporting.gdb"),
            "gis_archived": os.path.join(self.base_path, "gis", "archived"),
            "metadata": os.path.join(self.base_path, "metadata"),
            "notebooks": os.path.join(self.base_path, "notebooks"),
            "scripts": os.path.join(self.base_path, "scripts"),
            "scripts_archived": os.path.join(self.base_path, "scripts", "archived"),        
        }
        # Print the project directories
        if not silent:
            print("Project Directories:")
            for key, value in prj_dirs.items():
                print(f"- {key}: {value}")
        # Return the project directories
        return prj_dirs


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# End of Script ----
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
