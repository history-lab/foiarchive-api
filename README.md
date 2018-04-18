## dev notes for migration to python

### results

#### works (with probe_request() removed)
- http://127.0.0.1:5001/declass/v0.4/fields
- http://127.0.0.1:5001/declass/v0.4/entity_info
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_cnts/
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_collection/
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_cnts_year/
- http://127.0.0.1:5001/declass/v0.4/visualizations/overview/
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_topics/
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_persons/
- http://127.0.0.1:5001/declass/v0.4/random/
- http://127.0.0.1:5001/declass/v0.4/topics/frus/topic/1001
- http://127.0.0.1:5001/declass/v0.4/topics/doc/frus1969-76ve14p1d26

#### does not work
- http://127.0.0.1:5001/declass/v0.4/collections
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_countries/
- http://127.0.0.1:5001/declass/v0.4/documents/?id=1977ACCRA03397
- http://127.0.0.1:5001/declass/v0.4/textdrop/?text=test
- http://127.0.0.1:5001/declass/v0.4/topics/collection/frus

#### not clear
- http://127.0.0.1:5001/declass/v0.4/overview/
- http://127.0.0.1:5001/declass/v0.4/documents/1977ACCRA03397/similar/ (not implemented yet)
- http://127.0.0.1:5001/declass/v0.4/classification/collection/frus
- http://127.0.0.1:5001/declass/v0.4/text/


### instructions

#### to install dependencies:
```sh
virtualenv env
source env/bin/activate
env/bin/python setup.py install
```

#### to run

`python run.py`

#### to test

`python test.py`
