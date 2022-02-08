import json
import unittest
from datetime import datetime

import odeo.client
from odeo.exceptions.general_error import GeneralError
from odeo.exceptions.input_validation_error import InputValidationError
from odeo.models.request import Request
from odeo.models.transfer import Transfer
from tests.service_test_case import ServiceTestCase


class CashServiceTestCase(ServiceTestCase):
    def test_create_bulk_transfers(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/bulk-transfer',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'TPGgchibPJopgD2RSgD7H69kT6RimGUZqVhHwgovTrI='
            },
            text=json.dumps({
                'transfers': [{
                    'transfer_id': '123',
                    'sender_user_id': '456',
                    'receiver_user_id': '789',
                    'amount': 1000000,
                    'reference_id': 'EXAMPLE-REF-ID-001',
                    'note': 'Example description',
                    'created_at': '1612137600'
                }],
            })
        )

        self.assertEqual(
            [Transfer(
                transfer_id='123',
                sender_user_id='456',
                receiver_user_id='789',
                amount=1000000,
                reference_id='EXAMPLE-REF-ID-001',
                note='Example description',
                created_at=datetime(2021, 2, 1)
            )],
            self.client.cash.create_bulk_transfers([
                Request(
                    sender_user_id=456,
                    receiver_user_id=789,
                    amount=1000000,
                    reference_id='EXAMPLE-REF-ID-001',
                    note='Example description'
                )
            ])
        )

    def test_create_bulk_transfers_with_default_params(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/bulk-transfer',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Oncl5GPNiNlQHi/SKtuWa/HGjyGY7rkQ9jBA+j9aey4='
            },
            text=json.dumps({
                'transfers': [{
                    'transfer_id': '123',
                    'sender_user_id': '456',
                    'receiver_user_id': '789',
                    'amount': 1000000,
                    'reference_id': 'EXAMPLE-REF-ID-001',
                    'created_at': '1612137600'
                }],
            })
        )

        self.assertEqual(
            [Transfer(
                transfer_id='123',
                sender_user_id='456',
                receiver_user_id='789',
                amount=1000000,
                reference_id='EXAMPLE-REF-ID-001',
                created_at=datetime(2021, 2, 1)
            )],
            self.client.cash.create_bulk_transfers([
                Request(
                    receiver_user_id=789,
                    amount=1000000,
                    reference_id='EXAMPLE-REF-ID-001'
                )
            ])
        )

    def test_create_bulk_transfers_failed_amount_out_of_range(self):
        self._create_failed_bulk_transfers_test(
            InputValidationError,
            10001,
            'The requests.0.amount must be between 1000 and 1000000'
        )

    def test_create_bulk_transfers_failed_reference_id_already_used(self):
        self._create_failed_bulk_transfers_test(
            GeneralError, 10000, 'EXAMPLE-REF-ID-001 reference id exists'
        )

    def _create_failed_bulk_transfers_test(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/bulk-transfer',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Oncl5GPNiNlQHi/SKtuWa/HGjyGY7rkQ9jBA+j9aey4='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.cash.create_bulk_transfers([
                Request(
                    receiver_user_id=789,
                    amount=1000000,
                    reference_id='EXAMPLE-REF-ID-001'
                )
            ])
        self.assertEqual(str(ctx.exception), message)


if __name__ == '__main__':
    unittest.main()
