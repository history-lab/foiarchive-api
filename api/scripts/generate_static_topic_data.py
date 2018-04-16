import os
import pymysql
import pymysql.cursors
import pandas
import yaml
from flask import jsonify, make_response

DECLASS_API = os.getenv('DECLASS_API')
config_file = open(os.path.join(DECLASS_API, 'config', 'api_config.yml'))
config = yaml.load(config_file.read())['databases']


################################################
################ HELPER METHODS ################
################################################


def get_topic_title(cursor, topic_id=None):
    db_name = cursor.connection.db
    fields = config[db_name]['tables'][0]['fields']
    query_template = """
        SELECT
            id as topic_id,
            title
        FROM
            {db}.top_topics
        {where}
        ;
    """

    if topic_id is not None:
        query = query_template.format(where='WHERE id = {}'.format(topic_id), db=db_name)
    else:
        query = query_template.format(where='', db=db_name)

    cursor.execute(query)
    result = cursor.fetchall()

    for d in result:
        if d['title'] is None:
            d['title'] = 'ANONYMOUS'

    return result


def get_topic_tokens(cursor, topic_id, limit):
    query_template = """
        SELECT
            t.value as token,
            tt.token_score as score
        FROM
            topic_token tt INNER JOIN tokens t
                ON tt.token_id = t.id
        WHERE tt.topic_id = {topic_id}
        ORDER BY tt.token_score DESC
        LIMIT {limit}
        ;
    """
    query = query_template.format(topic_id=topic_id, limit=limit)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_topic_docs(cursor, topic_id, limit):
    db_name = cursor.connection.db
    fields = config[db_name]['tables'][0]['fields']
    query_template = """
        SELECT
            d.id,
            td.topic_score as topic_score,
            d.date,
            d.collection,
            d.title
        FROM
            {db}.topic_doc td INNER JOIN {db}.docs d
                ON td.doc_id = d.id
        WHERE td.topic_id = {topic_id}
        ORDER BY td.topic_score DESC
        LIMIT {limit}
        ;
    """
    query = query_template.format(topic_id=topic_id, limit=limit, db=db_name)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_top_topics(cursor, limit):
    query_template = """
        SELECT
            AVG(topic_score) as average_score,
            COUNT(topic_id) as doc_count,
            topic_id
        FROM topic_doc
        GROUP BY topic_id
        LIMIT {limit}
        ;
    """

    query = query_template.format(limit=limit)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_topics_given_doc(cursor, doc_id):
    query_template = """
        SELECT
            topic_id,
            topic_score
        FROM topic_doc
        WHERE doc_id = '{doc_id}'
        ;
    """
    query = query_template.format(doc_id=doc_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def custom_response(data, resp_code=200):
    count = len(data)
    response = make_response(jsonify(
        {'count': count, 'results': data}), resp_code)
    response.mimetype = 'application/json'
    response.headers['Content-Type'] = 'application/json'
    return response





try:
    os.mkdir('../topic_data')
except OSError:
    pass

try:
    os.mkdir('../topic_data/tokens')
except OSError:
    pass

try:
    os.mkdir('../topic_data/docs')
except OSError:
    pass

collections = [
    'cables',
    'ddrs',
    'frus',
    'kissinger',
    'clinton'
    'cpdoc'
]

# Loop over all possible collections and
# generate the appropriate files.
for collection_name in collections:

    try:
        os.mkdir('../topic_data/docs/{}'.format(collection_name))
    except OSError:
        pass

    try:
        os.mkdir('../topic_data/tokens/{}'.format(collection_name))
    except OSError:
        pass

    dbinfo = {
        'host': 'history-lab.org',
        'database': 'declassification_{}'.format(collection_name),
        'user': 'de_reader',
        'passwd': 'XreadF403',
        'cursorclass': pymysql.cursors.DictCursor}


    # Get possible topic ids.
    with pymysql.connect(**dbinfo) as cursor:
        query = """
            SELECT DISTINCT(topic_id)
            FROM topic_doc
            ;
        """
        cursor.execute(query)
        valid_topic_ids = {d['topic_id'] for d in cursor}


    # Load in all the topic
    print("Downloading token data for {}...".format(collection_name))
    tokens_limit = 100
    '''
    top_topic_tokens = {}
    for i, topic_id in enumerate(valid_topic_ids, 1):
        print("\t{0:.2f}%".format((100.0 * i) / len(valid_topic_ids)))
        topic_tokens = get_topic_tokens(cursor, topic_id, tokens_limit)
        df = pandas.DataFrame(topic_tokens)
        df.to_csv('../topic_data/tokens/{}/{}.csv'.format(collection_name, topic_id), index=False)
    '''

    # Load in all the doc data.
    print("Downloading doc data...")
    doc_limit = 100
    top_topic_docs = {}
    for i, topic_id in enumerate(valid_topic_ids, 1):
        print("\t{0:.2f}%".format((100.0 * i) / len(valid_topic_ids)))
        topic_docs = get_topic_docs(cursor, topic_id, tokens_limit)
        df = pandas.DataFrame(topic_docs)
        df.to_csv('../topic_data/docs/{}/{}.csv'.format(collection_name, topic_id), index=False)
