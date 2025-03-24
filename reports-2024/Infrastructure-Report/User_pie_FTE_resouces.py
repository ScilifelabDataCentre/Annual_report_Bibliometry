#! /home/larsowe/venv/bin/python

# Chart will generate global pie chart looking at available FTE resources per user category

# Note: need to trim out data from xlsx file
import pandas as pd
import plotly.graph_objects as go
import os
from colour_science_2024 import (
    SCILIFE_COLOURS,
)

FTEusercat_data = pd.read_excel(
    "Data/Resources by Category 2024.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Round percentages to integrer
FTEusercat_data["Round_perc"] = (FTEusercat_data["Percent"] * 100).round().astype(int)
# print(FTEusercat_data)

colours = [
    SCILIFE_COLOURS[8],
    SCILIFE_COLOURS[0],
    SCILIFE_COLOURS[12],
    SCILIFE_COLOURS[4],
    SCILIFE_COLOURS[14],
    SCILIFE_COLOURS[16],
] * 2

FTEusercat_data = FTEusercat_data.set_axis(["Category", "Percent", "Round_perc"], axis=1)
# print(FTEusercat_data.info())

# Edited this to fit more nicely
FTEusercat_data["Category"] = FTEusercat_data["Category"].replace(
    "Other Governmental Organizations",
    "Other Government Organizations",
)
FTEusercat_data["Category"] = FTEusercat_data["Category"].replace(
    "Internal Technology Development",
    "Internal Technology<br>Development",
)

fig = go.Figure(
    go.Pie(
        values=FTEusercat_data["Round_perc"],
        labels=FTEusercat_data["Category"],
        hole=0.7,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} <br>%{value}%",
    textfont=dict(family="Arial", size=25),
)
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    showlegend=False,
    width=1000,
    height=1000,
    autosize=False,
)
if not os.path.isdir("Plots"):
    os.mkdir("Plots")

# fig.show()

fig.write_image("Plots/Distribution_of_FTE_resource.png", scale=3)
fig.write_image("Plots/FTE_Resource_per_usercat.svg", scale=3)
