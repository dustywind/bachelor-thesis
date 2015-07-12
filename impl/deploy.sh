
#!/bin/bash

python='python3'
sqlite='sqlite3'
databasedir='./database'
sphinx_sourcedir='./documentation/source/_static'
product_data_image_dir='./product_data/img/'
product_image_source='https://wwwcip.cs.fau.de/~___FOOBAR___/bachelor-thesis/product_images.tar.gz'


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

echo 'downloading pictures'
bash ./helper/download_pictures.sh

#echo 'adding product images to project'
#mkdir -p $product_data_image_dir
#wget --output-document=./product_data/img/product_images.tar.gz $product_image_source
#cd $product_data_image_dir
#tar -xvf product_images.tar.gz
#cd ~-

echo 'preparing onlineshop/node.js server'
cd onlineshop
npm install
cd ..

echo 'copying static resources to node-project'
cp ./product_data/img/*.jpg ./onlineshop/public/images/



