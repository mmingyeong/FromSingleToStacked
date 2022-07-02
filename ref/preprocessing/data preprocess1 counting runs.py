#!/usr/bin/env python
# coding: utf-8


import glob
import math
import os
import time

import astropy
import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits

np.zeros(0)


BAND = "g"

h5f = h5py.File("D:\\research\\stacked\\ALL\\stacked_%s_info.h5" % BAND, "w")
T0 = T1 = time.time()
# run = '206'
# camcol = 6

cnts_T = np.zeros(0)
for run in ["106", "206"]:
    for camcol in range(1, 7):
        FILE_LIST = sorted(
            glob.glob(
                "D:\\research\\stacked\\ALL\\%s\\%s\\*%s%d-*.fit.gz"
                % (run, BAND, BAND, camcol)
            )
        )
        RUNS = []
        for i in range(len(FILE_LIST)):
            RUNS.append([])
        for i in range(len(FILE_LIST)):
            RUNS[i].append(fits.open(FILE_LIST[i])[0].header[18:])

        cnts = np.ones(len(FILE_LIST))
        for j in range(len(FILE_LIST)):
            for i in range(len(RUNS[j][0]) - 1):
                if RUNS[j][0][i + 1][5:11] != RUNS[j][0][i][5:11]:
                    cnts[j] += 1
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


BAND = "r"
h5f = h5py.File("D:\\research\\stacked\\ALL\\stacked_%s_info.h5" % BAND, "r")
cnts_T = np.zeros(0)
for run in ["106", "206"]:
    for camcol in range(1, 7):
        cnts = h5f["cnts_%s_cc%d" % (run, camcol)][:]
        cnts_T = np.append(cnts_T, cnts)
h5f.close()


len(cnts)


print(cnts.max() - cnts.min() + 1)
plt.rcParams["figure.figsize"] = (10, 8)
plt.hist(cnts_T, bins=38, range=(0.5, 38.5))
# plt.xlim(17,35)


print(cnts.max() - cnts.min() + 1)
plt.rcParams["figure.figsize"] = (10, 8)
plt.hist(cnts_T, bins=38, range=(0.5, 38.5))
# plt.xlim(17,35)


hist_array = plt.hist(cnts_T, bins=40, range=(-0.5, 39.5))[0]
plt.xlim(0, 40)


hist_array[0]


B = np.linspace(0, 39, 40)


C = 0
for i in range(len(B)):
    C += hist_array[i] * B[i]
print(C)
print(C / np.sum(hist_array))
print(np.sqrt(C / np.sum(hist_array)))


C = 0
for i in range(15, 35):
    C += hist_array[i] * B[i]
print(C)
print(C / np.sum(hist_array[15:35]))
print(np.sqrt(C / np.sum(hist_array[15:35])))


AAAA = 28
BBBB = 0
for i in range(len(cnts_T)):
    if cnts_T[i] == AAAA:
        BBBB += 1
print(BBBB)


HDUF = fits.open("E:\\cGAN\\tsField-004207-2-40-0264.fit")


HDUF = fits.open("E:\\cGAN\\tsField-200006-2-2-0294.fit")


HDUF.info()


HDUF[1].header


HDUF[1].data[0][27]


HDUF = fits.open("E:\\cGAN\\asTrans-004207.fit")


HDUF.info()


HDUF[6].header
