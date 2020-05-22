import argparse
import csv
import os
import json
from datetime import datetime
from cae import call_endpoint


def run_test_suite(test_suite, server):
    print("Running test suite {0} against {1}".format(test_suite, server))
    test_suite_dir = os.getenv('FOIAPI_TSDIR', './data/suite/')
    test_out_dir = os.getenv('FOIAPI_TODIR', './data/out/')
    test_suite_file = test_suite_dir + test_suite + '.csv'
    with open(test_suite_file, 'r') as tsfile:
        test_reader = csv.reader(tsfile)
        test_num = 0
        tests_passed = 0
        for test in test_reader:
            test_num += 1
            url = server + test[1]
            starttime = datetime.now()
            r = call_endpoint(url)
            endtime = datetime.now()
            if 'error' in r:
                result = 'fail'
            else:
                result = 'pass'
                tests_passed += 1
            print('{0:2d}. {1:>12s}: {2}'.format(test_num, test[0], result))
            print(url)
            print('runtime: {0}'.format(endtime-starttime))
            test_out_file = test_out_dir + test[0] + '.json'
            with open(test_out_file, 'w') as tofile:
                tofile.write(json.dumps(r, indent=4))
    print('Test suite {0} complete.'.format(test_suite))
    print('{0} tests run: {1} passed/{2} failed.'.format(test_num,
          tests_passed, test_num-tests_passed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='runs an API test suite')
    parser.add_argument('test_suite', type=str, help='API test suite')
    parser.add_argument('server', type=str, help='API server url')
    args = parser.parse_args()
    run_test_suite(args.test_suite, args.server)
