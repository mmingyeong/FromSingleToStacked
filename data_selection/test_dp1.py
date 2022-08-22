#!/usr/bin/env python
# coding: utf-8

# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-08-01
# @Filename: test_dp1.py
# review data preprocess1 counting runs.py


import glob  # library for file list
import math
import os
import time

import astropy
import h5py  # library for big data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits

np.zeros(0)  # create a arrry of length 0 with all value 0

BAND = "g"

h5f = h5py.File("stacked_%s_info.h5" % BAND, "w")
T0 = T1 = time.time()
# run = '206'
# camcol = 6

cnts_T = np.zeros(0)
for run in ["106", "206"]:
    for camcol in range(1, 7):
        # return file list
        # The element of the file list is the name of each data file.
        FILE_LIST = sorted(
            glob.glob(
                "\\%s\\%s\\cc%d\\*%s%d-*.fit.gz" % (run, BAND, camcol, BAND, camcol)
            )
        )
        RUNS = []
        for i in range(len(FILE_LIST)):
            RUNS.append([])
        # counting run numbers
        for i in range(len(FILE_LIST)):
            # header from 18 to the end == COADD_0 ~ COADD_N
            # Put COADD header information in i-th element of the RUNS list.
            # If N RUNs are COADDed, the list with N+1 elements of COADD information will be the i-th element of the RUNS list.
            # How many COADDs are in the i-th data file
            RUNS[i].append(fits.open(FILE_LIST[i])[0].header[18:])
        cnts = np.ones(len(FILE_LIST))
        for j in range(len(FILE_LIST)):
            # length for COADD number - 1
            for i in range(len(RUNS[j][0]) - 1):
                if (
                    RUNS[j][0][i + 1][5:11] != RUNS[j][0][i][5:11]
                ):  # Check the inside of the list with your own eyes
                    cnts[j] += 1

        # for run in ["106", "206"]:
        # for camcol in range(1, 7):
        # ex. cnts_106_cc1
        h5f.create_dataset("cnts_%s_cc%d" % (run, camcol), data=cnts)
        for i in range(len(FILE_LIST)):
            if cnts[i] == 1:
                print(FILE_LIST[i])

        cnts_T = np.append(cnts_T, cnts)
        print("%0.2f, %0.2f" % (time.time() - T1, time.time() - T0))
        T1 = time.time()

h5f.close()
print("finished")

cnts_T = np.zeros(0)

BAND = "g"
h5f = h5py.File("stacked_%s_info.h5" % BAND, "r")
cnts_T = np.zeros(0)
for run in ["106", "206"]:
    for camcol in range(1, 7):
        cnts = h5f["cnts_%s_cc%d" % (run, camcol)][:]
        cnts_T = np.append(cnts_T, cnts)
h5f.close()
