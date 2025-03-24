#! /usr/bin/python

# List researcher publications with hosting organisation
# Based on data from KTH

import pandas as pd
import numpy as np

# information from KTH

Pubs_raw = pd.read_excel(
    # "Data/SciLifeLab-affiliates-20241204.xlsx",
    # "Data/SciLifeLab-infrastructure-20241204.xlsx",
    "Data/SciLifeLab-affiliates-20241204.xlsx",
    sheet_name="publ_info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

Authors_raw = pd.read_excel(
    "Data/SciLifeLab-affiliates-20241204.xlsx",
    # "Data/SciLifeLab-infrastructure-20241204.xlsx",
    sheet_name="authors",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter for the appropriate time frame

#Pubs_raw = Pubs_raw[
#    (Pubs_raw["Publication_year"] == 2024)
#]

# Need to join the two above files; easier to work with only columns of interest

Authors_sub = Authors_raw[
    [
        "UT",
        "Name_eng",
#        "City",
        "Country_name",
        "name_full",
    ]
]

#Authors_sub = Authors_sub[
#    (Authors_sub["Name_eng"].startswith(['Link']))
#]

Pubs_sub = Pubs_raw[
    [
        "UT",
        "Title",
        "Publication_year",
        "Journal",
    ]
]

Merged = pd.merge(
    Pubs_sub,
    Authors_sub,
    on="UT",
)

#JIF_merge_abbnames.drop_duplicates(subset="UT", keep="first", inplace=True)

Merged.to_excel("Publ with organisation.xlsx")
