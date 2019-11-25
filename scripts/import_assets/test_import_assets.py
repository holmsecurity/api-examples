from unittest import TestCase

import import_assets


class TestMyUnits(TestCase):
    def test_str_to_bool_one(self):
        result = import_assets.str_to_bool('True')

        self.assertEqual(result, True)

    def test_str_to_bool_two(self):
        result = import_assets.str_to_bool('true')

        self.assertEqual(result, True)

    def test_str_to_bool_three(self):
        result = import_assets.str_to_bool('false')

        self.assertEqual(result, False)

    def test_str_to_bool_four(self):
        result = import_assets.str_to_bool('False')

        self.assertEqual(result, False)

    def test_str_to_bool_five(self):
        with self.assertRaises(ValueError):
            import_assets.str_to_bool('test_error')

    def test_str_to_bool_six(self):
        with self.assertRaises(ValueError):
            import_assets.str_to_bool('')

    def test_get_asset_type_one(self):
        result = import_assets.get_asset_type('192.143.53/5')

        self.assertEqual(result, 'network')

    def test_get_asset_type_two(self):
        result = import_assets.get_asset_type('139.175.53.3')

        self.assertEqual(result, 'host')

    def test_get_asset_type_three(self):
        with self.assertRaises(ValueError):
            import_assets.get_asset_type('somestring')

    def test_get_asset_type_four(self):
        with self.assertRaises(ValueError):
            import_assets.get_asset_type('')

    def test_prep_dicts_field_one(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', 'False', '192.170.5.1/24'
        ]
        results = import_assets.prep_dict_fields(row)[0]
        dict_test = {
            "name": row[0],
            "type": "network",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip_range": '192.170.5.1/24'
        }

        self.assertDictEqual(dict_test, results)

    def test_prep_dicts_field_two(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', 'False', '192.170.5.1'
        ]
        results = import_assets.prep_dict_fields(row)[0]
        dict_test = {
            "name": row[0],
            "type": "host",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip": '192.170.5.1'
        }

        self.assertDictEqual(dict_test, results)

    def test_prep_dicts_field_three(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', '', '192.170.5.1'
        ]
        results = import_assets.prep_dict_fields(row)[0]
        dict_test = {
            "name": row[0],
            "type": "host",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip": '192.170.5.1'
        }

        self.assertDictEqual(dict_test, results)
