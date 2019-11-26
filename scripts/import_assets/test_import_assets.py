from unittest import TestCase

import import_assets


class TestMyUnits(TestCase):
    def test_str_to_bool_should_return_True_on_True_str(self):
        result = import_assets.str_to_bool('True')

        self.assertEqual(result, True)

    def test_str_to_bool_should_return_True_on_true_str(self):
        result = import_assets.str_to_bool('true')

        self.assertEqual(result, True)

    def test_str_to_bool_should_return_False_on_false_str(self):
        result = import_assets.str_to_bool('false')

        self.assertEqual(result, False)

    def test_str_to_bool_should_return_False_on_False_str(self):
        result = import_assets.str_to_bool('False')

        self.assertEqual(result, False)

    def test_str_to_bool_should_raise_value_error_on_incorrect_input(self):
        with self.assertRaises(ValueError):
            import_assets.str_to_bool('test_error')

    def test_str_to_bool_should_raise_value_error_on_empty_str(self):
        with self.assertRaises(ValueError):
            import_assets.str_to_bool('')

    def test_get_asset_type_should_return_network_for_ip_range(self):
        result = import_assets.get_asset_type('192.143.53/5')

        self.assertEqual(result, 'network')

    def test_get_asset_type_should_return_host_for_ip(self):
        result = import_assets.get_asset_type('139.175.53.3')

        self.assertEqual(result, 'host')

    def test_get_asset_type_should_raise_value_error_on_incorrect_input(self):
        with self.assertRaises(ValueError):
            import_assets.get_asset_type('somestring')

    def test_get_asset_type_raise_value_error_on_empty_str(self):
        with self.assertRaises(ValueError):
            import_assets.get_asset_type('')

    def test_prep_dicts_field_returns_dict_with_ip_range(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', 'False', '192.170.5.1/24'
        ]
        dict_fields, _ = import_assets.prep_dict_fields(row)
        dict_test = {
            "name": row[0],
            "type": "network",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip_range": '192.170.5.1/24'
        }

        self.assertDictEqual(dict_test, dict_fields)

    def test_prep_dicts_field_returns_dict_with_ip(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', 'False', '192.170.5.1'
        ]
        dict_fields, _ = import_assets.prep_dict_fields(row)
        dict_test = {
            "name": row[0],
            "type": "host",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip": '192.170.5.1'
        }

        self.assertDictEqual(dict_test, dict_fields)

    def test_prep_dicts_returns_dict_from_empty_hosts_personal_data(self):
        row = [
            'test_three', '', 'description of asset test three',
            '186e0a25-e28b-4ecf-b9ad-223c8ee2a62d', '', '192.170.5.1'
        ]
        dict_fields, _ = import_assets.prep_dict_fields(row)
        dict_test = {
            "name": row[0],
            "type": "host",
            "tags": [row[3]],
            "details": row[2],
            "business_impact": "neutral",
            "hosts_personal_data": False,
            "ip": '192.170.5.1'
        }

        self.assertDictEqual(dict_test, dict_fields)
