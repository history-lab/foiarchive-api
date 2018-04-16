import re
import os
import yaml
import logging

from datetime import date, datetime
from urllib.request import unquote
from flask.json import JSONEncoder
from flask import jsonify, make_response
from logging import Formatter, FileHandler

class Clerk(object):
    """
    This class is responsible for providing any and all utility functions
    necessary for the Controller and the main declass_api files to
    process data.
    """

    def __init__(self, controller):
        self.JSON = Clerk.CustomJSONEncoder()
        self.controller = controller
        self.LOG_FILE = os.path.join(controller.DECLASS_API, 'src/api.log')


    def process(self, data, resp_code, json_encoder=jsonify, page=None, page_size=None, next_page=None, count=None):
        """
        Custom respose function to prepare JSON output to user.
        """
        if count is None:
            count = len(data)

        output = {'count': count, 'results': data}
        if page:
            output.update({'page': page})
        if page_size:
            output.update({'page_size':page_size})
        if next_page:
            output.update({'next_page':next_page})
        response = make_response(json_encoder(output), resp_code)

        return response


    def complain(self, err_code, err_message, api_errors):
        """
        Custom error response function.
        """
        error = {'error': {'code': err_code, 'message': err_message},
                 'apiErrors': api_errors}
        response = make_response(jsonify(error), err_code)
        return response


    def make_response(self, data, status):
        """
        Custon make_response that invokes the flask.make_response() function.
        """
        return make_response(data, status)


    def is_valid_version(self, version):
        """
        This function checks whether the input version is valid.
        """
        if version not in self.controller.supported_versions:
            return False
        return True


    def is_missing_param_key_val(self, request):
        """
        This function check that every parameter has a value associated to it.
        """
        passed_items = request.args.items()
        for (k, v) in passed_items:
            if not v:
                return True

        return False


    def is_valid_pagination(self, request, page_type="numeric"):
        """
        This function checks if the entered page (number or hash) is valid.
        """
        valid_collections = self.controller.get_collection_names()

        page_valid = False
        page_size_valid = False

        page = request.args.get('page')
        if not page:
            page_valid = True

        # Validate correct page format
        if page and page_type == "hash":
            offsets = page.split(':')
            iterator = iter(offsets)
            if len(offsets) == (len(valid_collections)*2):
                page_valid = True

            if page_valid:
                for x in iterator:
                    if x not in valid_collections or not next(iterator).isdigit():
                        page_valid = False

            #Hack for website frontend
            if page == "1":
                page_valid = True

        # Exception for page = digit
        if page and page_type == "numeric":
            if page.isdigit():
                page_valid = True

        page_size = request.args.get('page_size')
        if not page_size:
            page_size_valid = True

        if page_size and page_size.isdigit():
            page_size_valid = True

        return page_valid and page_size_valid


    def set_page_start_index(self, page):
        """
        This function sets the page index for all collections being queried.

        Assumes a page_number of the following format:
        frus:n_1:ddrs:n_2:statedeptcables:n_3:kissinger:n_4

        or page = 1 (only first page call allowed)
        """
        collection_last_index = {}
        for collection in self.controller.get_collection_names():
            collection_last_index[collection] = 0

        if page and page != "1":
            offsets = page.split(':')
            iterator = iter(offsets)
            for collection in iterator:
                collection_last_index[collection] = int(next(iterator))

        return collection_last_index


    def valid_params(self, passed_params, accepted_params, request):
        """
        This function verifies that a user has not inserted unacceptable or
        unknown parameters. It also verifies that every parameter has been
        assigned a value.
        """
        # Remove this in the future, this is to hide a bug on the site
        if accepted_params:
            accepted_params.update({'total_pages':None})

        # check if user has inserted any parameter not in accepted_params
        bad_params = set(passed_params) - set(accepted_params)
        if bad_params or len(passed_params) == 0:
            return False

        if "start_date" in passed_params and "end_date" not in passed_params:
            return False
        if "end_date" in passed_params and "start_date" not in passed_params:
            return False
        if "date" in passed_params and "start_date" in passed_params:
            return False

        # Check that every parameter has a value
        passed_items = request.args.items()
        for (k, v) in passed_items:
            if not v:
                return False

        return True


    def valid_entities(self, passed_params, request):
        """
        This function verifies if the person_ids, topic_ids, and geo_ids
        and their logical operands have been properly set by the user.
        """
        # Validate if entity structures are correct

        person_ids = None if (not request.args.get('person_ids')) else request.args.get('person_ids').lower()
        geo_ids = None if (not request.args.get('geo_ids')) else request.args.get('geo_ids').lower()
        topic_ids = None if (not request.args.get('topic_ids')) else request.args.get('topic_ids').lower()
        classification_ids = None if (not request.args.get('classification_ids')) else request.args.get('classification_ids').lower()


        if 'person_ids' in passed_params:
            if not person_ids:
                return False
            if "or" in person_ids and "and" in person_ids:
                return False

        if 'geo_ids' in passed_params:
            if not geo_ids:
                return False
            if "or" in geo_ids and "and" in geo_ids:
                return False

        if 'topic_ids' in passed_params:
            if not topic_ids:
                return False
            if "or" in topic_ids and "and" in topic_ids:
                return False

        if 'classification_ids' in passed_params:
            if not classification_ids:
                return False
            if "or" in classification_ids and "and" in classification_ids:
                return False

        # Assign Entities values
        person_ids = request.args.get('person_ids', None)
        person_logic = "OR"

        if person_ids:
            split_and = request.args.get('person_ids').lower().split('and')
            split_or = request.args.get('person_ids').lower().split('or')

            if len(split_and) > 1 and len(split_or) > 1:
                #self.complain(404, "Invalid API parameters",[{'KeyError':'cannot combine AND and OR in a call for an entity'}])
                return False

            person_ids = split_or
            person_logic = "OR"

            if len(split_and) > 1:
                person_ids = split_and
                person_logic = "AND"

            # check that input is all integers
            for p_id in person_ids:
                if not p_id.isdigit():
                    #self.complain(404, "Invalid API parameters",[{'KeyError':'person_ids need to be digits'}])
                    return False

        geo_ids = request.args.get('geo_ids', None)
        geo_logic = "OR"

        if geo_ids:
            split_and = request.args.get('geo_ids').lower().split('and')
            split_or = request.args.get('geo_ids').lower().split('or')

            if len(split_and) > 1 and len(split_or) > 1:
                #self.complain(404, "Invalid API parameters",[{'KeyError':'cannot combine AND and OR in a call for an entity'}])
                return False

            geo_ids = split_or
            geo_logic = "OR"

            if len(split_and) > 1:
                geo_ids = split_and
                geo_logic = "AND"

            # check that input is all integers
            for g_id in geo_ids:
                if not g_id.isdigit():
                    #self.complain(404, "Invalid API parameters",[{'KeyError':'geo_ids need to be digits'}])
                    return False


        topic_ids = request.args.get('topic_ids', None)
        topic_logic = "OR"

        if topic_ids:
            split_and = request.args.get('topic_ids').lower().split('and')
            split_or = request.args.get('topic_ids').lower().split('or')

            if len(split_and) > 1 and len(split_or) > 1:
                #self.complain(404, "Invalid API parameters",[{'KeyError':'cannot combine AND and OR in a call for an entity'}])
                return False

            topic_ids = split_or
            topic_logic = "OR"

            if len(split_and) > 1:
                topic_ids = split_and
                topic_logic = "AND"

            # check that input is all integers
            for t_id in topic_ids:
                if not t_id.isdigit():
                    #self.complain(404, "Invalid API parameters",[{'KeyError':'classification_ids need to be digits'}])
                    return False


        classification_ids = request.args.get('classification_ids', None)
        classification_logic = "OR"

        if classification_ids:
            split_and = request.args.get('classification_ids').lower().split('and')
            split_or = request.args.get('classification_ids').lower().split('or')

            if len(split_and) > 1 and len(split_or) > 1:
                #self.complain(404, "Invalid API parameters",[{'KeyError':'cannot combine AND and OR in a call for an entity'}])
                return False

            classification_ids = split_or
            classification_logic = "OR"

            if len(split_and) > 1:
                classification_ids = split_and
                classification_logic = "AND"

            # check that input is all integers
            for t_id in classification_ids:
                if not t_id.isdigit():
                    #self.complain(404, "Invalid API parameters",[{'KeyError':'topic_ids need to be digits'}])
                    return False

        return {"person_ids":person_ids, "person_logic":person_logic, "geo_ids":geo_ids, "geo_logic":geo_logic, "topic_ids":topic_ids, "topic_logic":topic_logic, "classification_ids":classification_ids, "classification_logic":classification_logic}


    def valid_fields(self, passed_fields, accepted_fields):
        """
        This function check if a user has inserted unacceptable fields
        """
        bad_fields = set(passed_fields) - set(accepted_fields)
        if bad_fields:
            return False
        return True


    def valid_filters(self, filters):
        """
        This function verifies that the user specified url filters are valid.
        """
        start_date = filters['start_date']
        end_date = filters['end_date']
        exact_date = filters['exact_date']
        page = filters['page']
        collections = filters['collections']

        valid_collections = self.controller.get_collection_names()

        try:
            # Validate correct date format
            if exact_date:
                datetime.strptime(exact_date, '%Y-%m-%d')
            if start_date:
                datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                datetime.strptime(end_date, '%Y-%m-%d')

            # Validate correct collections
            if collections:
                if not set(collections).issubset(set(valid_collections)):
                    return False

        except:
            return False

        return True


    def build_link(self, url, old_link, next_link, has_next):
        """
        This function builds the next_link string variable returned with
        every API query.
        """
        if not has_next:
            return

        url = unquote(url).decode('utf-8')  # Converts the url into utf-8 (for escaped % parameters)
        url = re.sub(r'&page='+old_link, r'', url)
        return url + '&page=%s' % next_link


    def escapeString(self, text):
        return re.escape(text)


    def file_handler_setup(self):
        file_h = FileHandler(self.LOG_FILE)
        file_h.setLevel(logging.WARNING)
        file_h.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(funcName)s:%(lineno)d]'))
        return file_h


    class CustomJSONEncoder(JSONEncoder):
        """
        JSON ENCODER (custom to handle both date and datetime data)
        """
        def default(self, obj):
            try:
                if isinstance(obj, date):
                    return obj.isoformat()
                iterable = iter(obj)
            except TypeError:
                pass
            else:
                return list(iterable)
            return JSONEncoder.default(self, obj)
