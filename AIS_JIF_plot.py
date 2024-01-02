# want to create JIF and AIS plots for the last 5 years
# Data comes from dataprep scripts
# Need to complete manual checking during data preparation to maximise matching. This must be done before the plots are made.
# Note, it is only necessary to maximise matches for EITHER JIF or AIS, as both are matched on the same thing
import pandas as pd
import os
import plotly.graph_objects as go

from colour_science_2023 import (
    SCILIFE_COLOURS,
)

# infrastructure data - JIF
from AIS_JIF_data_prep_inf import infpubs_jif_count

# infrastructure data - AIS
from AIS_JIF_data_prep_inf import infpubs_ais_count

# fellows data - JIF
from AIS_JIF_data_prep_fell import fellpubs_jif_count

# fellows data - AIS
from AIS_JIF_data_prep_fell import fellpubs_ais_count

# affiliates data - JIF
from AIS_JIF_data_prep_aff import affpubs_jif_count

# affiliates data - AIS
from AIS_JIF_data_prep_aff import affpubs_ais_count

# JIF_sub_group_inf = JIF_sub_group_inf[JIF_sub_group_inf.Year != "nan"]

# Make JIF plots


def JIF_graph_func(input, name):
    JIFcounts = input
    # split down dataframes to enable stacking
    UnknownJIF = JIFcounts[(JIFcounts["Category"] == "JIF unknown")]
    Undersix = JIFcounts[(JIFcounts["Category"] == "JIF <6")]
    sixtonine = JIFcounts[(JIFcounts["Category"] == "JIF 6-9")]
    ninetotwentyfive = JIFcounts[(JIFcounts["Category"] == "JIF 9-25")]
    overtwentyfive = JIFcounts[(JIFcounts["Category"] == "JIF >25")]
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
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF 6 - 9",
                x=sixtonine.Year,
                y=sixtonine.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF 9 - 25",
                x=ninetotwentyfive.Year,
                y=ninetotwentyfive.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="JIF > 25",
                x=overtwentyfive.Year,
                y=overtwentyfive.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=1)
                ),
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=30),  # 58 for fellows
        margin=dict(r=125, t=0, b=0, l=0),
        width=900,
        height=600,
        showlegend=False,
    )
    # List years to use in x-axis
    Years = JIFcounts["Year"].unique().astype(str)
    Years_int = JIFcounts["Year"].unique()
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        # add more years as needed
        ticktext=[
            "<b> 2018 </b>",
            "<b> 2019 </b>",
            "<b> 2020 </b>",
            "<b> 2021 </b>",
            "<b> 2022 </b>",
            "<b> 2023 </b>",
        ],
        tickvals=[
            Years[0],
            Years[1],
            Years[2],
            Years[3],
            Years[4],
            Years[5],
        ],
    )

    Year_one = JIFcounts[(JIFcounts["Year"] == Years_int[0])]
    Year_two = JIFcounts[(JIFcounts["Year"] == Years_int[1])]
    Year_three = JIFcounts[(JIFcounts["Year"] == Years_int[2])]
    Year_four = JIFcounts[(JIFcounts["Year"] == Years_int[3])]
    Year_five = JIFcounts[(JIFcounts["Year"] == Years_int[4])]
    Year_six = JIFcounts[(JIFcounts["Year"] == Years_int[5])]

    highest_y_value = max(
        Year_one["Count"].sum(),
        Year_two["Count"].sum(),
        Year_three["Count"].sum(),
        Year_four["Count"].sum(),
        Year_five["Count"].sum(),
        Year_six["Count"].sum(),
    )

    if highest_y_value < 10:
        yaxis_tick = 1
    if highest_y_value > 10:
        yaxis_tick = 2
    if highest_y_value > 20:
        yaxis_tick = 5
    if highest_y_value > 50:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 20
    if highest_y_value > 150:
        yaxis_tick = 40
    if highest_y_value > 500:
        yaxis_tick = 100
    if highest_y_value > 1000:
        yaxis_tick = 100

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.1)],
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image("Plots/{}_JIF.png".format(name))
    fig.write_image("Plots/{}_JIF.svg".format(name))


# make JIF plots by applying function

JIF_graph_func(infpubs_jif_count, "infrastructure")
JIF_graph_func(affpubs_jif_count, "affiliates")
JIF_graph_func(fellpubs_jif_count, "fellows")

# Make AIS plots


def AIS_graph_func(input, name):
    AIScounts = input
    # split down dataframes to enable stacking
    UnknownAIS = AIScounts[(AIScounts["Category"] == "AIS unknown")]
    Underone = AIScounts[(AIScounts["Category"] == "AIS <1")]
    Overone = AIScounts[(AIScounts["Category"] == "AIS >1")]
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="AIS unknown",
                x=UnknownAIS.Year,
                y=UnknownAIS.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[17], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="AIS < 1",
                x=Underone.Year,
                y=Underone.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=1)
                ),
            ),
            go.Bar(
                name="AIS > 1",
                x=Overone.Year,
                y=Overone.Count,
                marker=dict(
                    color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=1)
                ),
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=30),
        margin=dict(r=125, t=0, b=0, l=0),
        width=900,
        height=600,
        showlegend=False,
    )
    # List years to use in x-axis
    Years = AIScounts["Year"].unique().astype(str)
    Years_int = AIScounts["Year"].unique()
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        # add more years as needed
        ticktext=[
            "<b> 2018 </b>",
            "<b> 2019 </b>",
            "<b> 2020 </b>",
            "<b> 2021 </b>",
            "<b> 2022 </b>",
            "<b> 2023 </b>",
        ],
        tickvals=[
            Years[0],
            Years[1],
            Years[2],
            Years[3],
            Years[4],
            Years[5],
        ],
    )

    Year_one = AIScounts[(AIScounts["Year"] == Years_int[0])]
    Year_two = AIScounts[(AIScounts["Year"] == Years_int[1])]
    Year_three = AIScounts[(AIScounts["Year"] == Years_int[2])]
    Year_four = AIScounts[(AIScounts["Year"] == Years_int[3])]
    Year_five = AIScounts[(AIScounts["Year"] == Years_int[4])]
    Year_six = AIScounts[(AIScounts["Year"] == Years_int[5])]

    highest_y_value = max(
        Year_one["Count"].sum(),
        Year_two["Count"].sum(),
        Year_three["Count"].sum(),
        Year_four["Count"].sum(),
        Year_five["Count"].sum(),
        Year_six["Count"].sum(),
    )

    if highest_y_value < 10:
        yaxis_tick = 1
    if highest_y_value > 10:
        yaxis_tick = 2
    if highest_y_value > 20:
        yaxis_tick = 5
    if highest_y_value > 50:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 20
    if highest_y_value > 150:
        yaxis_tick = 40
    if highest_y_value > 500:
        yaxis_tick = 100
    if highest_y_value > 1000:
        yaxis_tick = 100

    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.1)],
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image("Plots/{}_AIS.png".format(name))
    fig.write_image("Plots/{}_AIS.svg".format(name))


# make plots by applying function

AIS_graph_func(infpubs_ais_count, "infrastructure")
AIS_graph_func(affpubs_ais_count, "affiliates")
AIS_graph_func(fellpubs_ais_count, "fellows")
