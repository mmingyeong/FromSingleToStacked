#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-07-12
# @Filename: fits_view.py

# handling fits file
# reference:
# https://himbopsa.tistory.com/33

# DTYPE
# 100006 == 106 == South strip
# 200006 == 206 == North strip

# File Format: FITS image
# Name: fpC-rrrrrr-bc-ffff.fit
# where rrrrrr is the imaging run number,
# b is the filter used (u, g, r, i, or z),
# c is camera column (1-6)
# ffff is the field number within the run.

# The science and weight images are named ‘S82 xxy zzz.fits’ and
# ‘S82 xxy zzz.wht.fits’,
# where ‘xx’ is the scanline number from 01 to 12
# south camcol 01-06 == scanline 01-06
# north camcol 01-06 == scanline 07-12
# ‘y’ is the filter
# ‘zzz’ is the region number from 001 to 401.


import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np


class handling_fits:
    """handling the fits file"""

    def __init__(self, file_name: str):
        self.file = fits.open(file_name)
        self.data = self.file[0].data

    def view_image(self):
        """View the image from the fits file"""
        image = np.array(self.data)

        max_value = np.percentile(image, 99.8)
        min_value = np.percentile(image, 15)

        plt.figure(figsize=(8, 6))
        plt.imshow(image, cmap="gray", vmax=max_value, vmin=min_value, origin="lower")
        # default
        # plt.xlim(1000,1750)
        # plt.ylim(300,1000)
        plt.xlim(0, 2050)
        plt.ylim(0, 1500)
        plt.show()

    def view_header(self):
        """View the header information from the fits file"""
        header = self.file[0].header
        self.file.info()
        print(header)
        # keywords = header.keys()
        # print(keywords)


single_image_file_name = "sample_data/fpC-001045-g1-0062.fit"
stacked_image_byannis_file_name = "sample_data/fpC-100006-g1-0062.fit"
COADD_0_image_file_name = "sample_data/fpC-004930-g1-0052.fit"
newfirm_image_file_name = "sample_data/20071110_A01c.fits"
stacked_image_byjiangs_file_name = "sample_data/S82_01g_001.fits"
weight_image = "sample_data/S82_01g_001.wht.fits"

f = handling_fits(COADD_0_image_file_name)
# f.view_header()
f.view_image()
