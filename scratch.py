import os, sys
from tl_metadata import tl_metadata_from_path


path = "F://Professional//OCPW Projects//OCGD//OCTL//OCTLRaw"

metadata = tl_metadata_from_path(path, export = True)
metadata["2025"]