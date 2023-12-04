# Annual Report Bibliometry

This repository contains the code required to perform the bibliometric analysis presented in the SciLifeLab annual report. The subfolders represent scripts related to a given year. The scripts outside of a subfolder are the scripts for the latest year. The scripts are be categorised according to the plot that they relate to.

## colour_science_year.py (used in multiple plots)

Used to assign colours in multiple graphs. There is no need to run this script or edit it before use, it is simply imported.

## Calculation of collaboration between infrastructure units

Used to calculate the level of collaboration between infrastructure units. Rules change periodically, this script uses rules applicable in a given year.

**infra_collab_calc.py** - This uses the rules set out by OO (infra) in each year, some units are considered together, so collaborations between them are not counted.

## JIF stacked plot

This plot shows the number of publications produced in each year for a 5 year timespan (e.g. for 2021, use 2016-2021). It also shows the number of papers that fall into each category of JIF score.

**JIF_aff_data_prep.py** - this script prepares the data for the affiliates dataset. You must ensure that the link to the data is set up the same way for the script to work unedited.

**JIF_fell_data_prep.py** - this script prepares the data for the fellows dataset. You must ensure that the link to the data is set up the same way for the script to work unedited.

**JIF_inf_data_prep.py** - this script prepares the data for the infrastructure dataset. You must ensure that the link to the data is set up the same way for the script to work unedited.

**JIF_plot.py** - this script uses the data from the data_prep scripts above to create the JIF plots for each group. If the prep scripts are set up, then this script can be used directly and unedited.

## Citation number plot

This plot represents the number of citations acquired by all scilifelab affiliates/infrastructure users in each year for the last 5 years e.g. 2016-21 for 2021.

**citation_number.py** - this script completes the calculations required to sum the number of citations and produce the plots.

## Venn plot

**venn_diagram.py** - This plot shows the numbers of papers produced by scilifelab infrastructure users and affiliated researchers, and how many they collaborated on in the last 5 years. All instructions for use are available in the script itself.

## Benchmarking plot

**benchmarking.py** - This plot shows the pptop(10) scores of papers produced by scilifelab infrastructure users and affiliated researchers, compared to overall scores for papers produced by Swedish researchers in general. We focus on the 6 subjects in which SciLifeLab completed the most work in the last 5. All instructions for use are available in the script itself.
