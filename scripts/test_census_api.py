import os
import sys
import json
import requests
import pandas as pd
import pytidycensus as tc
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






api_key = os.getenv("CENSUS_API_KEY")
tc.set_census_api_key(api_key)
#tc.set_census_api_key(api_key, install = True)

df = tc.get_acs(
    geography = "tract",
    variables = ["B01001_001E"],
    state = "CA",
    county = "Orange",
    year = 2022,
    geometry = True
)



import urllib.request
import urllib.parse
import json
import sys
import requests

# Original URL: https://api.census.gov/data/2023/acs/acs5/subject?get=NAME,S0101_C01_001E&for=county:059&in=state:06

# Year used in the Census API path (appears after /data/)
year = 2023


def fetch_census(year: int, table_id: str, var_id: str = None, geography: str = "county"):
    """Fetch JSON from the Census API using urllib (no external deps).

    Args:
        get_vars: comma-separated variables for `get` param.
        for_clause: the `for` query value (e.g., 'county:059').
        in_clause: the `in` query value (e.g., 'state:06').

    Returns:
        Parsed JSON response.

    Raises:
        urllib.error.HTTPError on HTTP failures.
        json.JSONDecodeError if response isn't valid JSON.
    """
    year = str(year)

    # If var_id is provided, construct get_vars accordingly
    get_vars = f"NAME,group({table_id})"
    if var_id:
        get_vars = f"NAME,{table_id}_{var_id}"

    base = f"https://api.census.gov/data/{year}/acs/acs5/subject"

    match geography:
        case "county":
            params = {
                "get": get_vars,
                "for": "county:059",
                "in": "state:06"
            }
        case "cousub":
            params = {
                "get": get_vars,
                "for": "county subdivision:*",
                "in": ["state:06", "county:059"]
            }
        case "tract":
            params = {
                "get": get_vars,
                "for": "tract:*",
                "in": ["state:06", "county:059"]
            }
        case "place":
            params = {
                "get": get_vars,
                "for": "place:*",
                "in": "state:06"
            }
        case "consolidated city":
            params = {
                "get": get_vars,
                "for": "consolidated city:*",
                "in": "state:06"
            }
        case "congressional district":
            params = {
                "get": get_vars,
                "for": "congressional district:*",
                "in": "state:06"
            }
        case _:
            raise ValueError(f"Unsupported geography: {geography}")

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


data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "county")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "cousub")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "tract")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "place")
print(json.dumps(data, indent=4))

data = fetch_census(year = 2023, table_id = "S0101", var_id = "C01_001E", geography = "congressional district")
print(json.dumps(data, indent=4))


data2 = fetch_census(year = 2010, table_id = "S0101", geography = "county")
print(json.dumps(data2, indent=4))



def fetch_acs_variables(year: int):
    """Fetch ACS variable metadata using requests (external dependency)."""
    url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

acs_vars_2023 = fetch_acs_variables(2023)
print(json.dumps(acs_vars_2023, indent=4))

# Convert the acs_vars_2023 dict to a pandas DataFrame for easier viewing, where the keys are the variable rows and the values are the columns.
import pandas as pd
df = pd.DataFrame.from_dict(acs_vars_2023['variables'], orient='index')
print(df)

