from datetime import datetime, timedelta
import requests
from pprint import pprint
import dateutil.parser
import pytz
from requests.exceptions import MissingSchema
import argparse

"""
This file gives some examples/use cases of how to use the JSON REST API provided by HOLM SECURITY.

API URL: https://se-api.holmsecurity.com/v1
API documentation: https://se-api.holmsecurity.com/docs/
"""


def get_api_data(url, api_key, offset):
    headers = {"Authorization": f"Token {api_key}"}
    api_url = f"{url}?offset={offset}"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response


def filter_api_data_on_time_period(data, time_period):
    content = data
    content_filter_time_period = [x for x in content['results']
                                  if dateutil.parser.parse(x['started_date']) >=
                                  pytz.UTC.localize(datetime.now()) - timedelta(hours=time_period)]
    return content_filter_time_period


def get_data_as_list(data_list, results):
    for data in data_list:
        results.append(data)


"""
get_net_scans - returns all network scans found using parameters for call from HOLM REST API

Parameters: 
    time_period (int): Timeperiod to grab scan results from: Specified in hours e.g 24 or 48 or 768 (default: 24)
    result_limit (int): Limit of max nr of scan results to grab. (default: 10)
    api_key: API key of the SC account
    api_endpoint: API endpoint DC: e.g se-api or my-api (default: se-api)
    
Returns: 
    JSON data in a list
"""


def get_net_scans(time_period, results_limit, api_key, api_endpoint):
    api_url = f"{api_endpoint}/net-scans"
    offset = 0
    num_of_items = 0
    response = get_api_data(api_url, api_key, offset)
    results = []
    if response.status_code == 200:
        content = response.json()
        while content['next']:
            filtered_data = filter_api_data_on_time_period(content, time_period)
            if len(filtered_data) > 0:
                get_data_as_list(filtered_data, results)
            if len(results) > 0:
                num_of_items = len(results)
            if num_of_items >= results_limit:
                if num_of_items > results_limit:
                    results = results[:results_limit]
                return pprint(results)
            try:
                offset += 10
                response = get_api_data(api_url, api_key, offset)
                content = response.json()
            except MissingSchema:
                break
        filtered_data = filter_api_data_on_time_period(content, time_period)
        get_data_as_list(filtered_data, results)
        if len(filtered_data) > 0:
            num_of_items = len(results)
            if num_of_items >= results_limit:
                results = results[:results_limit]
                return pprint(results)
        return pprint(results)
    else:
        return pprint(response.content)


"""
get_web_scans - returns all web scans found using parameters for call from HOLM REST API

Parameters: 
    time_period (int): Timeperiod to grab scan results from: Specified in hours e.g 24 or 48 or 768 (default: 24)
    result_limit (int): Limit of max nr of scan results to grab. (default: 10)
    api_key: API key of the SC account
    api_endpoint: API endpoint DC: e.g se-api or my-api (default: se-api)

Returns: 
    JSON data in a list
"""


def get_web_scans(time_period, results_limit, api_key, api_endpoint):
    api_url = f"{api_endpoint}/web-scans"
    offset = 0
    num_of_items = 0
    response = get_api_data(api_url, api_key, offset)
    results = []
    if response.status_code == 200:
        content = response.json()
        while content['next']:
            filtered_data = filter_api_data_on_time_period(content, time_period)
            if len(filtered_data) > 0:
                get_data_as_list(filtered_data, results)
            if len(results) > 0:
                num_of_items = len(results)
            if num_of_items >= results_limit:
                if num_of_items > results_limit:
                    results = results[:results_limit]
                return pprint(results)
            try:
                offset += 10
                response = get_api_data(api_url, api_key, offset)
                content = response.json()
            except MissingSchema:
                break
        filtered_data = filter_api_data_on_time_period(content, time_period)
        get_data_as_list(filtered_data, results)
        if len(filtered_data) > 0:
            num_of_items = len(results)
            if num_of_items >= results_limit:
                results = results[:results_limit]
                return pprint(results)
            results.append(filtered_data)
        return pprint(results)
    else:
        return pprint(response.content)


"""
Below is some example code how to run this code using CLI and arguments. Please note the calls to the functions:

get_net_scans = get_net_scans(
        time_period=args.time,
        results_limit=args.limit,
        api_key='KEY',
        api_endpoint='URL'
    )
"""

parser = argparse.ArgumentParser()
parser.add_argument("key", help="API key to be used")
parser.add_argument("--api", "-a", help="API URL to use, default https://se-api.holmsecurity.com/v1",
                    default="https://api-dev.holmsecurity.com/v1")
parser.add_argument("--time", "-t", help="Timeperiod to grab scan results from: Specified in hours e.g 24, 48 or 768 "
                                         "(default: 24)", type=int, default=24)
parser.add_argument("--limit", "-l", help="result limit, eg. maximum number of scans to return. (default: 10)",
                    type=int, default=10)
parser.add_argument("--type", "-tp", help="scan type to run, eg. net_scan or web_scan, default net_scan",
                    default="net_scan")
args = parser.parse_args()

if args.type == 'net_scan':
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("---------------------GET NET SCANS----------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")

    get_net_scans = get_net_scans(
        time_period=args.time,
        results_limit=args.limit,
        api_key=args.key,
        api_endpoint=args.api,
    )
elif args.type == 'web_scan':
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("---------------------GET WEB SCANS----------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")

    get_web_scans = get_web_scans(
        time_period=args.time,
        results_limit=args.limit,
        api_key=args.key,
        api_endpoint=args.api,
    )
