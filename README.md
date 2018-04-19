# declass-api
notes for refactoring + upgrading to python3

[![Build Status](https://travis-ci.org/mnyrop/declass-api.svg?branch=master)](https://travis-ci.org/mnyrop/declass-api)
[![Dependency Status](https://gemnasium.com/badges/github.com/mnyrop/declass-api.svg)](https://gemnasium.com/github.com/mnyrop/declass-api)

### instructions

#### clone
```sh
$ git clone https://github.com/mnyrop/declass-api.git && cd declass-api
```

#### install dependencies:
```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

#### run

`python run.py`

#### test

`python test.py`


### to do:
- [x] use modern python
- [x] secure DB credentials (from user input)
- [x] reorganize + modularize components
- [x] pin down and monitor dependencies
- [ ] write and use unit tests for BDD/CI
- [ ] re-add and fix `probe_request()` function
- [ ] document!!!

### current results

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
- ~~http://127.0.0.1:5001/declass/v0.4/collections~~ <~ __fixed__
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_countries/
- http://127.0.0.1:5001/declass/v0.4/?ids=frus1945-50Inteld105,1974STATE085546
- http://127.0.0.1:5001/declass/v0.4/?start_date=1947-01-01&end_date=1950-12-01
- http://127.0.0.1:5001/declass/v0.4/?date=1945-10-02


#### not clear
- http://127.0.0.1:5001/declass/v0.4/overview/
- http://127.0.0.1:5001/declass/v0.4/documents/1977ACCRA03397/similar/ (not implemented yet)
- http://127.0.0.1:5001/declass/v0.4/classification/collection/frus
- http://127.0.0.1:5001/declass/v0.4/text/
