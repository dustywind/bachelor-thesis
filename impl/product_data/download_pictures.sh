#!/bin/bash

#results=$(echo 'SELECT image_name FROM Product ORDER BY document_id LIMIT 87;' | sqlite3 recommender.sqlite3)
#$urls=($results)


for index in {2..100}
do
    line=$(head -n $index DamenBlusen.txt | tail -n 1)
    a=( $line )
    echo $a
    outputfile=$(echo $a | sed -r 's/\///g' | sed -r 's/http://g' )
    curl ${a[0]} > $outputfile 
done


