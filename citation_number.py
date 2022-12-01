import pandas as pd
import plotly.graph_objects as go
import os

# # Fellows data prep

# Fellows_data = pd.read_excel(
#     "Data/XXXXXXXXXXXXXXXXXXXXX.xlsx",
#     sheet_name="XXXXXXXXXXXXXXXFellows",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )

# # Last 5 years for fellows
# Fellows_data_sub = Fellows_data[
#     [
#         "citations_self_excl_2016",
#         "citations_self_excl_2017",
#         "citations_self_excl_2018",
#         "citations_self_excl_2019",
#         "citations_self_excl_2020",
#         "citations_self_excl_2021",
#     ]
# ]


# Fellows_data_sum = Fellows_data_sub.sum(axis=0, skipna=True)

# Fellows_data_group = Fellows_data_sum.to_frame(
#     name="sum_val",
# )
# Fellows_data_group["Citation_Year"] = Fellows_data_group.index
# Fellows_data_group.reset_index(drop=True, inplace=True)
# # print(Fellows_data_group)


# Affiliates data prep

Affiliates_data = pd.read_excel(
    "Data/Updated_cite_data/SciLifeLab-byaddress-20211217.xlsx",
    sheet_name="citations_per_year",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


# Last 5 years affiliates
Affiliates_data_sub = Affiliates_data[
    [
        "citations_self_excl_2016",
        "citations_self_excl_2017",
        "citations_self_excl_2018",
        "citations_self_excl_2019",
        "citations_self_excl_2020",
        "citations_self_excl_2021",
    ]
]


Affiliates_data_sum = Affiliates_data_sub.sum(axis=0, skipna=True)

Affiliates_data_group = Affiliates_data_sum.to_frame(
    name="sum_val",
)
Affiliates_data_group["Citation_Year"] = Affiliates_data_group.index
Affiliates_data_group.reset_index(drop=True, inplace=True)
print(Affiliates_data_group)


# Last 5 years for infrastructure

Infra_data = pd.read_excel(
    "Data/Updated_cite_data/SciLifeLab-facilities-20211217.xlsx",
    sheet_name="citations_per_year",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


Infra_data_sub = Infra_data[
    [
        "citations_self_excl_2016",
        "citations_self_excl_2017",
        "citations_self_excl_2018",
        "citations_self_excl_2019",
        "citations_self_excl_2020",
        "citations_self_excl_2021",
    ]
]


Infra_data_sum = Infra_data_sub.sum(axis=0, skipna=True)

Infra_data_group = Infra_data_sum.to_frame(
    name="sum_val",
)
Infra_data_group["Citation_Year"] = Infra_data_group.index
Infra_data_group.reset_index(drop=True, inplace=True)
print(Infra_data_group)

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
            "<b>2016</b>",
            "<b>2017</b>",
            "<b>2018</b>",
            "<b>2019</b>",
            "<b>2020</b>",
            "<b>2021</b>",
        ],
        tickvals=[
            Citation_year[0],
            Citation_year[1],
            Citation_year[2],
            Citation_year[3],
            Citation_year[4],
            Citation_year[5],
        ],
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


Citation_graph_func(Affiliates_data_group, "Affiliates")
Citation_graph_func(Infra_data_group, "Infra")
# Citation_graph_func(Fellows_data_group, "Fellows")
