import argparse
import csv
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError

DEFAULT_API_URL = 'https://se-api.holmsecurity.com/v2/'


def get_args():
    parser = argparse.ArgumentParser(description='API key of the sc account')

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


def get_asset_request(args, offset=0):
    """
    gets data from the endpoint and rewrites it to desired format.
    """
    list_one = []
    resp_dict = make_request(args, offset)
    list_one.append(resp_dict)

    while resp_dict['next']:
        offset += 10
        resp_dict = make_request(args, offset)
        list_one.append(resp_dict)
        if not resp_dict['next']:
            break
    return list_one


def make_request(args, offset):
    url = urljoin(args.url, f'net-scans/assets?offset={offset}')
    headers = {"Authorization": f"TOKEN {args.key_token}"}
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        raise HTTPError(http_err, response.text)
    resp_dict = response.json()
    return resp_dict


def get_data(list_new):
    asset_list = []
    for resp_dict in list_new:
        assets = resp_dict['results']
        for dicts in assets:
            dict_fields = {
                'uuid': dicts['uuid'],
                'name': dicts['name'],
                'type': dicts['type'],
                'tags': [],
                'ip': dicts['ip'],
                'ip_range': dicts['ip_range']
            }
            for elements in dicts['tags']:
                dict_fields['tags'].append(elements['uuid'])
            joined_tags = "|".join(dict_fields['tags'])
            dict_fields['tags'] = joined_tags
            asset_list.append(dict_fields)
    return asset_list


def save_csv(assets_list):
    """
    input: a list including filterd dictionaries and save the data in the file.csv
    """

    with open('assets.csv', "w") as csv_file:
        for assets in assets_list:
            ip_value = assets.pop('ip', None)
            ip_range_value = assets.pop('ip_range', None)
            if ip_value:
                assets['ips'] = ip_value
            elif ip_range_value:
                assets['ips'] = ip_range_value
            else:
                raise ValueError('Expected ip or ip_range to be present.')
            fieldnames = ['name', 'uuid', 'type', 'tags', 'ips']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(assets)
    return


if __name__ == '__main__':
    args = get_args()
    full_asset_info = get_asset_request(args, offset=0)
    filterd_assets_list = get_data(full_asset_info)
    save_csv(filterd_assets_list)
