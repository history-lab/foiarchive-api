from flask import Flask
from api import app, args

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=args.port, debug=args.debug, use_reloader=True)
