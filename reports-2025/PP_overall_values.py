#! /usr/bin/python

# Want to calculate overall PP(top10) values for inclusion in text

import pandas as pd

years_of_interest = range(2020, 2024) # for 2025 is 2020-23

# Load data
fellows_bib = pd.read_excel(
    "Data/SciLifeLab-Fellows-20251204.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

infra_bib = pd.read_excel(
    "Data/SciLifeLab-Infrastructure-20251204.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

affiliates_bib = pd.read_excel(
    "Data/SciLifeLab-Affiliates-20251204.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

# Filter all dataframes to include only years and article types of interest
fell_filtered = fellows_bib[fellows_bib["Publication_year"].isin(years_of_interest) &
                          fellows_bib["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]
inf_filtered = infra_bib[infra_bib["Publication_year"].isin(years_of_interest) &
                         infra_bib["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]
aff_filtered = affiliates_bib.copy()[affiliates_bib["Publication_year"].isin(years_of_interest) &
                              affiliates_bib["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]
aff_filtered.drop(aff_filtered.index[aff_filtered["top10_scxwo"] == "None"], inplace=True)

# Now get total PP values for the publications by each group
print(f"       Fellows: {fell_filtered["top10_scxwo"].astype(float).mean():.2%}")
print(f"Infrastructure: {inf_filtered["top10_scxwo"].astype(float).mean():.2%}")
print(f"    Affiliates: {aff_filtered["top10_scxwo"].astype(float).mean():.2%}")
