import argparse
import csv
import requests
from urllib.parse import urljoin

DEFAULT_API_URL = 'https://se-api.holmsecurity.com/v1/'


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


def get_asset_request(args):
    """
    gets data from the endpoint and rewrites it to desired format.
    """

    url = urljoin(args.url, 'net-scans/assets')
    headers = {"Authorization": f"TOKEN {args.key_token}"}
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    list_values = [v for v in response.json().values()]
    assets_content = list_values[3]
    list = []
    list_new = []
    for dicts in assets_content:
        dict_new = {
            key: dicts[key]
            for key in dicts.keys()
            & {'uuid', 'name', 'type', 'tags', 'ip', 'ip_range'}
        }
        list.append(dict_new)
    for row in list:
        dict_fields = {
            'uuid': row['uuid'],
            'name': row['name'],
            'type': row['type'],
            'tags': [],
            'ip': row['ip'],
            'ip_range': row['ip_range']
        }
        for elements in row['tags']:
            dict_fields['tags'].append(elements['uuid'])
        dict_joined = "|".join(dict_fields['tags'])
        dict_fields['tags'] = dict_joined
        list_new.append(dict_fields)
    return list_new


def save_csv(list):
    """
    input: a list including filterd dictionaries and save the data in the file.csv
    """

    with open('assets.csv', "w") as csv_file:
        fieldnames = ['name', 'uuid', 'type', 'tags', 'ip', 'ip_range']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for key_value_tuple in list:
            csv_writer.writerow(key_value_tuple)
    csv_file.close()
    return


if __name__ == '__main__':
    args = get_args()
    list_new = get_asset_request(args)
    output = save_csv(list_new)
