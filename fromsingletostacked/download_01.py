#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2023-05-11
# @Filename: download_01.py
# This will download the flc fit files from MAST Archive.

import glob
import os
import shutil
from astroquery.mast import Observations

os.environ['CRDS_SERVER_URL'] = 'https://hst-crds.stsci.edu'
os.environ['CRDS_PATH'] = os.path.abspath(os.path.join('.', 'reference_files'))

os.environ['iref'] = os.path.abspath(os.path.join('.', 'reference_files', 'references', 'hst', 'wfc3')) + os.path.sep
os.environ['jref'] = os.path.abspath(os.path.join('.', 'reference_files', 'references', 'hst', 'acs')) + os.path.sep

file_name = "file_name_list.txt"
file = open(file_name, "r")
hudf_obs_id = []

while True:
    line = file.readline()
    if not line: break
    
    name = str(line)
    name_split = name.split("_")
    obs_id = name_split[0] + "_" + name_split[1] + "_" + name_split[2] + "_" + name_split[3] + "_" + name_split[4] + "_" + name_split[5]
    hudf_obs_id.append(str(obs_id))

set_list = set(hudf_obs_id)
hudf_obs_id = list(set_list)

obsTable = Observations.query_criteria(obstype='all', 
    obs_id=hudf_obs_id)

# Download the files
products = Observations.get_product_list(obsTable)
Observations.download_products(products,download_dir='',
                               mrp_only=False,
                               productSubGroupDescription='FLC')

# Move to working directory (not necessary, but outputs will all be in the same place if this is done)
input_flcs = glob.glob(os.path.join('mastDownload', 'HST', '*', '*.fits'))

os.mkdir("data")
os.mkdir("data/flc_f606w")
if os.path.isdir("./flc_f606w"):
    for flc in input_flcs:
        shutil.copy(flc, os.path.basename(flc))
        shutil.move(flc, os.path.join('flc_f606w'))
    #remove mast download dir now that we've moved the files
    shutil.rmtree('mastDownload') 
