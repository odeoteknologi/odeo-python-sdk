import json
import unittest

import odeo.client
from odeo.models.payment import Payment, Status
from tests.service_test_case import ServiceTestCase


class PaymentGatewayServiceTestCase(ServiceTestCase):

    def test_get_payment_by_payment_id(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/pg/v1/payment/123',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'EzU4wy5jf/AAFckiSp/jmZVvWESdo6PimmZ4Gk72Mf0='
            },
            text=json.dumps({
                'payment_id': 123,
                'amount': 1000000,
                'fee': 3000,
                'status': 30000,
                'reference_id': 'EXAMPLE-REF-ID-001'
            })
        )

        self.assertEqual(
            Payment(
                123,
                1000000,
                3000,
                Status.PAYMENT_VERIFICATION_IS_ON_PROGRESS,
                'EXAMPLE-REF-ID-001'
            ),
            self.client.payment_gateway.get_payment(by_payment_id=123)
        )

    def test_get_payment_by_reference_id(self):
        path = '/pg/v1/payment/reference-id/EXAMPLE-REF-ID-001'
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + path,
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'AYUsBQsmajE9idsHKxjtLY9s06fdaUv2S+CUAOwiF/g='
            },
            text=json.dumps({
                'payment_id': 123,
                'amount': 1000000,
                'fee': 3000,
                'status': 30000,
                'reference_id': 'EXAMPLE-REF-ID-001'
            })
        )

        self.assertEqual(
            Payment(
                123,
                1000000,
                3000,
                Status.PAYMENT_VERIFICATION_IS_ON_PROGRESS,
                'EXAMPLE-REF-ID-001'
            ),
            self.client.payment_gateway.get_payment(by_reference_id='EXAMPLE-REF-ID-001')
        )

    def test_get_payment_mutually_exclusive_parameters(self):
        with self.assertRaises(AssertionError):
            self.client.payment_gateway.get_payment()

        with self.assertRaises(AssertionError):
            self.client.payment_gateway.get_payment(by_payment_id=123, by_reference_id='123')


if __name__ == '__main__':
    unittest.main()
