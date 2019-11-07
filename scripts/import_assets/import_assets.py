import argparse
import csv
import json
from urllib.parse import urljoin
import requests
from requests.exceptions import HTTPError

DEFAULT_API_URL = 'https://se-api.holmsecurity.com/v1/'
"""
This code importing csv files including information about assets and creates assets in the holm-api endpoint. 
"""


def read_and_create_assets(args):
    """
    Reads data from CSV file and posts it as JSON to the API.
    """

    with open(args.csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            ip = row[5]
            asset_type = get_asset_type(ip)
            name = row[0]
            business_impact = row[1]
            details = row[2]
            hosts_personal_data = row[4]
            tags = [t for t in row[3].split('|') if t]
            dict_fields = {
                "name": name,
                "type": asset_type,
                "business_impact": business_impact,
                "details": details,
                "tags": tags,
                "hosts_personal_data": str_to_bool(hosts_personal_data)
            }
            if asset_type == 'network':
                dict_fields.update({"ip_range": ip})
            else:
                dict_fields.update({"ip": ip})
            try:
                post_asset_request(args, dict_fields)
                print(f"{name} with the ip {ip} was added successfully")
            except HTTPError as err:
                errors = json.loads(err.response.content)["errors"]
                print(f"The asset could not be added because: {errors}")


def str_to_bool(s):
    if s in ['true', 'True']:
        return True
    elif s in ['false', 'False']:
        return False
    else:
        raise ValueError


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


def post_asset_request(args, dict_fields):
    url = urljoin(args.url, 'net-scans/assets')
    json_data = json.dumps(dict_fields)
    headers = {
        "Authorization": f"TOKEN {args.key_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url=url, data=json_data, headers=headers)
    response.raise_for_status()
    return response


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


if __name__ == '__main__':
    args = get_args()
    asset_data = read_and_create_assets(args)
