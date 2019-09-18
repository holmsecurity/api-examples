from datetime import datetime, timedelta
import requests
import dateutil.parser
import pytz

"""
Helper functions for api-examples script
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