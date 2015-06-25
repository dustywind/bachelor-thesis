
#!/bin/bash

echo 'start testing'
python3 -m unittest discover -s ./unittest -p 'informationretrieval_test.py'
echo 'finished testing'
