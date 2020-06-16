"""
Main API file containing all end-point routes. Initializes a Controller
object and a Clerk object to communicate with the Declass Database and
return JSON formatted responses.
"""


from flask import redirect, request, abort
from flask_cors import cross_origin
from api import app, clerk, controller


@app.route('/')
@cross_origin()
def api_root():
    """
    Displays a welcome text to the user.

    @rtype:   string
    @return:  API welcome text.
    """
    return 'Welcome to the FOIArchive REST API'


@app.route('/<version>/fields')
@cross_origin()
def declass_fields(version):
    """
    This end-point returns the metadata fields that a user can expect
    to be returned by the API quering available collecitons.

    @rtype:   json
    @return:  Array of available metadata across collections.
    """

    probe_request(version, request)

    return controller.get_config_fields(display=True)


@app.route('/<version>/collections')
@cross_origin()
def declass_available_collections(version):
    """
    This end-point displays the available collections to query from.

    @rtype:   json
    @return:  Array of available collections in database.
    """
    probe_request(version, request)

    return controller.get_collection_names(display=True)


@app.route('/<version>/entity_info/')
@cross_origin()
def declass_entity_info(version):
    """
    This end-point displays the available entities for a particular
    collection. It also displays the results of a particular entity search
    for a collection.

    The end-point can be called in the following ways:
    /<version>/entity_info/?collection=<colleciton_name>
    /<version>/entity_info/?collection=<colleciton_name>&entity=<entity_name>
    /<version>/entity_info/?collection=<colleciton_name>&entity=<entity_name>&page_size=<number>&page=<number>

    @type  collection: string
    @param colleciton: The name of a collection. (ex. frus)
    @type  entity: string
    @param entity: The entity that you would like to search. (ex. countries,
        topics, persons)
    @type  page_size: number
    @param page_size: The number of results to be returned for a query.
    @type  page: number
    @param page: This parameter displays a specific results page.

    @rtype:   json
    @return:  Array of entity records for a particular collections in database.
    """
    accepted_params = {'entity', 'collection', 'page', 'page_size'}
    probe_request(version, request, accepted_params)

    # Loading the header request fields
    entity = request.args.get('entity')
    collection = request.args.get('collection')

    # Make sure page is valid if any.
    page = request.args.get('page')
    if page and not page.isdigit():
        complain('InvalidValues')

    page = int(request.args.get('page', 1))

    page_size = int(request.args.get('page_size',
                                     controller.PAGE_SIZE_DEFAULT))

    return controller.get_entity_info(entity, collection, page, page_size,
                                      request.url)


@app.route('/<version>/overview/')
@cross_origin()
def declass_overview(version):
    """
    This end-point displays an overview of the top mentioned
    entities of a particular collection.

    The end-point can be called in the following ways:
    /<version>/overview/?collection=<colleciton_name>&entity=<entity_name>&start_date=<date1>&end_date=<date2>

    The searchable entities are countries, topics, and persons. One can
    also update the topics and persons entities given country_ids:
    /<version>/overview/?collection=<colleciton_name>&entity=<entity_name>&start_date=<date1>&end_date=<date2>&geo_ids=<country_id>

    @type  collection: string
    @param colleciton: The name of a collection. (ex. frus)
    @type  entity: string
    @param entity: The entity that you would like to search. (ex. countries,
        topics, persons)
    @type  start_date: date
    @param start_date: The starting date for query selection.
    @type  end_date: date
    @param end_date: The ending date for query selection.
    @type  geo_ids: string
    @param geo_ids: Country ids (optional) This provides an updated count for
        topics and persons given selected countries.
    @type  limit: number
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of top counts for persons or countries or topics
    for a particular collection.
    """
    accepted_params = {'entity', 'collection', 'start_date', 'end_date',
                       'geo_ids', 'limit'}
    probe_request(version, request, accepted_params)

    entity = request.args.get('entity', None)
    if entity != 'persons' and entity != 'countries' and \
       entity != 'topics' and entity != 'classifications':
        complain('InvalidValues')

    filters = {}
    filters['collections'] = [] if (not request.args.get('collection')) else \
                             [request.args.get('collection').lower()]
    filters['start_date'] = request.args.get('start_date',  None)
    filters['end_date'] = request.args.get('end_date', None)
    filters['exact_date'] = None
    filters['page'] = None

    # Check if user entered an invalid filter
    if not filters['collections']:
        complain('InvalidValues')

    if not clerk.valid_filters(filters):
        complain("Filters", accepted_params)

    # Make sure limit is valid.
    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 100, int)

    # Verifying if geo_ids is passed in properly
    passed_params = [] if (not list(request.args.items())) else \
                    [i[0].lower() for i in list(request.args.items())]
    entities = clerk.valid_entities(passed_params, request)
    if not entities:
        complain("Entities", accepted_params)

    geo_ids = entities['geo_ids']
    geo_logic = entities['geo_logic']

    if geo_logic and geo_logic != "OR":
        complain('InvalidValues')

    return controller.get_overview_data(entity, limit, geo_ids, filters,
                                        request.url)


@app.route('/<version>/visualizations/doc_cnts/')
@cross_origin()
def declass_viz_doc_cnts(version):
    """
    Route for the declass.visualizations.doc_cnts table.
    Simply returns all the content of that table.
    """
    probe_request(version, request)

    return controller.get_viz_docs('doc_cnts')


@app.route('/<version>/visualizations/doc_collection/')
@cross_origin()
def declass_viz_doc_collect(version):
    """
    Route for the declass.visualizations.doc_collection table.
    Simply returns all the content of that table.
    """
    probe_request(version, request)

    return controller.get_viz_docs('doc_collection')


@app.route('/<version>/visualizations/doc_cnts_year/')
@cross_origin()
def declass_viz_doc_counts_year(version):
    """
    Route for declass.visualizations.doc_cnts_year table.
    Returns all of the content from the table
    """
    probe_request(version, request)

    return controller.get_viz_docs('doc_cnts_year')


@app.route('/<version>/visualizations/overview/')
@cross_origin()
def declass_viz_overview(version):
    """
    Route for the overview tables. Simply returns all the content with
    user-defined limit.
    """
    database = request.args.get('database', 'frus')
    # Validate database input.
    databases = database.split(',')
    acceptable_databases = ['frus', 'statedeptcables', 'ddrs', 'kissinger',
                            'clinton', 'cpdoc', 'cabinet', 'pdb']
    if set(databases) - set(acceptable_databases):
        return clerk.complain(404, "Invalid API parameters",
                                   "Invalid Database name(s).")

    table = request.args.get('table', 'top_persons')
    # Validate table input.
    tables = table.split(',')
    acceptable_tables = ['top_persons', 'top_countries', 'top_topics',
                         'doc_counts', 'top_classifications']
    if set(tables) - set(acceptable_tables):
        return clerk.complain(404, "Invalid API parameters",
                                   "Invalid table name(s).")

    limit = request.args.get('limit', 10)
    # Validate limit input.
    if limit == 'null':
        limit = None
    else:
        limit_error = False
        try:
            limit = int(limit)
        except ValueError:
            limit_error = True
        if limit_error or limit <= 0:
            return clerk.complain(404, "Invalid API parameters",
                                       "limit must be a positive integer.")

    return controller.get_viz_overview(databases, tables, limit)


@app.route('/<version>/visualizations/<collection_name>/\
classification_topics/')
@cross_origin()
def declass_viz_classification_topics(version, collection_name):
    """
    Route for classification topics visualizations
    """
    probe_request(version, request)

    return controller.get_classification_topics(collection_name)


@app.route('/<version>/visualizations/<collection_name>/\
classification_countries/')
@cross_origin()
def declass_viz_classification_countries(version, collection_name):
    """
    Route for classification topics visualizations
    """
    probe_request(version, request)
    return controller.get_classification_countries(collection_name)


@app.route('/<version>/visualizations/<collection_name>/\
classification_persons/')
@cross_origin()
def declass_viz_classification_persons(version, collection_name):
    """
    Route for classification topics visualizations
    """
    probe_request(version, request)
    return controller.get_classification_persons(collection_name)


@app.route('/<version>/random/')
@cross_origin()
def random_doc_ids(version):
    """
    This end-point displays a list of random document ids from across
    all available collections.

    Can be invoked by:
    /v0.4/random
    /v0.4/random/?limit=<number>

    @type  limit: number (optional, default 10)
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of document ids.
    """
    print(request)
    accepted_params = {'limit'}
    probe_request(version, request, accepted_params)

    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 10, int)
    return controller.get_random_doc_ids(limit)


@app.route('/<version>/documents/<doc_ids>/')
@cross_origin()
def documents(version, doc_ids):
    """
    This end-point redirects traffic to another end-point.
    """
    return redirect('/%s/?ids=%s' % (
        version, doc_ids), code=303)


@app.route('/<version>/textdrop/')
@cross_origin()
def declass_text_drop(version):
    """
    This end-point allows a user to enter a long piece of text and
    searchers for documents across different collections that
    contain similar text. It is powered by Merriam.

    Can be invoked by:
    /v0.4/textdrop/?text=<long_text>
    /v0.4/textdrop/?text=<long_text>&limit=<number>

    @type  text: string
    @param text: A piece of text to use for finding similar documents.
    @type  limit: number (optional, default 25)
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of documents info related to text.
    """
    accepted_params = {'limit', 'text'}
    probe_request(version, request, accepted_params)

    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 25, int)
    text = request.args.get('text', None)

    merriam_link = controller.get_merriam_link()
    return controller.text_drop_search(merriam_link, text, limit)


@app.route('/<version>/documents/<doc_id>/similar/')
@cross_origin()
def documents_similar(version, doc_id):
    """
    This end-point searches for documents that are similar to
    a given doc_id. It is powered by Merriam.
    Status: Not implemented yet.

    @rtype:   json
    @return:  Array of documents info related to doc_id.
    """
    probe_request(version, request)

    return "Not implemented yet"
    # merriam_link = controller.get_merriam_link()
    # return redirect('%s/%s/?%s' % (merriam_link, doc_id,
    #    request.query_string), code=303)


@app.route('/<version>/entities/autocomplete/')
@cross_origin()
def declass_entity_autocomplete(version):
    """
    This end-point provides the functionality for entity
    autocompletion across all collections.

    Can be invoked by:
    /v0.4/entities/autocomplete/?type=<entity>&autocomplete_text=<query>

    @type  type: string
    @param type: A valid collection entity (persons, countries, topics).

    @type  autocomplete_text: string
    @param search: An autocomplete query.

    @rtype:   json
    @return:  Array of documents info starting with <word_start>.
    """
    accepted_params = {'type', 'autocomplete_text'}
    word_start = request.args.get('autocomplete_text')

    probe_request(version, request, accepted_params)

    entity_type = request.args.get('type')

    return controller.get_entity_autocomplete(word_start, entity_type)


@app.route('/<version>/')
@cross_origin()
def api(version):
    """
    This end-point provides the core functionality for quering the
    available collections.

    @type  id: string
    @param id: A document id.
    @type  ids: string
    @param ids: A comma seperated list of document ids.
    @type  start_date: date
    @param start_date: The starting date for query selection.
    @type  end_date: date
    @param end_date: The ending date for query selection.
    @type  date: date
    @param date: The exact date for query selection.
    @type  collections: string
    @param collecitons: The name(s) of a collection. (ex. frus)
    @type  fields: string
    @param fields: A comma seperated list of filtering metadata fields
        to query.
    @type  person_ids: string
    @param person_ids: A list of person ids joined by AND / OR.
    @type  geo_ids: string
    @param geo_ids: A list of country ids joined by AND / OR.
    @type  topic_ids: string
    @param topic_ids: A list of topic ids joined by AND / OR
    @type  page_size: number
    @param page_size: The number of results to be returned for a query.
    @type  page: string
    @param page: This parameter displays a specific results page.
        It is a hashed pagination variable.

    @rtype:   json
    @return:  Array of documents info.
    """
    if not clerk.is_valid_version(version):
        complain("Version")

    if clerk.is_missing_param_key_val(request):
        complain("Partial")

    if not clerk.is_valid_pagination(request, page_type="hash"):
        complain("Pagination")

    # Load the list of accepted paramaters and fields
    accepted_params = controller.get_config_parameters()
    accepted_fields = controller.get_config_fields()

    # ------------------------------------------------------------------- #
    # Analyze user input to validate requested parameters and fields
    # ------------------------------------------------------------------- #

    passed_params = [] if (not list(request.args.items())) \
        else [i[0].lower() for i in list(request.args.items())]
    passed_fields = [] if (not request.args.get('fields')) \
        else request.args.get('fields').lower().split(',')
    filters = {}
    filters['start_date'] = request.args.get('start_date',  None)
    filters['end_date'] = request.args.get('end_date', None)
    filters['exact_date'] = request.args.get('date', None)
    filters['page'] = request.args.get('page')
    filters['page_size'] = int(request.args.get('page_size',
                                                controller.PAGE_SIZE_DEFAULT))
    filters['page_start_index'] = clerk.set_page_start_index(filters['page'])
    filters['page_url'] = request.url

    filters['collections'] = [] if (not request.args.get('collections')) \
        else request.args.get('collections').lower().split(',')
    if not filters['collections']:
        filters['collections'] = controller.get_collection_names()
    filters['fields'] = accepted_fields
    if passed_fields:
        filters['fields'] = passed_fields

    # Check if user entered an invalid parameter
    if not clerk.valid_params(passed_params, accepted_params, request):
        complain("Parameters", accepted_params)

    # Check if user entered an invalid field
    if not clerk.valid_fields(passed_fields, accepted_fields):
        complain("Fields", accepted_fields)

    # Check if user entered an invalid entity
    entities = clerk.valid_entities(passed_params, request)
    if not entities:
        complain("Entities", accepted_params)

    # Assign any Entities
    person_ids = entities['person_ids']
    person_logic = entities['person_logic']

    geo_ids = entities['geo_ids']
    geo_logic = entities['geo_logic']

    topic_ids = entities['topic_ids']
    topic_logic = entities['topic_logic']

    classification_ids = entities['classification_ids']
    classification_logic = entities['classification_logic']

    # Check if user entered an invalid filter
    if not clerk.valid_filters(filters):
        complain("Filters", accepted_fields)

    # ---------------------------------------------------------------------- #
    # Perform a search operation depending on specified parameters
    # ---------------------------------------------------------------------- #

    # 1: Search documents by single id or list of ids
    if "id" in passed_params or "ids" in passed_params:
        accepted_params = {'id', 'fields'}
        doc_ids = [request.args.get('id')]

        if "ids" in passed_params:
            accepted_params = {'ids', 'fields'}
            doc_ids = [doc for doc in request.args.get('ids').split(',')]

        if not clerk.valid_params(passed_params, accepted_params, request):
            complain("Parameters", accepted_params)

        return controller.find_docs_by_ids(doc_ids, filters)

    # 2: Search documents by classification, persons, countries, and topics
    if "person_ids" in passed_params and "geo_ids" in passed_params and \
       "topic_ids" in passed_params and "classification_ids" in passed_params:
        return controller.find_docs_by_person_country_topic_classification(
          person_ids, person_logic, geo_ids, geo_logic, topic_ids, topic_logic,
          classification_ids, classification_logic, filters)

    # 3: Search documents by persons, countries, and topics entities combined
    if "person_ids" in passed_params and "geo_ids" in passed_params and \
       "topic_ids" in passed_params:
        return controller.find_docs_by_person_country_topic(
          person_ids, person_logic, geo_ids, geo_logic, topic_ids, topic_logic,
          filters)

    # 4: Search documents by classification, topics, and persons
    if "person_ids" in passed_params and \
       "classification_ids" in passed_params and "topic_ids" in passed_params:
        return controller.find_docs_by_person_classification_topic(
          person_ids, person_logic, classification_ids, classification_logic,
          topic_ids, topic_logic, filters)

    # 5: Search documents by classification, topics, and countries
    if "classification_ids" in passed_params and \
       "geo_ids" in passed_params and "topic_ids" in passed_params:
        return controller.find_docs_by_classification_country_topic(
          classification_ids, classification_logic, geo_ids, geo_logic,
          topic_ids, topic_logic, filters)

    # 6: Search documents by classification, persons, and countries
    if "person_ids" in passed_params and "geo_ids" in passed_params and \
       "classification_ids" in passed_params:
        return controller.find_docs_by_person_country_classification(
          person_ids, person_logic, geo_ids, geo_logic,
          classification_ids, classification_logic, filters)

    # 7: Search documents by persons and countries combined
    if "person_ids" in passed_params and "geo_ids" in passed_params:
        return controller.find_docs_by_person_country(
          person_ids, person_logic, geo_ids, geo_logic, filters)

    # 8: Search documents by persons and topics combined
    if "person_ids" in passed_params and "topic_ids" in passed_params:
        return controller.find_docs_by_person_topic(
          person_ids, person_logic, topic_ids, topic_logic, filters)

    # 9: Search documents by countries and topics combined
    if "geo_ids" in passed_params and "topic_ids" in passed_params:
        return controller.find_docs_by_country_topic(
          geo_ids, geo_logic, topic_ids, topic_logic, filters)

    # 10: Search documents by classification and persons
    if "person_ids" in passed_params and "classification_ids" in passed_params:
        return controller.find_docs_by_person_classification(
          person_ids, person_logic, classification_ids, classification_logic,
          filters)

    # 11: Search documents by classification and countries
    if "geo_ids" in passed_params and "classification_ids" in passed_params:
        return controller.find_docs_by_classification_country(
          classification_ids, classification_logic, geo_ids, geo_logic,
          filters)

    # 12: Search documents by classification and topics
    if "classification_ids" in passed_params and "topic_ids" in passed_params:
        return controller.find_docs_by_classification_topic(
          classification_ids, classification_logic, topic_ids, topic_logic,
          filters)

    # 13: Search documents by persons only
    if "person_ids" in passed_params:
        return controller.find_docs_by_persons(
          person_ids, person_logic, filters)

    # 14: Search documents by countries only
    if "geo_ids" in passed_params:
        return controller.find_docs_by_country(geo_ids, geo_logic, filters)

    # 15: Search documents by topics only
    if "topic_ids" in passed_params:
        return controller.find_docs_by_topic(topic_ids, topic_logic, filters)

    # 16: Search documents by classification only
    if "classification_ids" in passed_params:
        return controller.find_docs_by_classification(
          classification_ids, classification_logic, filters)

    # 17: Search all documents by date or date range
    if filters['exact_date'] or filters['start_date']:
        return controller.find_docs_by_date(filters)

    complain("Parameters", accepted_params)


@app.route('/<version>/topics/collection/<collection_name>')
@cross_origin()
def declass_collection_topics(version, collection_name):
    """
    This end-point lists topic information in a particular collection.

    @type  limit: number
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of topic information for a collection.
    """
    accepted_params = {'limit'}
    probe_request(version, request, accepted_params)

    # Make sure limit is valid.
    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 10, int)
    return controller.get_collection_topics(collection_name, limit)


@app.route("/<version>/topics/<collection_name>/topic/<topic_id>")
@cross_origin()
def declass_topic_tokens(version, collection_name, topic_id):
    """
    This end-point lists tokens for a particular topic in a collection.

    @type  limit: number
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of token information for a topic in a collection.
    """
    accepted_params = {'limit'}
    probe_request(version, request, accepted_params)

    # Make sure limit and topic_id are valid integers
    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    if not topic_id.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 25, int)
    return controller.get_topic_tokens(collection_name, int(topic_id), limit)


@app.route("/<version>/topics/<collection_name>/docs/<topic_id>")
@cross_origin()
def declass_topic_docs(version, collection_name, topic_id):
    """
    This end-point lists the documents associated with a particular topic.

    @type  limit: number
    @param limit: The number of records to be returned for the query.

    @rtype:   json
    @return:  Array of documents info for a topic in a collection.
    """
    accepted_params = {'limit'}
    probe_request(version, request, accepted_params)

    # Make sure limit and topic_id are valid integers
    limit = request.args.get('limit')
    if limit and not limit.isdigit():
        complain('InvalidValues')

    if not topic_id.isdigit():
        complain('InvalidValues')

    limit = request.args.get('limit', 25, int)
    return controller.get_topic_docs(collection_name, int(topic_id), limit)


@app.route("/<version>/topics/doc/<doc_id>")
@cross_origin()
def declass_doc_topics(version, doc_id):
    """
    This end-point lists the topics associated with a particular document.

    @rtype:   json
    @return:  Array of topics info for a document id.
    """
    # Check that this is a valid doc_id.
    probe_request(version, request)
    return controller.get_doc_topics(doc_id)


@app.route("/<version>/classification/collection/<collection_name>")
@cross_origin()
def declass_classification_count(version, collection_name):
    """
    This end-point lists the topics associated with a particular document.

    @rtype:   json
    @return:  Array of topics info for a document id.
    """
    # Check that this is a valid doc_id.
    probe_request(version, request)
    return controller.get_classification_collection(collection_name)


@app.route("/<version>/tags/collection/<collection_name>/doc/<doc_id>")
@cross_origin()
def declass_tag_doc(version, collection_name, doc_id):
    """
    This end-point lists the topics associated with a particular document.

    @rtype:   json
    @return:  Array of topics info for a document id.
    """
    # Check that this is a valid doc_id.
    probe_request(version, request)
    return controller.get_tag_docs(collection_name, doc_id)


@app.route("/<version>/text/")
@cross_origin()
def declass_full_text_search(version):
    """
    This end-point uses Elasticsearch to perform user query.

    @type  search: string
    @param search: A search query.
    @type  start_date: date
    @param start_date: The starting date for query search.
    @type  end_date: date
    @param end_date: The ending date for query search.
    @type  collections: string
    @param collecitons: The name(s) of a collection. (ex. frus)
    @type  page_size: number
    @param page_size: The number of results to be returned for a query.
    @type  page: number
    @param page: This parameter displays a specific results page.

    @rtype:   json
    @return:  Array of documents info.
    """

    accepted_params = {'search', 'page_size', 'page', 'start_date', 'end_date',
                       'collections'}
    passed_params = [] if (not list(request.args.items())) \
        else [i[0].lower() for i in list(request.args.items())]

    filters = {}
    filters['start_date'] = request.args.get('start_date',  None)
    filters['end_date'] = request.args.get('end_date', None)
    filters['exact_date'] = None
    filters['page'] = request.args.get('page', '1')
    filters['page_size'] = request.args.get('page_size',
                                            str(controller.PAGE_SIZE_DEFAULT))
    filters['page_url'] = request.url
    search_text = request.args.get('search')

    filters['collections'] = [] if (not request.args.get('collections')) \
        else request.args.get('collections').lower().split(',')
    if not filters['collections']:
        filters['collections'] = controller.get_collection_names()

    if not clerk.is_valid_version(version):
        complain("Version")

    if not clerk.valid_params(passed_params, accepted_params, request):
        complain("Parameters", accepted_params)

    if clerk.is_missing_param_key_val(request):
        complain("Partial")

    if not clerk.valid_filters(filters):
        complain("Filters", accepted_params)

    if not search_text:
        complain("Parameters", accepted_params)

    if filters['page'] and not filters['page'].isdigit():
        complain('InvalidValues')

    if filters['page_size'] and not filters['page_size'].isdigit():
        complain('InvalidValues')

    return controller.full_text_search(search_text, filters)


@app.errorhandler(404)
def page_not_found(e):
    """
    This function captures all invalid requests and page not found
    results.
    """
    return clerk.complain(404, "Invalid API parameters",
                          [{'KeyError': 'invalid request;'}])


@app.errorhandler(Exception)
def all_exception_handler(error):
    """
    This function encapsulates all errors and hides them from the user.
    If any error occurs, the exception trace is hidden and a default
    message is provided instead.
    """
    return clerk.complain(404, "Service raised an exception", "Please contact \
administrator if this issue persists")


def probe_request(version, request, accepted_params=None):
    """
    This function checks for valid API requests.

    @type  version: string
    @param version: The API version to use (ex. v0.4).
    @type  request: string
    @param request: The url header invoked by the user
    @type  accepted_params: list
    @param accepted_params: A list of parameters that the method accepts.

    @rtype:   None
    @return:  Returns an error message if the url is unacceptable.
    """
    if not clerk.is_valid_version(version):
        complain("Version")

    if list(request.args.items()):
        request_args = list(request.args.items())
        print(request_args)
        if accepted_params is None:
            complain("NoParameters")

        passed_params = [] if (not request_args) \
            else [i[0].lower() for i in request_args]

        if not clerk.valid_params(passed_params, accepted_params, request):
            complain("Parameters", accepted_params)

    if clerk.is_missing_param_key_val(request):
        complain("Partial")

    if not clerk.is_valid_pagination(request):
        complain("Pagination")


def complain(message, parameters=None):
    """
    This function returns an error message to the user.

    @type  message: string
    @param message: The error message to be returned to the user.
    @type  params: list
    @param params: A list of parameters that the user can call.

    @rtype:   string
    @return:  Returns an error message to the user.
    """
    if message == "Version":
        valid_versions = controller.supported_versions
        complaint = clerk.complain(404, "Invalid API version", [{'KeyError':
                                   'invalid version; try one of the following: \
                                   %s' % (','.join(str(i)
                                                   for i in valid_versions))}])

    if message == "Parameters":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid parameters; try one of the \
                                   ''following: %s' % (','.join(parameters))}])

    if message == "NoParameters":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'request does not expect to take any \
                                   parameter'}])

    if message == "Fields":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid fields; try one of the \
                                   ''following: %s' % (','.join(parameters))}])

    if message == "Entities":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid fields; try one of the \
                                   ''following: %s' % (','.join(parameters))}])

    if message == "Filters":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid filters; try one of the \
                                   ''following: %s' % (','.join(parameters))}])

    if message == "Partial":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'some keys do not contain values'}])

    if message == "Pagination":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid page or page_size values'}])

    if message == "InvalidValues":
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid parameter value(s)'}])

    if message == 404:
        complaint = clerk.complain(404, "Invalid API parameters", [{'KeyError':
                                   'invalid request; try one of the \
                                   ''following: %s' % (parameters)}])

    abort(complaint)
