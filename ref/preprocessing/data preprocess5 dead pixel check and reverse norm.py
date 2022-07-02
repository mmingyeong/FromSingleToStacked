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
from sklearn.linear_model import TheilSenRegressor, RANSACRegressor
def LINEAR(X, B):
    return B*X
def IMG_LOG(IMAGE):
    a = 1000
    return np.log(IMAGE*a+1)/np.log(a)

# In[2]:


stacked_no = 34

#making delete list
if stacked_no == 34:
    delF = ['1-0573', '1-0606', '2-0579', '2-0592', '2-0606', '2-0609', '2-0612', '2-0614', '2-0682', '3-0548', '3-0569'
            , '3-0604', '4-0550', '4-0589', '4-0592'
            , '4-0595', '4-0612', '4-0666', '4-0674', '4-0697', '5-0589', '5-0586', '5-0604', '5-0612', '5-0656', '5-0683', '5-0697'
            , '6-0612', '6-0617']
    print(len(delF))    
    print(204-len(delF))
    
SIST_NormF = np.zeros(3*6).reshape(3,6)
SIST_NormF[0,0] = 3.3352685988765955   # g-band
SIST_NormF[0,1] = 3.8186011621684126
SIST_NormF[0,2] = 3.745866840446125
SIST_NormF[0,3] = 3.694717372301556
SIST_NormF[0,4] = 4.006293466645047
SIST_NormF[0,5] = 3.831022324602731
SIST_NormF[1,0] = 5.079505778912232    # r-band
SIST_NormF[1,1] = 5.140171408876091
SIST_NormF[1,2] = 5.1310723025130525
SIST_NormF[1,3] = 5.236631702748523
SIST_NormF[1,4] = 4.957325790847507
SIST_NormF[1,5] = 5.210639505070301
SIST_NormF[2,0] = 7.162752103626512    #i-band
SIST_NormF[2,1] = 7.263528082123479
SIST_NormF[2,2] = 6.678249889369915
SIST_NormF[2,3] = 6.51081223805739
SIST_NormF[2,4] = 6.956327915830884
SIST_NormF[2,5] = 6.950627077059037

# In[3]:


SIST_NormF

# In[3]:



bands = ['g', 'r', 'i']

qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

dellist_1 = []
for BAND in bands:
    if BAND == 'g':
        band_no = 0 
    elif BAND == 'r':
        band_no = 1
    elif BAND == 'i':
        band_no = 2
    REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

    LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
    LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

    LIST_CC = []
    for i in range(len(LIST_STA)):
        LIST_CC.append(LIST_SIN[i][-15])

    ID_STA = []
    ID_SIN = []
    for i in range(len(LIST_STA)):
        ID_STA.append(LIST_STA[i][-27:])
        ID_SIN.append(LIST_SIN[i][-27:])
    
    IMG_STA = np.zeros(len(LIST_STA)*pix*pix).reshape(len(LIST_STA),pix,pix)
    IMG_SIN = np.zeros(len(LIST_SIN)*pix*pix).reshape(len(LIST_SIN),pix,pix)

    for i in range(len(LIST_STA)):
        IMG_STA[i] = fits.open(LIST_STA[i])[0].data[qpix:ISIZE-qpix, qpix:ISIZE-qpix]
        IMG_SIN[i] = fits.open(LIST_SIN[i])[0].data[qpix:ISIZE-qpix, qpix:ISIZE-qpix]
        
    for i in range(len(IMG_STA)):
        CC = int(LIST_CC[i])
    
        if IMG_STA[i].min()/SIST_NormF[band_no, CC-1] < -20 or IMG_STA[i].max()/SIST_NormF[band_no, CC-1] > 80000:
            dellist_1.append(i)
        if IMG_SIN[i].min() < -200 or IMG_SIN[i].max()> 80000:
            dellist_1.append(i)        
        for j in range(len(delF)):
            if LIST_STA[i][-15:-9] == delF[j]:
                dellist_1.append(i)
    dellist_1 = sorted(list(set(dellist_1)))
    print(len(dellist_1))

# In[7]:


print(len(dellist_1))

# In[8]:



mini = -1000/5
maxi = 400000/5

for BAND in bands:
    if BAND == 'g':
        band_no = 0 
    elif BAND == 'r':
        band_no = 1
    elif BAND == 'i':
        band_no = 2
    REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

    LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
    LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

    LIST_CC = []
    for i in range(len(LIST_STA)):
        LIST_CC.append(LIST_SIN[i][-15])

    ID_STA = []
    ID_SIN = []
    for i in range(len(LIST_STA)):
        ID_STA.append(LIST_STA[i][-27:])
        ID_SIN.append(LIST_SIN[i][-27:])
    
    IMG_STA = np.zeros(len(LIST_STA)*pix*pix).reshape(len(LIST_STA),pix,pix)
    IMG_SIN = np.zeros(len(LIST_SIN)*pix*pix).reshape(len(LIST_SIN),pix,pix)
    for i in range(len(LIST_STA)):
        IMG_STA[i] = fits.open(LIST_STA[i])[0].data[qpix:ISIZE-qpix, qpix:ISIZE-qpix]
        IMG_SIN[i] = fits.open(LIST_SIN[i])[0].data[qpix:ISIZE-qpix, qpix:ISIZE-qpix]

    ID_STA = np.delete(ID_STA, dellist_1, axis=0)
    ID_SIN = np.delete(ID_SIN, dellist_1, axis=0)

    IMG_STA = np.delete(IMG_STA, dellist_1, axis=0)
    IMG_SIN = np.delete(IMG_SIN, dellist_1, axis=0)

    LIST_CC = np.delete(LIST_CC, dellist_1, axis=0)

    IMG_SIN = (IMG_SIN - mini)/(maxi-mini)

    for i in range(len(IMG_STA)):
        CC = int(LIST_CC[i])
        IMG_STA[i] = ((IMG_STA[i]/SIST_NormF[band_no, CC-1]) - mini)/(maxi-mini)
        
    SEP = []
    SEP.append(0)
    for i in range(len(ID_STA)-1):
        if str(ID_STA[i])[-15:-9] != str(ID_STA[i+1])[-15:-9]:
            SEP.append(i+1)
            #print(i+1, ID_106[i][5:8], ID_106[i+1][5:8])
    SEP_5_test = []
    for i in range(int(len(SEP)/5)):
        SEP_5_test.append(SEP[5*i])
    #SEP_5_test.append(len(ID_106)-1)
    dellist = []
    for i in range(len(SEP)):
        for j in SEP_5_test:
            if SEP[i] == j:
                dellist.append(i)
    SEP_5_tr = np.delete(SEP,dellist)
    #print('test',SEP_5_test)
    #print('tr',SEP_5_tr)

    TE_STA_ID = []
    TE_SIN_ID = []

    TE_STA_IMG = []
    TE_SIN_IMG = []

    TR_STA_ID = []
    TR_SIN_ID = []

    TR_STA_IMG = []
    TR_SIN_IMG = []

    ##갯수 제한 train~12000개, test~3000개
    SEP_5_test2, SEP_5_tr2 = [], []
    if stacked_no == 34:
        SEP_5_test2 = SEP_5_test
        SEP_5_tr2 = SEP_5_tr

    for j in SEP_5_test2:
        for i in range(len(ID_STA)):
            if str(ID_STA[i])[-15:-9] == str(ID_STA[j])[-15:-9]:
                TE_STA_ID.append(ID_STA[i])            
                TE_SIN_ID.append(ID_SIN[i])            
                TE_STA_IMG.append(IMG_STA[i])            
                TE_SIN_IMG.append(IMG_SIN[i])
            
    for j in SEP_5_tr2:
        for i in range(len(ID_STA)):
            if str(ID_STA[i])[-15:-9] == str(ID_STA[j])[-15:-9]:
                TR_STA_ID.append(ID_STA[i])            
                TR_SIN_ID.append(ID_SIN[i])            
                TR_STA_IMG.append(IMG_STA[i])            
                TR_SIN_IMG.append(IMG_SIN[i])
    
    pix = ISIZE
    bnd = int(ISIZE/128)

    SAVE_PATH = 'D:\\research\\cGAN\\stack%d\\'%stacked_no

    for i in range(len(TE_STA_ID)):
        fits_file = fits.PrimaryHDU(data=TE_STA_IMG[i].astype('float64').reshape(pix,pix)[bnd:pix-bnd,bnd:pix-bnd])
        fits_file.writeto(SAVE_PATH + 'test\\stacked\\%s\\%s'% (BAND, TE_STA_ID[i]))

    for i in range(len(TE_SIN_ID)):
        fits_file = fits.PrimaryHDU(data=TE_SIN_IMG[i].astype('float64').reshape(pix,pix)[bnd:pix-bnd,bnd:pix-bnd])
        fits_file.writeto(SAVE_PATH + 'test\\single\\%s\\%s'% (BAND, TE_SIN_ID[i]))

    for i in range(len(TR_STA_ID)):
        fits_file = fits.PrimaryHDU(data=TR_STA_IMG[i].astype('float64').reshape(pix,pix))
        fits_file.writeto(SAVE_PATH + 'train\\stacked\\%s\\%s'% (BAND, TR_STA_ID[i]))

    for i in range(len(TR_SIN_ID)):
        fits_file = fits.PrimaryHDU(data=TR_SIN_IMG[i].astype('float64').reshape(pix,pix))
        fits_file.writeto(SAVE_PATH + 'train\\single\\%s\\%s'% (BAND, TR_SIN_ID[i]))

    del TR_STA_IMG, TR_SIN_IMG, TE_STA_IMG, TE_SIN_IMG
print("finished")

# In[ ]:


## for r band


