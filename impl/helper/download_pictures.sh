#!/bin/bash

mkdir -p ./product_data/img
cd ./product_data/img

for index in {2..100}
do
    line=$(head -n $index ../DamenBlusen.txt | tail -n 1)
    a=( $line )
    echo $a
    outputfile=$(echo $a | sed -r 's/\///g' | sed -r 's/http://g' )
    curl ${a[0]} > $outputfile 
done

for index in {2..497}
do
    line=$(head -n $index ../HerrenHosen.txt | tail -n 1)
    a=( $line )
    echo $a
    outputfile=$(echo $a | sed -r 's/\///g' | sed -r 's/http://g' )
    curl ${a[0]} > $outputfile 
done

cd ~-

