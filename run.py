from flask import Flask
from api import app, args

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port, debug=args.debug, use_reloader=True)
