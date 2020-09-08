# foiarchive-api
Implemented in Python3 and Flask  
The website interface of the Freedom of Information Archive (FOIArchive) is available through the History Lab website at [http://history-lab.org/search](http://history-lab.org/search).
<!--
[![Build Status](https://travis-ci.org/mnyrop/declass-api.svg?branch=master)](https://travis-ci.org/mnyrop/declass-api)
[![](https://img.shields.io/librariesio/github/mnyrop/declass-api.svg)](https://libraries.io/github/mnyrop/declass-api)
-->
### installation instructions
Clone the repo, install the requirements and run run.py.
<!--
#### clone
```sh
$ git clone https://github.com/mnyrop/declass-api.git && cd declass-api
```

#### install dependencies:
```sh
$ virtualenv env # might need to run as `python3 -m virtualenv env`
$ source env/bin/activate
$ pip install -r requirements.txt
```

#### run

`python run.py`

#### test

`python test.py`
-->

### to do:
- [x] use modern python
- [x] secure DB credentials (from user input)
- [x] reorganize + modularize components
- [x] pin down and monitor dependencies
- [ ] write and use unit tests for BDD/CI
- [ ] re-add and fix `probe_request()` function
- [ ] document!!!

### current results

#### works, i.e., returns data (with probe_request() removed)
- http://127.0.0.1:5001/declass/v0.4/fields
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_cnts/
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_collection/
- http://127.0.0.1:5001/declass/v0.4/visualizations/doc_cnts_year/
- http://127.0.0.1:5001/declass/v0.4/visualizations/overview/
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_topics/
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_persons/
- http://127.0.0.1:5001/declass/v0.4/random/
- http://127.0.0.1:5001/declass/v0.4/topics/frus/topic/1001
- http://127.0.0.1:5001/declass/v0.4/topics/doc/frus1969-76ve14p1d26
- http://127.0.0.1:5001/declass/v0.4/collections
- http://127.0.0.1:5001/declass/v0.4/?ids=frus1945-50Inteld105,1974STATE085546
- http://127.0.0.1:5001/declass/v0.4/classification/collection/frus

#### does not work
- http://127.0.0.1:5001/declass/v0.4/?start_date=1947-01-01&end_date=1950-12-01  hangs and returns:
```
{"apiErrors":"Please contact administrator if this issue persists","error":{"code":404,"message":"Service raised an exception"}}
```
- http://127.0.0.1:5001/declass/v0.4/?date=1945-10-02 hangs and returns:
```
{"apiErrors":"Please contact administrator if this issue persists","error":{"code":404,"message":"Service raised an exception"}}
```
- http://127.0.0.1:5001/declass/v0.4/visualizations/frus/classification_countries/ returns:
```
{"apiErrors":"Please contact administrator if this issue persists","error":{"code":404,"message":"Service raised an exception"}}
```
- http://127.0.0.1:5001/declass/v0.4/entity_info returns:
```
{"apiErrors":[{"KeyError":"invalid request;"}],"error":{"code":404,"message":"Invalid API parameters"}}
```

- http://127.0.0.1:5001/declass/v0.4/text/ returns:
```
{"apiErrors":[{"KeyError":"invalid parameters; try one of the following: start_date,total_pages,end_date,page,collections,search,page_size"}],"error":{"code":404,"message":"Invalid API parameters"}}
```
- http://127.0.0.1:5001/declass/v0.4/documents/1977ACCRA03397/similar/ returns:
```
Not implemented yet
```
- http://127.0.0.1:5001/declass/v0.4/overview/ returns:
```
{"apiErrors":[{"KeyError":"invalid parameter value(s)"}],"error":{"code":404,"message":"Invalid API parameters"}}
```
