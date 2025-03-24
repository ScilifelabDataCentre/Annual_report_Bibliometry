#! /home/larsowe/venv/bin/python

"""This script produces the plots required for the one-pagers"""

# 5 plots required in total for each reporting facility included in the 2022 mid term report
# 3 pie charts showing users in each year 2022-2024
# 2 stacked bar plots (one for JIF score, one for type of publication: service, collab...)

# In input_data.py data is formatted accordingly
# Need to bring the data across
# in colour science script, colours are given

import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from colour_science_2024 import (
    SCILIFE_COLOURS,
    FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB,
)

from Data_prep import affiliate_data, pub_cat_data, JIF_data

# affiliate_data - a combined dataset of affiliates for each facility and year
# pub_cat_data - a summary of the number of each 'type' of publication for each fac and year
# JIF_data - a summary of data in JIF categories (e.g. JIF = 6-9) for each fac and year

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

# Make Pie charts for each year (last 3) and unit

def Aff_pies_func(input, stacked, sizing):
    aff_data = input
    if sum(aff_data.Count) < 2:
        pi_plural = "PI"
    else:
        pi_plural = "PIs"

    colours = np.array([""] * len(aff_data["PI_aff"]), dtype=object)
    for i in aff_data["PI_aff"]:
        colours[
            np.where(aff_data["PI_aff"] == i)
        ] = FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB[str(i)]
    fig = go.Figure(
        go.Pie(
            values=aff_data["Count"],
            labels=aff_data["PI_aff"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )

    if stacked:
        fig.update_traces(
            textposition="outside",
            texttemplate="%{label} <br>(%{percent:.1%})",
        )
    else: 
        fig.update_traces(
            textposition="outside",
            ## #        texttemplate="%{label} (%{percent:.1%f})",
            texttemplate="%{label} (%{percent:.1%})",
            # the :.1%f does to 1 decimal place. do .0 to round to whole numbers.
            # HOWEVER! whole numbers the end to give 0% as a value. Wouldnt recommend
        )  # texttemplate="%{label} (%{percent})")
    fig.update_layout(
        margin=dict(
            l=100, r=100, b=100, t=100
        ),  # original values l=200, r=200 b=100 t=300
        font=dict(size=sizing),
        annotations=[
            dict(
                showarrow=False,
                text="{} {}".format(sum(aff_data.Count), pi_plural),
                font=dict(size=50),  # should work for all centre bits
                x=0.5,
                y=0.5,
            )
        ],
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/Aff_Pies/"):
        os.mkdir("Plots/Aff_Pies/")
    if sum(aff_data.Count) > 0:
        fig.write_image(
            "Plots/Aff_Pies/{}_{}_affs.svg".format(
                input["Unit"][input["Unit"].first_valid_index()],
                input["Year"][input["Year"].first_valid_index()],
            )
        )
    else:
        print("Warning: not all unit year combinations have data - check whether this is expected")

# Some plots fit better with the labels in the pie chart stacked
# Others fit better with the labels in pie charts side by side.
# This will likely change, and the list can easily be modified in future years

stackedUnits = [
    "AIDA Data Hub",
    # "Affinity Proteomics Stockholm",
    # "Affinity Proteomics Uppsala",
    "Ancient DNA",
    "Autoimmunity and Serology Profiling",
    #    "BioImage Informatics",
    "Chalmers Mass Spectrometry Infrastructure",
    #  "Chemical Proteomics"
    #  "Clinical Genomics Gothenburg"
    "Clinical Genomics Linköping",
    # "Clinical Genomics Lund",
    "Clinical Genomics Örebro",
    "Clinical Genomics Stockholm",
    #  "Clinical Genomics Umeå",
    #    "Clinical Genomics Uppsala",
    #    "CRISPR Functional Genomics",
    # "Drug Discovery and Development",
    "Exposomics",
    "Global Proteomics and Proteogenomics",
    # "In Situ Sequencing",
    # "Integrated Microscopy Technologies Gothenburg",
    # "Integrated Microscopy Technologies Stockholm",
    # "Integrated Microscopy Technologies Umeå",
    "Spatial Mass Spectrometry",
    "Spatial Proteomics",
    "Structural Proteomics",
    # "Support, Infrastructure and Training",
    #    "Swedish NMR Centre",
    "Swedish Metabolomics Centre",
]

## #affiliate_data = affiliate_data[affiliate_data["Year"].isin(["2022", "2023", "2024"])]
for i in affiliate_data["Year"].unique():
    temp = affiliate_data[(affiliate_data["Year"] == i)]
    for z in temp["Unit"].unique():
        if (z in stackedUnits):
            Aff_pies_func(temp[(temp["Unit"] == z)], True, 32)
        else:
            Aff_pies_func(temp[(temp["Unit"] == z)], False, 34)  # 36 works for most

# Note - some combinations of year and unit might be missing if they are new units etc.

## Create publication category plots

def pub_cat_func(input):
    pubcats = input
    # split down dataframes to enable stacking
    Collaborative = pubcats[(pubcats["Qualifiers"] == "Collaborative")]
    Service = pubcats[(pubcats["Qualifiers"] == "Service")]
    Tech_dev = pubcats[(pubcats["Qualifiers"] == "Technology development")]
    No_cat = pubcats[(pubcats["Qualifiers"] == "No category")]
    # This gives: A value is trying to be set on a copy of a slice from a DataFrame
    # and has to be rewritten prior to Panda 3
    #pubcats.drop(
    #pubcats[pubcats["Qualifiers"] == "Technology development"].index, inplace=True
    #)
    pubcats = pubcats[pubcats["Qualifiers"] != "Technology development"]
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="No category",
                x=No_cat.Year,
                y=No_cat.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="Collaborative",
                x=Collaborative.Year,
                y=Collaborative.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="Service",
                x=Service.Year,
                y=Service.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[0],
                    line=dict(color="#000000", width=1),  # was4
                ),
            ),
            # go.Bar(
            #     name="Technology<br>development",
            #     x=Tech_dev.Year,
            #     y=Tech_dev.Count,
            #     marker=dict(
            #         color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)
            #     ),
            # ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        font=dict(size=26),
        autosize=False,
        margin=dict(r=250, t=0, b=0, l=0),
        width=600,
        height=600,
        showlegend=True,
        annotations=[
            dict(
                showarrow=False,
                text="Total Tech.<br>Dev. papers<br>2022-2024: {}".format(sum(Tech_dev.Count)),
                font=dict(size=28),
                align="left",
                xref="paper",
                yref="paper",
                bordercolor="#045C64",
                borderwidth=5,
#                x=1.8,
                x=1.9, # NGI has so many papers that it won't fit to the right with 1.8
                y=0.4,
            )
        ],
    )
    # List years to use in x-axis
    Years = pubcats["Year"].unique().astype(str)
    Years = Years[-3:]
    Years_int = pubcats["Year"].unique()
    Years_int = Years_int[-3:]
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        ticktext=[
            "<b>" + Years[0] + "</b>",
            "<b>" + Years[1] + "</b>",
            "<b>" + Years[2] + "</b>",
        ],
        tickvals=[Years[0], Years[1], Years[2]],
    )

    Year_one = pubcats[(pubcats["Year"] == Years_int[0])]
    Year_two = pubcats[(pubcats["Year"] == Years_int[1])]
    Year_three = pubcats[(pubcats["Year"] == Years_int[2])]

    highest_y_value = max(
        Year_one["Count"].sum(), Year_two["Count"].sum(), Year_three["Count"].sum()
    )

    if highest_y_value < 10:
        yaxis_tick = 1
    if highest_y_value >= 10:
        yaxis_tick = 2
    if highest_y_value > 20:
        yaxis_tick = 5
    if highest_y_value > 50:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 20
    if highest_y_value > 150:
        yaxis_tick = 40
    if highest_y_value > 200:
        yaxis_tick = 50
    if highest_y_value > 1000:
        yaxis_tick = 100

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="black",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.15)],
    )
    if not os.path.isdir("Plots/pubcat_plots/"):
        os.mkdir("Plots/pubcat_plots/")
    fig.write_image(
        "Plots/pubcat_plots/{}_cats.svg".format(
            input["Unit"][input["Unit"].first_valid_index()]
        )
    )

# function to iterate through all units for publication category/type

for i in pub_cat_data["Unit"].unique():
    pub_cat_func(pub_cat_data[(pub_cat_data["Unit"] == i)])

## Create JIF plots

def JIF_graph_func(input):
    JIFcounts = input
    # split down dataframes to enable stacking
    UnknownJIF = JIFcounts[(JIFcounts["JIFcat"] == "JIF unknown")]
    Undersix = JIFcounts[(JIFcounts["JIFcat"] == "JIF <6")]
    sixtonine = JIFcounts[(JIFcounts["JIFcat"] == "JIF 6-9")]
    ninetotwentyfive = JIFcounts[(JIFcounts["JIFcat"] == "JIF 9-25")]
    overtwentyfive = JIFcounts[(JIFcounts["JIFcat"] == "JIF >25")]
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="JIF unknown",
                x=UnknownJIF.Year,
                y=UnknownJIF.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF < 6",
                x=Undersix.Year,
                y=Undersix.Count,
                marker=dict(color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="JIF 6 - 9",
                x=sixtonine.Year,
                y=sixtonine.Count,
                marker=dict(color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="JIF 9 - 25",
                x=ninetotwentyfive.Year,
                y=ninetotwentyfive.Count,
                marker=dict(color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="JIF > 25",
                x=overtwentyfive.Year,
                y=overtwentyfive.Count,
                marker=dict( color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=1)),
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=26),
        margin=dict(r=250, t=0, b=0, l=0),
        width=600,
        height=600,
        showlegend=True,
    )
    # List years to use in x-axis
    Years = JIFcounts["Year"].unique().astype(str)
    Years = Years[-3:]
    Years_int = JIFcounts["Year"].unique()
    Years_int = Years_int[-3:]
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        ticktext=[
            "<b>" + Years[0] + "</b>",
            "<b>" + Years[1] + "</b>",
            "<b>" + Years[2] + "</b>",
        ],
        tickvals=[Years[0], Years[1], Years[2]],
    )

    Year_one = JIFcounts[(JIFcounts["Year"] == Years_int[0])]
    Year_two = JIFcounts[(JIFcounts["Year"] == Years_int[1])]
    Year_three = JIFcounts[(JIFcounts["Year"] == Years_int[2])]

    highest_y_value = max(
        Year_one["Count"].sum(), Year_two["Count"].sum(), Year_three["Count"].sum()
    )

    if highest_y_value < 10:
        yaxis_tick = 1
    if highest_y_value >= 10:
        yaxis_tick = 2
    if highest_y_value > 20:
        yaxis_tick = 5
    if highest_y_value > 50:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 20
    if highest_y_value > 150:
        yaxis_tick = 40
    if highest_y_value > 200:
        yaxis_tick = 50
    if highest_y_value > 1000:
        yaxis_tick = 100

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="black",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.15)],
    )
    if not os.path.isdir("Plots/JIF_plots/"):
        os.mkdir("Plots/JIF_plots/")
    fig.write_image(
        "Plots/JIF_plots/{}_JIF.svg".format(
            input["Unit"][input["Unit"].first_valid_index()]
        )
    )

# function to iterate through all units for JIF

for i in JIF_data["Unit"].unique():
    JIF_graph_func(JIF_data[(JIF_data["Unit"] == i)])
