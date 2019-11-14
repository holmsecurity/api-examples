import argparse
import csv
from urllib.parse import urljoin
import requests

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


def get_asset_request(args, offset=0):
    """
    gets data from the endpoint and rewrites it to desired format.
    """
    list_one = []
    url = urljoin(args.url, f'net-scans/assets?offset={offset}')
    headers = {"Authorization": f"TOKEN {args.key_token}"}
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    resp_dict = response.json()
    list_one.append(resp_dict)

    while resp_dict['next']:
        offset += 10
        url = urljoin(args.url, f'net-scans/assets?offset={offset}')
        headers = {"Authorization": f"TOKEN {args.key_token}"}
        response = requests.get(url=url, headers=headers)
        resp_dict = response.json()
        list_one.append(resp_dict)
        if resp_dict['next'] == None:
            break
    return list_one


def get_data(list_new):
    list_dicts = []
    new_list = []

    for resp_dict in list_new:
        assets = resp_dict['results']
        for dicts in assets:
            dict_new = {
                key: dicts[key]
                for key in dicts.keys()
                & {'uuid', 'name', 'type', 'tags', 'ip', 'ip_range'}
            }
            list_dicts.append(dict_new)

    for row in list_dicts:
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
        joined_tags = "|".join(dict_fields['tags'])
        dict_fields['tags'] = joined_tags
        new_list.append(dict_fields)
    return new_list


def save_csv(list_new):
    """
    input: a list including filterd dictionaries and save the data in the file.csv
    """

    with open('assets.csv', "w") as csv_file:
        fieldnames = ['name', 'uuid', 'type', 'tags', 'ip', 'ip_range']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for key_value_tuple in list_new:
            csv_writer.writerow(key_value_tuple)
    csv_file.close()
    return


if __name__ == '__main__':
    args = get_args()
    list_new = get_asset_request(args, offset=0)
    list_neww = get_data(list_new)
    save_csv(list_neww)
