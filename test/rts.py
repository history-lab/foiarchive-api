import argparse
import csv
import os
from cae import call_endpoint


def print_fmt_output(num, name, url, r):
    print(f'{num}. {name}')
    print(f'url: {url}')


def run_test_suite(test_suite, server):
    with open(test_suite, 'r') as tsfile:
        test_reader = csv.reader(tsfile)
        test_num = 0
        for test in test_reader:
            test_num += 1
            url = 'http://' + server + '/' + test[1]
            r = call_endpoint(url)
            # print_fmt_output(test_num, test[0], url, r)
            # print(r)
            print(type(r.json()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='runs an API test suite')
    parser.add_argument('test_suite', type=str, help='API test suite')
    parser.add_argument('server', type=str, help='API server url')
    args = parser.parse_args()
    test_suite_file = os.getenv('FOIAPI_TSDIR', './data/suite/') +\
        args.test_suite + '.csv'
    run_test_suite(test_suite_file, args.server)
