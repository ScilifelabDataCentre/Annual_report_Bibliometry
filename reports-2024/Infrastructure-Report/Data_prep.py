#! /home/larsowe/venv/bin/python

import pandas as pd
import numpy as np

### FAC MAP
# to their labels in the publication database
fac_map_input = pd.read_excel(
    "Data/Reporting Units 2024.xlsx",
    sheet_name="Reporting units",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
fac_map_input["PDB label"] = fac_map_input["Publication Database Label"].str.replace(
    r"\(.*\)", "", regex=True
)
# You need the above to make sure you don't get spaces in file names
fac_map_input = fac_map_input[["Unit", "PDB label"]]
fac_map_input = fac_map_input.replace("", np.nan)
fac_map_input["PDB label"] = fac_map_input["PDB label"].fillna(fac_map_input["Unit"])
fac_map_input.rename(columns={"PDB label": "Label"}, inplace=True)
fac_map = dict(zip(fac_map_input.Label, fac_map_input.Unit))

### AFFILIATES
# Years of interest in 2024 - 2022-2024
# We have 3 data files from OO for this (one for each year)

aff_2022_raw = pd.read_excel(
    "Data/Users 2022.xlsx",
    sheet_name="Users 2022",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_2023_raw = pd.read_excel(
    "Data/Users 2023.xlsx",
    sheet_name="Users 2023",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

aff_2024_raw = pd.read_excel(
    "Data/Users 2024.xlsx",
    sheet_name="Users 2024",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
# For users 2021 & 2022, we need to combine 'Advanced Fish Technologies' and 'Spatial Proteomics'
aff_2022_raw["Unit"] = aff_2022_raw["Unit"].replace("Advanced FISH Technologies", "Spatial Proteomics",)

# Want to get counts of how many of each individual affiliation for each unit
affiliates_data_2022 = (
    aff_2022_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)
affiliates_data_2023 = (
    aff_2023_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)
affiliates_data_2024 = (
    aff_2024_raw.groupby(["Unit", "PI affiliation"]).size().reset_index()
)

affiliates_data_2022.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_2023.columns = ["Unit", "PI_aff", "Count"]
affiliates_data_2024.columns = ["Unit", "PI_aff", "Count"]

affiliates_data_2022.insert(loc=2, column="Year", value="2022")
affiliates_data_2023.insert(loc=2, column="Year", value="2023")
affiliates_data_2024.insert(loc=2, column="Year", value="2024")

aff_comb = pd.concat([affiliates_data_2022, affiliates_data_2023, affiliates_data_2024])
# print(aff_comb)
# aff_comb.to_excel("test_affiliates_users_2024.xlsx")
# Now need to replace all of the affiliation names with a shortened version

aff_map_abbr = {
    "Chalmers University of Technology": "Chalmers",
    "KTH Royal Institute of Technology": "KTH",
    "Swedish University of Agricultural Sciences": "SLU",
    "Karolinska Institutet": "KI",
    "Linköping University": "LiU",
    "Lund University": "LU",
    "Naturhistoriska Riksmuséet": "NRM",
    "Stockholm University": "SU",
    "Umeå University": "UmU",
    "University of Gothenburg": "GU",
    "Uppsala University": "UU",
    "Örebro University": "ÖU",
    "International University": "Int Univ",
    "Other Swedish University": "Other Swe Univ",
    "Other Swedish organization": "Other Swe Org",
    "Other international organization": "Other Int Org",
    "Industry ": "Industry",
    "Industry": "Industry",
    "Healthcare": "Healthcare",
}

affiliate_data = aff_comb.replace(aff_map_abbr, regex=True)
## #
affiliate_data.to_excel("test_aff_user_data_2024.xlsx")
# print(affiliate_data.PI_aff.unique())


### UNIT DATA ## changes to unit from facility, will change throughout the script.
# Single data contains all basic data for unit
# Read in to pdf almost directly
# rename columns for clarity
Unit_data = pd.read_excel(
    "Data/Single Data 2024.xlsx",
    sheet_name="Single Data",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# below, mostly changed year in header
Unit_data.rename(
    columns={
        "Head of Unit": "HOU",  # updated from Head of facility (HOF)
        "Co-PD (DDD)": "CDU",  # Platform Co-Director
        "Platform Scientific Director": "PSD",  # updated from Facility director (FD) now needs to come AFTER head (was before previously)
        "SciLifeLab unit since": "SLL_since",
        "Host university": "H_uni",
        "FTEs financed by SciLifeLab": "SLL_FTEs",
        "Funding 2024 SciLifeLab (kSEK)": "Amount (kSEK)",
        "Resource allocation 2024 Acadmia (national)": "RA_nat",
        "Resource allocation 2024 Acadmia (international)": "RA_int",
        "Resource allocation 2024 Internal tech. dev.": "RA_tech",
        "Resource allocation 2024 Industry": "RA_Ind",
        "Resource allocation 2024 Healthcare": "RA_Health",
        "Resource allocation 2024 Other gov. agencies": "RA_ogov",
        "User Fees 2024 Total (kSEK)": "UF_Tot",
        "Cost reagents": "UF_reag",
        "Cost instrument": "UF_instr",
        "Cost salaries": "UF_sal",
        "Cost rents": "UF_rent",
        "Cost other": "UF_other",
        "SciLifeLab Instrument Funding 2024": "SLL_Instr_fund",  # This is new for 2021, need to integrate in
        "User fees by sector 2024 Academia (national)": "UF_sect_nat",
        "User fees by sector 2024 Academia (international)": "UF_sect_int",
        "User fees by sector 2024 Industry": "UF_sect_ind",
        "User fees by sector 2024 Healthcare": "UF_sect_health",
        "User fees by sector 2024 Other gov. agencies": "UF_sect_othgov",
    },
    inplace=True,
)

### FUNDING
# This involves data from 'other funding' and 'single data'
# both files provided by OO
# Need to add SLL funding to other funding data and get a total

other_funding = pd.read_excel(
    "Data/Other Funding 2024.xlsx",
    sheet_name="Other Funding 2024",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Some funding info also included in the unit data
# extract SLL funding data from single(unit) data

SLL_funding = Unit_data[["Unit", "Platform", "Amount (kSEK)"]]
SLL_funding.insert(loc=2, column="Financier", value="SciLifeLab")

# Need to add instrument funding for 2022 statistics

instru_funding = Unit_data[["Unit", "Platform", "SLL_Instr_fund"]]
instru_funding.insert(loc=2, column="Financier", value="SciLifeLab Instrument")
instru_funding = instru_funding[instru_funding.SLL_Instr_fund != 0]
instru_funding.rename(
    columns={
        "SLL_Instr_fund": "Amount (kSEK)",
    },
    inplace=True,
)
# This bit added, because some values in the instrument funding were blank
instru_funding["Amount (kSEK)"] = instru_funding["Amount (kSEK)"].replace(
    "", np.nan, regex=True
)
instru_funding = instru_funding.dropna()

# need to drop 'platform no' column from other data before bringing these datasets together

other_funding = other_funding[["Unit", "Platform", "Financier", "Amount (kSEK)"]]

# now concatenate this with other funding
# also calculate total funding
Funding_comb = pd.concat([SLL_funding, instru_funding, other_funding])
## #Funding_comb["Amount (kSEK)"] = pd.to_numeric(Funding_comb["Amount (kSEK)"])
tot_fund = Funding_comb.groupby(["Unit"],group_keys=False).sum().reset_index()
tot_fund = tot_fund[["Unit", "Platform", "Amount (kSEK)"]]
tot_fund.insert(loc=2, column="Financier", value="Total")
Funding = pd.concat([Funding_comb, tot_fund])
## #print(Funding)

###PUBLICATIONS!

# Used in the two graphs for one-pagers
# Need to use this data in 2 ways:
# (1) Make a barplot of publications by category
# (2) Make the barplot with JIF scores
# whilst the rest of the data comes from OO,
# This data is taken from:
# (1) publications database
# (2) publications db and JIF scores

# import raw publications data

# Focus on data for (1) - extract individual labels for records from pub db

Pubs_cat_raw = pd.read_excel(
    "Data/infra_2024_singlelab.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# # Need to get data for (fac) and groupby

pub_sub = Pubs_cat_raw[["Year", "Labels", "Qualifiers"]]
pub_sub = pub_sub.replace(r"^\s*$", "No category", regex=True)
pub_sub["Qualifiers"] = pub_sub["Qualifiers"].astype("category")
# pub_sub.to_excel("quick_initial_check.xlsx")

# # Clinical Biomarkers and PLA and Single Cell Proteomics merged to Affinity Proteomics Uppsala.
# # Manually deleted 'duplicates' for labels in file - so only one of the above labels for any paper
# pub_sub = pub_sub.replace(
#     "Clinical Biomarkers", "Affinity Proteomics Uppsala", regex=True
# )

# pub_sub = pub_sub.replace(
#     "PLA and Single Cell Proteomics", "Affinity Proteomics Uppsala", regex=True
# )

pub_sub = pub_sub[pub_sub["Year"] >= 2022]

pub_cat_group = pub_sub.groupby(["Year", "Labels", "Qualifiers"], observed=False).size().reset_index()

pub_cat_group["Labels"] = pub_cat_group["Labels"].str.replace(r"\(.*\)", "", regex=True)

pub_cat_data = pub_cat_group.replace(fac_map, regex=True)

# # # in 2021 (onwards), don't need the previous duplication for the two mass cytometry centres

# Need to name the column produced by groupby
pub_cat_data.columns = ["Year", "Unit", "Qualifiers", "Count"]

# Now for data for (2)
# This time work with pub data with labels combined
# i.e. one record per publication

Pubs_JIF_raw = pd.read_excel(
    "Data/infra_2024_comblab.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

JIF_scores_raw = pd.read_excel(
    "Data/JCR-2024-affadded.xlsx",
    sheet_name="Info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Store JIF score in different dictionaries

issn_jif, eissn_jif, journal_jif = ({}, {}, {})

for index, row in JIF_scores_raw.iterrows():
    jif_score = row["JIF Without Self Cites"]
    # store JIF based on ISSN
    issn = row["ISSN"].replace("N/A", "")
    if issn and issn not in issn_jif.keys():
        issn_jif[issn] = jif_score
    # store JIF based on eISSN
    eissn = row["eISSN"].replace("N/A", "")
    if eissn and eissn not in eissn_jif.keys():
        eissn_jif[eissn] = jif_score
    # store JIF based on Journal Abbreviation
    ## #    journal = row["JCR Abbreviation"].lower().replace("-basel", "")
    journal = row["JCR Abbreviation"].lower()
    if journal and journal not in journal_jif.keys():
        journal_jif[journal] = jif_score
    journal = row["Journal name"].lower()
    if journal and journal not in journal_jif.keys():
        journal_jif[journal] = jif_score

pub_and_jif = [] 

for index, row in Pubs_JIF_raw.iterrows():
    title = row["Title"].lower()
    issn = row["ISSN"].replace("N/A", "")
    issn_l = row["ISSN-L"].replace("N/A", "")
    journal = row["Journal"].lower().replace(".", "")
    jif_score = issn_jif.get(issn) or eissn_jif.get(issn) or issn_jif.get(issn_l) or journal_jif.get(journal) or -1
    pub_and_jif.append([title, jif_score])

pub_with_jif = pd.DataFrame(pub_and_jif, columns=["Title", "JIF"])
pwj = pd.DataFrame(pub_and_jif)

Pubs_cat_raw["Title"] = Pubs_cat_raw["Title"].str.lower()

match_JIF_seplabs = pd.merge(
    Pubs_cat_raw,
    pub_with_jif,
    how="left",
    on="Title",
)

match_JIF_seplabs["JIF"] = match_JIF_seplabs["JIF"].fillna(-1)
match_JIF_seplabs["JIF"] = pd.to_numeric(match_JIF_seplabs["JIF"])
match_JIF_seplabs["JIFcat"] = pd.cut(
    match_JIF_seplabs["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

# # replace facility labels

match_JIF_seplabs["Labels"] = match_JIF_seplabs["Labels"].str.replace(
    r"\(.*\)", "", regex=True
)

JIF_match_basic = match_JIF_seplabs.replace(fac_map, regex=True)
JIF_match_basic.to_excel("match.xlsx")

# Need to do a group by and check the sums work! (and align with above pub numbers)

JIF_data = JIF_match_basic[["Year", "Labels", "JIFcat", "Qualifiers"]]
# need to drop out the technology development papers
# This gives: A value is trying to be set on a copy of a slice from a DataFrame
# and has to be rewritten prior to Panda 3
#JIF_data.drop(
#    JIF_data[JIF_data["Qualifiers"] == "Technology development"].index, inplace=True
#)
JIF_data = JIF_data[JIF_data["Qualifiers"] != "Technology development"]

JIF_data = JIF_data.groupby(["Year", "Labels", "JIFcat"], observed=False).size().reset_index()
JIF_data.columns = ["Year", "Unit", "JIFcat", "Count"]
JIF_data = JIF_data[JIF_data["Year"] >= 2022]

# # # As a check, can compare publications data divided by category and JIF for each unit
# # # The total numbers for each unit and for each year should align.
JIF_data.to_excel("Check_JIFdata.xlsx")
#pub_cat_data.to_excel("Check_pubcatdata.xlsx")

# Tech_dev = pub_cat_data[(pub_cat_data["Qualifiers"] == "Technology development")]
# print(Tech_dev.Count)
