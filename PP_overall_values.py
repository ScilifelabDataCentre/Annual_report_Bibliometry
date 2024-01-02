# Want to calculate overall PP(top10) values for inclusion in text

import pandas as pd

# Load data

fellows_bib = pd.read_excel(
    "Data/2023/SciLifeLab-Fellows-20231208.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

infra_bib = pd.read_excel(
    "Data/2023/SciLifeLab-Infrastructure-20231208.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

affiliates_bib = pd.read_excel(
    "Data/2023/SciLifeLab-Affiliates-20231208.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

# Filter all dataframes to include only years of interest (for 2023 is 2018-21)

fell_scores = fellows_bib[
    (fellows_bib["Publication_year"] == 2018)
    | (fellows_bib["Publication_year"] == 2019)
    | (fellows_bib["Publication_year"] == 2020)
    | (fellows_bib["Publication_year"] == 2021)
]

inf_scores = infra_bib[
    (infra_bib["Publication_year"] == 2018)
    | (infra_bib["Publication_year"] == 2019)
    | (infra_bib["Publication_year"] == 2020)
    | (infra_bib["Publication_year"] == 2021)
]

aff_scores = affiliates_bib[
    (affiliates_bib["Publication_year"] == 2018)
    | (affiliates_bib["Publication_year"] == 2019)
    | (affiliates_bib["Publication_year"] == 2020)
    | (affiliates_bib["Publication_year"] == 2021)
]

# Filter for just the article types of interest

fell_filtered = fell_scores[
    (fell_scores["Doc_type_code_rev"] == "RV")
    | (fell_scores["Doc_type_code_rev"] == "AR")
    | (fell_scores["Doc_type_code_rev"] == "PP")
]

inf_filtered = inf_scores[
    (inf_scores["Doc_type_code_rev"] == "RV")
    | (inf_scores["Doc_type_code_rev"] == "AR")
    | (inf_scores["Doc_type_code_rev"] == "PP")
]

aff_filtered = aff_scores[
    (aff_scores["Doc_type_code_rev"] == "RV")
    | (aff_scores["Doc_type_code_rev"] == "AR")
    | (aff_scores["Doc_type_code_rev"] == "PP")
]
aff_filtered.drop(
    aff_filtered.index[aff_filtered["top10_scxwo"] == "None"], inplace=True
)
# Now get total PP values for the publications by each group

fell_filtered["top10_scxwo"] = fell_filtered["top10_scxwo"].astype(float)
avfells = fell_filtered["top10_scxwo"].mean()
print(avfells)  # 24.9 in 2023

inf_filtered["top10_scxwo"] = inf_filtered["top10_scxwo"].astype(float)
avinf = inf_filtered["top10_scxwo"].mean()
print(avinf)  # 20.4 in 2023

aff_filtered["top10_scxwo"] = aff_filtered["top10_scxwo"].astype(float)
avaffs = aff_filtered["top10_scxwo"].mean()
print(avaffs)  # 20.8 in 2023
