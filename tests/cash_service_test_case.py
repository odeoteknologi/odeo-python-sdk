import json
import unittest
from datetime import datetime

import odeo.client
from odeo.exceptions.general_error import GeneralError
from odeo.exceptions.input_validation_error import InputValidationError
from odeo.models.balance import Balance, Cash
from odeo.models.cash_transaction import CashTransaction
from odeo.models.channel import Channel
from odeo.models.transactions_history import TransactionsHistory
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

    def test_find_active_va_topup(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/active',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '9JcNSUOjeLKP0ENLp671MTl4rYBX55iEtg6Q/V0dNo0='
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
            self.client.cash.find_active_va_topup()
        )

    def test_find_active_va_topup_with_user_id_parameter(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/active',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'rdg9EpRwjKbHPRwos6L1clPGP15w6zHTUOUM+4uUk3A='
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
            self.client.cash.find_active_va_topup(123)
        )

    def test_find_active_va_topup_failed_no_active_topup_order(self):
        message = 'Order not found'
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/active',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'rdg9EpRwjKbHPRwos6L1clPGP15w6zHTUOUM+4uUk3A='
            },
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10000
            })
        )

        with self.assertRaises(GeneralError) as ctx:
            self.client.cash.find_active_va_topup(123)

        self.assertEqual(str(ctx.exception), message)

    def test_cancel_va_topup(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/cancel',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Xx6lyK8XK7FJmwzQPVLngIMFUaIq4e+cYyue/nw/ET8='
            },
            text=json.dumps({})
        )

        self.assertEqual({}, self.client.cash.cancel_va_topup())

    def test_cancel_va_topup_with_user_id_parameter(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/cancel',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'D1TXjaSBB5x+sCyzHgqz+hdXK0nu4fN6ClnZsRQYTPE='
            },
            text=json.dumps({})
        )

        self.assertEqual({}, self.client.cash.cancel_va_topup(123))

    def test_cancel_va_topup_failed_no_active_topup_order(self):
        self._create_failed_cancel_va_topup(GeneralError, 10000, 'Order not found')

    def test_cancel_va_topup_failed_sub_user_does_not_exists(self):
        self._create_failed_cancel_va_topup(GeneralError, 10000, 'User not found')

    def test_cancel_va_topup_failed_not_the_order_owner(self):
        self._create_failed_cancel_va_topup(
            GeneralError, 10000, "You don't have credential to access this data."
        )

    def test_cancel_va_topup_failed_order_already_confirmed(self):
        self._create_failed_cancel_va_topup(GeneralError, 10000, "Can't cancel this order.")

    def _create_failed_cancel_va_topup(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/va-topup/cancel',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'D1TXjaSBB5x+sCyzHgqz+hdXK0nu4fN6ClnZsRQYTPE='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.cash.cancel_va_topup(123)
        self.assertEqual(str(ctx.exception), message)

    def test_get_balance(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/me/balance',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'ms3Xm918ZnQ8rayEjAvnV86uKTxQLqFv/7M6F+SJ1kk='
            },
            text=json.dumps({
                'cash': {
                    'amount': 1000000,
                    'currency': 'IDR',
                    'formatted_amount': 'Rp1,000,000'
                },
                'locked_cash': {
                    'amount': 100000,
                    'currency': 'IDR',
                    'formatted_amount': 'Rp100,000'
                }
            })
        )

        self.assertEqual(
            Balance(
                cash=Cash(1000000, 'IDR', 'Rp1,000,000'),
                locked_cash=Cash(100000, 'IDR', 'Rp100,000')
            ),
            self.client.cash.get_balance()
        )

    def test_get_balance_with_user_id_parameter(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/123/balance',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '8ek7fHgiGmYXUDRO/7ygi2enSnxrAwEvEUDo13AJQJ8='
            },
            text=json.dumps({
                'cash': {
                    'amount': 1000000,
                    'currency': 'IDR',
                    'formatted_amount': 'Rp1,000,000'
                },
                'locked_cash': {
                    'amount': 100000,
                    'currency': 'IDR',
                    'formatted_amount': 'Rp100,000'
                }
            })
        )

        self.assertEqual(
            Balance(
                cash=Cash(1000000, 'IDR', 'Rp1,000,000'),
                locked_cash=Cash(100000, 'IDR', 'Rp100,000')
            ),
            self.client.cash.get_balance(123)
        )

    def test_get_balance_failed_user_does_not_exists(self):
        message = ''
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/123/balance',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': '8ek7fHgiGmYXUDRO/7ygi2enSnxrAwEvEUDo13AJQJ8='
            },
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': 10000
            })
        )

        with self.assertRaises(GeneralError) as ctx:
            self.client.cash.get_balance(123)

        self.assertEqual(str(ctx.exception), message)

    def test_get_transactions_history(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/transactions',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'mDAKk7c//3X7r4X6Q/G0EtlY0fq0Ix7xQG2Gn4oI/A4='
            },
            text=json.dumps({
                'cash_transactions': [{
                    'cash_transaction_id': '123',
                    'user_id': '456',
                    'amount': 1000000,
                    'balance_before': 1000000,
                    'balance_after': 2000000,
                    'transaction_type': 'api_disbursement',
                    'created_at': '1612137600'
                }],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            TransactionsHistory(
                cash_transactions=[
                    CashTransaction(
                        cash_transaction_id='123',
                        user_id='456',
                        amount=1000000,
                        balance_before=1000000,
                        balance_after=2000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 2, 1)
                    )
                ],
                next_page_token='abcdef'
            ),
            self.client.cash.get_transactions_history()
        )

    def test_get_transactions_history_with_parameters(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/transactions',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'cONLC0e0B/lAd7k0NV3TP7gOHTAAR5O5VzX7O8hUf5k='
            },
            text=json.dumps({
                'cash_transactions': [{
                    'cash_transaction_id': '123',
                    'user_id': '456',
                    'amount': 1000000,
                    'balance_before': 1000000,
                    'balance_after': 2000000,
                    'transaction_type': 'api_disbursement',
                    'created_at': '1612137600'
                }],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            TransactionsHistory(
                cash_transactions=[
                    CashTransaction(
                        cash_transaction_id='123',
                        user_id='456',
                        amount=1000000,
                        balance_before=1000000,
                        balance_after=2000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 2, 1)
                    )
                ],
                next_page_token='abcdef'
            ),
            self.client.cash.get_transactions_history(
                start_date=datetime(2021, 2, 1),
                end_date=datetime(2021, 4, 3),
                page_token='ghijkl'
            )
        )

    def test_get_sub_user_transactions_history(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/sub-user-transactions',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'Br3ynlMByEKQfm7IZFi96JQ3jHluDpuGPalutS49Vtk='
            },
            text=json.dumps({
                'cash_transactions': [
                    {
                        'cash_transaction_id': '111',
                        'user_id': '456',
                        'amount': 1000000,
                        'balance_before': 1000000,
                        'balance_after': 2000000,
                        'transaction_type': 'api_disbursement',
                        'created_at': '1612137600'
                    },
                    {
                        'cash_transaction_id': '222',
                        'user_id': '789',
                        'amount': 3000000,
                        'balance_before': 3000000,
                        'balance_after': 4000000,
                        'transaction_type': 'api_disbursement',
                        'created_at': '1617408000'
                    }
                ],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            TransactionsHistory(
                cash_transactions=[
                    CashTransaction(
                        cash_transaction_id='111',
                        user_id='456',
                        amount=1000000,
                        balance_before=1000000,
                        balance_after=2000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 2, 1)
                    ),
                    CashTransaction(
                        cash_transaction_id='222',
                        user_id='789',
                        amount=3000000,
                        balance_before=3000000,
                        balance_after=4000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 4, 3)
                    )
                ],
                next_page_token='abcdef'
            ),
            self.client.cash.get_transactions_history([456, 789])
        )

    def test_get_sub_user_transactions_history_with_parameters(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/cash/sub-user-transactions',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'kFIBW9qN5Z3IKUR1blmXIwxgdluIPLffCw3Kz5sWSKU='
            },
            text=json.dumps({
                'cash_transactions': [
                    {
                        'cash_transaction_id': '111',
                        'user_id': '456',
                        'amount': 1000000,
                        'balance_before': 1000000,
                        'balance_after': 2000000,
                        'transaction_type': 'api_disbursement',
                        'created_at': '1612137600'
                    },
                    {
                        'cash_transaction_id': '222',
                        'user_id': '789',
                        'amount': 3000000,
                        'balance_before': 3000000,
                        'balance_after': 4000000,
                        'transaction_type': 'api_disbursement',
                        'created_at': '1617408000'
                    }
                ],
                'next_page_token': 'abcdef'
            })
        )

        self.assertEqual(
            TransactionsHistory(
                cash_transactions=[
                    CashTransaction(
                        cash_transaction_id='111',
                        user_id='456',
                        amount=1000000,
                        balance_before=1000000,
                        balance_after=2000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 2, 1)
                    ),
                    CashTransaction(
                        cash_transaction_id='222',
                        user_id='789',
                        amount=3000000,
                        balance_before=3000000,
                        balance_after=4000000,
                        transaction_type='api_disbursement',
                        created_at=datetime(2021, 4, 3)
                    )
                ],
                next_page_token='abcdef'
            ),
            self.client.cash.get_transactions_history(
                user_ids=[456, 789],
                start_date=datetime(2021, 2, 1),
                end_date=datetime(2021, 4, 3),
                page_token='ghijkl'
            )
        )

    if __name__ == '__main__':
        unittest.main()
