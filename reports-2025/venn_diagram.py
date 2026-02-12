#! /usr/bin/python

from matplotlib_venn import venn2, venn2_unweighted, venn2_circles
import matplotlib.pyplot as plt
import pandas as pd

years_of_interest = range(2020, 2026) # for 2025 is 2020-25

# So you both got the same intersect number and that's great. We match
# just the affiliates (we don't consider the fellows file here) and
# the infrastructure. For affiliates, the KTH-B file is the correct
# one to use to get all of the affiliates (intersect plus 'only
# affiliates'). For the infrastructure, we use the KTH-B file to get
# the intersect (nice, easy matching), and use the infrastructure file
# that we get from our publications database. This is because, for
# infrastructure, we know that there are more and use those numbers
# throughout the rest of the report, so it would look odd if we only
# included the files from KTH-B here.
#
# The logic for matching on the KTH-B files is this - even though we
# have more files in our publications database for infrastructure,
# they did not occur in the KTH-B database (BIBMET), so it would not
# be possible to match them anyway as they could not appear in the
# affiliates file.
#
# I agree that the fellows and affiliates being mismatched isn't ideal
# (as fellows is supposed to be a subset of affiliates). I have long
# advocated for this to be cleaned up a bit. However, for now at
# least, it's seen as important that we take the fellows 'at their
# word' for what they reported, because that's likely to be more
# complete. They SHOULD acknowledge their affiliation to SciLifeLab,
# so everything SHOULD appear in the affiliates file too. This is
# never perfect, though. In general, understanding how accurate we are
# with regard to affiliates is basically impossible, because we do not
# have a list of the researchers affiliated with SciLifeLab (as in,
# no-one does).

# This script makes a simple 2 group venn diagram
# Information on n and % of publications is calculated automatically.
# put data for 2 groups - infrastructure and affiliates

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
Pubs_JIF = pd.read_excel(
    "Data/KTH Infrastructure Extraction 2025-12-22.xlsx",
    sheet_name="Publications",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

preprint_journals = [
    "biorxiv",
    "chemrxiv",
    "lakartidningen",
    "medrxiv",
    "optica open",
    "osf",
    "research square",
    "res sq",
    "ssrn journal",
    "ssrn", # temp
]

# IMPORTANT! KTH searches don't give 100% coverage
# as such, fewer publications in KTH extract than in extracts from the publication database
# for this reason, we must make adjust to ensure that the infrastructure numbers match up.

# Filter to specific years
inf_bib = infra_bib[infra_bib["Publication_year"].isin(years_of_interest)]
affs_bib = affiliates_bib[affiliates_bib["Publication_year"].isin(years_of_interest)]
Pubs_JIF = Pubs_JIF[Pubs_JIF["Year"].isin(years_of_interest)]
Pubs_JIF = Pubs_JIF[-Pubs_JIF["Journal"].str.lower().isin(preprint_journals)]
actual_infra_number = len(Pubs_JIF)

# Create sets of unique values for each dataset
inf_set_DOI = set(inf_bib["UT"])
aff_set_DOI = set(affs_bib["UT"])

## Sets will only include publications that have a DOI, but not all do
## Need to correct the values so that they align with 'actual' totals
inoverlap = len(inf_set_DOI.intersection(aff_set_DOI))
infraonly = actual_infra_number - inoverlap
affiliateonly = len(aff_set_DOI) - inoverlap

real_total = inoverlap + infraonly + affiliateonly

percover = int(round((inoverlap / real_total) * 100, 0))
percinf = int(round((infraonly / real_total) * 100, 0))
percaff = int(round((affiliateonly / real_total) * 100, 0))

print(f"Total number of publications: {real_total}")
print(f"         Infrastructure only: {infraonly} ({percinf}%)")
print(f"             Affiliates only: {affiliateonly} ({percaff}%)")
print(f"                     Overlap: {inoverlap} ({percover}%)")

# Make a weighted Venn with initial values
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
plt.savefig("Plots/Venn_annualreport.svg", dpi=300)
plt.savefig("Plots/Venn_annualreport.png", dpi=300)
