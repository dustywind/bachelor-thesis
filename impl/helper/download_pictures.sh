#!/bin/bash

#results=$(echo 'SELECT image_name FROM Product ORDER BY document_id LIMIT 87;' | sqlite3 recommender.sqlite3)
#$urls=($results)

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
    line=$(head -n $index ../HerrenHosen| tail -n 1)
    a=( $line )
    echo $a
    outputfile=$(echo $a | sed -r 's/\///g' | sed -r 's/http://g' )
    curl ${a[0]} > $outputfile 
done

cd ~-

