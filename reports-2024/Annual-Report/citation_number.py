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
YEARS_RANGE = [2019, 2024]  # The range of years to consider for processing.


def run():
    """Runs the script for all discovered files in the configured data path."""
    years = range(YEARS_RANGE[0], YEARS_RANGE[1] + 1)

    filenames = glob.glob(DATA_PATH + "/SciLifeLab-*.xlsx")

    if len(filenames) == 0:
        print("No input files found. Exiting.")
        return

    for file in filenames:
        print(f"Now processing file {file}")
        pub_group = file.split("-")[1]

        df = pd.read_excel(
            file,
            sheet_name="citations_per_year",
            header=0,
            engine="openpyxl",
            keep_default_na=False,
        )

        # Last 5 years
        data_sub = df[
            [
                f"citations_self_excl_{years[0]}",
                f"citations_self_excl_{years[1]}",
                f"citations_self_excl_{years[2]}",
                f"citations_self_excl_{years[3]}",
                f"citations_self_excl_{years[4]}",
                f"citations_self_excl_{years[5]}",
            ]
        ]

        data_sum = data_sub.sum(axis=0, skipna=True)

        data_group = data_sum.to_frame(
            name="sum_val",
        )
        data_group["Citation_Year"] = data_group.index
        data_group.reset_index(drop=True, inplace=True)
        # print(data_group)

        __create_citation_graph(data_group, pub_group, years)

    print(f"Done. Any generaed plots were saved to output path {OUTPUT_PATH}")


# Private functions


def __create_citation_graph(citations, pub_group, years):
    """Creates a citation graph for a single publication group.

    :param dataframe citations: A dataframe containing the input data.
    :param string pub_group: The name of the publication group.
    :param range years: A range of int of the years to plot.
    """


# # Create graph function


# def Citation_graph_func(input, pub_group):
#     Citation = input
#     # Make bar chart
#     fig = go.Figure(
#         go.Bar(
#             x=Citation.Citation_Year,
#             y=Citation.sum_val,
#             marker=dict(color="#A7C947", line=dict(color="#000000", width=1)),
#         )
#     )
#     fig.update_layout(
#         plot_bgcolor="white",
#         autosize=False,
#         font=dict(size=75),
#         margin=dict(r=250, t=0, b=0, l=0),
#         width=2500,
#         height=1700,
#         showlegend=False,
#     )
#     # add more years as needed
#     Citation_year = Citation["Citation_Year"].unique()
#     fig.update_xaxes(
#         title=" ",
#         showgrid=True,
#         linecolor="black",
#         # add more years as needed
#         ticktext=[
#             "<b>2016</b>",
#             "<b>2017</b>",
#             "<b>2018</b>",
#             "<b>2019</b>",
#             "<b>2020</b>",
#             "<b>2021</b>",
#         ],
#         tickvals=[
#             Citation_year[0],
#             Citation_year[1],
#             Citation_year[2],
#             Citation_year[3],
#             Citation_year[4],
#             Citation_year[5],
#         ],
#     )

#     highest_y_value = max(Citation["sum_val"])

#     if highest_y_value > 50000:
#         yaxis_tick = 10000
#     if highest_y_value > 20000:
#         yaxis_tick = 5000
#     if highest_y_value <= 10000:
#         yaxis_tick = 1000

#     # modify y-axis
#     fig.update_yaxes(
#         title=" ",
#         showgrid=True,
#         gridcolor="lightgrey",
#         linecolor="black",
#         dtick=yaxis_tick,
#         range=[0, float(highest_y_value * 1.15)],
#     )
#     if not os.path.isdir("Plots/"):
#         os.mkdir("Plots/")
#     # fig.show()
#     fig.write_image("Plots/{}_Citation_eachyear.png".format(pub_group))
#     fig.write_image("Plots/{}_Citation_eachyear.svg".format(pub_group))


# Citation_graph_func(Affiliates_data_group, "Affiliates")
# Citation_graph_func(Infra_data_group, "Infra")
# # Citation_graph_func(Fellows_data_group, "Fellows")
