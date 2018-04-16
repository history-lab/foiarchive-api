# ENV VARS
ROOT=$PWD
export PYTHONPATH=$ROOT:$PYTHONPATH
export DECLASS_API=$ROOT/api

# DOWNLOADING DEPENDENCIES
# virtualenv env
# source env/bin/activate
# pip install -r requirements.txt

## UBUNTU
# apt-get install build-essential python-dev libmysqlclient-dev

echo "ALL DOWNLOADS DONE, LAUNCHING API..."
python $ROOT/api/src/declass_api.py -c do -d True -l False
