import json

import requests_mock

from odeo.client import Client, DEVELOPMENT_BASE_URL


def test_request_access_token():
    access_token = '12345'

    adapter = requests_mock.Adapter()
    adapter.register_uri(
        'POST',
        DEVELOPMENT_BASE_URL + '/oauth2/token',
        text=json.dumps({
            'access_token': access_token,
            'expires_in': 1800,
            'scope': 'dg_disbursement:write dg_inquiry:write pg_get_payment:read',
            'token_type': 'Bearer'
        })
    )

    client = Client('123', '456', '789')
    client.set_transport_adapter('https://', adapter)

    assert client.request_access_token() == access_token
