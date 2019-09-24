from datetime import datetime, timedelta
import requests
import dateutil.parser
import pytz

"""
Helper functions for api-examples script
"""


def get_data_from_api(url, api_key, offset):
    headers = {"Authorization": f"Token {api_key}"}
    api_url = f"{url}?offset={offset}"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response


def get_scan_results_from_api(api_url, api_key, severity):
    offset = 0
    result = []
    response = get_data_from_api(api_url, api_key, offset)
    if response.status_code == 200:
        content = response.json()
        filtered_data = filter_scan_results_on_severity(content, severity)
        if len(filtered_data) > 0:
            result.append(filtered_data)
        while content['next']:
            try:
                offset += 10
                response = get_data_from_api(api_url, api_key, offset)
                if response.status_code == 200:
                    content = response.json()
                    filtered_data = filter_scan_results_on_severity(content, severity)
                    if len(filtered_data) > 0:
                        result.append(filtered_data)
                else:
                    break
            except KeyError:
                break
        filtered_data = filter_scan_results_on_severity(content, severity)
        if len(filtered_data) > 0:
            result.append(filtered_data)
        if result:
            return result
        else:
            return
    else:
        return response.content


def filter_scans_on_time_period(data, time_period):
    data_filtered_on_time_period = [x for x in data['results']
                                    if dateutil.parser.parse(x['started_date']) >=
                                    pytz.UTC.localize(datetime.now()) - timedelta(hours=time_period)]
    return data_filtered_on_time_period


def filter_scan_results_on_severity(scans, severity):
    scan_results_filtered_on_severity = [x for x in scans['results'] if x['severity'] in severity]
    return scan_results_filtered_on_severity


def get_scan_results(scans, api_url, api_key, severity):
    results = []
    for scan in scans:
        uuid = scan['uuid']
        api_url_scan = f"{api_url}/{uuid}/results"
        scan_results = get_scan_results_from_api(api_url_scan, api_key, severity)
        if scan_results:
            results.append(scan_results)
    return results


def get_data_as_list(data_list):
    results = []
    for data in data_list:
        results.append(data)
    return results

