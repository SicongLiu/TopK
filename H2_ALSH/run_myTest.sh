#!/bin/bash
# make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters
# ------------------------------------------------------------------------------
n=1000
d=5

qn=1
K=4
L=6
dPath=./data/anti_correlated_5_1000.txt
qPath=./query/query_5D.txt
oFolder=./result/result_5D

# ------------------------------------------------------------------------------
#  Ground-Truth
# ------------------------------------------------------------------------------
./alsh -alg 0 -n ${n} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} \
    -ts ${oFolder}.mip
