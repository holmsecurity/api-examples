import argparse
import csv
import json
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError
DEFAULT_API_URL = 'https://se-api.holmsecurity.com/v1/'
"""
This code takes in the modified CSV file and sends a patch request for updating the assets.
"""


def get_args():
    parser = argparse.ArgumentParser(description='API key of the sc account')
    parser.add_argument('-p',
                        '--csv-path',
                        help='Path to the CSV file',
                        required=True)
    parser.add_argument('-k',
                        '--key-token',
                        type=str,
                        help='Token needed to access sc-dev',
                        required=True)
    parser.add_argument(
        '-u',
        '--url',
        help=f"API URL to use, default is set to {DEFAULT_API_URL}",
        default=DEFAULT_API_URL)

    return parser.parse_args()


def read_data(args):
    """
    Reads data from CSV file and posts it as JSON to the API.
    """

    with open(args.csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            ip = row[4]
            asset_type = get_asset_type(ip)
            name = row[0]
            tags = row[3]
            uuid = row[1]
            dict_fields = {
                "name": name,
                "uuid": uuid,
                "type": asset_type,
                "tags": [t for t in tags.split('|') if t]
            }
            if asset_type == 'network':
                dict_fields.update({"ip_range": ip})
            else:
                dict_fields.update({"ip": ip})

            update_asset_request(args, dict_fields)


def get_asset_type(ip_row):
    """"
    Check the type of the asset by the IP/IP range. We support two types of assets:
    - network  (eg. 192.168.0.1/24)
    - host        (eg. 192.168.0.134)
    """

    if "/" in ip_row:
        asset_type = "network"
    else:
        asset_type = "host"
    return asset_type


def update_asset_request(args, dict_fields):
    """
    take the dict and args input and send update request.
    """

    uuid = dict_fields['uuid']
    json_data_new = json.dumps(dict_fields)
    url = urljoin(args.url, f'net-scans/assets/{uuid}')
    headers = {
        "Authorization": f"TOKEN {args.key_token}",
        "Content-Type": "application/json"
    }
    response = requests.patch(url=url, data=json_data_new, headers=headers)
    response.raise_for_status()
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        raise HTTPError(http_err, response.text)
    return


if __name__ == '__main__':
    args = get_args()
    read_data(args)
