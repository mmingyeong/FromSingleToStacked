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

# In[8]:


stacked_no = 34
band = "g"
REF_PATH = "D:\\research\\single\\"
REF_LIST = glob.glob(REF_PATH + "stack%d\\*.csv" % stacked_no)

for i in range(len(REF_LIST)):
    REF_NS = REF_LIST[i][-11:-8]
    REF_CC = int(REF_LIST[i][-5])
    MOVE_LIST = []
    try:
        for REF_fields in pd.read_csv(REF_LIST[i], header=None).values[:, 0]:
            MOVE_LIST.append(
                glob.glob(
                    "D:\\research\\stacked\\ALL\\%s\\%s\\*%d-%04d.fit.gz"
                    % (REF_NS, band, REF_CC, REF_fields)
                )
            )
    except pandas.io.common.EmptyDataError:
        print("aaa")
    if len(MOVE_LIST) == 0 or len(MOVE_LIST[0]) == 0:
        continue
    for j in range(len(MOVE_LIST)):
        shutil.move(
            MOVE_LIST[j][0], "D:\\research\\stacked\\stack%d\\%s\\" % (stacked_no, band)
        )

# In[6]:


MOVE_LIST

# In[4]:


stacked_no = 22
f = open("E:\\stacked\\stack%d\\down.sh" % stacked_no, "w")

REF_PATH = "E:\\single\\"
REF_LIST = glob.glob(REF_PATH + "stack%d\\*.csv" % stacked_no)
for i in range(len(REF_LIST)):
    REF_NS = REF_LIST[i][-11:-8]
    REF_CC = int(REF_LIST[i][-5])
    if REF_NS == "206":
        DOWN_LIST = []
        try:
            for REF_fields in pd.read_csv(REF_LIST[i], header=None).values[:, 0]:
                DOWN_LIST.append("%04d.fit.gz" % (REF_fields))
        except pandas.io.common.EmptyDataError:
            print("aaa")
        if len(DOWN_LIST) == 0 or len(DOWN_LIST[0]) == 0:
            continue
        for j in range(len(DOWN_LIST)):
            f.write(
                "wget http://das.sdss.org/raw/200006/2/corr/%d/fpC-200006-r%d-%s\n"
                % (REF_CC, REF_CC, DOWN_LIST[j])
            )
    elif REF_NS == "106":
        DOWN_LIST = []
        try:
            for REF_fields in pd.read_csv(REF_LIST[i], header=None).values[:, 0]:
                DOWN_LIST.append("%04d.fit.gz" % (REF_fields))
        except pandas.io.common.EmptyDataError:
            print("aaa")
        if len(DOWN_LIST) == 0 or len(DOWN_LIST[0]) == 0:
            continue
        for j in range(len(DOWN_LIST)):
            f.write(
                "wget http://das.sdss.org/raw/100006/2/corr/%d/fpC-100006-r%d-%s\n"
                % (REF_CC, REF_CC, DOWN_LIST[j])
            )


f.close()

# In[54]:


DOWN_LIST[0]
