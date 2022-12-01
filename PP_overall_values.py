# Want to calculate overall PP(top10) values for inclusion in text

import pandas as pd

# Load data

fellows_bib = pd.read_excel(
    "Data/SciLifeLab-fellows-20211217.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

infra_bib = pd.read_excel(
    "Data/SciLifeLab-facilities-20211217.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

affiliates_bib = pd.read_excel(
    "Data/SciLifeLab-byaddress-20211217.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

# Filter all dataframes to include only years of interest (for 2021 is 2016-9)

fell_201619 = fellows_bib[
    (fellows_bib["Publication_year"] == 2016)
    | (fellows_bib["Publication_year"] == 2017)
    | (fellows_bib["Publication_year"] == 2018)
    | (fellows_bib["Publication_year"] == 2019)
]

inf_201619 = infra_bib[
    (infra_bib["Publication_year"] == 2016)
    | (infra_bib["Publication_year"] == 2017)
    | (infra_bib["Publication_year"] == 2018)
    | (infra_bib["Publication_year"] == 2019)
]

aff_201619 = affiliates_bib[
    (affiliates_bib["Publication_year"] == 2016)
    | (affiliates_bib["Publication_year"] == 2017)
    | (affiliates_bib["Publication_year"] == 2018)
    | (affiliates_bib["Publication_year"] == 2019)
]

# Filter for just the article types of interest

fell_filtered = fell_201619[
    (fell_201619["Doc_type_code_rev"] == "RV")
    | (fell_201619["Doc_type_code_rev"] == "AR")
    | (fell_201619["Doc_type_code_rev"] == "PP")
]

inf_filtered = inf_201619[
    (inf_201619["Doc_type_code_rev"] == "RV")
    | (inf_201619["Doc_type_code_rev"] == "AR")
    | (inf_201619["Doc_type_code_rev"] == "PP")
]

aff_filtered = aff_201619[
    (aff_201619["Doc_type_code_rev"] == "RV")
    | (aff_201619["Doc_type_code_rev"] == "AR")
    | (aff_201619["Doc_type_code_rev"] == "PP")
]
aff_filtered.drop(
    aff_filtered.index[aff_filtered["top10_scxwo"] == "None"], inplace=True
)
# Now get total PP values for the publications by each group

fell_filtered["top10_scxwo"] = fell_filtered["top10_scxwo"].astype(float)
avfells = fell_filtered["top10_scxwo"].mean()
print(avfells)

inf_filtered["top10_scxwo"] = inf_filtered["top10_scxwo"].astype(float)
avinf = inf_filtered["top10_scxwo"].mean()
print(avinf)

aff_filtered["top10_scxwo"] = aff_filtered["top10_scxwo"].astype(float)
avaffs = aff_filtered["top10_scxwo"].mean()
print(avaffs)
