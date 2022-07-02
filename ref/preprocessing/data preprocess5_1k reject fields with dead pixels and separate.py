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

# In[2]:


stacked_no = 34

REF_PATH = 'E:\\cGAN\\1k\\'
LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\stack%d\\*.fit'%stacked_no))
LIST_SIN_g = sorted(glob.glob(REF_PATH + 'single\\stack%d\\g\\*.fit'%stacked_no))
LIST_SIN_r = sorted(glob.glob(REF_PATH + 'single\\stack%d\\r\\*.fit'%stacked_no))
LIST_SIN_i = sorted(glob.glob(REF_PATH + 'single\\stack%d\\i\\*.fit'%stacked_no))


# In[3]:


if stacked_no == 22:
    delF = ['1-0150', '1-0151', '1-0152', '1-0159', '1-0171', '1-0175', '1-0181', '1-0186', '1-0193', '1-0201', '1-0253', '1-0254'
            , '1-0300', '1-0798'
            , '2-0129', '2-0151', '2-0152', '2-0170', '2-0171', '2-0179', '2-0180', '2-0198', '2-0253', '2-0274', '2-0277', '2-0278'
            , '2-0279', '2-0280', '2-0285', '2-0286', '2-0287', '2-0288', '2-0290', '2-0291', '2-0292', '2-0293', '2-0294', '2-0302'
            , '2-0798'
            , '3-0150', '3-0151', '3-0152', '3-0155', '3-0179', '3-0180', '3-0181', '3-0182', '3-0190', '3-0199', '3-0200', '3-0204'
            , '3-0215', '3-0230', '3-0233', '3-0234', '3-0267', '3-0274', '3-0276', '3-0277', '3-0285', '3-0286', '3-0293', '3-0798'
            , '4-0118', '4-0124', '4-0125', '4-0141', '4-0162', '4-0163', '4-0166', '4-0167', '4-0168', '4-0171', '4-0174', '4-0175'
            , '4-0176', '4-0177', '4-0178', '4-0179', '4-0180', '4-0181', '4-0182', '4-0183', '4-0191', '4-0197', '4-0198', '4-0199'
            , '4-0204', '4-0238', '4-0271', '4-0799'
            , '5-0144', '5-0162', '5-0163', '5-0164', '5-0183', '5-0197', '5-0198', '5-0232', '5-0271', '5-0292', '5-0797']
    print(len(delF))    
    print(330-len(delF))
if stacked_no == 28:
    delF = ['1-0313', '1-0315', '1-0316', '1-0317', '1-0330', '1-0361', '1-0364', '1-0365', '1-0387', '1-0388', '1-0392'
            , '1-0397', '1-0400', '1-0401', '1-0406', '1-0453', '1-0458', '1-0460', '1-0461', '1-0462', '1-0471', '1-0499'
            , '1-502', '1-0724', '1-0734', '1-0735', '1-0782', '1-0786'
            , '2-0316', '2-0317', '2-0364', '2-0383', '2-0384', '2-0434', '2-0451', '2-0452', '2-0453', '2-0470', '2-0472', '2-0758'
            , '2-0759'
            , '3-0323', '3-0383', '3-0401', '3-0447', '3-0460', '3-0461', '3-0462', '3-0469', '3-0711', '3-0767', '3-0783', '3-0784'
            , '4-0317', '4-0383', '4-0446', '4-0454', '4-0457', '4-0458', '4-0459', '4-0462', '4-0469', '4-0472', '4-0473', '4-0487'
            , '4-0497', '4-0522', '4-0736', '4-0737'
            , '5-0316', '5-0317', '5-0350', '5-0351', '5-0353', '5-0380', '5-0383', '5-0384', '5-0425', '5-0435', '5-0469', '5-0470'
            , '5-0471', '5-0477', '5-0487']
    print(len(delF))    
    print(310-len(delF))
elif stacked_no == 34:
    delF = ['1-0573', '1-0606', '2-0579', '2-0592', '2-0606', '2-0609', '2-0612', '2-0614', '2-0682', '3-0548', '3-0569'
            , '3-0604', '4-0550', '4-0589', '4-0592'
            , '4-0595', '4-0612', '4-0666', '4-0674', '4-0697', '5-0589', '5-0586', '5-0604', '5-0612', '5-0656', '5-0683', '5-0697']
    print(len(delF))    
    print(180-len(delF))

NUM_STA = []
for i in range(len(LIST_STA)):
    NUM_STA.append(LIST_STA[i][-10:-4])
    
dellist_1 = []
for i in range(len(LIST_STA)):
    for j in range(len(delF)):
        if LIST_STA[i][-10:-4] == delF[j]:
            dellist_1.append(i)
dellist_1 = sorted(list(set(dellist_1)))

# In[4]:



nn = 0
for i in range(len(NUM_STA)):
    if any(x == NUM_STA[i] for x in delF):
        del LIST_STA[i-nn]
        del LIST_SIN_g[i-nn]
        del LIST_SIN_r[i-nn]
        del LIST_SIN_i[i-nn]
        
        nn += 1

# In[5]:


TELI_STA = []
TELI_SIN_g = []
TELI_SIN_r = []
TELI_SIN_i = []

TRLI_STA = []
TRLI_SIN_g = []
TRLI_SIN_r = []
TRLI_SIN_i = []

for i in range(len(LIST_STA)):
    if i % 5 == 2:
        TELI_STA.append(LIST_STA[i])
        TELI_SIN_g.append(LIST_SIN_g[i])
        TELI_SIN_r.append(LIST_SIN_r[i])
        TELI_SIN_i.append(LIST_SIN_i[i])
    else:
        TRLI_STA.append(LIST_STA[i])
        TRLI_SIN_g.append(LIST_SIN_g[i])
        TRLI_SIN_r.append(LIST_SIN_r[i])
        TRLI_SIN_i.append(LIST_SIN_i[i])
        

# In[6]:


for i in range(len(TELI_STA)):
    DATA_STA = fits.open(TELI_STA[i])[0].data
    fits_STA = fits.PrimaryHDU(data = DATA_STA)
    
    DATA_SIN_g = fits.open(TELI_SIN_g[i])[0].data
    fits_SIN_g = fits.PrimaryHDU(data = DATA_SIN_g)
    
    DATA_SIN_r = fits.open(TELI_SIN_r[i])[0].data
    fits_SIN_r = fits.PrimaryHDU(data = DATA_SIN_r)
    
    DATA_SIN_i = fits.open(TELI_SIN_i[i])[0].data
    fits_SIN_i = fits.PrimaryHDU(data = DATA_SIN_i)
    if DATA_STA.min() > 0 and DATA_SIN_g.min() > 0 and DATA_SIN_r.min() > 0 and DATA_SIN_i.min() > 0:
        fits_STA.writeto('E:\\cGAN\\1k\\stack%d\\test\\stacked\\%s.fit'%(stacked_no, TELI_STA[i][-22:-4]))
        fits_SIN_g.writeto('E:\\cGAN\\1k\\stack%d\\test\\single\\g\\%s.fit'%(stacked_no, TELI_SIN_g[i][-22:-4]))
        fits_SIN_r.writeto('E:\\cGAN\\1k\\stack%d\\test\\single\\r\\%s.fit'%(stacked_no, TELI_SIN_r[i][-22:-4]))
        fits_SIN_i.writeto('E:\\cGAN\\1k\\stack%d\\test\\single\\i\\%s.fit'%(stacked_no, TELI_SIN_i[i][-22:-4]))
    
    
for i in range(len(TRLI_STA)):
    DATA_STA = fits.open(TRLI_STA[i])[0].data
    fits_STA = fits.PrimaryHDU(data = DATA_STA)
    
    DATA_SIN_g = fits.open(TRLI_SIN_g[i])[0].data
    fits_SIN_g = fits.PrimaryHDU(data = DATA_SIN_g)
    
    DATA_SIN_r = fits.open(TRLI_SIN_r[i])[0].data
    fits_SIN_r = fits.PrimaryHDU(data = DATA_SIN_r)
    
    DATA_SIN_i = fits.open(TRLI_SIN_i[i])[0].data
    fits_SIN_i = fits.PrimaryHDU(data = DATA_SIN_i)
    if DATA_STA.min() > 0 and DATA_SIN_g.min() > 0 and DATA_SIN_r.min() > 0 and DATA_SIN_i.min() > 0:
        fits_STA.writeto('E:\\cGAN\\1k\\stack%d\\train\\stacked\\%s.fit'%(stacked_no, TRLI_STA[i][-22:-4]))
        fits_SIN_g.writeto('E:\\cGAN\\1k\\stack%d\\train\\single\\g\\%s.fit'%(stacked_no, TRLI_SIN_g[i][-22:-4]))
        fits_SIN_r.writeto('E:\\cGAN\\1k\\stack%d\\train\\single\\r\\%s.fit'%(stacked_no, TRLI_SIN_r[i][-22:-4]))
        fits_SIN_i.writeto('E:\\cGAN\\1k\\stack%d\\train\\single\\i\\%s.fit'%(stacked_no, TRLI_SIN_i[i][-22:-4]))


# In[11]:


for i in range(len(TRLI_STA)):
    DATA_STA = fits.open(TRLI_STA[i])[0].data
    DATA_SIN_g = fits.open(TRLI_SIN_g[i])[0].data
    DATA_SIN_r = fits.open(TRLI_SIN_r[i])[0].data
    DATA_SIN_i = fits.open(TRLI_SIN_i[i])[0].data
    if DATA_STA.min() < 0 or DATA_SIN_g.min() < 0 or DATA_SIN_r.min() < 0 or DATA_SIN_i.min() < 0:
        print(i, TRLI_STA[i],'\n', TRLI_SIN_g[i])

# In[ ]:


for i in range(len(TELI_STA)):
    fits_col.writeto('E:\\cGAN\\1k\\stack%d\\test\\single\\gi\\%s.fit'%(stacked_no, TELI_SIN_g[i][-22:-4]))
    

# In[16]:


TELI_SIN_i[0][-22:-4]

# In[20]:


len(TRLI_STA)

# In[ ]:


ID_STA = []
ID_SIN_g = []
ID_SIN_r = []
ID_SIN_i = []
for i in range(len(LIST_STA)):
    ID_STA.append(LIST_STA[i][-27:])
    ID_SIN_g.append(LIST_SIN_g[i][-27:])
    ID_SIN_r.append(LIST_SIN_r[i][-27:])
    ID_SIN_i.append(LIST_SIN_i[i][-27:])
for i in range(len(LIST_STA)):
    
