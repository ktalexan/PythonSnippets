import os
import sys
import json
import urllib.request
import urllib.parse
import requests
import pandas as pd

#import pytidycensus as tc
#from census import Census
#from us import states
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

fields = ("GEO_ID", "NAME", "B01003_001E")

c = Census(os.getenv("CENSUS_API_KEY"))
tables_dict = c.acs5.tables()
print(json.dumps(tables_dict, indent=4))


# Orange County
county_data = c.acs5.get(fields, geo={"for": "county:059", "in": f"state:{states.CA.fips}"})
print(county_data)
print(len(county_data))


c.acs5.state_county(fields, states.CA.fips, "059", year = 2022)
c.acs5.state_county_subdivision(fields, states.CA.fips, "059", Census.ALL, year = 2022)
c.acs5.state_county_blockgroup(fields, states.CA.fips, "059", Census.ALL, year = 2022)
c.acs5.state_county_tract(fields, states.CA.fips, "059", Census.ALL, year = 2022)
c.acs5.state_place(fields, states.CA.fips, Census.ALL, year = 2022)

c.acs5.state_county_blockgroup(fields, states.CA.fips, "059", Census.ALL, year = 2013)


# County Subdivisions
cousub_data = c.acs5.get(fields, geo={"for": "county subdivision:*", "in": [f"state:{states.CA.fips}", "county:059"]}, year = 2010)
print(cousub_data)
print(len(cousub_data))


# Block Groups
blockgroup_data = c.acs5.get(fields, geo={"for": "block group:*", "in": [f"state:{states.CA.fips}", "county:059", "tract:*"]}, year = 2010)
print(blockgroup_data)
print(len(blockgroup_data))


#https://api.census.gov/data/2023/acs/acs5?get=NAME,B01001_001E&for=block%20group:*&in=state:06&in=county:073&in=tract:*

api_key = os.getenv("CENSUS_API_KEY")
tc.set_census_api_key(api_key)
#tc.set_census_api_key(api_key, install = True)

demo_vars = {
    "Total_Population": "B01003_001",
    "Median_Household_Income": "B19013_001", 
    "Median_Home_Value": "B25077_001"
}
df_year = 2020

df_county = tc.get_acs(
    geography = "county",
    variables = demo_vars,
    year = df_year,
    survey = "acs5",
    state = "CA",
    county = "Orange",
    geometry = True,
    keep_geo_vars = True
)
print(df_county)

df_subdivision = tc.get_acs(
    geography = "county subdivision",
    variables = demo_vars,
    year = df_year,
    survey = "acs5",
    state = "CA",
    county = "Orange",
    geometry = True,
    keep_geo_vars = True
)
print(df_subdivision)

df_tract = tc.get_acs(
    geography = "tract",
    variables = demo_vars,
    year = df_year,
    survey = "acs5",
    state = "CA",
    county = "Orange",
    geometry = True,
    keep_geo_vars = True
)
print(df_tract)

df = tc.get_acs(
    geography = "block group:*",
    variables = demo_vars,
    state = "CA",
    county = "Orange",
    year = 2022,
    geometry = True
)
print(df.head())



# Get 2020 Census population data
pop_2020 = tc.get_decennial(
    geography = "county",
    variables = {"TPOP": "P1_001N"},
    year = 2020,
    state = "CA",
    county = "Orange",
    geometry = True
)

print(pop_2020.head())


var_dict = {
    "demographic": {
        "pop": {
            "id": "B01003_001",
            "alias": "Total Population"
        },
        "male": {
            "id": "B01001_002",
            "alias": "Male Population"
        },
        "female": {
            "id": "B01001_026",
            "alias": "Female Population"
        }
    },
    "social": {

    },
    "economic": {

    },
    "housing": {

    }
}

use_vars = {key: value["id"] for key, value in var_dict["demographic"].items()}


df = tc.get_acs(
    geography = "tract",
    variables = use_vars,
    state = "CA",
    county = "Orange",
    survey = "acs5",
    year = 2022,
    geometry = True
)
print(df)

df = tc.get_acs(
    geography = "county",
    variables = use_vars,
    state = "CA",
    county = "Orange",
    survey = "acs5",
    year = 2022,
    geometry = True
)
print(df)

df = tc.get_acs(
    geography = "place",
    variables = use_vars,
    state = "06",
    county = "059",
    survey = "acs5",
    year = 2022,
    geometry = True
)
print(df)

df = tc.get_acs(
    geography = "block group",
    variables = "B01003_001",
    survey = "acs5",
    year = 2022,
    geometry = True
)
print(df)



print(df)

df.columns


import urllib.request
import urllib.parse
import json
import sys
import requests

# Original URL: https://api.census.gov/data/2023/acs/acs5/subject?get=NAME,S0101_C01_001E&for=county:059&in=state:06

# Year used in the Census API path (appears after /data/)
year = 2023
dataset = ["acs", 5]
var_list = ["B01003_001E", "B01001_002E", "B01001_026E"]
geographies = {
    "for": {"level": "county", "value": "059"},
    "in": {"level": "state", "value": "06"},
}
api_key = os.getenv("CENSUS_API_KEY")

# Geographies
if "for" in geographies:
    geo = f"&for={geographies["for"]["level"]}:{geographies["for"]["value"]}"
if "in" in geographies:
    geo = f"{geo}&in={geographies["in"]["level"]}:{geographies["in"]["value"]}"


host_name = f"https://api.census.gov/data/{year}/{dataset[0]}/{dataset[0]}{dataset[1]}?get=GEO_ID,NAME,{",".join(var_list)}{geo}&key={api_key}"




# manual: https://www2.census.gov/data/api-documentation/api-user-guide.pdf

def fetch_census(year: int, dataset: list, var_dict: dict, geography: dict):
    year = str(year)
    api_key = os.getenv("CENSUS_API_KEY")

    match var_dict["type"]:
        case "list":
            var_string = f"GEO_ID,NAME,{",".join(var_dict["data"])}"
        case "group":
            var_string = f"GEO_ID,NAME,group({var_dict["data"]})"

    match geography:
        case "county":
            params = {
                "get": var_string,
                "for": "county:059",
                "in": "state:06",
                "key": api_key
            }
        case "cousub":
            params = {
                "get": var_string,
                "for": "county subdivision:*",
                "in": ["state:06", "county:059"],
                "key": api_key
            }
        case "tract":
            params = {
                "get": var_string,
                "for": "tract:*",
                "in": ["state:06", "county:059"],
                "key": api_key
            }
        case "place":
            params = {
                "get": var_string,
                "for": "place:*",
                "in": ["state:06", "county:059"],
                "key": api_key
            }
        case "block group":
            params = {
                "get": var_string,
                "for": "block group:*",
                "in": ["state:06", "county:059"],
                "key": api_key
            }
        case _:
            raise ValueError(f"Invalid geography: {geography}")

    base = f"https://api.census.gov/data/{year}/{dataset[0]}/{dataset[0]}{dataset[1]}"

    # Use doseq=True so sequence values (like multiple `in` clauses)
    # produce repeated query keys: &in=state:06&in=county:059
    url = base + "?" + urllib.parse.urlencode(params, doseq=True)
    try:
        with urllib.request.urlopen(url) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            text = resp.read().decode(charset)
            raw = json.loads(text)
            # Census API returns a top-level list where the first sublist
            # is the headers and subsequent sublists are rows of values.
            if isinstance(raw, list) and len(raw) >= 1 and all(isinstance(r, list) for r in raw):
                headers = raw[0]
                rows = raw[1:]
                return [dict(zip(headers, row)) for row in rows]
            return raw
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        try:
            body = e.read().decode("utf-8", errors="replace")
            print(body, file=sys.stderr)
        except (UnicodeDecodeError, ValueError, TypeError, AttributeError):
            pass
        raise

year = 2023
dataset = ["acs", 5]
var_dict = {
    "type": "list",
    "data": ["B01003_001E", "B01001_002E", "B01001_026E"]
}

data = fetch_census(year = year, dataset = dataset, var_dict = var_dict, geography = "county")
print(json.dumps(data, indent=4))

data = fetch_census(year = year, dataset = dataset, var_dict = var_dict, geography = "cousub")
print(json.dumps(data, indent=4))

data = fetch_census(year = year, dataset = dataset, var_dict = var_dict, geography = "tract")
print(json.dumps(data, indent=4))

data = fetch_census(year = year, dataset = dataset, var_dict = var_dict, geography = "block group")
print(json.dumps(data, indent=4))
# Length of data
print(len(data))


data = fetch_census(year = year, dataset = dataset, var_dict = var_dict, geography = "place")
print(json.dumps(data, indent=4))

