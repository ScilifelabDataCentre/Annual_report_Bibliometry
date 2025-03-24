#! /home/larsowe/venv/bin/python

# generates stacked barplot with units on y-axis and funding amount on x-axis,
# stacks divided by user categories

import pandas as pd
import plotly.graph_objects as go
import os
from colour_science_2024 import (
    SCILIFE_COLOURS,
)

# Add data
Res_user_cat = pd.read_excel(
    "Data/Resources by Category 2024.xlsx",
    sheet_name="Single Data",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


Res_user_cat = Res_user_cat.rename(
    columns={
        "Academy, National": "Acad_Nat",
        "Akademi, International": "Acad_Int",
        "Internal Technology Development": "Int_Techdev",
        "Other Governmental Organizations": "Oth_Gov",
    }
)
# print(Res_user_cat.info())

# Make stacked bar chart
fig = go.Figure(
    data=[
        go.Bar(
            name="Academia National",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Acad_Nat,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Academia Internat.",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Acad_Int,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Internal Tech. Dev.",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Int_Techdev,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Industry",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Industry,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[14], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Healthcare",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Healthcare,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Other Gov. Agencies",
            y=Res_user_cat.Unit,
            x=Res_user_cat.Oth_Gov,
            orientation="h",
            marker=dict(color=SCILIFE_COLOURS[16], line=dict(color="#000000", width=1)),
        ),
    ]
)
# fig.update_layout(xaxis=go.layout.XAxis(tickangle=45))
fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    font=dict(size=35),
    autosize=False,
    margin=dict(r=0, t=0, b=0, l=0),
    width=3000,
    height=2200,
    yaxis={"categoryorder": "total ascending"},
    showlegend=True,
    legend=dict(
        itemwidth=50,
        traceorder="normal",
        orientation="h",
        yanchor="top",
        y=1.06,
        xanchor="left",
        x=-0.4,
        font=dict(size=52),
    ),
)

# modify x-axis
fig.update_yaxes(
    title=" ",
    showgrid=True,
    linecolor="black",
)

# modify y-axis
fig.update_xaxes(
    title="<br>Resources per User Category",  # keep the break to give y-axis title space between graph
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # ticktext=[
    #     0,
    #     10
    #     20,
    #     30,
    #     40,
    #     50,
    #     60,
    #     70,
    #     80,
    #     90,
    #     100,
    # ],
    # tickvals=[
    #     0,
    #     10
    #     20,
    #     30,
    #     40,
    #     50,
    #     60,
    #     70,
    #     80,
    #     90,
    #     100,
    # ],
    dtick=10,  # 10 will work fine with most values
    range=[0, 102],
)
if not os.path.isdir("Plots"):
    os.mkdir("Plots")
# fig.show()
fig.write_image("Plots/Resources_per_user_2024.png")
fig.write_image("Plots/Resources_per_user_2024.svg")
