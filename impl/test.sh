
#!/bin/bash

echo 'start testing'
python3 -m unittest discover -s ./unittest -p '*_test.py'
echo 'finished testing'
