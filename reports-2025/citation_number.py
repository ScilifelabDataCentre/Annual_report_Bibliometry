#!/usr/bin/python
# citation_number.py

"""Script to generate plots of number of citations per group.

To use:
    Copy the source data files to a subfolder.
    Edit the settings section.
    Activate the virtual environment.
    Run this python script.
"""

import os
import glob
import pandas as pd
import plotly.graph_objects as go

# SETTINGS
DATA_PATH = "Data"  # The relative path to the data files.
OUTPUT_PATH = "Plots"  # The relative path to the output folder.
years = range(2020, 2026)  # The range of years to consider for processing.

def GetPubGroup(file):
    df = pd.read_excel(
        file,
        sheet_name="citations_per_year",
        header=0,
        engine="openpyxl",
        keep_default_na=False,
        usecols=[               # Last 5 years
            f"citations_self_excl_{years[0]}",
            f"citations_self_excl_{years[1]}",
            f"citations_self_excl_{years[2]}",
            f"citations_self_excl_{years[3]}",
            f"citations_self_excl_{years[4]}",
            f"citations_self_excl_{years[5]}",
        ]
    )

    data_sum = df.sum(axis=0, skipna=True)

    data_group = data_sum.to_frame(name="sum_val")
    data_group["Citation_Year"] = data_group.index
    data_group.reset_index(drop=True, inplace=True)
    # print(data_group)
    return data_group

# Create graph function
def Citation_graph_func(input, pub_group):
    Citation = input
    # Make bar chart
    fig = go.Figure(
        go.Bar(
            x=Citation.Citation_Year,
            y=Citation.sum_val,
            marker=dict(color="#A7C947", line=dict(color="#000000", width=1)),
        )
    )
    fig.update_layout(
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=75),
        margin=dict(r=250, t=0, b=0, l=0),
        width=2500,
        height=1700,
        showlegend=False,
    )
    # add more years as needed
    Citation_year = Citation["Citation_Year"].unique()
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        # add more years as needed
        ticktext=[
            f"<b>{years[0]}</b>",
            f"<b>{years[1]}</b>",
            f"<b>{years[2]}</b>",
            f"<b>{years[3]}</b>",
            f"<b>{years[4]}</b>",
            f"<b>{years[5]}</b>",
        ],
        tickvals=Citation_year
    )

    highest_y_value = max(Citation["sum_val"])

    if highest_y_value > 50000:
        yaxis_tick = 10000
    if highest_y_value > 20000:
        yaxis_tick = 5000
    if highest_y_value <= 10000:
        yaxis_tick = 1000

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, float(highest_y_value * 1.15)],
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image("Plots/{}_Citation_eachyear.png".format(pub_group))
    fig.write_image("Plots/{}_Citation_eachyear.svg".format(pub_group))


Infra_data_group = GetPubGroup("Data/SciLifeLab-Infrastructure-20251204.xlsx")
Affiliates_data_group = GetPubGroup("Data/SciLifeLab-Affiliates-20251204.xlsx")
Fellows_data_group = GetPubGroup("Data/SciLifeLab-Fellows-20251204.xlsx")
Citation_graph_func(Infra_data_group, "Infra")
Citation_graph_func(Affiliates_data_group, "Affiliates")
# # Citation_graph_func(Fellows_data_group, "Fellows")
