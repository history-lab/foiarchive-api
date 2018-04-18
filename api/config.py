import os
import yaml

if os.getenv('CI'):
    credentials = {
        'host':     'history-lab.org',
        'user':     os.getenv('DECLASS_API_USER'),
        'password': os.getenv('DECLASS_API_PW')
    }
else:
    if os.path.exists('credentials.yml'):
        credentials  = yaml.load(open('credentials.yml'))
    else:
        credentials = {
            'host':     input("host: "),
            'user':     input("user: "),
            'password': input("password: ")
        }
        with open('credentials.yml', 'w') as f:
            yaml.dump(credentials, f, default_flow_style=False)
