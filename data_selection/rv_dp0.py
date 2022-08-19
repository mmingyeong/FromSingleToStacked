#!/usr/bin/env python
# coding: utf-8

# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-08-01
# @Filename: rv_dp0.py
# review data preprocess0 download stacked images.py

# set a wavelength band and south/north for the data
# the filter used (g, r, i)
# DTYPE
# 100006 == 106 == South strip
# 200006 == 206 == North strip
# camera column (1-6)

band = "i"
DTYPE = "206"
for CAMCOL in range(1, 7):
    if DTYPE == "106":
        # Since a large file needs to be downloaded, the commands that allow each file to be downloaded are stored in the shell file.
        f = open(
            "\\stacked\\106\\%s\\cc%d\\get_%s%s_cc%d_axel.sh"
            % (band, CAMCOL, band, DTYPE, CAMCOL),
            "w",
        )
        for i in range(62, 801):
            f.write(
                "axel -a -n 2 http://das.sdss.org/raw/100006/2/corr/%d/fpC-100006-%s%d-%04d.fit.gz\n"
                % (CAMCOL, band, CAMCOL, i)
            )
        f.close()
    elif DTYPE == "206":
        f = open(
            "\\stacked\\206\\%s\\cc%d\\get_%s%s_cc%d_axel.sh"
            % (band, CAMCOL, band, DTYPE, CAMCOL),
            "w",
        )
        f.write("wget -a -n 2")
        for i in range(62, 801):
            f.write(
                " http://das.sdss.org/raw/200006/2/corr/%d/fpC-200006-%s%d-%04d.fit.gz"
                % (CAMCOL, band, CAMCOL, i)
            )
        f.close()
