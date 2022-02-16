import unittest

import odeo.client
from tests.service_test_case import ServiceTestCase


class BaseServiceTestCase(ServiceTestCase):

    def test_get_request(self):
        path = '/test/path'
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'MngMIubMnbT6hNRYzb1ETOMmMIIjNRM5x52iJ+KglGU='
            },
        )

        self.client.request_access_token()
        self.assertIsNotNone(self.client.request('GET', path))

    def test_get_request_with_query_string(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/test/path?first=123&second=one+two+three',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'PFhHZo+7M7aB7tU4cJnXOV9wGWEC0dd50ggk0UpxJBk='
            },
        )

        self.client.request_access_token()
        self.assertIsNotNone(
            self.client.request('GET', '/test/path', {'first': 123, 'second': 'one two three'})
        )

    def test_post_request(self):
        path = '/test/path'
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'ycJgzu+gmPf0nmP651Ul+TaxLYuQKdUu/HTc77z4ZzY='
            },
        )

        self.client.request_access_token()
        self.assertIsNotNone(self.client.request('POST', path))

    def test_post_request_with_parameters(self):
        path = '/test/path'
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Gpb9VNdWlVxvkjC/YZCtJCVyyU1MqhsFUMuGchjZ7SQ='
            },
        )

        self.client.request_access_token()
        self.assertIsNotNone(
            self.client.request('POST', path, {'first': 123, 'second': 'one two three'})
        )

    def test_put_request_with_parameters(self):
        path = '/test/path'
        self.adapter.register_uri(
            'PUT',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'z4o4jFYxYx8dlJnlCD1hPhqmL4MYwI6XQevOM1HcHb0='
            },
        )

        self.client.request_access_token()
        self.assertIsNotNone(
            self.client.request('PUT', path, {'first': 123, 'second': 'one two three'})
        )


if __name__ == '__main__':
    unittest.main()
