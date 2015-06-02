#!/bin/bash

mass=$1

echo "Vary qb"
cat tables_14TeV/scale_var_new_${1}GeV | grep "#\|  0 \|  7 \|  8 " | awk {'print $1" "$4" "$7'}

echo "Vary qf"
cat tables_14TeV/scale_var_new_${1}GeV | grep "#\|  0 \|  4 \|  5 " | awk {'print $1" "$2" "$7'}

echo "Vary qr"
cat tables_14TeV/scale_var_new_${1}GeV | grep "#\|  0 \| 11 \| 14 " | awk {'print $1" "$3" "$7'}

#max: where qb and qf are varied in some direction; and qr is not varied at all or into same direction