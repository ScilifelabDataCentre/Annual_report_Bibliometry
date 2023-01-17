# Preparation of the data related to infrastructure for JIF plot
# Based on data from infrastructure publications database (filtered for active facilities each year)

import pandas as pd
import numpy as np

# information from publication database

Pubs_JIF_raw = pd.read_excel(
    "Data/infrastructure_pd_extract_22.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# information for JIF scores

JIF_scores_raw = pd.read_excel(
    "Data/JCR_JournalResults_12_2022_byISSN_221208.xlsx",
    sheet_name="JCR",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter for the appropriate time frame

Pubs_JIF_raw = Pubs_JIF_raw[
    (Pubs_JIF_raw["Year"] > 2016) & (Pubs_JIF_raw["Year"] < 2023)
]

# Need to join the two above files and align JIF with ISSN/ISSN-L
# simpler to work with only columns of interest

Pubs_JIF_sub = Pubs_JIF_raw[
    [
        "Title",
        "Year",
        "Labels",
        "Journal",
        "ISSN",
        "ISSN-L",
    ]
]

JIF_scores_sub = JIF_scores_raw[
    [
        "ISSN",
        "eISSN",
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ]
]

# Must maximise matching of JIF. I recommend checking over
# May be necessary to do some manual work

Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "", regex=True)
JIF_scores_sublow["JCR Abbreviation"] = JIF_scores_sublow[
    "JCR Abbreviation"
].str.replace("-basel", "", regex=True)

JIF_merge = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    on="ISSN",
)

JIF_mergebackori = pd.merge(
    Pubs_JIF_sublow,
    JIF_merge,
    on=[
        "Title",
        "Year",
        "Labels",
        "Journal",
        "ISSN",
        "ISSN-L",
    ],
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

# JIF_merge_abbnames.to_excel("infra_check_manual.xlsx")

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

# JIF_merge_weISSN.to_excel("infra_check_manual_update.xlsx")

# # # segment up the JIFs to groups

JIF_merge_weISSN.rename(
    columns={
        "ISSN_x": "ISSN",
        "JIF Without Self Cites_x": "JIF",
    },
    inplace=True,
)

JIF_merge_weISSN = JIF_merge_weISSN.replace("n/a", np.nan)

JIF_merge_weISSN["JIF"] = JIF_merge_weISSN["JIF"].fillna(-1)

JIF_merge_weISSN["JIF"] = pd.to_numeric(JIF_merge_weISSN["JIF"])
JIF_merge_weISSN["JIFcat"] = pd.cut(
    JIF_merge_weISSN["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)
JIF_merge_weISSN.to_excel("JIF_TESTING.xlsx")
# # Need to do a group by and check the sums work

JIF_sub = JIF_merge_weISSN[["Year", "Labels", "JIFcat"]]


JIF_sub_group_inf = JIF_sub.groupby(["Year", "JIFcat"]).size().reset_index()

JIF_sub_group_inf.columns = ["Year", "JIFcat", "Count"]


# # Use this to check that the sums are as expected given the original publication files
# JIF_sub_group_inf.to_excel("infra_JIF_groups_1.xlsx")
