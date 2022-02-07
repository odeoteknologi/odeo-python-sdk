import json
import unittest

import odeo.client
from odeo.exceptions.general_error import GeneralError
from odeo.exceptions.input_validation_error import InputValidationError
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

    def test_create_sub_user(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'IyMSYxV1An/jebiOlsVaWAz1XPlVQ663J5spsJlxlro='
            },
            text=json.dumps({
                'user_id': '123',
                'name': 'Agus Hartono',
                'phone_number': '081234567890',
                'email': 'agus@example.com'
            })
        )

        self.assertEqual(
            SubUser('123', 'Agus Hartono', '081234567890', 'agus@example.com'),
            self.client.sub_user.create_sub_user(
                'agus@example.com', 'Agus Hartono', '081234567890'
            )
        )

    def test_create_sub_user_failed_email_invalid(self):
        message = 'The email must be a valid email address'
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'DIQNg7zkrqYnM1bMFk563xv+Z2ljQOF8ptx5oR5LmZA='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10001
            })
        )

        with self.assertRaises(InputValidationError) as ctx:
            self.client.sub_user.create_sub_user(
                'agus-example.com', 'Agus Hartono', '081234567890'
            )

        self.assertEqual(str(ctx.exception), message)

    def test_create_sub_user_failed_phone_number_already_registered(self):
        message = 'Phone number registered'
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'IyMSYxV1An/jebiOlsVaWAz1XPlVQ663J5spsJlxlro='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10000
            })
        )

        with self.assertRaises(GeneralError) as ctx:
            self.client.sub_user.create_sub_user(
                'agus@example.com', 'Agus Hartono', '081234567890'
            )

        self.assertEqual(str(ctx.exception), message)

    def test_update_sub_user(self):
        self.adapter.register_uri(
            'PUT',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'tcw7lg3kRTbH4h/80Tv3cidIa+uCqZecHKRKgXtC+3Y='
            },
            text=json.dumps({
                'user_id': '123',
                'name': 'Agus Hartono',
                'phone_number': '081234567890',
                'email': 'agus@example.com'
            })
        )

        self.assertEqual(
            SubUser('123', 'Agus Hartono', '081234567890', 'agus@example.com'),
            self.client.sub_user.update_sub_user(
                123, 'agus@example.com', 'Agus Hartono', '081234567890'
            )
        )

    def test_update_sub_user_failed_email_invalid(self):
        message = 'The email must be a valid email address'
        self.adapter.register_uri(
            'PUT',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'qcZEJpP9vS1KNRVqCqS5qzyxmEUxn8xi8pBgEprySaU='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10001
            })
        )

        with self.assertRaises(InputValidationError) as ctx:
            self.client.sub_user.update_sub_user(
                123, 'agus-example.com', 'Agus Hartono', '081234567890'
            )

        self.assertEqual(str(ctx.exception), message)

    def test_update_sub_user_failed_user_not_found(self):
        message = 'Data not found'
        self.adapter.register_uri(
            'PUT',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'tcw7lg3kRTbH4h/80Tv3cidIa+uCqZecHKRKgXtC+3Y='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10000
            })
        )

        with self.assertRaises(GeneralError) as ctx:
            self.client.sub_user.update_sub_user(
                123, 'agus@example.com', 'Agus Hartono', '081234567890'
            )

        self.assertEqual(str(ctx.exception), message)

    def test_update_sub_user_failed_phone_number_already_registered(self):
        message = 'Phone number registered'
        self.adapter.register_uri(
            'PUT',
            odeo.client.DEVELOPMENT_BASE_URL + '/sub-users/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'tcw7lg3kRTbH4h/80Tv3cidIa+uCqZecHKRKgXtC+3Y='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10000
            })
        )

        with self.assertRaises(GeneralError) as ctx:
            self.client.sub_user.update_sub_user(
                123, 'agus@example.com', 'Agus Hartono', '081234567890'
            )

        self.assertEqual(str(ctx.exception), message)


if __name__ == '__main__':
    unittest.main()
