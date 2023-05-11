#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2023-05-11
# @Filename: filtering_06.py
# This will filter bad images and split datasets.

import glob
import os
import shutil

import numpy as np
from astropy.io import fits
from sklearn.model_selection import train_test_split

input_flcs = glob.glob("data/LowExp/LowExpCut/512/*.fits")
HighExp_flcs = glob.glob("data/HighExpCut/*.fits")

for file in input_flcs:
    # check output image
    hdu = fits.open(file)
    data = hdu[0].data
    zero = 0

    for value in data:
        indic = np.isnan(value)
        if np.any(indic) == True:
            os.remove(file)
        else:
            pass

for file in HighExp_flcs:
    # check output image
    hdu = fits.open(file)
    data = hdu[0].data
    zero = 0

    for value in data:
        indic = np.isnan(value)
        if np.any(indic) == True:
            os.remove(file)
        else:
            pass

os.mkdir("dataset")
os.mkdir("dataset/Test")
os.mkdir("dataset/Test/Input")
os.mkdir("dataset/Train")
os.mkdir("dataset/Train/Input")
os.mkdir("dataset/Train/Target")

Train_input, Test_input = train_test_split(input_flcs)

for file in Train_input:
    shutil.move(file, "dataset/Train/Input")

for file in Test_input:
    shutil.move(file, "dataset/Test/Input")

for file in HighExp_flcs:
    shutil.move(file, "dataset/Train/Target")
