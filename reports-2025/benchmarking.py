#!/usr/bin/env python3

import pandas as pd
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
import os

# we calculate the scores based on the last 3 years for which scores are available
years_of_interest = range(2020, 2024) # for 2025 is 2020-23
subjects = ["BIOCHEMICAL RESEARCH METHODS", "BIOCHEMISTRY & MOLECULAR BIOLOGY",
            "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "CELL BIOLOGY", "GENETICS & HEREDITY", "ONCOLOGY"]

# The benchmark values come separately from KTH
benchmark = pd.read_excel(
    "Data/SciLifeLab_swe_benchmark.xlsx",
    sheet_name="SciLifeLab_swe_benchmark",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["Publication_year", "Subject_category", "Prop_Top10_scxwo_full"]
)

# The information for affiliates will come with their subjects and impact scores assigned
affiliates = pd.read_excel(
    "Data/SciLifeLab_cf_subj_cat_affiliates.xlsx",
    sheet_name="SciLifeLab_cf_subj_cat_affiliat",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["Publication_year", "Subject_category", "Top10_scxwo", "Doc_type_code_rev"]
)

# The information for infrastructure units will come with their subjects and impact scores assigned
infra_sub = pd.read_excel(
    "Data/SciLifeLab_cf_subj_cat_infrastructure.xlsx",
    sheet_name="SciLifeLab_cf_subj_cat_infrastr",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
    usecols=["Publication_year", "Subject_category", "Top10_scxwo", "Doc_type_code_rev"]
)

benchmark = benchmark[benchmark["Publication_year"].isin(years_of_interest)]

bench_pp_fields = (benchmark.groupby("Subject_category")["Prop_Top10_scxwo_full"].mean().reset_index())

# Below function can be used to check
# print(bench_pp_fields)

# work out for affiliates
# need to keep just the values for just the article types used in these calculations
affiliates = affiliates[affiliates["Publication_year"].isin(years_of_interest) &
                       affiliates["Subject_category"].isin(subjects) &
                       affiliates["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]
affiliates["Top10_scxwo"] = affiliates["Top10_scxwo"].astype(float)

aff_pp_fields = (affiliates.groupby("Subject_category")["Top10_scxwo"].mean().reset_index())
aff_pp_fields = aff_pp_fields.rename(
    columns={
        "Top10_scxwo": "aff_pp",
    }
)

# print(aff_pp_fields)

# work out values for infrastructure
# filter for categories for which benchmarking values have been calculated
# filter for publication type
infra_sub = infra_sub[infra_sub["Publication_year"].isin(years_of_interest) &
                      infra_sub["Subject_category"].isin(subjects) &
                      infra_sub["Doc_type_code_rev"].isin(["RV", "AR", "PP"])]
infra_sub["Top10_scxwo"] = infra_sub["Top10_scxwo"].astype(float)

inf_pp_fields = (infra_sub.groupby("Subject_category")["Top10_scxwo"].mean().reset_index())
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
comb_all.to_excel("PPtop10benchmarkingvalues.xlsx")

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
    tickvals=subjects,
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

fig.write_image("Plots/benchmark_pptop10_swe.svg")
fig.write_image("Plots/benchmark_pptop10_swe.png")
