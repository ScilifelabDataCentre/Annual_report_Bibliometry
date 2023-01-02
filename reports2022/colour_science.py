#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the updated colour science code to reflect the
# 2020 SciLifeLab visual ID.

# Colourblind friendly colour sets - not typically used in reporting
COLOURS = {
    1: ["#4477AA"],
    2: ["#4477AA", "#CC6677"],
    3: ["#4477AA", "#DDCC77", "#CC6677"],
    4: ["#4477AA", "#117733", "#DDCC77", "#CC6677"],
    5: ["#332288", "#88CCEE", "#117733", "#DDCC77", "#CC6677"],
    6: ["#332288", "#88CCEE", "#117733", "#DDCC77", "#CC6677", "#AA4499"],
    7: ["#332288", "#88CCEE", "#44AA99", "#117733", "#DDCC77", "#CC6677", "#AA4499"],
    8: [
        "#332288",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#CC6677",
        "#AA4499",
    ],
    9: [
        "#332288",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#CC6677",
        "#882255",
        "#AA4499",
    ],
    10: [
        "#332288",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#661100",
        "#CC6677",
        "#882255",
        "#AA4499",
    ],
    11: [
        "#332288",
        "#6699CC",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#661100",
        "#CC6677",
        "#882255",
        "#AA4499",
    ],
    12: [
        "#332288",
        "#6699CC",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#661100",
        "#CC6677",
        "#AA4466",
        "#882255",
        "#AA4499",
    ],
    "12-mix": [
        "#DDCC77",
        "#117733",
        "#6699CC",
        "#661100",
        "#882255",
        "#332288",
        "#AA4466",
        "#88CCEE",
        "#44AA99",
        "#999933",
        "#CC6677",
        "#AA4499",
    ],
}
SCILIFE_COLOURS = [
    "#A7C947",  # 100% green
    "#E9F2D1",  # 25% green
    "#D3E4A3",  # 50% green
    "#BDD775",  # 75% green
    "#045C64",  # 100% teal
    "#C0D6D8",  # 25% teal
    "#82AEB2",  # 50% teal
    "#43858B",  # 75% teal
    "#4C979F",  # 100% aqua
    "#D2E5E7",  # 25% aqua
    "#A6CBCF",  # 50% aqua
    "#79B1B7",  # 75% aqua
    "#491F53",  # 100% grape
    "#D2C7D4",  # 25% grape
    "#A48FA9",  # 50% grape
    "#77577E",  # 75% grape
    "#E5E5E5",  # light grey
    "#A6A6A6",  # medium grey
    "#3F3F3F",  # dark grey
]
SCILIFE_COLOURS_NOGREY = [
    "#A7C947",  # 100% green
    "#E9F2D1",  # 25% green
    "#D3E4A3",  # 50% green
    "#BDD775",  # 75% green
    "#045C64",  # 100% teal
    "#C0D6D8",  # 25% teal
    "#82AEB2",  # 50% teal
    "#43858B",  # 75% teal
    "#4C979F",  # 100% aqua
    "#D2E5E7",  # 25% aqua
    "#A6CBCF",  # 50% aqua
    "#79B1B7",  # 75% aqua
    "#491F53",  # 100% grape
    "#D2C7D4",  # 25% grape
    "#A48FA9",  # 50% grape
    "#77577E",  # 75% grape
]
SCILIFE_COLOURS_GREYS = [
    "#E5E5E5",  # light grey
    "#A6A6A6",  # medium grey
    "#3F3F3F",  # dark grey
]
# below is with the users unabbreviated (under this is abbreviated, used for pies)
FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_UNABB = {
    "Chalmers University of Technology": "#006C5C",  # https://www.chalmers.se/SiteCollectionDocuments/om%20chalmers%20dokument/Grafisk%20profil/Chalmers_visuella_identitet_1.0_2018.pdf
    "Karolinska Institutet": "#79084A",  # https://ki.se/medarbetare/farger-i-kis-grafiska-profil
    "KTH Royal Institute of Technology": "#1954A6",  # https://intra.kth.se/administration/kommunikation/grafiskprofil/profilfarger-for-print-1.845077
    "Linköping University": "#00B9E7",  # https://insidan.liu.se/kommunikationsstod/grafiskprofil/valkommen/1.750068/Liu_grafisk_manual_12english_selections.pdf
    "Lund University": "#9C6114",  # https://www.staff.lu.se/sites/staff.lu.se/files/profile-colours-eng-a4.png
    "Stockholm University": "#002F5F",  # https://www.su.se/medarbetare/kommunikation/grafisk-manual/f%C3%A4rger-1.362110
    "Swedish University of Agricultural Sciences": "#154734",  # https://internt.slu.se/globalassets/mw/stod-serv/kommmarkn.for/kommunikator/img/colour-palette-eng.pdf
    "Umeå University": "#2A4765",  # https://www.aurora.umu.se/stod-och-service/kommunikation/grafisk-profil/
    "University of Gothenburg": "#004B89",  # https://medarbetarportalen.gu.se/Kommunikation/visuell-identitet/grundprofil/farger/
    "Uppsala University": "#990000",  # https://mp.uu.se/documents/432512/911394/Grafiska+riktlinjerokt2018.pdf/b4c90d05-2cc7-d59e-b0af-c357fb33c84b
    "Örebro University": "#D4021D",  # NOT official - red taken from logo at https://eitrawmaterials.eu/orebro-university/
    "Naturhistoriska Riksmuséet": "#408EBF",  # NOT official I pulled it from the logo at http://www.nrm.se/
    "Healthcare": "#FF99DD",  # pink
    "Industry": "#9FA1A3",  # grey
    "International University": "#91D88C",  # light green
    "Other international organization": "#FFFF99",  # yellow
    "Other Swedish organization": "#B15928",  # burnt orange
    "Other Swedish University": "#FF7C5B",  # red orange
}

# abbreviated to match names given in pies (IAB 2021)
FACILITY_USER_AFFILIATION_COLOUR_OFFICIAL_ABB = {
    "Chalmers": "#006C5C",  # https://www.chalmers.se/SiteCollectionDocuments/om%20chalmers%20dokument/Grafisk%20profil/Chalmers_visuella_identitet_1.0_2018.pdf
    "KI": "#79084A",  # https://ki.se/medarbetare/farger-i-kis-grafiska-profil
    "KTH": "#1954A6",  # https://intra.kth.se/administration/kommunikation/grafiskprofil/profilfarger-for-print-1.845077
    "LiU": "#00B9E7",  # https://insidan.liu.se/kommunikationsstod/grafiskprofil/valkommen/1.750068/Liu_grafisk_manual_12english_selections.pdf
    "LU": "#9C6114",  # https://www.staff.lu.se/sites/staff.lu.se/files/profile-colours-eng-a4.png
    "SU": "#002F5F",  # https://www.su.se/medarbetare/kommunikation/grafisk-manual/f%C3%A4rger-1.362110
    "SLU": "#154734",  # https://internt.slu.se/globalassets/mw/stod-serv/kommmarkn.for/kommunikator/img/colour-palette-eng.pdf
    "UmU": "#2A4765",  # https://www.aurora.umu.se/stod-och-service/kommunikation/grafisk-profil/
    "GU": "#004B89",  # https://medarbetarportalen.gu.se/Kommunikation/visuell-identitet/grundprofil/farger/
    "UU": "#990000",  # https://mp.uu.se/documents/432512/911394/Grafiska+riktlinjerokt2018.pdf/b4c90d05-2cc7-d59e-b0af-c357fb33c84b
    "ÖU": "#D4021D",  # NOT official - red taken from logo at https://eitrawmaterials.eu/orebro-university/
    "NRM": "#408EBF",  # NOT official I pulled it from the logo at http://www.nrm.se/
    "Healthcare": "#FF99DD",  # pink
    "Industry": "#9FA1A3",  # grey
    "Int Univ": "#91D88C",  # light green
    "Other Int Org": "#FFFF99",  # yellow
    "Other Swe Org": "#B15928",  # burnt orange
    "Other Swe Univ": "#FF7C5B",  # red orange
}

# Author of colour gradient stuff: Ben Southgate https://bsou.io/posts/color-gradients-with-python


def hex_to_RGB(hex):
    """ "#FFFFFF" -> [255,255,255]"""
    # Pass 16 to the integer function for change of base
    return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    """[255,255,255] -> "#FFFFFF" """
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#" + "".join(
        ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB]
    )


def color_dict(gradient):
    """Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on"""
    return {
        "hex": [RGB_to_hex(RGB) for RGB in gradient],
        "r": [RGB[0] for RGB in gradient],
        "g": [RGB[1] for RGB in gradient],
        "b": [RGB[2] for RGB in gradient],
    }


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF")"""
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    return color_dict(RGB_list)


def rand_hex_color(num=1):
    """Generate random hex colors, default is one,
    returning a string. If num is greater than
    1, an array of strings is returned."""
    colors = [RGB_to_hex([x * 255 for x in np.random.rand(3)]) for i in range(num)]
    if num == 1:
        return colors[0]
    else:
        return colors


def polylinear_gradient(colors, n):
    """returns a list of colors forming linear gradients between
    all sequential pairs of colors. "n" specifies the total
    number of desired output colors"""
    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col + 1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next[k][1:]
    return gradient_dict
