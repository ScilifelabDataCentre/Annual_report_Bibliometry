# Data prep for JIF and AIS values for infrastructure and fellows

import pandas as pd
import numpy as np

# Load publications data

publications = pd.read_excel(
    "Data/2023/SciLifeLab_publications_Infrastucture_2023.xlsx",
    sheet_name="Publications 20231204-1239",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter raw pubs (2013-23 for annual report 2023)

publications = publications[
    (publications["Year"] > 2017) & (publications["Year"] < 2024)
]

# Load journal info data

journal_info = pd.read_excel(
    "Data/2023/JCR_JournalResults_2023_MB_neat.xlsx",
    sheet_name="AIS_2",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# For easier processing combine ISSN and eISSN columns in Jounal to one

journals = pd.concat(
    [
        journal_info[["ISSN", "JIF Without Self Cites", "Article Influence Score"]],
        journal_info[
            ["eISSN", "JIF Without Self Cites", "Article Influence Score"]
        ].rename(columns={"eISSN": "ISSN"}),
    ],
    ignore_index=True,
)
journals = journals[journals["ISSN"] != "N/A"]
journals.drop_duplicates(subset="ISSN", keep="first", inplace=True)

# Take IUID and ISSN columns from publication DF, here ISSN is
# the important coulmn we need as it will be used to merge the
# JIF and AIS values from Journals DF. If a ISSN in publication
# doesn't exist in Jounals, then the values will be NA

pubs_jif_ais_info = pd.merge(
    publications[["IUID", "Year", "ISSN"]],
    journals,
    how="left",
    left_on="ISSN",
    right_on="ISSN",
)
pubs_jif_ais_info = pubs_jif_ais_info.replace("N/A", np.nan)
pubs_jif_ais_info["JIF Without Self Cites"] = pd.to_numeric(
    pubs_jif_ais_info["JIF Without Self Cites"].fillna(-1)
)
pubs_jif_ais_info["Article Influence Score"] = pd.to_numeric(
    pubs_jif_ais_info["Article Influence Score"].fillna(-1)
)

# Create a category column for JIF and AIS based on their values

pubs_jif_ais_info["JIF_category"] = pd.cut(
    pubs_jif_ais_info["JIF Without Self Cites"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

pubs_jif_ais_info["AIS_category"] = pd.cut(
    pubs_jif_ais_info["Article Influence Score"],
    bins=[-1, 0, 1, 1000],
    include_lowest=True,
    labels=["AIS unknown", "AIS <1", "AIS >1"],
)

# Now count each category in each year

infpubs_jif_count = (
    pubs_jif_ais_info.groupby(["Year", "JIF_category"]).size().reset_index()
)
infpubs_jif_count.columns = ["Year", "Category", "Count"]

infpubs_ais_count = (
    pubs_jif_ais_info.groupby(["Year", "AIS_category"]).size().reset_index()
)
infpubs_ais_count.columns = ["Year", "Category", "Count"]

# Write output to an excel sheet (one sheet for JIF and one sheet for AIS)

with pd.ExcelWriter("infra_publications_JIF_AIS_counts.xlsx") as out_excel:
    infpubs_jif_count.to_excel(out_excel, sheet_name="JIF", index=False)
    infpubs_ais_count.to_excel(out_excel, sheet_name="AIS", index=False)
