# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python Snippet: Census API Classes Definition ----
# Description: The following python classes provide a structured way to interact with
#              the US Census Bureau's API, allowing users to fetch demographic, 
#              social, economic, and housing data. The classes encapsulate methods for
#              constructing API requests, handling responses, and managing parameters.
# Author: Dr. Kostas Alexandridis
# Date: January 2026
# License: MIT License
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Import Libraries ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import json
import urllib.request
import urllib.parse
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## CensusAPI Class Definition ----
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ACSAPI:
    """
    ACSAPI: A class to interact with the US Census Bureau's American Community Survey (ACS) API.
    """
    BASE_URL = "https://api.census.gov/data"

    def __init__(self, year: int, dataset: str):
        """
        Initialize the ACSAPI class with the specified year, dataset, and optional API key.

        Args:
            year (int): The year of the ACS data to access.
            dataset (str): The specific ACS dataset (e.g., 'acs/acs5').
            api_key (str, optional): The Census API key. Defaults to None.
        """
        self.year = year
        self.dataset = dataset
        
        # Get the API key from the dot environment variable if not provided
        self.api_key = os.getenv("CENSUS_API_KEY")
    
        if not self.api_key:
            raise ValueError("An API key must be provided either as an argument or via the CENSUS_API_KEY environment variable.")

    def build_url(self, variables: list, geo: str) -> str:
        """
        Build the API request URL.

        Args:
            variables (list): List of variable names to retrieve.
            geo (str): Geographic specification for the data request.

        Returns:
            str: The constructed API request URL.
        """
        var_string = ",".join(variables)
        url = f"{self.BASE_URL}/{self.year}/{self.dataset}?get={var_string}&for={geo}&key={self.api_key}"
        return url

    def fetch_data(self, variables: list, geo: str) -> pd.DataFrame:
        """
        Fetch data from the Census API.

        Args:
            variables (list): List of variable names to retrieve.
            geo (str): Geographic specification for the data request.

        Returns:
            pd.DataFrame: A DataFrame containing the fetched data.
        """
        url = self.build_url(variables, geo)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

