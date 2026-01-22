import os, sys
from tl_metadata import tl_metadata_from_path


path = "D:\\Professional\\OCPW Projects\\OCGD\\OCTL\\OCTLRaw"

metadata = tl_metadata_from_path(path, export = True)
metadata["2025"]

metadata["2020"]["cd"]


