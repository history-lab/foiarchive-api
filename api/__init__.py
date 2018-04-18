from flask import Flask
from api import helpers
from api.config import credentials
from api.controller import Controller

app = Flask(__name__)
args = helpers.parse_args()

controller = Controller(credentials)
clerk = controller.clerk

from api import views
