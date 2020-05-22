import requests
import json
import argparse


def call_endpoint(url):
    r = requests.get(url)
    return(r.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='tests an API endpoint')
    parser.add_argument('endpoint', type=str, help='API endpoint')
    parser.add_argument('server', type=str, help='API server url')
    args = parser.parse_args()
    url = args.server + args.endpoint
    print(json.dumps(call_endpoint(url), indent=2))
