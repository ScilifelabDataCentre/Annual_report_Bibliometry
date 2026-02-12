#! /usr/bin/python

# Preparation of the data related to affiliated researchers for JIF plot
# Based on data from KTH

import pandas as pd
import numpy as np

years_of_interest = range(2020, 2026) # for 2025 is 2020-25
pub_type = "Affiliates"

# information from KTH
Pubs_JIF_raw = pd.read_excel(
    "Data/SciLifeLab-Affiliates-20251204.xlsx",
    sheet_name="publ_info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["UT", "Title", "Publication_year", "Journal"]
)

# information for JIF scores
# easier to work with only columns of interest.
JIF_scores_sub = pd.read_excel(
    "Data/JCR-2025.xlsx",
    sheet_name="JIF2024",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["Journal name", "JCR Abbreviation", "JIF Without Self Cites"]
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
Pubs_JIF_sub = Pubs_JIF_raw[Pubs_JIF_raw["Publication_year"].isin(years_of_interest)]
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

JIF_merge_abbnames = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="JCR Abbreviation",
)

JIF_merge_abbnames.drop_duplicates(subset="UT", keep="first", inplace=True)

JIF_merge_abbnames = JIF_merge_abbnames.drop(
    ["Journal name", "JCR Abbreviation"],
    axis=1,
)

JIF_merge_fullnames = pd.merge(
    JIF_merge_abbnames,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="Journal name",
)

JIF_merge_fullnames.drop_duplicates(subset="UT", keep="first", inplace=True)
JIF_merge_fullnames["JIF Without Self Cites_y"] = JIF_merge_fullnames[
    "JIF Without Self Cites_y"
].fillna(JIF_merge_fullnames["JIF Without Self Cites_x"])
JIF_merge_fullnames = JIF_merge_fullnames.drop(
    ["Journal name", "JCR Abbreviation", "JIF Without Self Cites_x"],
    axis=1,
)

# below prints out a file that can be checked to determine whether
# manual work may increase the number of matches
JIF_merge_fullnames.rename(
    columns={
        "JIF Without Self Cites_y": "JIF",
        "Publication_year": "Year",
    },
    inplace=True,
)

JIF_merge_fullnames.to_excel("Check_me_manual_improve_aff.xlsx")

JIF_merge_fullnames = JIF_merge_fullnames.replace("n/a", np.nan)
JIF_merge_fullnames["JIF"] = JIF_merge_fullnames["JIF"].fillna(-1)

JIF_merge_fullnames["JIF"] = pd.to_numeric(JIF_merge_fullnames["JIF"])

JIF_merge_fullnames["JIFcat"] = pd.cut(
    JIF_merge_fullnames["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

# For debugging
unknowns = JIF_merge_fullnames[JIF_merge_fullnames["JIF"] < 0]
unknowns = unknowns.drop(["JIFcat", "JIF"], axis=1)
unknowns.to_excel("Unknown_" + pub_type + "_JIF.xlsx")

# Need to do a group by and check the sums work
JIF_sub = JIF_merge_fullnames[["Year", "JIFcat"]]
JIF_data = JIF_sub.groupby(["Year", "JIFcat"], observed=False).size().reset_index()
JIF_data.columns = ["Year", "JIFcat", "Count"]

rows, columns = Pubs_JIF_sub.shape
print(f"Total of {rows} {pub_type} articles.")

# Use this to check that the sums are as expected given the original publication files
JIF_data.to_excel(pub_type + "-JIF-groups.xlsx")

JIF_sub_group_aff = JIF_data
