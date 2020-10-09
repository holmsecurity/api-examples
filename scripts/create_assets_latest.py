import argparse
import csv
import json
import logging
import urlparse

import requests
from requests.exceptions import HTTPError
import time




DEFAULT_API_URL = 'https://api-dev.holmsecurity.com/public/v2/'

"""
This code will get a path to a csv file which have the following columns order:
1st:name
2nd:ip
3rd:list of Tags splited by |
4th:Business_impact
5th:Owner
6th:Personal data holder
7th:Description

The assets will then be posted to SC

Note: If you are using older api version then you are not allowed to use other than latin characters 
"""


def get_tags_uuids(args, offset=0):
    # This function will get all the tags and return a dict with tags
    url = urlparse.urljoin(args.url, 'tags?offset=%s' % offset)
    headers = {"Authorization": "TOKEN %s" % args.key_token}
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        raise HTTPError(http_err, response.text)
    resp_dict = response.json()
    return resp_dict


def get_tags_uuids_full_list(args, offset=0):
    # this function will make sure that tags are returned
    list_one = []
    resp_dict = get_tags_uuids(args, offset)
    list_one.append(resp_dict)

    while resp_dict['next']:
        offset += 10
        resp_dict = get_tags_uuids(args, offset)
        list_one.append(resp_dict)
        if not resp_dict['next']:
            break
    return list_one


def get_uuid_and_tag_dict(args, offset=0):
    # this function will return a dict with uuid as key and the tag name as value
    uuid_tags_dict = {}
    data = get_tags_uuids_full_list(args, offset)
    for items in data:
        for k in items['results']:
            uuid = k['uuid']
            tag_name = k['name']
            uuid_tags_dict.update({uuid: tag_name})
    return uuid_tags_dict


def make_post_request(args, dict_field):
    # This function will take the args and make the post request and return the response
    url = urlparse.urljoin(args.url, 'net-assets')
    json_data_new = json.dumps(dict_field)
    headers = {"Authorization": "TOKEN %s" % args.key_token,
               "Content-Type": "application/json"}
    time.sleep(0.3)
    try:
        response = requests.post(url=url, data=json_data_new, headers=headers)
        response.raise_for_status()
    except HTTPError:
        logging.error('Failed url:{}, response:{}'.format(url, response.text))
    return response.json()


def prep_dict_fields(row, uuid_tags_dict):
    #this function will get the row and the uuid_tags_dict. It returns the tags to be returned
    name = row[0]
    ip = row[1]
    tags = row[2]
    business_impact = row[3]
    personal_data_holder = row[5]
    description = row[6]

    if ip == "":
        raise ValueError("ip must be inserted")

    if name == "":
        name = ip
    if business_impact == "":
        business_impact = "neutral"
    true_type = ["true", "True"]

    if personal_data_holder in true_type:
        personal_data_holder = True
    else:
        personal_data_holder = False
    tags_list = [t for t in tags.split('|') if t]
    list_uuids = []
    for items in tags_list:
        if items in uuid_tags_dict.values():
            index = uuid_tags_dict.values().index(items)
            list_uuids.append(uuid_tags_dict.keys()[index].encode('utf-8'))
    dict_to_post = {'name': name,
                    'tags': list_uuids,
                    'ip': ip,
                    'business_impact': business_impact,
                    'hosts_personal_data': personal_data_holder,
                    'details': description,
                    'type': "host"}
    return dict_to_post


def read_csv_and_return_dict(args, uuid_tags_dict):
    with open(args.csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                dict_to_post = prep_dict_fields(row, uuid_tags_dict)
                make_post_request(args, dict_to_post)
            except:
                pass


def get_args():
    parser = argparse.ArgumentParser(description='API key of the sc account')
    parser.add_argument(
        '-p',
        '--csv-path',
        help='Path to the CSV file',
        required=True
    )
    parser.add_argument(
        '-k',
        '--key-token',
        type=str,
        help='Token needed to access sc public_api',
        required=True
    )
    parser.add_argument(
        '-u',
        '--url',
        help="API URL to use, default is set to %s" % DEFAULT_API_URL,
        default=DEFAULT_API_URL
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    uuid_tags_dict = get_uuid_and_tag_dict(args)
    read_csv_and_return_dict(args, uuid_tags_dict)
