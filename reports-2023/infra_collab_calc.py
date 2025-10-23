import pandas as pd

# get the data
infra = pd.read_excel(
    "Data/2023/SciLifeLab_publications_Infrastucture_2023.xlsx",
    sheet_name="Publications 20231204-1239",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# filter as needed (just latest year, only need a couple of columns)

infra_collabs = infra[(infra["Year"] == 2023)]  # set year here!!
infra_collabs = infra_collabs[["DOI", "Labels"]]

# Replace string values with respect to the rules set out by OO

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("Genome Engineering Zebrafish", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("National Genomics Infrastructure", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("|National Genomics Infrastructure", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("|Bioinformatics Compute and Storage", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("Bioinformatics Compute and Storage|", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("Bioinformatics Compute and Storage", "")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "Bioinformatics Long-term Support WABI",
        "Bioinformatics Support, Infrastructure and Training",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "Systems Biology", "Bioinformatics Support, Infrastructure and Training"
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "Bioinformatics Support and Infrastructure",
        "Bioinformatics Support, Infrastructure and Training",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Stockholm (Genomics Applications)",
        "NGI Short-read and Genotyping",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Stockholm (Genomics Production)",
        "NGI Short-read and Genotyping",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Uppsala (SNP&SEQ Technology Platform)",
        "NGI Short-read and Genotyping",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Long read",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Uppsala (Uppsala Genome Center)",
        "NGI Long-read",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Other",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Proteomics",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Short read",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI SNP genotyping",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Single cell",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "NGI Spatial omics",
        "",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "Affinity Proteomics Stockholm",
        "Affinity Proteomics",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace(
        "Affinity Proteomics Uppsala",
        "Affinity Proteomics",
    )
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: x.replace("||||", "|")
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(lambda x: x.replace("|||", "|"))

infra_collabs["Labels"] = infra_collabs["Labels"].apply(lambda x: x.replace("||", "|"))

# Count was incorrect when NGI at front because it often started with "|"" after others deleted
# corrected this by conditionally replacing based on start value

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"Bioinformatics Compute and Storage"
    if x.startswith("|Bioinformatics Compute and Storage")
    else x
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"National Genomics Infrastructure"
    if x.startswith("|National Genomics Infrastructure")
    else x
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"NGI Long-read" if x.startswith("|NGI Long-read") else x
)


infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"NGI Short-read and Genotyping"
    if x.startswith("NGI Short-read and Genotyping|")
    else x
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"NGI Short-read and Genotyping|NGI Long-read"
    if x.startswith("|NGI Short-read and Genotyping|NGI Long-read")
    else x
)

infra_collabs["Labels"] = infra_collabs["Labels"].apply(
    lambda x: f"NGI Short-read and Genotyping"
    if x.startswith("|NGI Short-read and Genotyping")
    else x
)

# split values to different columns, so there is one unit per column

new_bits = infra_collabs["Labels"].str.split("|", expand=True)

new_bits = new_bits.apply(
    lambda row: pd.Series(row).drop_duplicates(keep="first"), axis="columns"
)

# Now count the number of 'non empty columns' in each row
# This will how how many units worked on a publication

new_bits["No_units"] = new_bits.count(axis=1)

# This file is a test file you can use to check everything looks correct

# new_bits.to_excel("TESTCHECK_collaborations.xlsx")

# Need to work out a percantage to use in the report

Perc_collab = (
    (new_bits["No_units"].map(lambda x: x > 1).sum()) / (new_bits["No_units"].count())
) * 100

# Output percentage, so that it can be communicated to OO

print(Perc_collab)

# noticed that there are some errors in the automatic counts, so need to make manual adjustments
print((new_bits["No_units"].map(lambda x: x > 1).sum()) + 7)
print(new_bits["No_units"].count())

Perc_collab = (
    (new_bits["No_units"].map(lambda x: x > 1).sum() + 7)
    / (new_bits["No_units"].count())
) * 100

# Output percentage, so that it can be communicated to OO

print(Perc_collab)
# should be 10.14
