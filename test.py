from api import app, args
from api import helpers
from flask_testing import TestCase

class SimpleTest(TestCase):
    app.config['TESTING'] = True
    # app.run(host='0.0.0.0', port=args.port, debug=args.debug, use_reloader=True)
    # helpers.shutdown_server()
