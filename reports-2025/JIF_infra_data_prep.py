#! /usr/bin/python

# Preparation of the data related to infrastructure for JIF plot
# Based on data from infrastructure publications database (filtered for active facilities each year)

import pandas as pd
import numpy as np

years_of_interest = range(2020, 2026) # for 2025 is 2020-25
pub_type = "Infrastructure"

# information from publication database
Pubs_JIF_raw = pd.read_excel(
    "Data/KTH Infrastructure Extraction 2025-12-22.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["Title", "Year", "Labels", "Journal", "ISSN", "ISSN-L"]
)

# information for JIF scores
# easier to work with only columns of interest.
JIF_scores_sub = pd.read_excel(
    "Data/JCR-2025.xlsx",
    sheet_name="JIF2024",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["ISSN", "eISSN", "Journal name", "JCR Abbreviation", "JIF Without Self Cites"]
)

preprint_journals = [
    "biorxiv",
    "chemrxiv",
    "lakartidningen",
    "medrxiv",
    "optica open",
    "osf",
    "res sq",
    "ssrn journal",
    "ssrn", # temp
]

# Need to filter for the appropriate time frame
Pubs_JIF_sub = Pubs_JIF_raw[Pubs_JIF_raw["Year"].isin(years_of_interest)]
Pubs_JIF_sub = Pubs_JIF_sub[-Pubs_JIF_sub["Journal"].str.lower().isin(preprint_journals)]

# Should we also select the type of papers?
# Pubs_JIF_raw = Pubs_JIF_raw[Pubs_JIF_raw["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]

# Need to join the two files above and align JIF with ISSN/ISSN-L;
# Must maximise matching of JIF. I recommend checking over
# May be necessary to do some manual work
Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sublow.replace("", np.nan) # New for 2025!?
# Occationally the Clarivate JIF scores may be like '<0.10'
JIF_scores_sublow["JIF Without Self Cites"] = JIF_scores_sublow["JIF Without Self Cites"].str.replace("<", "")
Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "")
JIF_scores_sublow["JCR Abbreviation"] = JIF_scores_sublow["JCR Abbreviation"].str.replace("-basel", "")

JIF_merge = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    on="ISSN",
)

JIF_mergebackori = pd.merge(
    Pubs_JIF_sublow,
    JIF_merge,
    on=["Title", "Year", "Labels", "Journal", "ISSN", "ISSN-L"],
)

JIF_mergebackori.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_ISSNL = pd.merge(
    JIF_mergebackori,
    JIF_scores_sublow,
    how="left",
    left_on="ISSN-L",
    right_on="ISSN",  # changed to eISSN from ISSN (new file from clarivate)
)

JIF_merge_ISSNL.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_ISSNL["JIF Without Self Cites_x"] = JIF_merge_ISSNL[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_ISSNL["JIF Without Self Cites_y"])

JIF_merge_ISSNL = JIF_merge_ISSNL.drop(
    [
        "eISSN_x",
        "eISSN_y",
        "Journal name_x",
        "JCR Abbreviation_x",
        "ISSN_y",
        "eISSN_y",
        "Journal name_y",
        "JCR Abbreviation_y",
        "JIF Without Self Cites_y",
    ],
    axis=1,
)

# now attempt to match on journal names
JIF_merge_abbnames = pd.merge(
    JIF_merge_ISSNL,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="JCR Abbreviation",
)

JIF_merge_abbnames["JIF Without Self Cites_x"] = JIF_merge_abbnames[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_abbnames["JIF Without Self Cites"])

JIF_merge_abbnames.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_abbnames = JIF_merge_abbnames.drop(
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ],
    axis=1,
)

# print(JIF_merge_abbnames.info())

# another ISSN match (ISSN with eISSN)
JIF_merge_weISSN = pd.merge(
    JIF_merge_abbnames,
    JIF_scores_sublow,
    how="left",
    left_on="ISSN_x",
    right_on="eISSN",
)

JIF_merge_weISSN.drop_duplicates(subset="Title", keep="first", inplace=True)

JIF_merge_weISSN["JIF Without Self Cites_x"] = JIF_merge_weISSN[
    "JIF Without Self Cites_x"
].fillna(JIF_merge_weISSN["JIF Without Self Cites"])

JIF_merge_weISSN = JIF_merge_weISSN.drop(
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ],
    axis=1,
)

# segment up the JIFs to groups
JIF_merge_weISSN.rename(
    columns={
        "ISSN_x": "ISSN",
        "JIF Without Self Cites_x": "JIF",
    },
    inplace=True,
)

JIF_merge_weISSN = JIF_merge_weISSN.replace("n/a", np.nan)
JIF_merge_weISSN = JIF_merge_weISSN.replace("", np.nan) # New for 2025!?

JIF_merge_weISSN["JIF"] = JIF_merge_weISSN["JIF"].fillna(-1)
JIF_merge_weISSN["JIF"] = pd.to_numeric(JIF_merge_weISSN["JIF"])
JIF_merge_weISSN.to_excel("Check_me_manual_" + pub_type + "_improve.xlsx")

JIF_merge_weISSN["JIFcat"] = pd.cut(
    JIF_merge_weISSN["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

# For debugging
unknowns = JIF_merge_weISSN[JIF_merge_weISSN["JIF"] < 0]
unknowns = unknowns.drop(["JIFcat", "JIF"], axis=1)
unknowns.to_excel("Unknown_" + pub_type + "_JIF.xlsx")

# Need to do a group by and check the sums work
JIF_sub = JIF_merge_weISSN[["Year", "Labels", "JIFcat"]]
JIF_data = JIF_sub.groupby(["Year", "JIFcat"], observed=False).size().reset_index()
JIF_data.columns = ["Year", "JIFcat", "Count"]

rows, columns = Pubs_JIF_sub.shape
print(f"Total of {rows} {pub_type} articles.")

# Use this to check that the sums are as expected given the original publication files
JIF_data.to_excel(pub_type + "-JIF-groups.xlsx")

JIF_sub_group_inf = JIF_data
