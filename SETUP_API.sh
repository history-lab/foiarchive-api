# ENV VARS
ROOT="$PWD"
export PYTHONPATH=$ROOT:$PYTHONPATH
export DECLASS_API=$ROOT/api

if [ -z "$CI" ]; then
  virtualenv env
  source env/bin/activate
  pip install -r requirements.txt
  echo "ALL DOWNLOADS DONE, LAUNCHING API..."
  python $ROOT/api/src/declass_api.py -c do -d True -l False
else
  echo "ALL DOWNLOADS DONE, LAUNCHING API..."
  python $ROOT/api/src/test_api.py -c do -d True -l False
  echo "FINISHED WITHOUT FAILURE."
fi
