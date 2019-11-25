from unittest import TestCase

import get_assets
import update_assets


class TestMyUnits(TestCase):
    def test_get_asset_type_one(self):
        result = update_assets.get_asset_type('192.143.53/5')

        self.assertEqual(result, 'network')

    def test_get_asset_type_two(self):
        result = update_assets.get_asset_type('139.175.53.3')

        self.assertEqual(result, 'host')

    def test_get_asset_type_three(self):
        with self.assertRaises(ValueError):
            update_assets.get_asset_type('somestring')

    def test_get_asset_type_four(self):
        with self.assertRaises(ValueError):
            update_assets.get_asset_type('')

    def test_prep_dicts_field_one(self):
        row = [
            'test_three', 'the_uuid_is_inserted_here', '',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', '192.170.5.1/24'
        ]
        results = update_assets.prep_dict_fields(row)
        dict_test = {
            "name": row[0],
            "type": "network",
            "tags": ['186e0a25-e28b-4ecf-b9ad-223c8ee2a62d'],
            "uuid": row[1],
            "ip_range": '192.170.5.1/24'
        }

        self.assertDictEqual(dict_test, results)

    def test_prep_dicts_field_two(self):
        row = [
            'test_three', 'the_uuid_is_inserted_here', '',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', '192.170.5.1'
        ]
        results = update_assets.prep_dict_fields(row)
        dict_test = {
            "name": row[0],
            "type": "host",
            "tags": ['186e0a25-e28b-4ecf-b9ad-223c8ee2a62d'],
            "uuid": row[1],
            "ip": '192.170.5.1'
        }

        self.assertDictEqual(dict_test, results)

    def test_get_data_one(self):
        list_to_test = [{
            'count':
            1,
            'next':
            None,
            'previous':
            None,
            'results': [{
                'name':
                'test_two',
                'uuid':
                '83f21d03-efec-491e-8244-157b96def56b',
                'type':
                'host',
                'tags': [{
                    'name': 'Services',
                    'uuid': '7e03a282-0061-472f-b106-10b7edc7d634'
                }],
                'created':
                '2019-11-25T13:00:41.605932Z',
                'operating_system':
                None,
                'vulnerabilities_count':
                0,
                'last_detected':
                None,
                'times_detected':
                0,
                'ip':
                '192.169.5.1',
                'ip_range':
                None,
                'hostname':
                '192.169.5.1'
            }]
        }]
        results = get_assets.get_data(list_to_test)
        correct_output_list = [{
            'uuid': '83f21d03-efec-491e-8244-157b96def56b',
            'name': 'test_two',
            'type': 'host',
            'tags': '7e03a282-0061-472f-b106-10b7edc7d634',
            'ip': '192.169.5.1',
            'ip_range': None
        }]

        self.assertListEqual(correct_output_list, results)

    def test_get_data_two(self):
        list_to_test = [{
            'count':
            2,
            'next':
            None,
            'previous':
            None,
            'results': [{
                'name':
                'new_test',
                'uuid':
                '1a09b0d6-ca7d-480a-9e3e-167052b89c22',
                'type':
                'network',
                'tags': [{
                    'name': 'Operating systems',
                    'uuid': '28229346-c605-4944-a0c7-820d7d80a9cc'
                }, {
                    'name': 'Services',
                    'uuid': '7e03a282-0061-472f-b106-10b7edc7d634'
                }],
                'created':
                '2019-11-25T15:01:54.511433Z',
                'operating_system':
                None,
                'vulnerabilities_count':
                0,
                'last_detected':
                None,
                'times_detected':
                0,
                'ip':
                None,
                'ip_range':
                '176.74.192.32/27',
                'hostname':
                None
            }, {
                'name':
                'test_two',
                'uuid':
                '83f21d03-efec-491e-8244-157b96def56b',
                'type':
                'host',
                'tags': [{
                    'name': 'Services',
                    'uuid': '7e03a282-0061-472f-b106-10b7edc7d634'
                }],
                'created':
                '2019-11-25T13:00:41.605932Z',
                'operating_system':
                None,
                'vulnerabilities_count':
                0,
                'last_detected':
                None,
                'times_detected':
                0,
                'ip':
                '192.169.5.1',
                'ip_range':
                None,
                'hostname':
                '192.169.5.1'
            }]
        }]
        results = get_assets.get_data(list_to_test)
        correct_output_list = [{
            'uuid': '1a09b0d6-ca7d-480a-9e3e-167052b89c22',
            'name': 'new_test',
            'type': 'network',
            'tags':
            '28229346-c605-4944-a0c7-820d7d80a9cc|7e03a282-0061-472f-b106-10b7edc7d634',
            'ip': None,
            'ip_range': '176.74.192.32/27'
        }, {
            'uuid': '83f21d03-efec-491e-8244-157b96def56b',
            'name': 'test_two',
            'type': 'host',
            'tags': '7e03a282-0061-472f-b106-10b7edc7d634',
            'ip': '192.169.5.1',
            'ip_range': None
        }]

        self.assertListEqual(correct_output_list, results)
