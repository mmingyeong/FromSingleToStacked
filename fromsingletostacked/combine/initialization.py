from astroquery.mast import Observations
import os
import shutil
import stwcs
import subprocess
import glob

os.environ['CRDS_SERVER_URL'] = 'https://hst-crds.stsci.edu'
os.environ['CRDS_PATH'] = os.path.abspath(os.path.join('.', 'reference_files'))

os.environ['iref'] = os.path.abspath(os.path.join('.', 'reference_files', 'references', 'hst', 'wfc3')) + os.path.sep
os.environ['jref'] = os.path.abspath(os.path.join('.', 'reference_files', 'references', 'hst', 'acs')) + os.path.sep

input_flcs = glob.glob(os.path.join('flc_f606w/', '*.fits'))

for file in input_flcs:
    stwcs.updatewcs.updatewcs(file, use_db=False)