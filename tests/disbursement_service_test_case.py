import json
import time
import unittest

import odeo.client
from odeo.models.bank import Bank
from tests.service_test_case import ServiceTestCase


class DisbursementServiceTestCase(ServiceTestCase):

    def test_get_banks(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/banks',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'UxTAo4TnY4sMUX3kUMPJSRD7pYwP73UJ6wmJArXFyRs='
            },
            text=json.dumps({
                'banks': [{
                    'bank_id': 1,
                    'name': 'BCA',
                    'bank_code': '014',
                    'swift_code': 'CENAIDJA'
                }]
            })
        )

        self.assertEqual(
            [Bank(bank_id=1, name='BCA', bank_code='014', swift_code='CENAIDJA')],
            self.client.disbursement.get_banks()
        )


if __name__ == '__main__':
    unittest.main()
