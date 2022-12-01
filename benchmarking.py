import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
import os

# The benchmark values come separately from KTH

benchmark = pd.read_excel(
    "Data/SciLifeLab_swe_benchmark.xlsx",
    sheet_name="SciLifeLab_swe_benchmark",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# The information for affiliates will come with their subjects and impact scores assigned

affiliates = pd.read_excel(
    "Data/SciLifeLab_cf_subj_cat_byaddress-2.xlsx",
    sheet_name="SciLifeLab_cf_subj_cat_byaddres",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# The information for infrastructure units will come with their subjects and impact scores assigned

infra = pd.read_excel(
    "Data/SciLifeLab_cf_subj_cat_facilities.xlsx",
    sheet_name="SciLifeLab_cf_subj_cat_faciliti",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# we calculate the scores based on the last 3 years for which scores are available
# for 2021, this is 2016-2019

benchmark_compare = benchmark[
    [
        "Publication_year",
        "Subject_category",
        "Prop_Top10_scxwo_full",
    ]  # , "cf_scxwo_full"]
]
benchmark_compare = benchmark_compare[
    (benchmark_compare["Publication_year"] == 2016)
    | (benchmark_compare["Publication_year"] == 2017)
    | (benchmark_compare["Publication_year"] == 2018)
    | (benchmark_compare["Publication_year"] == 2019)
]

bench_pp_fields = (
    benchmark_compare.groupby("Subject_category")["Prop_Top10_scxwo_full"]
    .mean()
    .reset_index()
)

# Below function can be used to check

# print(bench_pp_fields)

# work out for affiliates

aff_sub = affiliates[
    [
        "Publication_year",
        "Subject_category",
        "Top10_scxwo",
        "Doc_type_code_rev",
    ]
]
aff_201619 = aff_sub[
    (aff_sub["Publication_year"] == 2016)
    | (aff_sub["Publication_year"] == 2017)
    | (aff_sub["Publication_year"] == 2018)
    | (aff_sub["Publication_year"] == 2019)
]
aff_201619 = aff_201619[
    (
        aff_201619["Subject_category"] == "BIOCHEMICAL RESEARCH METHODS"
    )  # add in the relevant 6 'top' fields
    | (aff_201619["Subject_category"] == "BIOCHEMISTRY & MOLECULAR BIOLOGY")
    | (aff_201619["Subject_category"] == "BIOTECHNOLOGY & APPLIED MICROBIOLOGY")
    | (aff_201619["Subject_category"] == "CELL BIOLOGY")
    | (aff_201619["Subject_category"] == "GENETICS & HEREDITY")
    | (aff_201619["Subject_category"] == "ONCOLOGY")
]

# need to keep just the values for just the article types used in these calculations

aff_201619 = aff_201619[
    (aff_201619["Doc_type_code_rev"] == "RV")
    | (aff_201619["Doc_type_code_rev"] == "AR")
    | (aff_201619["Doc_type_code_rev"] == "PP")
]

aff_201619["Top10_scxwo"] = aff_201619["Top10_scxwo"].astype(float)

aff_pp_fields = (
    aff_201619.groupby("Subject_category")["Top10_scxwo"].mean().reset_index()
)
aff_pp_fields = aff_pp_fields.rename(
    columns={
        "Top10_scxwo": "aff_pp",
    }
)

# print(aff_pp_fields)

# work out values for infrastructure

inf_sub = infra[
    ["Publication_year", "Subject_category", "Top10_scxwo", "Doc_type_code_rev"]
]
inf_201619 = inf_sub[
    (inf_sub["Publication_year"] == 2016)
    | (inf_sub["Publication_year"] == 2017)
    | (inf_sub["Publication_year"] == 2018)
    | (inf_sub["Publication_year"] == 2019)
]

# filter for categories for which benchmarking values have been calculated

inf_201619 = inf_201619[
    (
        inf_201619["Subject_category"] == "BIOCHEMICAL RESEARCH METHODS"
    )  # put in relevant subject categories
    | (inf_201619["Subject_category"] == "BIOCHEMISTRY & MOLECULAR BIOLOGY")
    | (inf_201619["Subject_category"] == "BIOTECHNOLOGY & APPLIED MICROBIOLOGY")
    | (inf_201619["Subject_category"] == "CELL BIOLOGY")
    | (inf_201619["Subject_category"] == "GENETICS & HEREDITY")
    | (inf_201619["Subject_category"] == "ONCOLOGY")
]

# filter for publication type

inf_201619 = inf_201619[
    (inf_201619["Doc_type_code_rev"] == "RV")
    | (inf_201619["Doc_type_code_rev"] == "AR")
    | (inf_201619["Doc_type_code_rev"] == "PP")
]

inf_201619["Top10_scxwo"] = inf_201619["Top10_scxwo"].astype(float)

inf_pp_fields = (
    inf_201619.groupby("Subject_category")["Top10_scxwo"].mean().reset_index()
)
inf_pp_fields = inf_pp_fields.rename(
    columns={
        "Top10_scxwo": "inf_pp",
    }
)

# print(inf_pp_fields)

comb_Bandaff = pd.merge(
    bench_pp_fields,
    aff_pp_fields,
    how="left",
    on=["Subject_category"],
)
comb_all = pd.merge(
    comb_Bandaff,
    inf_pp_fields,
    how="left",
    on=["Subject_category"],
)

comb_all["Prop_Top10_scxwo_full"] = comb_all["Prop_Top10_scxwo_full"] * 100
comb_all["aff_pp"] = comb_all["aff_pp"] * 100
comb_all["inf_pp"] = comb_all["inf_pp"] * 100

# use the below commands to check
# print(comb_all)
# comb_all.to_excel("PPtop10benchmarkingvalues.xlsx")

fig = go.Figure(
    data=[
        go.Bar(
            name="Sweden",
            x=comb_all.Subject_category,
            y=comb_all.Prop_Top10_scxwo_full,
            marker=dict(color="#4C979F", line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Affiliated Researchers",
            x=comb_all.Subject_category,
            y=comb_all.aff_pp,
            marker=dict(color="#A7C947", line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Infrastructure Users",
            x=comb_all.Subject_category,
            y=comb_all.inf_pp,
            marker=dict(color="#491F53", line=dict(color="#000000", width=1)),
        ),
    ]
)


fig.update_layout(
    barmode="group",
    plot_bgcolor="white",
    font=dict(size=39),
    margin=dict(r=150, l=10),
    autosize=False,
    width=1800,
    height=1200,
    # legend_title_text=" ",
    showlegend=False,
)

# modify x-axis
fig.update_xaxes(
    title=" ",
    tickvals=[
        "BIOCHEMICAL RESEARCH METHODS",
        "BIOCHEMISTRY & MOLECULAR BIOLOGY",
        "BIOTECHNOLOGY & APPLIED MICROBIOLOGY",
        "CELL BIOLOGY",
        "GENETICS & HEREDITY",
        "ONCOLOGY",
    ],
    ticktext=[
        "Biokemiska forskningsmetoder",
        "Biokemi och molekylärbiologi",
        "Bioteknologi och tillämpad mikrobiologi",
        "Cellbiologi",
        "Genetik och ärftlighet",
        "Onkologi",
    ],
    showgrid=True,
    linecolor="black",
)
# modify y-axis
fig.update_yaxes(
    title=" ",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    ticktext=["0", "10", "20", "30", "40"],
    tickvals=["0", "10", "20", "30", "40"],
    range=[0, 41],
)

# Use the below to look at the figure (initial draft)
# fig.show()

# use the below to save a finalised figure
if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig.write_image("Plots/benchmark_1619_pptop10_swe.svg")
fig.write_image("Plots/benchmark_1619_pptop10_swe.png")
