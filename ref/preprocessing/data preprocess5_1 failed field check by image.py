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
def IMG_LOG(IMAGE):
    a = 1000
    return np.log(IMAGE*a+1)/np.log(a)
def ASINH1(IMAGE):
    return np.arcsinh(IMAGE*10)/3
def ASINH2(IMAGE):
    return ASINH1(ASINH1(IMAGE))
def ASINH3(IMAGE):
    return ASINH1(ASINH2(IMAGE))
def ASINH4(IMAGE):
    return ASINH2(ASINH2(IMAGE))

def ASINH5(IMAGE):
    return ASINH2(ASINH3(IMAGE))

# In[2]:


stacked_no = 34
band = 'g'
FILE_LIST = sorted(glob.glob('D:\\research\\stacked\\stack%d\\%s\\*.fit.gz'%(stacked_no, band)))
#FILE_LIST = sorted(glob.glob('E:\\single\\stack%d\\%s\\ZSKY*.fit.gz'%(stacked_no, band)))


# In[3]:


FILE_LIST

# In[ ]:


(np.arcsinh(IMG_LOG((fits.open(FILE_LIST[0])[0].data-mini)/(maxi-mini))*10)/3).min()

# In[4]:


plt.rcParams['figure.figsize'] = (20.48/1.5, 14.89/1.5)
Fno = 0
'''
Fg, Fr, Fi = 5.9, 4.9, 4.5
if band == 'g':
    coef = Fg
elif band == 'r':
    coef = Fr
elif band == 'i':
    coef = Fi

mini, maxi = -500, 400000
'''    
coef = 4.957
mini, maxi = -1000, 400000

#plt.imshow(ASINH5((fits.open(FILE_LIST[Fno])[0].data*coef-mini)/(maxi-mini)), cmap = 'Spectral_r', vmax = 1., vmin = 0.5)
plt.imshow(ASINH5((fits.open(FILE_LIST[Fno])[0].data-mini)/(maxi-mini)), cmap = 'Spectral_r', vmax = 1., vmin = 0.5)


# In[5]:


Fno = 5

MEAN, MEDIAN, STD = sigma_clipped_stats(fits.open(FILE_LIST[Fno])[0].data)
plt.imshow(fits.open(FILE_LIST[Fno])[0].data, cmap = 'viridis', vmax = MEAN+STD, vmin = MEAN-STD)

# In[24]:


for Fno in range(len(FILE_LIST)-25,len(FILE_LIST)):#len(FILE_LIST)):
    print(Fno, FILE_LIST[Fno][-14:-7])
    plt.imshow(ASINH5((fits.open(FILE_LIST[Fno])[0].data-mini)/(maxi-mini)), cmap = 'Spectral_r', vmax = 1, vmin = 0.6)
    plt.show()


# In[22]:


len(FILE_LIST)

# In[5]:


plt.rcParams['figure.figsize'] = (20.48/1.5, 14.89/1.5)
kk=7

#kk=6
#for Fno in range(len(FILE_LIST)-25,len(FILE_LIST)):#len(FILE_LIST)):
for Fno in range(len(FILE_LIST)):
    
    print(Fno, FILE_LIST[Fno][-14:-7])
    MEAN, MEDIAN, STD = sigma_clipped_stats(fits.open(FILE_LIST[Fno])[0].data)
    plt.imshow(fits.open(FILE_LIST[Fno])[0].data, cmap = 'gray_r', vmax = MEAN+STD, vmin = MEAN-STD)
    plt.show()
    del MEAN, MEDIAN, STD

