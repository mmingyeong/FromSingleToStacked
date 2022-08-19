#!/usr/bin/env python
# coding: utf-8

# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-08-01
# @Filename: rv_dp2.py
# review data preprocess2 download single & check most frequent run & dec boundary.py

import glob
import math
import os
import time

import astropy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits


T0 = T1 = time.time()
run = "206"
BAND = "g"
camcol = 6
FILE_LIST = sorted(
    glob.glob(
        "D:\\research\\stacked\\ALL\\%s\\%s\\*%s%d*.fit.gz" % (run, BAND, BAND, camcol)
    )
)
FIELDS_HDR = []
RUNS = []
for i in range(len(FILE_LIST)):
    FIELDS_HDR.append([])
    RUNS.append([])
for i in range(len(FILE_LIST)):
    FIELDS_HDR[i].append(fits.open(FILE_LIST[i])[0].header[18:])
cnts = np.ones(len(FILE_LIST))
for j in range(len(FILE_LIST)):
    RUNS[j].append(int(FIELDS_HDR[j][0][0][5:11]))
    for i in range(len(FIELDS_HDR[j][0]) - 1):
        if FIELDS_HDR[j][0][i + 1][5:11] != FIELDS_HDR[j][0][i][5:11]:
            cnts[j] += 1
            RUNS[j].append(int(FIELDS_HDR[j][0][i + 1][5:11]))

print("%0.2f, %0.2f" % (time.time() - T1, time.time() - T0))
T1 = time.time()
print("finished")

# download the single image file

stacked_no = 34

if run == "206":
    single_run = "4207"
elif run == "106":
    single_run = "4203"
# Create the command shell file for a single image file with the corresponding condition
fg = open(
    "D:\\research\\single\\stack%d\\g\\down_g%s_cc%d.sh"
    % (stacked_no, single_run, camcol),
    "w",
)
fr = open(
    "D:\\research\\single\\stack%d\\r\\down_r%s_cc%d.sh"
    % (stacked_no, single_run, camcol),
    "w",
)
fi = open(
    "D:\\research\\single\\stack%d\\i\\down_i%s_cc%d.sh"
    % (stacked_no, single_run, camcol),
    "w",
)

# where is u, z band...? -> because bad quality

flist = open(
    "D:\\research\\single\\stack%d\\flist_%s_%s_cc%d.csv"
    % (stacked_no, run, BAND, camcol),
    "w",
)

DOWN_LIST = []
for i in range(len(RUNS)):
    # if RUN Number == maximum stacked number
    if len(RUNS[i]) == stacked_no:
        # print(i+62)
        if run == "206":
            DOWN_LIST.append(i + 62 - 30 - 1)
            DOWN_LIST.append(i + 62 - 30)
            DOWN_LIST.append(i + 62 - 30 + 1)
        elif run == "106":
            DOWN_LIST.append(i + 62 + 3 - 1)
            DOWN_LIST.append(i + 62 + 4 - 1)
            DOWN_LIST.append(i + 62 + 3)
            DOWN_LIST.append(i + 62 + 4)
            DOWN_LIST.append(i + 62 + 3 + 1)
            DOWN_LIST.append(i + 62 + 4 + 1)
        # the field number within run of the image file to be downloaded
        flist.write("%d\n" % (i + 62))
DOWN_LIST = sorted(list(set(DOWN_LIST)))

# for i in range(len(DOWN_LIST)):
#    fg.write('axel -a -n 3 http://das.sdss.org/raw/%s/40/corr/%d/fpC-%06d-g%d-%04d.fit.gz\n' % (single_run, camcol, int(single_run), camcol, DOWN_LIST[i]))
#    fr.write('axel -a -n 3 http://das.sdss.org/raw/%s/40/corr/%d/fpC-%06d-r%d-%04d.fit.gz\n' % (single_run, camcol, int(single_run), camcol, DOWN_LIST[i]))
#    fi.write('axel -a -n 3 http://das.sdss.org/raw/%s/40/corr/%d/fpC-%06d-i%d-%04d.fit.gz\n' % (single_run, camcol, int(single_run), camcol, DOWN_LIST[i]))

fg.close()
fr.close()
fi.close()
flist.close()


stacked_no = 34

for stacked_no in [34]:
    for run in ["206"]:
        if run == "206":
            single_run = "4207"
            CAMCOLS = range(3, 6)
        elif run == "106":
            single_run = "4203"
            CAMCOLS = range(2, 7)
        for camcol in CAMCOLS:
            f_g = pd.read_csv(
                "D:\\research\\single\\stack%d\\g\\down_g%s_cc%d.sh"
                % (stacked_no, single_run, camcol),
                sep="\s+",
                header=None,
            )
            for i in range(len(f_g)):
                # f_r values change
                # why??
                f_g.values[i, 1] = f_g.values[i, 1][:-14] + "r" + f_g.values[i, 1][-13:]
            fr = open(
                "D:\\research\\single\\stack%d\\r\\down_r%s_cc%d.sh"
                % (stacked_no, single_run, camcol),
                "w",
            )
            for i in range(len(f_g)):
                fr.write("axel -a -n 3 %s\n" % (f_g.values[i, 1]))
            fr.close()


# Coadded Field check

T0 = T1 = time.time()

stacked_no = 34
FILE_LIST_N = sorted(
    glob.glob("D:\\research\\stacked\\stack%d\\r\\*200006*.fit.gz" % (stacked_no))
)
FILE_LIST_S = sorted(
    glob.glob("D:\\research\\stacked\\stack%d\\r\\*100006*.fit.gz" % (stacked_no))
)

FIELDS_HDR_N = []
FIELDS_HDR_S = []

RUNS_N = []
RUNS_S = []

for i in range(len(FILE_LIST_N)):
    FIELDS_HDR_N.append([])
    RUNS_N.append([])

for i in range(len(FILE_LIST_N)):
    FIELDS_HDR_N[i].append(fits.open(FILE_LIST_N[i])[0].header[18:])
cnts_N = np.ones(len(FILE_LIST_N))
for j in range(len(FILE_LIST_N)):
    RUNS_N[j].append(int(FIELDS_HDR_N[j][0][0][5:11]))
    for i in range(len(FIELDS_HDR_N[j][0]) - 1):
        if FIELDS_HDR_N[j][0][i + 1][5:11] != FIELDS_HDR_N[j][0][i][5:11]:
            cnts_N[j] += 1
            RUNS_N[j].append(int(FIELDS_HDR_N[j][0][i + 1][5:11]))

for i in range(len(FILE_LIST_S)):
    FIELDS_HDR_S.append([])
    RUNS_S.append([])

for i in range(len(FILE_LIST_S)):
    FIELDS_HDR_S[i].append(fits.open(FILE_LIST_S[i])[0].header[18:])
cnts_S = np.ones(len(FILE_LIST_S))
for j in range(len(FILE_LIST_S)):
    RUNS_S[j].append(int(FIELDS_HDR_S[j][0][0][5:11]))
    for i in range(len(FIELDS_HDR_S[j][0]) - 1):
        if FIELDS_HDR_S[j][0][i + 1][5:11] != FIELDS_HDR_S[j][0][i][5:11]:
            cnts_S[j] += 1
            RUNS_S[j].append(int(FIELDS_HDR_S[j][0][i + 1][5:11]))

print("%0.2f, %0.2f" % (time.time() - T1, time.time() - T0))
T1 = time.time()
print("finished")


from collections import Counter

RUNS_for_count_N = []
for i in range(len(RUNS_N)):
    for j in range(len(RUNS_N[i])):
        RUNS_for_count_N.append(RUNS_N[i][j])

RUNS_for_count_S = []
for i in range(len(RUNS_S)):
    for j in range(len(RUNS_S[i])):
        RUNS_for_count_S.append(RUNS_S[i][j])



Counter(RUNS_for_count_N).most_common()[0][0]


camcol = 1
print(
    "(P.camcol = %d and P.run = %d and P.decmin > -400 and P.decmin < 400 and P.decmax > -400 and P.decmax < 400)"
    % (camcol, sorted(list(set(RUNS_for_count_N)))[0])
)
for i in range(1, len(sorted(list(set(RUNS_for_count_N))))):
    print(
        "  or (P.camcol = %d and P.run = %d and P.decmin > -400 and P.decmin < 400 and P.decmax > -400 and P.decmax < 400)"
        % (camcol, sorted(list(set(RUNS_for_count_N)))[i])
    )


stack34_N_cc1 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc1.csv" % stacked_no)
stack34_N_cc2 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc2.csv" % stacked_no)
stack34_N_cc3 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc3.csv" % stacked_no)
stack34_N_cc4 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc4.csv" % stacked_no)
stack34_N_cc5 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc5.csv" % stacked_no)
stack34_N_cc6 = pd.read_csv("D:\\research\\stacked\\stack%d_2_cc6.csv" % stacked_no)


print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc1.values[:, -1].max(),
        stack34_N_cc1.values[:, -1].min(),
        stack34_N_cc1.values[:, -1].max() - stack34_N_cc1.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc1.values[:, -2].max(),
        stack34_N_cc1.values[:, -2].min(),
        stack34_N_cc1.values[:, -2].max() - stack34_N_cc1.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc2.values[:, -1].max(),
        stack34_N_cc2.values[:, -1].min(),
        stack34_N_cc2.values[:, -1].max() - stack34_N_cc2.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc2.values[:, -2].max(),
        stack34_N_cc2.values[:, -2].min(),
        stack34_N_cc2.values[:, -2].max() - stack34_N_cc2.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc3.values[:, -1].max(),
        stack34_N_cc3.values[:, -1].min(),
        stack34_N_cc3.values[:, -1].max() - stack34_N_cc3.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc3.values[:, -2].max(),
        stack34_N_cc3.values[:, -2].min(),
        stack34_N_cc3.values[:, -2].max() - stack34_N_cc3.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc4.values[:, -1].max(),
        stack34_N_cc4.values[:, -1].min(),
        stack34_N_cc4.values[:, -1].max() - stack34_N_cc4.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc4.values[:, -2].max(),
        stack34_N_cc4.values[:, -2].min(),
        stack34_N_cc4.values[:, -2].max() - stack34_N_cc4.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc5.values[:, -1].max(),
        stack34_N_cc5.values[:, -1].min(),
        stack34_N_cc5.values[:, -1].max() - stack34_N_cc5.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc5.values[:, -2].max(),
        stack34_N_cc5.values[:, -2].min(),
        stack34_N_cc5.values[:, -2].max() - stack34_N_cc5.values[:, -2].min(),
    )
)


print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc1.values[:, -1].max(),
        stack34_N_cc1.values[:, -1].min(),
        stack34_N_cc1.values[:, -1].max() - stack34_N_cc1.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc1.values[:, -2].max(),
        stack34_N_cc1.values[:, -2].min(),
        stack34_N_cc1.values[:, -2].max() - stack34_N_cc1.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc2.values[:, -1].max(),
        stack34_N_cc2.values[:, -1].min(),
        stack34_N_cc2.values[:, -1].max() - stack34_N_cc2.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc2.values[:, -2].max(),
        stack34_N_cc2.values[:, -2].min(),
        stack34_N_cc2.values[:, -2].max() - stack34_N_cc2.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc3.values[:, -1].max(),
        stack34_N_cc3.values[:, -1].min(),
        stack34_N_cc3.values[:, -1].max() - stack34_N_cc3.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc3.values[:, -2].max(),
        stack34_N_cc3.values[:, -2].min(),
        stack34_N_cc3.values[:, -2].max() - stack34_N_cc3.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc4.values[:, -1].max(),
        stack34_N_cc4.values[:, -1].min(),
        stack34_N_cc4.values[:, -1].max() - stack34_N_cc4.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc4.values[:, -2].max(),
        stack34_N_cc4.values[:, -2].min(),
        stack34_N_cc4.values[:, -2].max() - stack34_N_cc4.values[:, -2].min(),
    )
)

print(
    "%0.5f, %0.5f, %0.7f"
    % (
        stack34_N_cc5.values[:, -1].max(),
        stack34_N_cc5.values[:, -1].min(),
        stack34_N_cc5.values[:, -1].max() - stack34_N_cc5.values[:, -1].min(),
    )
)
print(
    "%0.5f, %0.5f, %0.7f\n"
    % (
        stack34_N_cc5.values[:, -2].max(),
        stack34_N_cc5.values[:, -2].min(),
        stack34_N_cc5.values[:, -2].max() - stack34_N_cc5.values[:, -2].min(),
    )
)



stack34_N_cc1 = []
for i in range(len(stack34_N)):
    if stack34_N.values[i, 3] == 1:
        stack34_N_cc1.append(stack34_N.values[i])

# delete stack34_N_cc1
del stack34_N_cc1
