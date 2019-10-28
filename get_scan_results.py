#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import enum
from pprint import pprint

import pytz
import requests
from requests.exceptions import MissingSchema

import dateutil.parser
from utils import (filter_scans_on_time_period,
                   get_data_from_api, get_scan_results)

"""
This file gives some examples/use cases of how to use the JSON REST API provided by HOLM SECURITY.

API URL: https://se-api.holmsecurity.com/v1
API documentation: https://se-api.holmsecurity.com/docs/

KNOWN LIMITATIONS:
This script, being an example script, has some limits. The "limit" parameter does not only slice the returned list to
limit the number of elements but also stops the execution in order to prevent overflow/timeouts of large datasets.

If a limit is set to 10, it will stop asking for more results from the API after 10 scans have been returned, even
if there are newer scans to be found. This happens because the returned data from the API starts from the _beginning_ 
of recorded scan results.

For example, the script can be run with:

$ python3 get_scan_results.py abcd123456 -t 256 -l 2

This will send a request to the default API URL using provided "key" abcd123456,
get the network scans for the last 256 hours and limit the result to be the two latest scans.


Parameters:
    scan_type (str): Scan type: "web_scan" or "net_scan" (Default: net_scan)
    time_period (int): Timeperiod to grab scan results from: Specified in hours e.g 24 or 48 or 768 (default: 24)
    result_limit (int): Limit of max nr of scan results to grab. (default: 10)
    api_key: API key of the SC account
    api_endpoint: API endpoint DC: e.g se-api or my-api (default: se-api)
    severity: Severity level for filtering scan result vulnerabilities

"""

DEFAULT_API_URL = "https://se-api.holmsecurity.com/v1"


class ScanKind(enum.Enum):
    NET = 'net_scan'
    WEB = 'web_scan'


def get_scans(
    scan_type, time_period, results_limit, api_key, api_endpoint, severity
):
    col_size = 22
    if scan_type == ScanKind.WEB.value:
        api_url = f"{api_endpoint}/web-scans"
        pprint("-" * col_size + "GET WEB SCANS" + "-" * col_size)
    else:
        api_url = f"{api_endpoint}/net-scans"
        pprint("-" * col_size + "GET NET SCANS" + "-" * col_size)

    offset = 0
    num_of_items = 0
    response = get_data_from_api(api_url, api_key, offset)
    scans = []
    scan_results = []
    if response.status_code == 200:
        content = response.json()
        while content['next']:
            filtered_data = filter_scans_on_time_period(content, time_period)
            if len(filtered_data) > 0:
                scans = filtered_data
                scan_results = get_scan_results(
                    scans, api_url, api_key, severity
                )
            if len(scans) > 0:
                num_of_items = len(scans)
            if num_of_items >= results_limit:
                if num_of_items > results_limit:
                    scans = scans[-results_limit:]
                pprint(scans)
                pprint(scan_results)
                return
            try:
                offset += 10
                response = get_data_from_api(api_url, api_key, offset)
                content = response.json()
            except MissingSchema:
                break
        filtered_data = filter_scans_on_time_period(content, time_period)
        scans = filtered_data
        scan_results = get_scan_results(scans, api_url, api_key, severity)

        if len(filtered_data) > 0:
            num_of_items = len(scans)
            if num_of_items >= results_limit:
                scans = scans[-results_limit:]
        pprint(scans)
        pprint(scan_results)
        return
    else:
        pprint(response.content)
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="API key to be used")
    parser.add_argument(
        "--api", "-a", help="API URL to use", default=DEFAULT_API_URL
    )
    parser.add_argument(
        "--time",
        "-t",
        help="Timeperiod to grab scan results from: Specified in hours e.g 24, 48 or 768 "
        "(default: 24)",
        type=int,
        default=24
    )
    parser.add_argument(
        "--limit",
        "-l",
        help="result limit, eg. maximum number of scans to return. (default: 10)",
        type=int,
        default=10
    )
    parser.add_argument(
        "--type",
        "-tp",
        help="scan type to run, eg. net_scan or web_scan, default net_scan",
        default=ScanKind.NET.value,
        choices=[k.value for k in ScanKind]
    )
    parser.add_argument(
        "--severity",
        "-s",
        help="severity level for filtering scan result vulnerabilities. For multiple "
        "severities please provide a list as such: 'high, medium' !Note the space!"
        "(default: 'high')",
        default="high"
    )
    args = parser.parse_args()

    get_scans(
        scan_type=args.type,
        time_period=args.time,
        results_limit=args.limit,
        api_key=args.key,
        api_endpoint=args.api,
        severity=args.severity.split()
    )


if __name__ == '__main__':
    main()
