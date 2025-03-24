#!/usr/bin/python3

import pandas as pd

# get the data
infra = pd.read_excel(
    "Data/infra_2024_comblab.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# filter as needed (just latest year, only need a couple of columns)
infra_collabs = infra[(infra["Year"] == 2024)]  # set year here!!
infra_collabs = infra_collabs[["DOI", "Labels"]]

# Replace string values with respect to the rules set out by OO
renaming = [
    ("Bioinformatics Support and Infrastructure", "Bioinformatics Support, Infrastructure and Training"),
    ("Bioinformatics Long-term Support WABI", "Bioinformatics Support, Infrastructure and Training"),
    ("Systems Biology", "Bioinformatics Support, Infrastructure and Training"),
    ("Bioinformatics Support for Computational Resources", ""), # Omit
    ("Bioinformatics Compute and Storage", ""),
    ("NGI Stockholm (Genomics Applications)", "National Genomics Infrastructure"),
    ("NGI Stockholm (Genomics Production)", "National Genomics Infrastructure"),
    ("NGI Uppsala (SNP&SEQ Technology Platform)", "National Genomics Infrastructure"),
    ("NGI Uppsala (Uppsala Genome Center)", "National Genomics Infrastructure"),
    ("NGI Other", "National Genomics Infrastructure"),
    ("NGI Long read", "National Genomics Infrastructure"),
    ("NGI Proteomics", "National Genomics Infrastructure"),
    ("NGI Short read", "National Genomics Infrastructure"),
    ("NGI SNP genotyping", "National Genomics Infrastructure"),
    ("NGI Single cell", "National Genomics Infrastructure"),
    ("NGI Spatial omics", "National Genomics Infrastructure"),
    ("|||||", "|"), # Superfluous?
    ("||||", "|"),
    ("|||", "|"),
    ("||", "|"),
]

for ch in renaming:
    infra_collabs["Labels"] = infra_collabs["Labels"].apply(lambda x: x.replace(ch[0], ch[1]))

# Count was incorrect when NGI at front because it often started with "|"" after others deleted
# corrected this by conditionally replacing based on start value
infra_collabs["Labels"] = infra_collabs["Labels"].apply(lambda x: x.removeprefix("|"))
infra_collabs["Labels"] = infra_collabs["Labels"].apply(lambda x: x.removesuffix("|"))

# split values to different columns, so there is one unit per column
new_bits = infra_collabs["Labels"].str.split("|", expand=True)

new_bits = new_bits.apply(
    lambda row: pd.Series(row).drop_duplicates(keep="first"), axis="columns"
)

# Now count the number of 'non empty columns' in each row
# This will how how many units worked on a publication
new_bits["No_units"] = new_bits.count(axis=1)

# This file is a test file you can use to check everything looks correct
new_bits = new_bits.sort_values(by=['No_units'], ascending=False)
new_bits.to_excel("TESTCHECK_collaborations.xlsx")

# Output percentage, so that it can be communicated to OO
# If there are some errors in the automatic counts, manual adjustments may be necessary
no_units = new_bits["No_units"].count()
collab_units = new_bits["No_units"].map(lambda x: x > 1).sum()
print(no_units, "articles with more than one label, out of", collab_units, ", or a collaboration of",
      round((collab_units / no_units) * 100, 2), "percent.")
