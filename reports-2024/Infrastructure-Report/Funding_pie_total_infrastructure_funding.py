#! /home/larsowe/venv/bin/python

# This pie chart shows the total funding for infrastructure

# Note: potentially need to trim original file
# Has 'spare' rows, columns and totals for checking
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
from colour_science_2024 import (
    PLATFORM_FUNDING_COLOURS,
)

Plat_tot_fund_data = pd.read_excel(
    "Data/Total Funding and User Fees 2024.xlsx",
    sheet_name="Total Funding and User Fees",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


# OO requested percentages rounded to nearest percent for this graph
Plat_tot_fund_data["Fund_MSEK"] = Plat_tot_fund_data["MSEK"]
# print(Acaduser_data)
colours = np.array([""] * len(Plat_tot_fund_data["Financier"]), dtype=object)
for i in Plat_tot_fund_data["Financier"]:
    colours[np.where(Plat_tot_fund_data["Financier"] == i)] = PLATFORM_FUNDING_COLOURS[
        str(i)
    ]

fig = go.Figure(
    go.Pie(
        values=Plat_tot_fund_data["Fund_MSEK"],
        labels=Plat_tot_fund_data["Financier"],
        hole=0.7,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} <br>%{value:.1f} ",
    textfont=dict(family="Arial", size=26),
)
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    # annotations=[
    #     dict(
    #         showarrow=False,
    #         text="{}".format(round(sum(Plat_tot_fund_data["Fund_MSEK"]))),
    #         font=dict(family="Arial", size=50),  # should work for all centre bits
    #         x=0.5,
    #         y=0.5,
    #     )
    # ],
    showlegend=False,
    width=1000,
    height=1000,
    autosize=False,
)
if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

# fig.show()

fig.write_image("Plots/Total_infrastructure_funding.png", scale=3)
fig.write_image("Plots/total infrastructure funding.svg", scale=3)

