# Contributing to the API development #

This is a short guide showing how to add functionality to the api. Please
refer to SETUP.md for documention on how to start the API server. 

## Background ##

The API primarily uses the [python flask framework](http://flask.pocoo.org/), 
and [SQLAlchemy ORM](www.sqlalchemy.org) for all the DB interaction, with the 
addition of some custom functionality. Both libraries have documentation which 
is quite good and there are a number of great tutorials (
[basic](http://flask.pocoo.org/docs/quickstart/) and [in depth]
(http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)). 
If you are not familiar with API development or Flask, please work through some
of the online documentation before embarking on a project. The information below
assumes you are comfortable with the material. 

Data is returned in JSON format. To understand the declass API framework, 
standards for returned data, etc please see README.md.

## Pull Requests ##

Please fork the API, or create a new branch for development. When finished
send a pull request with a description of what has been done and what changes
are expected of the UI, or any other dependencies, to account for the new code. 

## Versioning ##

The API is versioned with base structure being 
http://api.declassification-engine.org/declass/v#/route where v# is the 
current version number. Please consider whether your contribution requires 
a new/next version or it is simple enough that it can be an addition to the 
current one. If a new version is warranted, please make sure to note this in 
the pull request comments. 

## HTTP Codes ##

Please use standard [http codes](http://en.wikipedia.org/wiki/List_of_HTTP_status_codes).
Flask make_response(), as well as our process() (found in api/util/clerk.py), 
allows for easy handling of these codes for success, error, etc. 

## CONFIGS ##

API configuration files live in api/config.
IMPORTANT! if you plan on changing any of the config files please make sure you
understand exactly what they do. At the moment it is best to talk to a declass 
lead. 

## UTILS ##

API utils live in api.util

These currently contain both data processing and common data rendering utls (clerk.py). 

### Debugging ###

It is virtually impossible to debug anything simply from browser errors, so 
Flask has a built in debug mode. This allows for both full traceback display 
as well as automatic reloading based on any file code changes (Flask listens 
to all system writes for files used in the API). 

You can run the code in debug mode by launching the API with:

```
python declass_api.py -d True
```

As usual just run 

```
python declass_api.py -h
```
to get the current run arguments. 

## Documentation ##

Please add/change documention whenever appropriate to reflect your 
contribution. 

