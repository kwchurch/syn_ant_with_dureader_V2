#!/bin/sh

cd /mnt/home/kwc/morphology/synonym_dictionary

for valset in /mnt/home/kwc/morphology/MoE-ASD-main/dataset_tag/*p[0-9]*.val
do
for trainset in /mnt/home/kwc/morphology/MoE-ASD-main/dataset_tag/*p[0-9]*.train
do
# echo valset: $valset trainset: $trainset
python paths.py $trainset < $valset|
 awk 'NR == 1 ||  NF < 6 { next}; 
 {n++; x += ($4 == ($5 % 2))}; 
 END {if(n > 0) print x/n, n+0, trainset, valset}' trainset=`basename $trainset` valset=`basename $valset`
done
done
