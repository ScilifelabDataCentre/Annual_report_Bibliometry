# Preparation of the data related to affiliated researchers for JIF plot
# Based on data from KTH

import pandas as pd

# information from KTH

Pubs_JIF_raw = pd.read_excel(
    "Data/SciLifeLab-byaddress-20211217.xlsx",
    sheet_name="publ_info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# information for JIF scores
JIF_scores_raw = pd.read_excel(
    "Data/JIF_scores_2021.xlsx",
    sheet_name="Sheet 1 - JournalHomeGrid",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter for the appropriate time frame

Pubs_JIF_raw = Pubs_JIF_raw[
    (Pubs_JIF_raw["Publication_year"] > 2015)
    & (Pubs_JIF_raw["Publication_year"] < 2022)
]

# Need to join the two above files and align JIF with ISSN/ISSN-L
# simpler to work with only columns of interest

Pubs_JIF_sub = Pubs_JIF_raw[
    [
        "UT",
        "Title",
        "Publication_year",
        "Journal",
    ]
]

JIF_scores_sub = JIF_scores_raw[
    [
        "Full Journal Title",
        "JCR Abbreviated Title",
        "Impact Factor without Journal Self Cites",
    ]
]

# Must maximise matching of JIF. I recommend checking over
# May be necessary to do some manual work

Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "", regex=True)
JIF_scores_sublow["JCR Abbreviated Title"] = JIF_scores_sublow[
    "JCR Abbreviated Title"
].str.replace("-basel", "", regex=True)


JIF_merge_abbnames = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="JCR Abbreviated Title",
)


JIF_merge_abbnames.drop_duplicates(subset="UT", keep="first", inplace=True)

JIF_merge_abbnames = JIF_merge_abbnames.drop(
    [
        "Full Journal Title",
        "JCR Abbreviated Title",
    ],
    axis=1,
)

JIF_merge_fullnames = pd.merge(
    JIF_merge_abbnames,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="Full Journal Title",
)

JIF_merge_fullnames.drop_duplicates(subset="UT", keep="first", inplace=True)


JIF_merge_fullnames["Impact Factor without Journal Self Cites_y"] = JIF_merge_fullnames[
    "Impact Factor without Journal Self Cites_y"
].fillna(JIF_merge_fullnames["Impact Factor without Journal Self Cites_x"])

JIF_merge_fullnames = JIF_merge_fullnames.drop(
    [
        "Full Journal Title",
        "JCR Abbreviated Title",
        "Impact Factor without Journal Self Cites_x",
    ],
    axis=1,
)

## below prints out a file that can be checked to determine whether
## manual work may increase the number of matches

JIF_merge_fullnames.rename(
    columns={
        "Impact Factor without Journal Self Cites_y": "JIF",
        "Publication_year": "Year",
    },
    inplace=True,
)

JIF_merge_fullnames.to_excel("Check_me_manual_improve_aff.xlsx")


JIF_merge_fullnames["JIF"] = JIF_merge_fullnames["JIF"].fillna(-1)

JIF_merge_fullnames["JIF"] = pd.to_numeric(JIF_merge_fullnames["JIF"])
JIF_merge_fullnames["JIFcat"] = pd.cut(
    JIF_merge_fullnames["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

# Need to do a group by and check the sums work

JIF_sub = JIF_merge_fullnames[["Year", "JIFcat"]]

JIF_sub_group_aff = JIF_sub.groupby(["Year", "JIFcat"]).size().reset_index()

JIF_sub_group_aff.columns = ["Year", "JIFcat", "Count"]


# Use this to check that the sums are as expected given the original publication files
JIF_sub_group_aff.to_excel("affiliates_JIF_groups.xlsx")
