#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-07-02
# @Filename: download_stacked_data.py


# DTYPE
# 100006 == 106 == South strip
# 200006 == 206 == North strip

bandtype = ["g", "r", "i"]
DTYPE_list = ["106", "206"]

for band in bandtype:
    for CAMCOL in range(1, 7):
        for DTYPE in DTYPE_list:
            if DTYPE == "106":
                f = open(
                    "106/%s/cc%d/get_%s%s_cc%d_axel.sh"
                    % (band, CAMCOL, band, DTYPE, CAMCOL),
                    "w",
                )
                for i in range(62, 801):
                    f.write(
                        "axel -a -n 2 http://das.sdss.org/imaging/100006/2/corr/%d/fpC-100006-%s%d-%04d.fit.gz\n"
                        % (CAMCOL, band, CAMCOL, i)
                    )
                f.close()

            elif DTYPE == "206":
                f = open(
                    "206/%s/cc%d/get_%s%s_cc%d_axel.sh"
                    % (band, CAMCOL, band, DTYPE, CAMCOL),
                    "w",
                )
                # f.write('wget -a -n 2')
                for i in range(62, 801):
                    f.write(
                        "axel -a -n 2 http://das.sdss.org/imaging/200006/2/corr/%d/fpC-200006-%s%d-%04d.fit.gz\n"
                        % (CAMCOL, band, CAMCOL, i)
                    )
                f.close()
