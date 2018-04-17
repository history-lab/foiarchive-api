from flask import Flask
from api import helpers
from api.controller import Controller

app = Flask(__name__)

args = helpers.parse_args()
conn_type = args.conn_type
controller = Controller(conn_type)
clerk = controller.clerk

from api import views
