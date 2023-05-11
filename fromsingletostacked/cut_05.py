#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2023-05-11
# @Filename: cut_05.py
# This will cut the images.

import glob
import os
import shutil
import warnings
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
from astrocut import fits_cut
from astropy import units as u
from astropy import wcs
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import ZScaleInterval
from mpdaf.obj import WCS, Image
from scipy import datasets, ndimage

os.mkdir("data/HighExpCut")
os.mkdir("data/LowExp/LowExpCut")
os.mkdir("data/LowExp/LowExpCut/sqaure")
os.mkdir("data/LowExp/LowExpCut/512")

# First square cut for high exposure image
input_file = "hlsp_udf_hst_acs-wfc_all_f606w_v1_drz_315_rot.fits"
cutout_size = [6950, 6950]

center_coord = SkyCoord(53.1620, -27.7914, unit="deg")
output_dir = "./data"
cutout_file = fits_cut(
    input_file, center_coord, cutout_size, single_outfile=True, output_dir=output_dir
)
high_exp_filename = f"{output_dir}/level5_sqaurecut.fits"
os.rename(cutout_file, high_exp_filename)

# Second 512 cut for high exposure image
fn = get_pkg_data_filename(high_exp_filename[0])
f = fits.open(fn)
w = WCS(f[1].header)
cutout_size = [512, 512]
pix_512_rang = np.arange(256, 6694, 256)

cut_center_coord_list_512 = []
for ra in pix_512_rang:
    for dec in pix_512_rang:
        cut_center_coord = w.pixel_to_world(ra, dec)
        cut_center_coord_list_512.append(cut_center_coord)

for coord in cut_center_coord_list_512:
    cutout_file = fits_cut(
        high_exp_filename, coord, cutout_size, single_outfile=True, output_dir="."
    )
    filename = "{}_{}_cut.fits".format(
        os.path.basename(input_file).rstrip("_sqaurecut.fits"),
        os.path.basename(cutout_file).rstrip("_astrocut.fits"),
    )
    os.rename(cutout_file, filename)
    shutil.move(filename, f"./data/HighExpCut/{filename}")


# first square cut for low exposure image
input_flcs = glob.glob("./data/LowExp/LowExpRot/*.fits")
cutout_size = [6950, 6950]

center_coord = SkyCoord(53.1620, -27.7914, unit="deg")
for input_file in input_flcs:
    cutout_file = fits_cut(
        input_file, center_coord, cutout_size, single_outfile=True, output_dir="."
    )
    filename = "{}_{}.fits".format(
        os.path.basename(input_file).rstrip(".fits"),
        os.path.basename(cutout_file).rstrip(".fits"),
    )
    os.rename(cutout_file, filename)
    filename = "{}_{}_squrecut.fits".format(
        os.path.basename(input_file).rstrip("_315_rot.fits"),
        os.path.basename(cutout_file).rstrip("_astrocut.fits"),
    )
    os.rename(cutout_file, filename)
    shutil.move(filename, f"./data/LowExp/LowExpCut/sqaure/{filename}")

# image cut using astrocut
input_flcs = glob.glob("./data/LowExp/LowExpCut/sqaure/*.fits")
# center_coord = SkyCoord("53.1349957 -27.7809885", unit='deg')
cutout_size = [512, 512]

for coord in cut_center_coord_list_512:
    for input_file in input_flcs:
        cutout_file = fits_cut(
            input_file, coord, cutout_size, single_outfile=True, output_dir="."
        )
        filename = "{}_{}_cut.fits".format(
            os.path.basename(input_file).rstrip(".fits"),
            os.path.basename(cutout_file).rstrip("_astrocut.fits"),
        )
        os.rename(cutout_file, filename)
        shutil.move(filename, f"./data/LowExp/LowExpCut/512/{filename}")

