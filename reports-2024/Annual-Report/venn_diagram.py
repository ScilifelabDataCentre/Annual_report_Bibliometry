#! /usr/bin/python
from matplotlib_venn import venn2, venn2_unweighted, venn2_circles
import matplotlib.pyplot as plt
import pandas as pd

# This script makes a simple 2 group venn diagram
# Information on n and % of publications is calculated automatically.
# put data for 2 groups - infrastructure and affiliates

infra_bib = pd.read_excel(
    "Data/SciLifeLab-infrastructure-20241204.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)
affiliates_bib = pd.read_excel(
    "Data/SciLifeLab-affiliates-20241204.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

# IMPORTANT! KTH searches don't give 100% coverage
# as such, fewer publications in KTH extract than in extracts from the publication database
# for this reason, we must make manual modifications to ensure that the infrastructure numbers 'matchup'


# Filter to specific years

inf_bib = infra_bib[
    (infra_bib["Publication_year"] > 2018) & (infra_bib["Publication_year"] < 2025)
]

affs_bib = affiliates_bib[
    (affiliates_bib["Publication_year"] > 2018)
    & (affiliates_bib["Publication_year"] < 2025)
]

##### all above here needs to be run in all cases

# # Create sets of unique values for each dataset

# inf_set_DOI = set(inf_bib["UT"])
# aff_set_DOI = set(affs_bib["UT"])

# # Make a weighted Venn with initial values

# total = len(inf_set_DOI.union(aff_set_DOI))
# v = venn2(
#     subsets=[inf_set_DOI, aff_set_DOI],
#     # next line would set labels outside the circles
#     set_labels=(
#         "Användare av SciLifeLab:s\nforskningsinfrastruktur   ",
#         "SciLifeLab:s forskare",
#     ),
#     set_colors=("#A7C947", "#4C979F"),
#     subset_label_formatter=lambda x: f"{x}\n({(x/total):1.0%})",
#     alpha=1.0,
#     ax=plt.gca(),
# )
# # set outer labels
# for text in v.set_labels:
#     text.set_fontsize(12)
# # below recolours overlapping sections to be consistent with scilifelab visual ID
# v.get_patch_by_id("11").set_color("#a48fa9")
# plt.show()

############## RUN ABOVE THIS LINE FIRST

## Read values from plt.show() above
## Sets will only include publications that have a DOI, but not all do
## Need to correct the values so that they align with 'actual' totals
## Comment out the above and uncomment the below after manually adding corrected values

## Add the manual values here for infa and affiliates ONLY on paper (infraonly and affiliateonly) and collabs (inoverlap)


inoverlap = 1519
infraonly = 3060
affiliateonly = 3608

real_total = inoverlap + infraonly + affiliateonly
print(real_total)
# percover = (inoverlap / real_total) * 100
# percinf = (infraonly / real_total) * 100
# percaff = (affiliateonly / real_total) * 100

# print(percover)
# print(percinf)
# print(percaff)

percover = 19
percinf = 37
percaff = 44


v_use = venn2(
    subsets=(percinf, percaff, percover),
    # set labels outside of circles
    set_labels=(
        "Användare av SciLifeLab:s\nforskningsinfrastruktur   ",
        "SciLifeLab:s forskare",
    ),
    # f"{x}\n({(x/real_total):1.0%})" shows both the raw number and the percentage that represents.
    # In IAB report, we only included the number. Here, better to have percentages and labels below too.
    subset_label_formatter=lambda x: f"{x}\n({(x/real_total):1.0%})",
    set_colors=("#A7C947", "#4C979F"),
    alpha=1.0,
    ax=plt.gca(),
)
v_use.get_label_by_id("01").set_text("{}\n({}%)".format(affiliateonly, percaff))
v_use.get_label_by_id("10").set_text("{}\n({}%)".format(infraonly, percinf))
v_use.get_label_by_id("11").set_text("{}\n({}%)".format(inoverlap, percover))
# set outer labels
for text in v_use.set_labels:
    text.set_fontsize(13)
for text in v_use.subset_labels:
    text.set_fontsize(18)
# # below recolours overlapping sections to be consistent with scilifelab visual ID
v_use.get_patch_by_id("11").set_color("#a48fa9")
# plt.show()
# Uncomment the above to show the figure - useful for tests, the below saves the figure, but a blank image will be saved if plt.show() is not commented out
plt.savefig("Plots/Venn_annualreport_1dp.svg", dpi=300)
plt.savefig("Plots/Venn_annualreport_1dp.png", dpi=300)
