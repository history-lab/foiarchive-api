import argparse
import datetime
import time
import rts


def run_api_monitor(query_list, server, pause):
    print("*** History Lab API Monitor ***")
    while True:
        rts.run_test_suite(query_list, server)
        print("{}: Sleeping for {} minutes".format(datetime.datetime.now(),
                                                   pause))
        time.sleep(pause * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='runs an API monitor')
    parser.add_argument('query_list', type=str, help='API query list')
    parser.add_argument('server', type=str, help='API server url')
    parser.add_argument('pause', type=int,
                        help='Minutes between iterations')
    args = parser.parse_args()
    run_api_monitor(args.query_list, args.server, args.pause)
