from datetime import datetime, timedelta
import requests
from pprint import pprint
import dateutil.parser
import pytz
from requests.exceptions import MissingSchema
import argparse
from utils import get_data_from_api, filter_scans_on_time_period, get_data_as_list, get_scan_results

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
"""

"""
get_scans - returns all scans found using parameters for call to HOLM REST API

Parameters: 
    scan_type (str): Scan type: "web_scan" or "net_scan" (Default: net_scan)
    time_period (int): Timeperiod to grab scan results from: Specified in hours e.g 24 or 48 or 768 (default: 24)
    result_limit (int): Limit of max nr of scan results to grab. (default: 10)
    api_key: API key of the SC account
    api_endpoint: API endpoint DC: e.g se-api or my-api (default: se-api)
    severity: Severity level for filtering scan result vulnerabilities
    
Returns:
    JSON data in a list
"""


def get_scans(scan_type, time_period, results_limit, api_key, api_endpoint, severity):
    if scan_type == "web_scan":
        api_url = f"{api_endpoint}/web-scans"
    else:
        api_url = f"{api_endpoint}/net-scans"
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
                scans = get_data_as_list(filtered_data)
                scan_results = get_scan_results(scans, api_url, api_key, severity)
            if len(scans) > 0:
                num_of_items = len(scans)
            if num_of_items >= results_limit:
                if num_of_items > results_limit:
                    scans = scans[-results_limit:]
                return pprint(scans), pprint(scan_results)
            try:
                offset += 10
                response = get_data_from_api(api_url, api_key, offset)
                content = response.json()
            except MissingSchema:
                break
        filtered_data = filter_scans_on_time_period(content, time_period)
        scans = get_data_as_list(filtered_data)
        scan_results = get_scan_results(scans, api_url, api_key, severity)

        if len(filtered_data) > 0:
            num_of_items = len(scans)
            if num_of_items >= results_limit:
                scans = scans[-results_limit:]
        return pprint(scans), pprint(scan_results)
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
    
For example, the script can be run with:

$ python3 api-examples.py abcd123456 -t 256 -l 2

This will send a request to the default API URL using provided "key" abcd123456, get the network scans for the last 256 
hours and limit the result to be the two latest scans. Output to expect should look something like this:

[{'finished_date': '2019-09-16T08:28:55Z',
  'name': 'Olof testing #2',
  'progress_percent': 0,
  'started_date': '2019-09-16T08:18:57Z',
  'status': 'completed',
  'target_assets': [{'name': 'DVWA',
                     'type': 'host',
                     'uuid': '90d4d197-6717-4a3a-ba36-a579cbcf1e8e'}],
  'uuid': 'fa0cbdbc-ab20-402b-a4ad-5e6b6c97955e',
  'vulnerabilities_count': 91},
 {'finished_date': '2019-09-16T14:24:24Z',
  'name': 'William test schedule',
  'progress_percent': 0,
  'started_date': '2019-09-16T13:55:09Z',
  'status': 'completed',
  'target_assets': [{'name': 'nosql',
                     'type': 'host',
                     'uuid': '2750ee89-2e35-49e9-af7e-e02f628f03d3'}],
  'uuid': '8f56d1bc-0c6f-4902-92f2-ca82e49b9024',
  'vulnerabilities_count': 41}]
  
  Following this data will be the results of each scan, this data can be quite extensive and will therefore
  not be exemplified.
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
parser.add_argument("--severity", "-s", help="severity level for filtering scan result vulnerabilities. For multiple "
                                             "severities please provide a list as such: 'high, medium' !Note the space!"
                                             "(default: 'high')",
                    default="high")
args = parser.parse_args()

if args.type == 'web_scan':
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("---------------------GET WEB SCANS----------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")

else:
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("---------------------GET NET SCANS----------------------------------")
    pprint("--------------------------------------------------------------------")
    pprint("--------------------------------------------------------------------")

get_scans = get_scans(
    scan_type=args.type,
    time_period=args.time,
    results_limit=args.limit,
    api_key=args.key,
    api_endpoint=args.api,
    severity=args.severity.split()
)
