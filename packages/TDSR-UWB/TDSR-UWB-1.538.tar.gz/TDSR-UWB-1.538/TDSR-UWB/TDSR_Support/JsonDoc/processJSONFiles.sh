#!/bin/sh

for f in ./*.txt; do echo "Processing $f file..."; ff=${f%.*}; convert -font "Liberation-Mono" label:"$(cat $f)" $ff.png ;done


./updateReadme.py