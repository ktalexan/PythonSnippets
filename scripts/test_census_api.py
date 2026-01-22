import os
import requests
import pandas as pd
import json
from dotenv import load_dotenv
load_dotenv()
from scripts.CensusAPI import ACSAPI

# Initialize the ACSAPI class
acs = ACSAPI(year = 2022, dataset = 'acs/acs5')

# Fetch data
variables = ["B01001_001E"]
geo = "tract:*"
data = acs.fetch_data(variables, geo)
print(data.head())
