#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2022-07-07
# @Filename: download_stacked_data.py

# If you want to download all NEWFIRM data, use,
# wget -i get_newfirm.txt

# But note that the size of the data is large (a total of 1 TB).

f = open(
    "newfirm/get_stripe82_newfirm.sh",
    "w",
)
f.write("wget -i get_newfirm.txt")
f.close()
