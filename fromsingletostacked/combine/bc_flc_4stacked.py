#!/usr/bin/env python
# coding: utf-8

# In[61]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-12-5
# @Filename:test_optimize_image_sampling.ipynb
# All imports needed through out this notebook are included at the beginning. 
import astropy.units as u
import glob
import numpy as np
import matplotlib.pyplot as plt
import os

from astropy.io import fits
from astropy.table import Table
from astropy.units import Quantity
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from astroquery.mast import Observations
from astroquery.sdss import SDSS

import ccdproc
from ccdproc import ImageFileCollection
from IPython.display import Image

from drizzlepac import tweakreg
from drizzlepac import astrodrizzle

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[65]:

collec = ImageFileCollection('flc_f606w/', glob_include="*flc.fits", ext=0,
                             keywords=["targname", "ra_targ", "dec_targ", "filter", "exptime", "postarg1", "postarg2"])

table = collec.summary
table['exptime'].format = '7.1f'
table['ra_targ'].format = '7.7f'
table['dec_targ'].format = '7.7f'
table['postarg1'].format = '7.2f'
table['postarg2'].format = '7.2f'
table

RA = table['ra_targ'][0]
Dec = table['dec_targ'][0]
print(RA)

coord = SkyCoord(ra=RA, dec=Dec, unit=(u.deg, u.deg))
radius = Quantity(6., u.arcmin)

gaia_query = Gaia.query_object_async(coordinate=coord, radius=radius)
gaia_query

reduced_query = gaia_query['ra', 'dec', 'phot_g_mean_mag']
reduced_query

reduced_query.write('gaia.cat', format='ascii.commented_header', overwrite=True)
# Final run with ideal parameters, updatehdr = True

refcat = 'gaia.cat'
cw = 3.5  # Set to two times the FWHM of the PSF.
wcsname = 'Gaia'  # Specify the WCS name for this alignment
input_flcs = glob.glob(f'flc_f606w/j8m8bc*.fits')


# In[67]:


# Final run with ideal parameters, updatehdr = True
# 1000/78 = threshold

tweakreg.TweakReg(input_flcs,
                  imagefindcfg={'threshold': 10, 'conv_width': 3.5, 'peakmax': 7000}, 
                  fitgeometry='general',
                  interactive=False,
                  shiftfile=False, 
                  updatehdr=False,
                  see2dplot=False, # See 2d histogram for initial offset?
                  wcsname=wcsname,  # Give our WCS a new name
                  reusename=True)



# In[68]:


astrodrizzle.AstroDrizzle(input_flcs,
    output='bc_4stacked',
    driz_sep_bits='4096',
    final_bits='4096',
    final_pixfrac=0.6,
    final_rot=0.,
    final_scale=0.03,
    context=False,
    build=True,
    preserve=False,
    clean=True)

import shutil
input_flcs = glob.glob("./*_4stacked.fits")
if not os.path.exists("data/LowExp"):
    os.mkdir("data/LowExp")
for file in input_flcs:
    shutil.move(file, f"./data/LowExp/{file}")