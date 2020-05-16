import requests
import json
import argparse


def call_endpoint(url):
    r = requests.get(url)
    return(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='tests an API endpoint')
    parser.add_argument('server', type=str, help='API server url')
    parser.add_argument('endpoint', type=str, help='API endpoint')
    args = parser.parse_args()
    url = 'http://' + args.server + '/' + args.endpoint
    print(call_endpoint(url))
