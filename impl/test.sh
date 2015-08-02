
#!/bin/bash

echo 'start testing'
python3 -m unittest discover -s ./unittest -p '*_test.py'

echo 'cleaning up'
rm unittest/test.sqlite3
echo 'finished testing'
