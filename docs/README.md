# Declassification Engine API (v0.4) #
The Declassification Engine API is a RESTful way to access information in the Declassification Engine Database using basic web-based requests. It returns JSON formatted data and is set up for [Cross-Origin Resource Sharing](http://en.wikipedia.org/wiki/Cross-origin_resource_sharing).

Currently the API is lightweight, supporting queries by unique Document IDs and certain entity fields. It can also furnish random Document IDs on request.

The API can be accessed by navigating to

```
http://api.declassification-engine.org/declass/v0.4/
```

## Retrieving Information ##

### Requests by Document ID ###
The API allows queries by document ids.
Example:
```
http://api.declassification-engine.org/declass/v0.4/?id=frus1945-50Inteld105
```
This will make a request to return _all available fields_ for the document with the id `frus1945-50Inteld105`. The user will recieve the [Standard Return Object](#returned-data).

Likewise, one can request mutiple Document IDs using comma-separated arguments at `?ids=`. For example:
```
http://api.declassification-engine.org/declass/v0.4/?ids=frus1945-50Inteld105,1974STATE085546
```
Which will return _all available fields_ for both of the Document IDs. They will appear as separate objects in the [Standard Return Object](#returned-data)
Note that you are able to mix Document IDs from different collections.

In addition to quering collections by document id, the API includes the ability to query based on countries, persons, topics, and dates.

The API takes the following parameters: geo_ids, person_ids, topic_ids, start_date, end_date, date and collections (it will also error and return a list of valid parameters if you pass something invalid). The ids are unique entity ids coming from the corresponding table in the DB, which are currently amended ISO codes for countries and internally generated ids for persons and topics. The dates are strings in any MySQL acceptable date format. You can combine geo_ids/person_ids/topic_ids via basic disjunctions ("AND") or conjunctions ("OR") but not both, i.e. you can request all documents which mention country X AND Y AND Z or which mention X OR Y OR Z, but not (X AND Y) OR Z, etc. The latter you can achieve easily with two purely disjunctive/conjunctive queries and, hence, these are not part of the API functionality. Below are some basic examples of use. You can specify which collections to query; currently supported include frus, kissinger, ddrs, statedeptcables, and clinton.

Welcome screen:
```
http://api.declassification-engine.org/declass
```

List all available document metadata fields the API can return:
```
http://api.declassification-engine.org/declass/v0.4/fields
```

List available collections a user can query:
```
http://api.declassification-engine.org/declass/v0.4/collections
```

Display the available entities for a particular collection:
```
http://api.declassification-engine.org/declass/v0.4/entity_info/?collection=collection_name
```

Queries the collection for the specified entity:
```
http://api.declassification-engine.org/declass/v0.4/entity_info/?collection=collection_name&entity=entity_name
```

Return random document ids (can include a limit):
```
http://api.declassification-engine.org/declass/v0.4/random/
http://api.declassification-engine.org/declass/v0.4/random/?limit=32
```

Autocomplete entity names:
```  
http://api.declassification-engine.org/declass/v0.4/entities/<start_word>/autocomplete/?type=persons
http://api.declassification-engine.org/declass/v0.4/entities/<start_word>/autocomplete/?type=countries
http://api.declassification-engine.org/declass/v0.4/entities/<start_word>/autocomplete/?type=topics
```

Start/end date range:
```
http://api.declassification-engine.org/declass/v0.4/?start_date=1947-01-01&end_date=1950-12-01
```

Exact date match:
```
http://api.declassification-engine.org/declass/v0.4/?date=1945-10-02
```

Geo match conjunctive:
```
http://api.declassification-engine.org/declass/v0.4/?geo_ids=004AND804
```

Geo match disjunctive:
```
http://api.declassification-engine.org/declass/v0.4/?geo_ids=004OR804OR040
```

Geo, persons and date:
```
http://api.declassification-engine.org/declass/v0.4/?person_ids=p_AD1ANDp_CIK1ANDp_MCA1&geo_ids=004OR804OR040&start_date=1947-01-01&end_date=1950-12-01
```

Topics:
```
http://api.declassification-engine.org/declass/<version>/?topic_ids=61  
http://api.declassification-engine.org/declass/<version>/?geo_ids=010&topic_ids=61
http://api.declassification-engine.org/declass/<version>/?person_ids=George&geo_ids=010&topic_ids=61
```

Specifying collections:
```
http://api.declassification-engine.org/declass/v0.4/?start_date=1950-01-01&end_date=1960-02-01&collections=frus,kissinger
```


Overview of the top entities:
```
http://api.declassification-engine.org/declass/v0.4/overview/?collection=colleciton_name&entity=entity_name&start_date=date1&end_date=date2
```

The searchable entities are countries, topics, and persons. One can also update the topics and persons entities given country_ids:
```
http://api.declassification-engine.org/declass/v0.4/overview/?collection=colleciton_name&entity=entity_name&start_date=date1&end_date=date2&geo_ids=country_id
```

Full-text search:
```
http://api.declassification-engine.org/declass/v0.4/text/?search=search_phrase&start_date=date&end_date=date&collections=c1,c2&page=3&page_size=20
```

### Topics ###

Lists topic information in a particular collection:
```
http://api.declassification-engine.org/declass/v0.4/topics/collection/collection_name
```

Lists tokens for a particular topic in a collection:
```
http://api.declassification-engine.org/declass/v0.4/topics/collection_name/topic/topic_id
```

Lists the documents associated with a particular topic:
```
http://api.declassification-engine.org/declass/v0.4/topics/collection_name/docs/topic_id
```

Lists the topics associated with a particular document:
```
http://api.declassification-engine.org/declass/v0.4/topics/doc/_doc_id_")
```

### Requesting Specific Fields Only ###

To request specific fields for a either a query by entities or document ids,  one must also include the fieldnames as comma-separated values to the `fields=` parameter in the querystring.

Examples:
```
http://api.declassification-engine.org/declass/v0.4/?ids=1974STATE085546,frus1945-50Inteld105&fields=subject,date

http://api.declassification-engine.org/declass/v0.4/?start_date=1950-01-01&end_date=1960-02-01&fields=subject,date
```
This will return two objects that only have values for `subject` and `date`. If a given collection does not contain a particular field a Null value will be returned for that field.

### Getting the Available Fields ###
One has to know what fields are available in order to make specific requests. In order to see all the available fields:
```
http://api.declassification-engine.org/declass/v0.4/fields
```
The user will recieve the [Standard Return Object](#returned-data) with an array of field names in the first object of the results array. It might look something like:
```javascript
{
  "count": 2,
  "results": [
    {
      "fields": [
        "body",
        "body_html",
        "body_summary",
        "chapt_title",
        "countries",
        "collection",
        "date",
        "date_year",
        "date_month",
        "doc_refs",
        "from_field",
        "id",
        "location",
        "nuclear",
        "persons",
        "topics",
        "refs",
        "cable_references",
        "source",
        "source_path",
        "cable_type",
        "subject",
        "title",
        "to_field",
        "tags",
        "description",
        "pdf"
      ]
    }
  ]
}
```

###REST implementation consistency
For the purposes of being consistent with frameworks like [backbone](http://backbonejs.org/)
the api offers a delegated document route.
Example:
```
http://api.declassification-engine.org/declass/v0.4/documents/frus1950-55Inteld203
http://api.declassification-engine.org/declass/v0.4/documents/frus1950-55Inteld203,frus1977-80v13d104
```

You can also pass api parameters and fields dicussed above.
Example:
```
http://api.declassification-engine.org/declass/v0.4/documents/frus1950-55Inteld203/?fields=names,date,body&page=0
```

###Similar documents (Textdrop)
Currently the similar document route redirects to the merriam api with default parameters.
Example:
```
http://api.declassification-engine.org/declass/v0.4/textdrop/?text=some_long_text
http://api.declassification-engine.org/declass/v0.4/textdrop/?text=some_long_text&limit=30
```

### Pagination ###
Version 0.4 of the API now supports hashed pagination, which will be useful for developers as we move forward. It allows those requesting data to put a limit on how many results will come back per each request.

In order to receive data in paginated form, the user must pass two querystring arguments:
* `page` => A string value that tells the API which page of data you want returned.
* `page_size` => is default 25

Example:
```
http://api.declassification-engine.org/declass/v0.3/?ids=
[over a hundred ids here]&page=fj897fsdUfIf80Dxcmsk887
```
This query will return the first page of data, which is given a `page_size` of 25.
NOTE: There are specific pagination attributes included on the [Standard Return Object](#returned-data) that will tell the user which page they are on and also give them the URL of the next page. Please see the section on [Returned Data](#returned-data) for more information.

## Returned Data ##
The Declassification Engine API v0.4 now returns JSON that is completely standardized, meaning that no matter what the user requests the structure of returned data will always be the same. 

### Basic Return Object ###
Should a request go through successfully, at minimum it will look something like this:
```javascript
{
  count: 2,
  results: [
    {
      id: '1976STATE01A',
      body: // body text here,
      date: '11-11-1976',
      drafter: '',
   },
   {
      id: '1977STATE2238YT',
      body: // body text here,
      date: '4-7-1977',
      drafter: 'Glenn Packer',
   }
  ],
  nextPage: null,
  page: string,
  page_size: 0
}
```

### Paginated Return Object ###
A paginated return object is just like the basic version, except that there will be values for `nextPage`, `page`, and `page_size`. Here's how they are structured:
* `page` => The current page of returned results
* `page_size` => The number to return for each page. This should reflect the value the user specified in the initial querystring.
* `nextPage` => A string that contains a properly contructed URL for retrieving the next page.

To see how `nextPage` works, consider this example. First we make a request for paginated data:
```
http://api.declassification-engine.org/declass/v0.3/?ids=[dozens of ids here]&fields=subject&page_size=10
```
This query will return something like:
```javascript
{
   count: 5,
   results: [
      {
         id: 'id1',
         subject: 'Subject 1'
      },
      {
         id: 'id2',
         subject: 'Subject 2',
      },
      // And so on for 8 more results
   ],
   page: some_string,
   page_size: 10,
   nextPage: 'http://api.declassification-engine.org/declass/v0.3/ids=[dozens of ids here]&fields=subject&page=fsfkj09dUkv89sdfkl234'
}
```


## Feature Requests / Reporting Bugs ##
We have been developing this API based on requested features and anticipation of upcoming needs. Should the API not currently do something that you might need it to, please [post an Issue](https://github.com/declassengine/api/issues?state=open) and mark it as a 'Feature Request'. If you come across some bug or error, please follow the same pattern but instead mark the Issue as a 'Bug'.

## Contributing ##

Please see CONTRIBUTING.md
