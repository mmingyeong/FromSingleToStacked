#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import math
import os
import shutil
import time

import astropy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.io.common
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from scipy.optimize import curve_fit


def LINEAR(X, A, B):
    return A + B * X


# In[3]:


## sky subtraction
T0 = T1 = time.time()
stacked_no = 34
band = "r"
REF_PATH = "D:\\research\\single\\"
REF_LIST = glob.glob(REF_PATH + "stack%d\\*.csv" % stacked_no)
BANDS = ["g", "r", "i"]

for band in BANDS:
    for i in range(len(REF_LIST)):
        REF_NS = REF_LIST[i][-11:-8]
        REF_CC = int(REF_LIST[i][-5])
        SINGLE_LIST = []
        SIN_un_LIST = []
        SIN_up_LIST = []

        if REF_NS == "206":
            try:
                for REF_fields in pd.read_csv(REF_LIST[i], header=None).values[:, 0]:
                    SIN_un_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004207-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields - 30 - 1)
                        )
                    )
                    SINGLE_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004207-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields - 30)
                        )
                    )
                    SIN_up_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004207-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields - 30 + 1)
                        )
                    )
            except pandas.io.common.EmptyDataError:
                print("Empty Data Skipped")
            if len(SINGLE_LIST) != 0 and len(SINGLE_LIST[0]) != 0:
                for j in range(len(SINGLE_LIST)):
                    F_HDU = fits.open(SINGLE_LIST[j][0])
                    FIMGS = np.zeros(3 * 1489 * 2048).reshape(3, 1489, 2048)
                    FIMGS[0] = fits.open(SIN_un_LIST[j][0])[0].data
                    FIMGS[1] = fits.open(SINGLE_LIST[j][0])[0].data
                    FIMGS[2] = fits.open(SIN_up_LIST[j][0])[0].data
                    SKYS = np.zeros(3 * 1489).reshape(3, 1489)
                    for k in range(3):
                        MEAN, MEDIAN, RMS = sigma_clipped_stats(
                            FIMGS[k], sigma=3, iters=5
                        )
                        for l in range(1489):
                            dellist = []
                            for m in range(2048):
                                if (
                                    FIMGS[k][l, m] > MEAN + 2 * RMS
                                    or FIMGS[k][l, m] < MEAN - 2 * RMS
                                ):
                                    dellist.append(i)
                            SKYS[k, l] = np.median(np.delete(FIMGS[k][l, :], dellist))
                    XX = np.linspace(0, 1489 * 3, 1489 * 3)
                    SKY_VECTOR = np.zeros(1489 * 3)
                    INITIAL_GUESS = [MEAN, 0]
                    for k in range(1489):
                        SKY_VECTOR[k] = SKYS[0][k]
                        SKY_VECTOR[1489 + k] = SKYS[1][k]
                        SKY_VECTOR[1489 * 2 + k] = SKYS[2][k]
                    popt, pcov = curve_fit(LINEAR, XX, SKY_VECTOR, p0=INITIAL_GUESS)
                    ZSKY = np.zeros(1489 * 2048).reshape(1489, 2048)
                    # print(LINEAR(XX, *popt))
                    for k in range(1489):
                        ZSKY[k, :] = FIMGS[1][k, :] - LINEAR(XX, *popt)[1489 + k]
                    # print(ZSKY)
                    fits_file = fits.PrimaryHDU(data=ZSKY)
                    # fits_file.header = F_HDU[0].header

                    fits_file.writeto(
                        "D:\\research\\single\\stack%d\\%s\\ZSKY-%s"
                        % (stacked_no, band, SINGLE_LIST[j][0][-21:])
                    )
                    print("%0.2f" % (time.time() - T1), "%0.2f" % (time.time() - T0))
                    T1 = time.time()
        elif REF_NS == "106":
            try:
                for REF_fields in pd.read_csv(REF_LIST[i], header=None).values[:, 0]:
                    SIN_un_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 3 - 1)
                        )
                    )
                    SINGLE_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 3)
                        )
                    )
                    SIN_up_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 3 + 1)
                        )
                    )

                    SIN_un_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 4 - 1)
                        )
                    )
                    SINGLE_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 4)
                        )
                    )
                    SIN_up_LIST.append(
                        glob.glob(
                            "D:\\research\\single\\stack%d\\%s\\fpC-004203-%s%d-*%04d.fit.gz"
                            % (stacked_no, band, band, REF_CC, REF_fields + 4 + 1)
                        )
                    )
            except pandas.io.common.EmptyDataError:
                print("Empty Data Skipped")
            if len(SINGLE_LIST) != 0 and len(SINGLE_LIST[0]) != 0:
                for j in range(len(SINGLE_LIST)):
                    F_HDU = fits.open(SINGLE_LIST[j][0])
                    FIMGS = np.zeros(3 * 1489 * 2048).reshape(3, 1489, 2048)
                    FIMGS[0] = fits.open(SIN_un_LIST[j][0])[0].data
                    FIMGS[1] = fits.open(SINGLE_LIST[j][0])[0].data
                    FIMGS[2] = fits.open(SIN_up_LIST[j][0])[0].data
                    SKYS = np.zeros(3 * 1489).reshape(3, 1489)
                    for k in range(3):
                        MEAN, MEDIAN, RMS = sigma_clipped_stats(
                            FIMGS[k], sigma=3, iters=5
                        )
                        for l in range(1489):
                            dellist = []
                            for m in range(2048):
                                if (
                                    FIMGS[k][l, m] > MEAN + 2 * RMS
                                    or FIMGS[k][l, m] < MEAN - 2 * RMS
                                ):
                                    dellist.append(i)
                            SKYS[k, l] = np.median(np.delete(FIMGS[k][l, :], dellist))
                    XX = np.linspace(0, 1489 * 3, 1489 * 3)
                    SKY_VECTOR = np.zeros(1489 * 3)
                    INITIAL_GUESS = [MEAN, 0]
                    for k in range(1489):
                        SKY_VECTOR[k] = SKYS[0][k]
                        SKY_VECTOR[1489 + k] = SKYS[1][k]
                        SKY_VECTOR[1489 * 2 + k] = SKYS[2][k]
                    popt, pcov = curve_fit(
                        LINEAR,
                        XX,
                        np.asarray(SKY_VECTOR).reshape(1489 * 3),
                        p0=INITIAL_GUESS,
                    )
                    ZSKY = np.zeros(1489 * 2048).reshape(1489, 2048)
                    for k in range(1489):
                        ZSKY[k, :] = FIMGS[1][k, :] - LINEAR(XX, *popt)[1489 + k]
                    fits_file = fits.PrimaryHDU(data=ZSKY)
                    # fits_file.header = F_HDU[0].header

                    fits_file.writeto(
                        "D:\\research\\single\\stack%d\\%s\\ZSKY-%s"
                        % (stacked_no, band, SINGLE_LIST[j][0][-21:])
                    )
                    print("%0.2f" % (time.time() - T1), "%0.2f" % (time.time() - T0))
                    T1 = time.time()
print("finished")

# In[2]:


### initial (r-band)

stacked_no = 34
band = "r"
STACKED_LIST = sorted(
    glob.glob("D:\\research\\stacked\\stack%d\\%s\\*.fit.gz" % (stacked_no, band))
)
SINGLE_LIST = sorted(
    glob.glob("D:\\research\\single\\stack%d\\%s\\ZSKY*.fit.gz" % (stacked_no, band))
)
SIN_HDR_LIST = sorted(
    glob.glob("D:\\research\\single\\stack%d\\%s\\ZSKY*.fit.gz" % (stacked_no, band))
)

for i in range(len(SIN_HDR_LIST)):
    SIN_HDR_LIST[i] = SIN_HDR_LIST[i][:-26] + "fpC" + SIN_HDR_LIST[i][-22:]

# In[3]:


RA_STA, DEC_STA = list(range(len(STACKED_LIST))), list(range(len(STACKED_LIST)))
for i in range(len(STACKED_LIST)):
    RA_STA[i] = fits.open(STACKED_LIST[i])[0].header[13]
    DEC_STA[i] = fits.open(STACKED_LIST[i])[0].header[12]

RA_SIN = list(range(len(SIN_HDR_LIST)))
DEC_SIN = list(range(len(SIN_HDR_LIST)))
for i in range(len(SIN_HDR_LIST)):
    RA_SIN[i] = fits.open(SIN_HDR_LIST[i])[0].header[-6]
    DEC_SIN[i] = fits.open(SIN_HDR_LIST[i])[0].header[-5]

# In[42]:


print(RA_SIN[3], RA_STA[6])


# In[4]:


pix = 260
OL = 130
dpp = 0.00011  # degree per pixel
dcrp = 745  # distance from center ra pixel
dcdp = 1025  # distance from center dec pixel
no_fields = len(STACKED_LIST)
decstart_STA = np.zeros(no_fields)
decstart_SIN = np.zeros(no_fields)
row = np.zeros(no_fields)
for i in range(no_fields):
    DEC_uplim = int(
        dcdp
        + abs(
            DEC_STA[i]
            - pd.read_csv(
                "D:\\research\\stacked\\stack%d_%s_cc%s.csv"
                % (stacked_no, STACKED_LIST[i][-21], STACKED_LIST[i][-13])
            )
            .values[:, -1]
            .min()
        )
        / dpp
    )
    DEC_unlim = 1 + int(
        dcdp
        - abs(
            DEC_STA[i]
            - pd.read_csv(
                "D:\\research\\stacked\\stack%d_%s_cc%s.csv"
                % (stacked_no, STACKED_LIST[i][-21], STACKED_LIST[i][-13])
            )
            .values[:, -2]
            .max()
        )
        / dpp
    )
    DEC_cent = (DEC_uplim + DEC_unlim) / 2
    DEC_range = DEC_uplim - DEC_unlim
    row[i] = (DEC_range - pix) // (pix - OL)
    decstart_STA[i] = int(
        round(DEC_unlim + (DEC_range - (pix + (row[i] - 1) * (pix - OL))) / 2)
    )
    decstart_SIN[i] = int(decstart_STA[i] + round((DEC_STA[i] - DEC_SIN[i]) / dpp))


# In[5]:


rastart_STA = np.zeros(no_fields)
rastart_SIN = np.zeros(no_fields)
col = np.zeros(no_fields)
for i in range(no_fields):
    RA_range = 0
    RA_range = int(abs((RA_STA[i] - 744 * dpp) - (RA_SIN[i] + 744.5 * dpp)) / dpp)
    col[i] = (RA_range - pix) // (pix - OL)
    rastart_STA[i] = int(round((RA_range - (pix + (col[i] - 1) * (pix - OL))) / 2))
    rastart_SIN[i] = int(rastart_STA[i] + round((RA_STA[i] - RA_SIN[i]) / dpp))

# In[6]:


STA_IMGS = np.zeros(len(STACKED_LIST) * 1489 * 2048).reshape(
    len(STACKED_LIST), 1489, 2048
)
SIN_IMGS = np.zeros(len(SINGLE_LIST) * 1489 * 2048).reshape(
    len(SINGLE_LIST), 1489, 2048
)
for i in range(len(STACKED_LIST)):
    STA_IMGS[i] = fits.open(STACKED_LIST[i])[0].data
for i in range(len(SINGLE_LIST)):
    SIN_IMGS[i] = fits.open(SINGLE_LIST[i])[0].data

## init end

# In[8]:


OUTPUT_STA = np.zeros(int(no_fields * col.max() * row.max() * pix * pix)).reshape(
    no_fields, int(col.max()), int(row.max()), pix, pix
)
OUTPUT_SIN = np.zeros(int(no_fields * col.max() * row.max() * pix * pix)).reshape(
    no_fields, int(col.max()), int(row.max()), pix, pix
)


for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            OUTPUT_STA[k, i, j] = STA_IMGS[k][
                int(rastart_STA[k] + (i * pix))
                - (OL * i) : int(rastart_STA[k] + ((i + 1) * pix))
                - (OL * i),
                int(decstart_STA[k] + (j * pix))
                - (OL * j) : int(decstart_STA[k] + ((j + 1) * pix))
                - (OL * j),
            ]
            OUTPUT_SIN[k, i, j] = SIN_IMGS[k][
                int(rastart_SIN[k] + (i * pix))
                - (OL * i) : int(rastart_SIN[k] + ((i + 1) * pix))
                - (OL * i),
                int(decstart_SIN[k] + (j * pix))
                - (OL * j) : int(decstart_SIN[k] + ((j + 1) * pix))
                - (OL * j),
            ]
            # print(k,i,j)


# In[8]:


## for low memory
for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            if (
                STA_IMGS[k][
                    int(rastart_STA[k] + (i * pix))
                    - (OL * i) : int(rastart_STA[k] + ((i + 1) * pix))
                    - (OL * i),
                    int(decstart_STA[k] + (j * pix))
                    - (OL * j) : int(decstart_STA[k] + ((j + 1) * pix))
                    - (OL * j),
                ].max()
                > 0
            ):
                fits_file = fits.PrimaryHDU(
                    data=STA_IMGS[k][
                        int(rastart_STA[k] + (i * pix))
                        - (OL * i) : int(rastart_STA[k] + ((i + 1) * pix))
                        - (OL * i),
                        int(decstart_STA[k] + (j * pix))
                        - (OL * j) : int(decstart_STA[k] + ((j + 1) * pix))
                        - (OL * j),
                    ]
                )
                fits_file.writeto(
                    "D:\\research\\cGAN\\stack%d\\stacked\\%s\\STA-%s-%02d%02d.fit"
                    % (stacked_no, band, STACKED_LIST[k][-21:-7], j + 1, i + 1)
                )

for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            if (
                STA_IMGS[k][
                    int(rastart_STA[k] + (i * pix))
                    - (OL * i) : int(rastart_STA[k] + ((i + 1) * pix))
                    - (OL * i),
                    int(decstart_STA[k] + (j * pix))
                    - (OL * j) : int(decstart_STA[k] + ((j + 1) * pix))
                    - (OL * j),
                ].max()
                > 0
            ):
                fits_file = fits.PrimaryHDU(
                    data=SIN_IMGS[k][
                        int(rastart_SIN[k] + (i * pix))
                        - (OL * i) : int(rastart_SIN[k] + ((i + 1) * pix))
                        - (OL * i),
                        int(decstart_SIN[k] + (j * pix))
                        - (OL * j) : int(decstart_SIN[k] + ((j + 1) * pix))
                        - (OL * j),
                    ]
                )
                fits_file.writeto(
                    "D:\\research\\cGAN\\stack%d\\single\\%s\\SIN-%s-%02d%02d.fit"
                    % (stacked_no, band, SINGLE_LIST[k][-21:-7], j + 1, i + 1)
                )


# In[8]:


for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            if OUTPUT_STA[k, i, j].max() > 0:
                fits_file = fits.PrimaryHDU(data=OUTPUT_STA[k, i, j])

                fits_file.writeto(
                    "E:\\cGAN\\STNUM\\stacked\\stack%d\\%s\\STA-%s-%02d%02d.fit"
                    % (stacked_no, band, STACKED_LIST[k][-21:-7], j + 1, i + 1)
                )

for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            if OUTPUT_STA[k, i, j].max() > 0:
                fits_file = fits.PrimaryHDU(data=OUTPUT_SIN[k, i, j])

                fits_file.writeto(
                    "E:\\cGAN\\STNUM\\single\\stack%d\\%s\\SIN-%s-%02d%02d.fit"
                    % (stacked_no, band, SINGLE_LIST[k][-21:-7], j + 1, i + 1)
                )


# In[19]:


###### for other bands(g-, i-bnad)
band = "g"
DATA = "single"

if DATA == "single":
    SINGLE_LIST = sorted(
        glob.glob(
            "D:\\research\\single\\stack%d\\%s\\ZSKY*.fit.gz" % (stacked_no, band)
        )
    )
    SIN_HDR_LIST = sorted(
        glob.glob(
            "D:\\research\\single\\stack%d\\%s\\ZSKY*.fit.gz" % (stacked_no, band)
        )
    )

    for i in range(len(SIN_HDR_LIST)):
        SIN_HDR_LIST[i] = SIN_HDR_LIST[i][:-26] + "fpC" + SIN_HDR_LIST[i][-22:]

    RA_SIN = list(range(len(SIN_HDR_LIST)))
    DEC_SIN = list(range(len(SIN_HDR_LIST)))
    for i in range(len(SIN_HDR_LIST)):
        RA_SIN[i] = fits.open(SIN_HDR_LIST[i])[0].header[-6]
        DEC_SIN[i] = fits.open(SIN_HDR_LIST[i])[0].header[-5]


elif DATA == "stacked":
    SINGLE_LIST = sorted(
        glob.glob("D:\\research\\stacked\\stack%d\\%s\\*.fit.gz" % (stacked_no, band))
    )

    RA_SIN, DEC_SIN = list(range(len(SINGLE_LIST))), list(range(len(SINGLE_LIST)))
    for i in range(len(SINGLE_LIST)):
        RA_SIN[i] = fits.open(SINGLE_LIST[i])[0].header[13]
        DEC_SIN[i] = fits.open(SINGLE_LIST[i])[0].header[12]


# In[20]:


decstart_SIN = np.zeros(no_fields)
rastart_SIN = np.zeros(no_fields)
for i in range(no_fields):
    decstart_SIN[i] = int(decstart_STA[i] + round((DEC_STA[i] - DEC_SIN[i]) / dpp))
for i in range(no_fields):
    rastart_SIN[i] = int(rastart_STA[i] + round((RA_STA[i] - RA_SIN[i]) / dpp))

# In[21]:


SIN_IMGS = np.zeros(len(SINGLE_LIST) * 1489 * 2048).reshape(
    len(SINGLE_LIST), 1489, 2048
)
for i in range(len(SINGLE_LIST)):
    SIN_IMGS[i] = fits.open(SINGLE_LIST[i])[0].data


# In[17]:


## much memory
OUTPUT_SIN = np.zeros(int(no_fields * col.max() * row.max() * pix * pix)).reshape(
    no_fields, int(col.max()), int(row.max()), pix, pix
)

for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            OUTPUT_SIN[k, i, j] = SIN_IMGS[k][
                int(rastart_SIN[k] + (i * pix))
                - (OL * i) : int(rastart_SIN[k] + ((i + 1) * pix))
                - (OL * i),
                int(decstart_SIN[k] + (j * pix))
                - (OL * j) : int(decstart_SIN[k] + ((j + 1) * pix))
                - (OL * j),
            ]
            # print(k,i,j)


# In[22]:


SAVE_PATH = "D:\\research\\cGAN\\stack%d\\%s\\%s\\" % (stacked_no, DATA, band)
for k in range(no_fields):
    for j in range(int(row[k])):
        for i in range(int(col[k])):
            if (
                STA_IMGS[k][
                    int(rastart_STA[k] + (i * pix))
                    - (OL * i) : int(rastart_STA[k] + ((i + 1) * pix))
                    - (OL * i),
                    int(decstart_STA[k] + (j * pix))
                    - (OL * j) : int(decstart_STA[k] + ((j + 1) * pix))
                    - (OL * j),
                ].max()
                > 0
            ):
                fits_file = fits.PrimaryHDU(
                    data=SIN_IMGS[k][
                        int(rastart_SIN[k] + (i * pix))
                        - (OL * i) : int(rastart_SIN[k] + ((i + 1) * pix))
                        - (OL * i),
                        int(decstart_SIN[k] + (j * pix))
                        - (OL * j) : int(decstart_SIN[k] + ((j + 1) * pix))
                        - (OL * j),
                    ]
                )
                if DATA == "single":
                    fits_file.writeto(
                        SAVE_PATH
                        + "SIN-%s-%02d%02d.fit" % (SINGLE_LIST[k][-21:-7], j + 1, i + 1)
                    )
                elif DATA == "stacked":
                    fits_file.writeto(
                        SAVE_PATH
                        + "STA-%s-%02d%02d.fit" % (SINGLE_LIST[k][-21:-7], j + 1, i + 1)
                    )


# In[12]:


SINGLE_LIST[0][-21:-7]

# In[ ]:
