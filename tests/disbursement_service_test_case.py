import datetime
import json
import unittest

import odeo.client
from odeo.exceptions.insufficient_balance_error import InsufficientBalanceError
from odeo.exceptions.invalid_bank_error import InvalidBankError
from odeo.models.bank import Bank
from odeo.models.bank_account import BankAccount
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

    def test_get_banks_failed(self):
        self.adapter.register_uri(
            'GET',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/banks',
            status_code=400,
            text=json.dumps({
                'message': 'Test error message',
                'status_code': 400,
                'error_code': 10000
            })
        )

        self.assertIsNone(self.client.disbursement.get_banks())

    def test_bank_account_inquiry(self):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/bank-account-inquiry',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'xXZNi3mjrdmp6NM6drpXFyTcZGec4b4dxuA5dB/cHqI='
            },
            text=json.dumps({
                'bank_id': 1,
                'account_number': '1234567890',
                'account_name': 'Agus Hartono',
                'customer_name': 'Agus Hartono',
                'fee': 1000,
                'status': 50000,
                'created_at': '1612137600',
                'bank_account_inquiry_id': '123',
                'validity': 100
            })
        )

        self.assertEqual(
            BankAccount(
                1,
                '1234567890',
                'Agus Hartono',
                'Agus Hartono',
                1000,
                50000,
                datetime.datetime(2021, 2, 1),
                '123',
                100
            ),
            self.client.disbursement.bank_account_inquiry(
                '1234567890', 1, 'Agus Hartono', True
            )
        )

    def test_bank_account_inquiry_failed_invalid_bank(self):
        self._create_failed_bank_account_inquiry_test(
            InvalidBankError, 40002, 'Unknown error: INVALID BANK'
        )

    def test_bank_account_inquiry_failed_insufficient_balance(self):
        self._create_failed_bank_account_inquiry_test(
            InsufficientBalanceError, 40011, 'Unknown error: INSUFFICIENT BALANCE'
        )

    def _create_failed_bank_account_inquiry_test(self, error, error_code, message):
        self.adapter.register_uri(
            'POST',
            odeo.client.DEVELOPMENT_BASE_URL + '/dg/v1/bank-account-inquiry',
            request_headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
                'X-Odeo-Timestamp': '1612137600',
                'X-Odeo-Signature': 'xXZNi3mjrdmp6NM6drpXFyTcZGec4b4dxuA5dB/cHqI='
            },
            status_code=400,
            text=json.dumps({
                'message': message,
                'status_code': 400,
                'error_code': error_code
            })
        )
        with self.assertRaises(error) as ctx:
            self.client.disbursement.bank_account_inquiry(
                '1234567890', 1, 'Agus Hartono', True
            )
        self.assertEqual(str(ctx.exception), message)
        self.assertEqual(ctx.exception.error_code, error_code)


if __name__ == '__main__':
    unittest.main()
