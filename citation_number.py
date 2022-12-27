#!/venv/bin python
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

DATA_PATH = "data/data2022/cite_data"       # The relative path to the data files.
OUTPUT_PATH = "reports2022/Plots"           # The relative path to the output folder.
YEARS_RANGE = [2017, 2022]                  # The range of years to consider for processing.




def run():
    """Runs the script for all discovered files in the configured data path."""
    years = range(YEARS_RANGE[0], YEARS_RANGE[1]+1)

    filenames = glob.glob(DATA_PATH + "/SciLifeLab-*.xlsx")

    if len(filenames) == 0:
        print("No input files found. Exiting.")
        return

    for file in filenames:
        print(f"Now processing file {file}")
        pub_group = file.split('-')[1]

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
        #print(data_group)

        __create_citation_graph(data_group, pub_group, years)

    print(f"Done. Any generaed plots were saved to output path {OUTPUT_PATH}")





# Private functions

def __create_citation_graph(citations, pub_group, years):
    """  Creates a citation graph for a single publication group.

        :param dataframe citations: A dataframe containing the input data.
        :param string pub_group: The name of the publication group.
        :param range years: A range of int of the years to plot.
    """

    # Make bar chart
    fig = go.Figure(
        go.Bar(
            x = citations.Citation_Year,
            y = citations.sum_val,
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

    # List years to use on x-axis
    citation_year = citations["Citation_Year"].unique()

    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        # years
        ticktext = [ "<b>" + str(years[i]) + "</b>" for i in range(len(years))  ],

        tickvals = [ citation_year[i] for i in range(len(years)) ],
    )

    highest_y_value = max(citations["sum_val"])

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

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    # Finally save the plots to png and svg files
    fig.write_image(f"{OUTPUT_PATH}/{pub_group}_Citation_eachyear.png")
    fig.write_image(f"{OUTPUT_PATH}/{pub_group}_Citation_eachyear.svg")





if __name__ == "__main__":

    print("Running citation_number script")
    run()
