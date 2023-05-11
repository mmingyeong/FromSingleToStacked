#!/usr/bin/env python
# coding: utf-8


band = "r"
DTYPE = "106"
for CAMCOL in range(1, 7):
    if DTYPE == "106":
        f = open(
            "D:\\research\\stacked\\ALL\\106\\%s\\cc%d\\get_%s%s_cc%d_axel.sh"
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
            "D:\\research\\stacked\\ALL\\206\\%s\\cc%d\\get_%s%s_cc%d_axel.sh"
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
