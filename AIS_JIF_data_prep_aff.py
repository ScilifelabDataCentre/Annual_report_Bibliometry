# Data prep for JIF and AIS values for affiliates (no ISSN available)

import pandas as pd
import numpy as np

# Load publications data

publications = pd.read_excel(
    "Data/2023/SciLifeLab-Affiliates-20231208.xlsx",
    sheet_name="publ_info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter raw pubs (2013-23 for annual report 2023)

publications = publications[
    (publications["Publication_year"] > 2017)
    & (publications["Publication_year"] < 2024)
]

# Load journal info data

journals = pd.read_excel(
    "Data/2023/JCR_JournalResults_2023_MB_neat.xlsx",
    sheet_name="AIS_2",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to match 'Journal name' in the journals file, and 'Journal' in the main data file
# Need to make everything same case

publications = publications.apply(lambda x: x.astype(str).str.lower())
journals = journals.apply(lambda x: x.astype(str).str.lower())

journals.drop_duplicates(subset="Journal name", keep="first", inplace=True)

# # Take IUID and Journal columns from publication DF, here Journal is
# # the important coulmn we need as it will be used to merge the
# # JIF and AIS values from Journals DF. If a Journal in publication
# # doesn't exist in Jounals, then the values will be NA

pubs_jif_ais_info = pd.merge(
    publications[["UT", "Publication_year", "Journal"]],
    journals,
    how="left",
    left_on="Journal",
    right_on="Journal name",
)
pubs_jif_ais_info = pubs_jif_ais_info.replace("n/a", np.nan)
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

affpubs_jif_count = (
    pubs_jif_ais_info.groupby(["Publication_year", "JIF_category"]).size().reset_index()
)
affpubs_jif_count.columns = ["Year", "Category", "Count"]

affpubs_ais_count = (
    pubs_jif_ais_info.groupby(["Publication_year", "AIS_category"]).size().reset_index()
)
affpubs_ais_count.columns = ["Year", "Category", "Count"]

# Write output to an excel sheet (one sheet for JIF and one sheet for AIS)

with pd.ExcelWriter("affiliates_publications_JIF_AIS_counts.xlsx") as out_excel:
    affpubs_jif_count.to_excel(out_excel, sheet_name="JIF", index=False)
    affpubs_ais_count.to_excel(out_excel, sheet_name="AIS", index=False)
