#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2023-05-11
# @Filename: rotate_04.py
# This will rotate the images.

import glob
import os
import shutil
import warnings

import numpy as np
from astrocut import fits_cut
from astropy import units as u
from astropy import wcs
from astropy.coordinates import SkyCoord
from astropy.io import fits
from mpdaf.obj import WCS, Image

# rotation for high exposure image
input_file = "data/hlsp_udf_hst_acs-wfc_all_f606w_v1_drz.fits"
angle = 315

hdu = fits.open(input_file)
data = hdu[0].data
hdu_header = fits.Header(hdu[0].header, copy=True)
img_wcs = WCS(hdu_header)
img_data = np.array(data)
ima = Image(data=img_data, wcs=img_wcs, data_header=hdu_header)

img_theta = ima.rotate(angle, reshape=True)
filename = "{}_{}_rot.fits".format(os.path.basename(input_file).rstrip(".fits"), angle)
img_theta.write(filename=filename)
shutil.move(filename, f"./data/{filename}")

# rotation for low exposure image
input_flcs = glob.glob("./LowExp/*.fits")
angle = 315
os.mkdir("data/LowExp/LowExpRot")

for input_file in input_flcs:
    hdu = fits.open(input_file)
    data = hdu[1].data
    hdu_header = fits.Header(hdu[1].header, copy=True)
    img_wcs = WCS(hdu_header)
    img_data = np.array(data)
    ima = Image(data=img_data, wcs=img_wcs, data_header=hdu_header)

    img_theta = ima.rotate(angle, reshape=True)
    filename = "{}_{}_rot.fits".format(
        os.path.basename(input_file).rstrip("_drc.fits"), angle
    )
    img_theta.write(filename=filename)
    shutil.move(filename, f"./LowExpRot/{filename}")

if os.path.exists("./data/LowExp/LowExpRot/*_315_rot.fits"):
    print("exists")
    pass
