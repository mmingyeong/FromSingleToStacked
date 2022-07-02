#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, glob, time, math, shutil
import numpy as np
import pandas as pd
import pandas.io.common
import matplotlib.pyplot as plt
%matplotlib inline
import astropy
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from scipy.optimize import curve_fit
def LINEAR(X, A, B):
    return A + B*X

# In[25]:


stacked_no = 34
ISIZE = 520
HSIZE = int(ISIZE/2)

cGAN_PATH = 'E:\\cGAN\\'
SI_PATH = cGAN_PATH + '1k\\single\\stack%d\\' % stacked_no
ST_PATH = cGAN_PATH + '1k\\stacked\\stack%d\\' % stacked_no

g_IMG_LIST = glob.glob(SI_PATH + 'g\\*.fit')
r_IMG_LIST = glob.glob(SI_PATH + 'r\\*.fit')
i_IMG_LIST = glob.glob(SI_PATH + 'i\\*.fit')
st_IMG_LIST = glob.glob(ST_PATH + '*.fit')



# In[12]:


ISHAPE = np.zeros(len(st_IMG_LIST)*2).reshape(len(st_IMG_LIST),2)
for i in range(len(st_IMG_LIST)):
    ISHAPE[i] = fits.open(st_IMG_LIST[i])[0].data.shape

# In[59]:


col = 2
row = 4
IMG_LIST = i_IMG_LIST

IOUT = np.zeros(len(IMG_LIST)*col*row*ISIZE*ISIZE).reshape(len(IMG_LIST),col,row,ISIZE,ISIZE)
for i in range(len(IMG_LIST)):
    for j in range(col):
        for k in range(row):
            COLST = int((ISHAPE[i][0] - ISIZE)/(col-1) *j)
            ROWST = int((ISHAPE[i][1] - ISIZE)/(row-1) *k)
            IIN = fits.open(IMG_LIST[i])[0].data
            IOUT[i,j,k] = IIN[COLST:COLST+ISIZE, ROWST:ROWST + ISIZE]


# In[60]:


for i in range(len(IMG_LIST)):
    for j in range(col):
        for k in range(row):
            fits_file = fits.PrimaryHDU(data = IOUT[i,j,k])
            if IMG_LIST[0][-18] == '1' or IMG_LIST[0][-18] == '2':
                fits_file.writeto(cGAN_PATH + '512\\stacked\\stack%d\\%s-%02d%02d.fit'%(stacked_no, IMG_LIST[i][-22:-4],j+1,k+1))
            else:
                fits_file.writeto(cGAN_PATH + '512\\single\\stack%d\\%s\\%s-%02d%02d.fit'%(stacked_no,IMG_LIST[i][-11],IMG_LIST[i][-22:-4],j+1,k+1))

# In[41]:


print(int((ISHAPE[0][0] - ISIZE)/(2) *0)+520)
print(int(ISHAPE[0][0]))
print(int((ISHAPE[0][1] - ISIZE)/(row-1) *3))

# In[52]:


IMG_LIST[0][-22:-4]
