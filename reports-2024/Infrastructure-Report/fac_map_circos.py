#! /home/larsowe/venv/bin/python

import pandas as pd
import numpy as np

### FAC MAP
# to their labels in the publication database
fac_map_input = pd.read_excel(
    "Data/Reporting Units 2024.xlsx",  ## file from Lars OO
    sheet_name="Reporting units",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
fac_map_input["PDB label"] = fac_map_input["Publication Database Label"].str.replace(
    r"\(.*\)", "", regex=True
)
fac_map_input["PDB label"] = fac_map_input["PDB label"].apply(lambda x: x.removesuffix(" "))
fac_map_input = fac_map_input[["Unit", "PDB label", "Platform"]]
fac_map_input = fac_map_input.replace("", np.nan)
fac_map_input["PDB label"] = fac_map_input["PDB label"].fillna(fac_map_input["Unit"])
fac_map_input.rename(columns={"PDB label": "Label"}, inplace=True)
fac_map_input = fac_map_input.replace(
    "Support, Infrastructure and Training",
    "Bioinformatics Support, Infrastructure and Training",
)
# Replace string values with respect to the rules set out by OO
renaming = [
    ("Bioinformatics Support and Infrastructure", "Bioinformatics Support, Infrastructure and Training"),
    ("Bioinformatics Long-term Support WABI", "Bioinformatics Support, Infrastructure and Training"),
    ("Systems Biology", "Bioinformatics Support, Infrastructure and Training"),
    ("Bioinformatics Support for Computational Resources", ""), # Omit
    ("Bioinformatics Compute and Storage", ""),
    ("NGI Stockholm", "National Genomics Infrastructure"),
    ("NGI Uppsala", "National Genomics Infrastructure"),
    ("NGI Other", "National Genomics Infrastructure"),
    ("NGI Long read", "National Genomics Infrastructure"),
    ("NGI Proteomics", "National Genomics Infrastructure"),
    ("NGI Short read", "National Genomics Infrastructure"),
    ("NGI SNP genotyping", "National Genomics Infrastructure"),
    ("NGI Single cell", "National Genomics Infrastructure"),
    ("NGI Spatial omics", "National Genomics Infrastructure"),
    (" |", "|"),
    ("||||", "|"),
    ("|||", "|"),
    ("||", "|"),
]

fac_map = dict(zip(fac_map_input.Label, fac_map_input.Unit))
# print(fac_map)
unit_map = dict(zip(fac_map_input.Label, fac_map_input.Platform))
# print(unit_map)
df = pd.read_excel(
    "Data/infra_2024_comblab.xlsx",
    sheet_name="Publications",
    engine="openpyxl",
)
df = df[(df["Year"] == 2024)]
# extract unit labels from the excel
df["Labels"] = df["Labels"].str.replace(r"\(.*?\)", "", regex=True)
for ch in renaming:
    df["Labels"] = df["Labels"].apply(lambda x: x.replace(ch[0], ch[1]))

df["Labels"] = df["Labels"].apply(lambda x: x.removeprefix("|"))
df["Labels"] = df["Labels"].apply(lambda x: x.removesuffix("|"))
df["Labels"] = df["Labels"].apply(lambda x: x.removesuffix(" ")) # Useful?

df = df.replace(fac_map, regex=True)
# need to do some manual changes given that labels are combined
# This is because some labels were deleted when the publication label ends in ()
# and the puctuation is replaced with str.replace(r"\(.*\)", "", regex=True)
df.to_excel("test.xlsx")
