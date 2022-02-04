import json
import unittest

import odeo.client
from odeo.models.sub_user import SubUser
from tests.service_test_case import ServiceTestCase


class SubUserServiceTestCase(ServiceTestCase):

    def test_list_sub_users(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'sHzLllqZvSFwpZTxd70qu1eGfTWHawv3a1nT1IXP3zs='
            },
            text=json.dumps({
                'sub_users': [{
                    'user_id': 123,
                    'name': 'Agus Hartono',
                    'phone_number': '081234567890',
                    'email': 'agus@example.com'
                }],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            ([SubUser(123, 'Agus Hartono', '081234567890', 'agus@example.com')], 'abcdef'),
            self.client.sub_user.list_sub_users()
        )

    def test_list_sub_users_empty(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'sHzLllqZvSFwpZTxd70qu1eGfTWHawv3a1nT1IXP3zs='
            },
            text=json.dumps({
                'sub_users': [],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(([], 'abcdef'), self.client.sub_user.list_sub_users())

    def test_list_sub_users_with_page_token(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users?page_token=abcdef',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'amWP0owDfbvyPoQGyG9jpBCZXYugX3D+zhkH/t4lA3k='
            },
            text=json.dumps({
                'sub_users': [{
                    'user_id': 123,
                    'name': 'Agus Hartono',
                    'phone_number': '081234567890',
                    'email': 'agus@example.com'
                }],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            ([SubUser(123, 'Agus Hartono', '081234567890', 'agus@example.com')], 'abcdef'),
            self.client.sub_user.list_sub_users('abcdef')
        )


if __name__ == '__main__':
    unittest.main()
