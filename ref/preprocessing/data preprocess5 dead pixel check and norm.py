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

# In[3]:


5/7.263528082123479

# In[ ]:



if BAND == 'r':
    if CC == 1:
        SIST_NormF = 5.079505778912232
    elif CC == 2:
        SIST_NormF = 5.140171408876091
    elif CC == 3:
        SIST_NormF = 5.1310723025130525
    elif CC == 4:
        SIST_NormF = 5.236631702748523
    elif CC == 5:
        SIST_NormF = 4.957325790847507
    elif CC == 6:
        SIST_NormF = 5.210639505070301

elif BAND == 'g':
    if CC == 1:
        SIST_NormF = 3.3352685988765955
    elif CC == 2:
        SIST_NormF = 3.8186011621684126
    elif CC == 3:
        SIST_NormF = 3.745866840446125
    elif CC == 4:
        SIST_NormF = 3.694717372301556
    elif CC == 5:
        SIST_NormF = 4.006293466645047
    elif CC == 6:
        SIST_NormF = 3.831022324602731

elif BAND == 'i':
    if CC == 1:
        SIST_NormF = 7.162752103626512
    elif CC == 2:
        SIST_NormF = 7.263528082123479
    elif CC == 3:
        SIST_NormF = 6.678249889369915
    elif CC == 4:
        SIST_NormF = 6.51081223805739
    elif CC == 5:
        SIST_NormF = 6.956327915830884
    elif CC == 6:
        SIST_NormF = 6.950627077059037


# In[2]:


stacked_no = 34
BAND = 'g'

REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

LIST_CC = []
for i in range(len(LIST_STA)):
    LIST_CC.append(LIST_SIN[i][-15])

mini = -1000
maxi = 400000


# In[3]:



qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

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
#fits.open(LIST_SIN_g[0])[0].data

# In[30]:


LIST_STA[0][-15:-9]

# In[4]:


#making delete list

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
            , '4-0595', '4-0612', '4-0666', '4-0674', '4-0697', '5-0589', '5-0586', '5-0604', '5-0612', '5-0656', '5-0683', '5-0697'
            , '6-0612', '6-0617']
    print(len(delF))    
    print(204-len(delF))


# In[6]:


dellist_1 = []
for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'r':
        if CC == 1:
            SIST_NormF = 5.079505778912232
        elif CC == 2:
            SIST_NormF = 5.140171408876091
        elif CC == 3:
            SIST_NormF = 5.1310723025130525
        elif CC == 4:
            SIST_NormF = 5.236631702748523
        elif CC == 5:
            SIST_NormF = 4.957325790847507
        elif CC == 6:
            SIST_NormF = 5.210639505070301
    elif BAND == 'g':
        if CC == 1:
            SIST_NormF = 3.3352685988765955
        elif CC == 2:
            SIST_NormF = 3.8186011621684126
        elif CC == 3:
            SIST_NormF = 3.745866840446125
        elif CC == 4:
            SIST_NormF = 3.694717372301556
        elif CC == 5:
            SIST_NormF = 4.006293466645047
        elif CC == 6:
            SIST_NormF = 3.831022324602731
    elif BAND == 'i':
        if CC == 1:
            SIST_NormF = 7.162752103626512
        elif CC == 2:
            SIST_NormF = 7.263528082123479
        elif CC == 3:
            SIST_NormF = 6.678249889369915
        elif CC == 4:
            SIST_NormF = 6.51081223805739
        elif CC == 5:
            SIST_NormF = 6.956327915830884
        elif CC == 6:
            SIST_NormF = 6.950627077059037
    if IMG_STA[i].min() < -100 or IMG_STA[i].max() > 400000:
        dellist_1.append(i)
    if IMG_SIN[i].min()*SIST_NormF < -1000 or IMG_SIN[i].max()*SIST_NormF > 400000:
        dellist_1.append(i)        
    for j in range(len(delF)):
        if LIST_STA[i][-15:-9] == delF[j]:
            dellist_1.append(i)
dellist_1 = sorted(list(set(dellist_1)))
print(len(dellist_1))

# In[42]:


len(set(delF))

# In[7]:


stacked_no = 34
BAND = 'r'

REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

LIST_CC = []
for i in range(len(LIST_STA)):
    LIST_CC.append(LIST_SIN[i][-15])


# In[8]:



qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

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
#fits.open(LIST_SIN_g[0])[0].data

# In[9]:


for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'r':
        if CC == 1:
            SIST_NormF = 5.079505778912232
        elif CC == 2:
            SIST_NormF = 5.140171408876091
        elif CC == 3:
            SIST_NormF = 5.1310723025130525
        elif CC == 4:
            SIST_NormF = 5.236631702748523
        elif CC == 5:
            SIST_NormF = 4.957325790847507
        elif CC == 6:
            SIST_NormF = 5.210639505070301
    elif BAND == 'g':
        if CC == 1:
            SIST_NormF = 3.3352685988765955
        elif CC == 2:
            SIST_NormF = 3.8186011621684126
        elif CC == 3:
            SIST_NormF = 3.745866840446125
        elif CC == 4:
            SIST_NormF = 3.694717372301556
        elif CC == 5:
            SIST_NormF = 4.006293466645047
        elif CC == 6:
            SIST_NormF = 3.831022324602731
    elif BAND == 'i':
        if CC == 1:
            SIST_NormF = 7.162752103626512
        elif CC == 2:
            SIST_NormF = 7.263528082123479
        elif CC == 3:
            SIST_NormF = 6.678249889369915
        elif CC == 4:
            SIST_NormF = 6.51081223805739
        elif CC == 5:
            SIST_NormF = 6.956327915830884
        elif CC == 6:
            SIST_NormF = 6.950627077059037
    if IMG_STA[i].min() < -100 or IMG_STA[i].max() > 400000:
        dellist_1.append(i)
    if IMG_SIN[i].min()*SIST_NormF < -1000 or IMG_SIN[i].max()*SIST_NormF > 400000:
        dellist_1.append(i)        
    for j in range(len(delF)):
        if LIST_STA[i][-15:-9] == delF[j]:
            dellist_1.append(i)
dellist_1 = sorted(list(set(dellist_1)))
print(len(dellist_1))

# In[10]:


stacked_no = 34
BAND = 'i'

REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

LIST_CC = []
for i in range(len(LIST_STA)):
    LIST_CC.append(LIST_SIN[i][-15])


# In[11]:



qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

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
#fits.open(LIST_SIN_g[0])[0].data

# In[12]:


for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'r':
        if CC == 1:
            SIST_NormF = 5.079505778912232
        elif CC == 2:
            SIST_NormF = 5.140171408876091
        elif CC == 3:
            SIST_NormF = 5.1310723025130525
        elif CC == 4:
            SIST_NormF = 5.236631702748523
        elif CC == 5:
            SIST_NormF = 4.957325790847507
        elif CC == 6:
            SIST_NormF = 5.210639505070301
    elif BAND == 'g':
        if CC == 1:
            SIST_NormF = 3.3352685988765955
        elif CC == 2:
            SIST_NormF = 3.8186011621684126
        elif CC == 3:
            SIST_NormF = 3.745866840446125
        elif CC == 4:
            SIST_NormF = 3.694717372301556
        elif CC == 5:
            SIST_NormF = 4.006293466645047
        elif CC == 6:
            SIST_NormF = 3.831022324602731
    elif BAND == 'i':
        if CC == 1:
            SIST_NormF = 7.162752103626512
        elif CC == 2:
            SIST_NormF = 7.263528082123479
        elif CC == 3:
            SIST_NormF = 6.678249889369915
        elif CC == 4:
            SIST_NormF = 6.51081223805739
        elif CC == 5:
            SIST_NormF = 6.956327915830884
        elif CC == 6:
            SIST_NormF = 6.950627077059037
    if IMG_STA[i].min() < -100 or IMG_STA[i].max() > 400000:
        dellist_1.append(i)
    if IMG_SIN[i].min()*SIST_NormF < -1000 or IMG_SIN[i].max()*SIST_NormF > 400000:
        dellist_1.append(i)        
    for j in range(len(delF)):
        if LIST_STA[i][-15:-9] == delF[j]:
            dellist_1.append(i)
dellist_1 = sorted(list(set(dellist_1)))
print(len(dellist_1))

# In[13]:


## for i band

ID_STA = np.delete(ID_STA, dellist_1, axis=0)
ID_SIN = np.delete(ID_SIN, dellist_1, axis=0)

IMG_STA = np.delete(IMG_STA, dellist_1, axis=0)
IMG_SIN = np.delete(IMG_SIN, dellist_1, axis=0)

LIST_CC = np.delete(LIST_CC, dellist_1, axis=0)

# In[19]:


## for i band
mini = -1000
maxi = 400000

IMG_STA = (IMG_STA - mini)/(maxi-mini)

for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'i':
        if CC == 1:
            SIST_NormF = 7.162752103626512
        elif CC == 2:
            SIST_NormF = 7.263528082123479
        elif CC == 3:
            SIST_NormF = 6.678249889369915
        elif CC == 4:
            SIST_NormF = 6.51081223805739
        elif CC == 5:
            SIST_NormF = 6.956327915830884
        elif CC == 6:
            SIST_NormF = 6.950627077059037
    IMG_SIN[i] = (IMG_SIN[i]*SIST_NormF - mini)/(maxi-mini)

# In[20]:


### separate train-test
## for i band

print(len(ID_STA))
#print(ID_106[17934])
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
print('test',SEP_5_test)
print('tr',SEP_5_tr)

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
elif stacked_no == 28:
    for i in range(len(SEP_5_test)):
        if i%3 != 1:
            SEP_5_test2.append(SEP_5_test[i])
    for i in range(len(SEP_5_tr)):
        if i%3 != 1:
            SEP_5_tr2.append(SEP_5_tr[i])


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
            

print(SEP)

# In[21]:


pix = ISIZE
bnd = int(ISIZE/128)

SAVE_PATH = 'D:\\research\\cGAN\\stack%d\\linear\\'%stacked_no

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

# In[23]:


stacked_no = 34
BAND = 'r'

REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

LIST_CC = []
for i in range(len(LIST_STA)):
    LIST_CC.append(LIST_SIN[i][-15])

qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

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
#fits.open(LIST_SIN_g[0])[0].data

# In[24]:


## for r band

ID_STA = np.delete(ID_STA, dellist_1, axis=0)
ID_SIN = np.delete(ID_SIN, dellist_1, axis=0)

IMG_STA = np.delete(IMG_STA, dellist_1, axis=0)
IMG_SIN = np.delete(IMG_SIN, dellist_1, axis=0)

LIST_CC = np.delete(LIST_CC, dellist_1, axis=0)

mini = -1000
maxi = 400000

IMG_STA = (IMG_STA - mini)/(maxi-mini)

for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'r':
        if CC == 1:
            SIST_NormF = 5.079505778912232
        elif CC == 2:
            SIST_NormF = 5.140171408876091
        elif CC == 3:
            SIST_NormF = 5.1310723025130525
        elif CC == 4:
            SIST_NormF = 5.236631702748523
        elif CC == 5:
            SIST_NormF = 4.957325790847507
        elif CC == 6:
            SIST_NormF = 5.210639505070301
    IMG_SIN[i] = (IMG_SIN[i]*SIST_NormF - mini)/(maxi-mini)

# In[25]:


### separate train-test
## for r band

print(len(ID_STA))
#print(ID_106[17934])
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
print('test',SEP_5_test)
print('tr',SEP_5_tr)

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
elif stacked_no == 28:
    for i in range(len(SEP_5_test)):
        if i%3 != 1:
            SEP_5_test2.append(SEP_5_test[i])
    for i in range(len(SEP_5_tr)):
        if i%3 != 1:
            SEP_5_tr2.append(SEP_5_tr[i])


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
            

print(SEP)

# In[26]:


## for r band

pix = ISIZE
bnd = int(ISIZE/128)

SAVE_PATH = 'D:\\research\\cGAN\\stack%d\\linear\\'%stacked_no

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

# In[27]:


stacked_no = 34
BAND = 'g'

REF_PATH = 'D:\\research\\cGAN\\stack%d\\raw\\'%stacked_no

LIST_STA = sorted(glob.glob(REF_PATH + 'stacked\\%s\\*.fit'%BAND))
LIST_SIN = sorted(glob.glob(REF_PATH + 'single\\%s\\*.fit'%BAND))

LIST_CC = []
for i in range(len(LIST_STA)):
    LIST_CC.append(LIST_SIN[i][-15])

qpix = 0
ISIZE = 260
pix = ISIZE-(qpix*2)

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
#fits.open(LIST_SIN_g[0])[0].data

# In[28]:


## for g band

ID_STA = np.delete(ID_STA, dellist_1, axis=0)
ID_SIN = np.delete(ID_SIN, dellist_1, axis=0)

IMG_STA = np.delete(IMG_STA, dellist_1, axis=0)
IMG_SIN = np.delete(IMG_SIN, dellist_1, axis=0)

LIST_CC = np.delete(LIST_CC, dellist_1, axis=0)

mini = -1000
maxi = 400000

IMG_STA = (IMG_STA - mini)/(maxi-mini)

for i in range(len(IMG_STA)):
    CC = int(LIST_CC[i])
    if BAND == 'g':
        if CC == 1:
            SIST_NormF = 3.3352685988765955
        elif CC == 2:
            SIST_NormF = 3.8186011621684126
        elif CC == 3:
            SIST_NormF = 3.745866840446125
        elif CC == 4:
            SIST_NormF = 3.694717372301556
        elif CC == 5:
            SIST_NormF = 4.006293466645047
        elif CC == 6:
            SIST_NormF = 3.831022324602731
    IMG_SIN[i] = (IMG_SIN[i]*SIST_NormF - mini)/(maxi-mini)

# In[29]:


### separate train-test
## for g band

print(len(ID_STA))
#print(ID_106[17934])
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
print('test',SEP_5_test)
print('tr',SEP_5_tr)

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
elif stacked_no == 28:
    for i in range(len(SEP_5_test)):
        if i%3 != 1:
            SEP_5_test2.append(SEP_5_test[i])
    for i in range(len(SEP_5_tr)):
        if i%3 != 1:
            SEP_5_tr2.append(SEP_5_tr[i])


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
            

print(SEP)

# In[30]:


## for g band

pix = ISIZE
bnd = int(ISIZE/128)

SAVE_PATH = 'D:\\research\\cGAN\\stack%d\\linear\\'%stacked_no

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
