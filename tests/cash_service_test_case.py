import json
import unittest
from datetime import datetime

import odeo.client
from odeo.exceptions.general_error import GeneralError
from odeo.exceptions.input_validation_error import InputValidationError
from odeo.models.channel import Channel
from odeo.models.list_transfers_response import ListTransfersResponse
from odeo.models.request import Request
from odeo.models.topup import Topup
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

    def test_list_transfers(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/transfers',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'YRHRKTH0L7nFSVGTO3Ng07KKBIys7olErXdtQFLVTio='
            },
            text=json.dumps({
                'transfers': [{
                    'transfer_id': '123',
                    'sender_user_id': '456',
                    'receiver_user_id': '789',
                    'amount': 1000000,
                    'reference_id': 'EXAMPLE-REF-ID-001',
                    'created_at': '1612137600'
                }]
            })
        )

        self.assertEqual(
            ListTransfersResponse(
                transfers=[
                    Transfer(
                        transfer_id='123',
                        sender_user_id='456',
                        receiver_user_id='789',
                        amount=1000000,
                        reference_id='EXAMPLE-REF-ID-001',
                        created_at=datetime(2021, 2, 1)
                    )
                ],
            ),
            self.client.cash.list_transfers()
        )

    def test_list_transfers_with_next_page_token(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/transfers',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'YRHRKTH0L7nFSVGTO3Ng07KKBIys7olErXdtQFLVTio='
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
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            ListTransfersResponse(
                transfers=[
                    Transfer(
                        transfer_id='123',
                        sender_user_id='456',
                        receiver_user_id='789',
                        amount=1000000,
                        reference_id='EXAMPLE-REF-ID-001',
                        created_at=datetime(2021, 2, 1)
                    )
                ],
                next_page_token='abcdef'
            ),
            self.client.cash.list_transfers()
        )

    def test_list_transfers_with_parameters(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/transfers',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '9OFvffcuY/Jxg8wAFhvyidu8dLU9Ga/u5XbQas6e9hA='
            },
            text=json.dumps({
                'transfers': [
                    {
                        'transfer_id': '11',
                        'sender_user_id': '22',
                        'receiver_user_id': '33',
                        'amount': 1000000,
                        'reference_id': 'REF-ID-111',
                        'created_at': '1612137600'
                    },
                    {
                        'transfer_id': '44',
                        'sender_user_id': '55',
                        'receiver_user_id': '66',
                        'amount': 2000000,
                        'reference_id': 'REF-ID-222',
                        'created_at': '1612137600'
                    }
                ],
                'next_page_token': 'ghijkl'
            })
        )

        self.assertEqual(
            ListTransfersResponse(
                transfers=[
                    Transfer(
                        transfer_id='11',
                        sender_user_id='22',
                        receiver_user_id='33',
                        amount=1000000,
                        reference_id='REF-ID-111',
                        created_at=datetime(2021, 2, 1)
                    ),
                    Transfer(
                        transfer_id='44',
                        sender_user_id='55',
                        receiver_user_id='66',
                        amount=2000000,
                        reference_id='REF-ID-222',
                        created_at=datetime(2021, 2, 1)
                    )
                ],
                next_page_token='ghijkl'
            ),
            self.client.cash.list_transfers(
                ['REF-ID-111', 'REF-ID-222'],
                start_date=datetime(2021, 2, 1),
                end_date=datetime(2021, 4, 3),
                page_token='abcdef'
            )
        )

    def test_create_va_topup(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '7LtJU4UaR9yUuNzbLww1sYyMEM14ctQCnfp4bTp4++A='
            },
            text=json.dumps({
                'channels': [{
                    'fee': '5000',
                    'channel_id': 31,
                    'pay_code': 'abcdef',
                    'amount': 1000000,
                    'total': 1005000
                }],
                'topup_id': '456',
                'expires_at': '1612137600'
            })
        )

        self.assertEqual(
            Topup(
                channels=[
                    Channel(
                        fee='5000',
                        channel_id=31,
                        pay_code='abcdef',
                        amount=1000000,
                        total=1005000
                    )
                ],
                topup_id='456',
                expires_at=datetime(2021, 2, 1)
            ),
            self.client.cash.create_va_topup(1000000, 123)
        )

    def test_create_va_topup_failed_minimum_amount(self):
        self._create_failed_create_va_topup(
            InputValidationError, 10001, 'The amount must be at least 10000'
        )

    def test_create_va_topup_failed_maximum_amount(self):
        self._create_failed_create_va_topup(
            InputValidationError, 10001, 'The amount may not be greater than 1000000000000'
        )

    def test_create_va_topup_failed_sub_user_does_not_exists(self):
        self._create_failed_create_va_topup(GeneralError, 10000, 'User not found')

    def test_create_va_topup_failed_theres_already_topup_request(self):
        self._create_failed_create_va_topup(GeneralError, 10000, 'Pending topup exists')

    def _create_failed_create_va_topup(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '7LtJU4UaR9yUuNzbLww1sYyMEM14ctQCnfp4bTp4++A='
            },
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.cash.create_va_topup(1000000, 123)
        self.assertEqual(str(ctx.exception), message)


if __name__ == '__main__':
    unittest.main()
