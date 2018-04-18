import argparse
from flask import request

def parse_args():
    parser = argparse.ArgumentParser(
        description=globals()['__doc__'],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--debug', default=False,
                    help='debugging True/False; default False')
    parser.add_argument('-l', '--logging', default=True,
                    help='logging True/False; default True')
    parser.add_argument('-a', '--alerts', default=False,
                    help='email alerts True/False; default False')
    parser.add_argument('-p', '--port', default=5001,
                    help='Port number for API server; default 5001')

    return parser.parse_args()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
