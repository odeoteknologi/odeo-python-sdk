import json
import unittest

import requests_mock
from freezegun import freeze_time

import odeo.client


@freeze_time('2021-02-01')
class ServiceTestCase(unittest.TestCase):
    client_id = 'test_client_id'
    client_secret = 'test_client_secret'
    signing_key = 'test_signing_key'
    access_token = 'test_access_token'

    client = odeo.client.Client(client_id, client_secret, signing_key)
    adapter = requests_mock.Adapter()

    def setUp(self) -> None:
        self.client.set_transport_adapter('https://', self.adapter)
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/oauth2/token',
            text=json.dumps({
                'access_token': self.access_token,
                'expires_in': 1800,
                'scope': 'dg_disbursement:write dg_inquiry:write pg_get_payment:read',
                'token_type': 'Bearer'
            })
        )
