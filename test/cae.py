import requests
import json
import argparse


def call_endpoint(url, error_handler, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        return(r.json())
    except requests.exceptions.RequestException as e:
        error_handler()
        raise SystemExit(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='tests an API endpoint')
    parser.add_argument('endpoint', type=str, help='API endpoint')
    parser.add_argument('server', type=str, help='API server url')
    args = parser.parse_args()
    url = args.server + args.endpoint
    print(json.dumps(call_endpoint(url), indent=2))
