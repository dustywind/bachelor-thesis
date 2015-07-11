
#!/bin/bash

python='python3'
sqlite='sqlite3'
databasedir='./database'
sphinx_sourcedir='./documentation/source/_static'


echo 'checking for required programs'


python_installed=$(which $python 2>/dev/null | grep -v "not found" | wc -l)
if [ $python_installed -eq 0 ]; then
    echo "MISSING $python!"
    exit
fi

sqlite_installed=$(which $sqlite 2>/dev/null | grep -v "not found" | wc -l)
if [ $sqlite_installed -eq 0 ]; then
    echo "MISSING $sqlite!"
    exit
fi


echo 'checking for database-directory'
if [ ! -d $databasedir ]; then
    echo 'creating missing database-directory'
    mkdir $databasedir
fi

echo 'checking for sphinx source/_static directory'
if [ ! -d $sphinx_sourcedir ]; then
    echo 'creating missing database-directory'
    mkdir -p $sphinx_sourcedir
fi

echo 'inserting products into the database'
python3 ./productimport.py


echo 'preparing onlineshop/node.js server'
cd onlineshop
npm install
cd ..


