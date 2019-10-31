from datetime import datetime, timedelta

import pytz
import requests

import dateutil.parser


"""
Helper functions for api-examples script
"""


def get_data_from_api(url, api_key, offset):
    """
    Make request to the API.

    Parameters:
        url: API url to use
        api_key: API key of the SC account
        offset: offset point to start with for pagination (incremented by 10 per run)

    Returns:
        API response
    """
    headers = {'Authorization': f'Token {api_key}'}
    api_url = f'{url}?offset={offset}'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response


def get_scan_results_from_api(api_url, api_key, severity_list):
    """
    Return scan result data from API.

    Parameters:
        api_url: API url to use
        api_key: API key of the SC account
        severity_list: list of all severities to filter by

    Returns:
        API response
    """
    offset = 0
    result = []
    response = get_data_from_api(api_url, api_key, offset)
    if response.status_code == 200:
        content = response.json()
        filtered_data = filter_scan_results_on_severity(content, severity_list)
        if len(filtered_data) > 0:
            result.append(filtered_data)
        while content['next']:
            try:
                offset += 10
                response = get_data_from_api(api_url, api_key, offset)
                if response.status_code == 200:
                    content = response.json()
                    filtered_data = filter_scan_results_on_severity(content, severity_list)
                    if len(filtered_data) > 0:
                        result.append(filtered_data)
                else:
                    break
            except KeyError:
                break
        filtered_data = filter_scan_results_on_severity(content, severity_list)
        if len(filtered_data) > 0:
            result.append(filtered_data)
        return result

    else:
        return response.content


def filter_scans_on_time_period(data, time_period):
    data_filtered_on_time_period = [x for x in data['results']
                                    if dateutil.parser.parse(x['started_date']) >=
                                    pytz.UTC.localize(datetime.now()) - timedelta(hours=time_period)]
    return data_filtered_on_time_period


def filter_scan_results_on_severity(scans, severity_list):
    return [
        x for x in scans['results'] if x['severity'] in severity_list
    ]


def get_scan_results(scans, api_url, api_key, severity_list):
    """
    Get scan results from each scan.

    Parameters:
        scans: list of scans containing UUID
        api_url: API url to use
        api_key: API key of the SC account
        severity_list: list of all severities to filter by

    Returns:
        API response
    """
    results = []
    for scan in scans:
        uuid = scan['uuid']
        api_url_scan = f'{api_url}/{uuid}/results'
        scan_results = get_scan_results_from_api(api_url_scan, api_key, severity_list)
        if scan_results:
            results.append(scan_results)
    return results
