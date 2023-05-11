#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2023-05-11
# @Filename: combine_03.py
# This will combine the images into drizzled image.

# All imports needed through out this notebook are included at the beginning.

import glob
import os
import shutil

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.table import Table
from astropy.units import Quantity
from astroquery.gaia import Gaia
from ccdproc import ImageFileCollection
from drizzlepac import astrodrizzle, tweakreg

input_flcs = glob.glob("data/flc_f606w/*flc.fits")
visit_nums = []

file_name = "visitnums.txt"
file = open(file_name, "r")
while True:
    line = file.readline()
    visit_nums.append(line)
    if not line:
        break

collec = ImageFileCollection(
    "data/flc_f606w/",
    glob_include="*flc.fits",
    ext=0,
    keywords=[
        "targname",
        "ra_targ",
        "dec_targ",
        "filter",
        "exptime",
        "postarg1",
        "postarg2",
    ],
)

table = collec.summary
table["exptime"].format = "7.1f"
table["ra_targ"].format = "7.7f"
table["dec_targ"].format = "7.7f"
table["postarg1"].format = "7.2f"
table["postarg2"].format = "7.2f"
table

RA = table["ra_targ"][0]
Dec = table["dec_targ"][0]
print(RA)

coord = SkyCoord(ra=RA, dec=Dec, unit=(u.deg, u.deg))
radius = Quantity(6.0, u.arcmin)

gaia_query = Gaia.query_object_async(coordinate=coord, radius=radius)
reduced_query = gaia_query["ra", "dec", "phot_g_mean_mag"]
reduced_query.write("gaia.cat", format="ascii.commented_header", overwrite=True)

refcat = "gaia.cat"
cw = 3.5  # Set to two times the FWHM of the PSF.
wcsname = "Gaia"  # Specify the WCS name for this alignment

# Final run with ideal parameters, updatehdr = True

for visit_num in visit_nums:
    input = glob.glob(f"data/flc_f606w/j8m8{visit_num}*.fits")

    tweakreg.TweakReg(
        input,
        imagefindcfg={
            "threshold": 10,
            "conv_width": 3.5,
            "peakmax": 7000,
        },
        fitgeometry="general",
        interactive=False,
        shiftfile=False,
        updatehdr=False,
        see2dplot=False,  # See 2d histogram for initial offset?
        wcsname=wcsname,  # Give our WCS a new name
        reusename=True,
    )

    astrodrizzle.AstroDrizzle(
        input,
        output=f"{visit_num}_4stacked",
        skymethod="localmin",
        combine_type="mean",
        driz_sep_bits="4096",
        final_bits="4096",
        final_pixfrac=0.6,
        final_rot=0.0,
        final_scale=0.03,
        context=False,
        build=True,
        preserve=False,
        clean=True,
    )

input_flcs = glob.glob("./*_4stacked.fits")
os.mkdir("data/LowExp")
for file in input_flcs:
    shutil.move(file, f"./data/LowExp/{file}")
